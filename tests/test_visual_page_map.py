import copy
import json
import math
from dataclasses import asdict

import pytest

from business_brief.visual_assembly import MatchingPolicy, assemble_page, overlap
from business_brief.visual_page_map import LAYOUT_SCHEMA, PageMapError, validate_layout


def region(identity, bbox):
    return {"region_id": identity, "bbox": bbox}


def article(identity="a", **changes):
    return {"article_id": identity, "kind": "article", "headline": [], "byline": [],
            "body_flow": [], "embedded_objects": [], "exclusions": [], "continuations": [],
            "needs_review": False, "notes": [], **changes}


def layout(articles, page_no=1, **changes):
    return {"page_no": page_no, "articles": articles, "exclusions": [],
            "needs_review": False, "notes": [], **changes}


def block(identity, text, bbox, **changes):
    return {"block_id": identity, "text": text, "bbox": bbox, "source_order": 0, **changes}


def page(blocks, **changes):
    return {"page_no": 1, "width": 100, "height": 100, "blocks": blocks, **changes}


def embedded(kind, box, **changes):
    return {"object_id": kind, "kind": kind, "footprint": [box], "caption_regions": [], **changes}


def test_explicit_reading_order_overrides_physical_source_order():
    source = page([block("r", "RIGHT", [55, 20, 90, 25], source_order=0),
                   block("l2", "LEFT SECOND", [5, 40, 45, 45], source_order=1),
                   block("h", "Headline", [5, 5, 90, 15]),
                   block("l1", "LEFT FIRST", [5, 20, 45, 25], source_order=3)])
    mapped = layout([article(headline=[region("h", [.04, .04, .91, .16])], body_flow=[
        region("left", [0, .16, .49, .9]), region("right", [.5, .16, 1, .9])])])
    result = assemble_page(source, mapped)
    assert result["articles"][0]["body_text"] == "LEFT FIRST\nLEFT SECOND\n\nRIGHT"
    assert result["articles"][0]["headline"][0]["block_ids"] == ["h"]
    assert result["coverage"] == {"total": 4, "assigned": 4, "excluded": 0, "unmatched": 0, "ambiguous": 0}
    assert not result["needs_review"]


def test_photo_overlap_preserves_line_whose_center_falls_in_photo():
    # Photo covers 55% of the first line, including its center. Center test lost it.
    source = page([block("line", "first full line", [10, 49, 40, 51]),
                   block("in", "photo text", [10, 20, 40, 22])])
    mapped = layout([article(body_flow=[region("body", [0, 0, .5, 1])],
        embedded_objects=[embedded("photo", [0, 0, .5, .501])])])
    result = assemble_page(source, mapped)
    assert result["articles"][0]["body_text"] == "first full line"
    assert [b["block_id"] for b in result["excluded_blocks"]] == ["in"]


@pytest.mark.parametrize("fraction,excluded", [(0.59, False), (0.6, False), (0.61, True)])
def test_photo_threshold_is_strict_and_configurable(fraction, excluded):
    source = page([block("line", "text", [10, 50, 40, 60])])
    mapped = layout([article(body_flow=[region("body", [0, 0, 1, 1])],
        embedded_objects=[embedded("photo", [0, 0, 1, .5 + fraction / 10])])])
    result = assemble_page(source, mapped)
    assert bool(result["excluded_blocks"]) == excluded


def test_whole_chart_footprint_pull_quote_ad_and_caption_are_not_body():
    source = page([block("body", "Body", [5, 10, 45, 14]),
                   block("legend", "Legend", [5, 20, 45, 24]),
                   block("note", "Source: chart note", [5, 40, 45, 44]),
                   block("quote", "Pull quote", [5, 50, 45, 54]),
                   block("caption", "Photo caption", [5, 70, 45, 74]),
                   block("ad", "BUY", [5, 90, 45, 94])])
    mapped = layout([article(body_flow=[region("body", [0, 0, .5, 1])], embedded_objects=[
        embedded("chart", [0, .18, .5, .45]), embedded("pull_quote", [0, .48, .5, .55]),
        embedded("photo", [.55, .5, 1, .8], caption_regions=[region("cap", [0, .68, .5, .75])])])],
        exclusions=[{"region_id": "ad", "kind": "advertisement", "bbox": [0, .88, 1, 1]}])
    result = assemble_page(source, mapped)
    assert result["articles"][0]["body_text"] == "Body"
    assert result["articles"][0]["embedded_objects"][2]["captions"][0]["text"] == "Photo caption"
    assert result["coverage"]["assigned"] == 2
    assert result["coverage"]["excluded"] == 4


def test_union_overlap_does_not_double_count_rectangles():
    assert overlap([0, 0, 1, 1], [[0, 0, .4, 1], [0, 0, .4, 1]]) == pytest.approx(.4)
    assert overlap([0, 0, 1, 1], [[0, 0, .4, 1], [.3, 0, .7, 1]]) == pytest.approx(.7)
    assert overlap([0, 0, 1, 1], [[-2, -2, 2, 2]]) == 1
    assert overlap([0, 0, 1, 1], [[1, 0, 2, 1]]) == 0


def test_ambiguous_assignment_is_flagged_not_duplicated():
    source = page([block("x", "Uncertain", [10, 10, 20, 20])])
    mapped = layout([article("a", body_flow=[region("a-zone", [0, 0, .5, .5])]),
                     article("b", body_flow=[region("b-zone", [0, 0, .5, .5])])])
    result = assemble_page(source, mapped)
    assert result["coverage"]["ambiguous"] == 1
    assert result["assignments"] == {}
    assert result["needs_review"]
    assert all(a["body_text"] == "" for a in result["articles"])
    assert all(a["needs_review"] for a in result["articles"])


def test_boundary_block_is_assigned_only_once_across_adjacent_body_zones():
    result = assemble_page(page([block("x", "boundary", [45, 10, 55, 20])]),
        layout([article(body_flow=[region("l", [0, 0, .5, 1]), region("r", [.5, 0, 1, 1])])]))
    assert result["coverage"]["ambiguous"] == 1
    assert len(result["ambiguous_blocks"][0]["candidates"]) == 2


def test_unmatched_and_empty_regions_require_review_and_account_for_all_blocks():
    result = assemble_page(page([block("x", "outside", [70, 70, 90, 90])]),
        layout([article(body_flow=[region("l", [0, 0, .5, 1])])]))
    assert result["unmatched_block_ids"] == ["x"]
    assert result["warnings"][0]["kind"] == "empty_region"
    assert result["needs_review"]
    assert result["articles"][0]["needs_review"]
    assert sum(result["coverage"][k] for k in ("assigned", "excluded", "unmatched", "ambiguous")) == result["coverage"]["total"]


@pytest.mark.parametrize("kind", ["article", "brief", "correction", "photo", "utility"])
def test_all_item_types_are_preserved(kind):
    result = assemble_page(page([block("x", "Exact evidence\u2014ligature \ufb01", [10, 10, 20, 20])]),
        layout([article(kind=kind, body_flow=[region("b", [0, 0, 1, 1])])]))
    assert result["articles"][0]["kind"] == kind
    assert result["articles"][0]["body_text"] == "Exact evidence\u2014ligature \ufb01"


def test_explicit_continuation_is_retained_but_not_merged():
    result = assemble_page(page([]), layout([article(continuations=[
        {"direction": "to", "page_no": 2, "printed_label": "Continued on A2"}])]))
    assert result["articles"][0]["continuations"][0]["page_no"] == 2
    assert result["needs_review"]


@pytest.mark.parametrize("mutation", ["nan", "infinity", "outside", "reversed", "zero", "extra", "missing", "duplicate", "page", "bool"])
def test_invalid_layouts_rejected(mutation):
    value = layout([article(body_flow=[region("b", [0, 0, .5, .5])])])
    bbox = value["articles"][0]["body_flow"][0]["bbox"]
    if mutation == "nan": bbox[0] = math.nan
    if mutation == "infinity": bbox[0] = math.inf
    if mutation == "outside": bbox[0] = -.01
    if mutation == "reversed": bbox[2] = -.1
    if mutation == "zero": bbox[2] = 0
    if mutation == "extra": value["body_text"] = "do not generate"
    if mutation == "missing": del value["notes"]
    if mutation == "duplicate": value["articles"][0]["body_flow"].append(copy.deepcopy(value["articles"][0]["body_flow"][0]))
    if mutation == "page": value["page_no"] = 2
    if mutation == "bool": value["page_no"] = True
    with pytest.raises(PageMapError): validate_layout(value, 1)


@pytest.mark.parametrize("key,value", [("photo_overlap", 0), ("photo_overlap", math.nan), ("region_overlap", 1.1)])
def test_invalid_matching_policy_rejected(key, value):
    with pytest.raises(PageMapError): MatchingPolicy(**{key: value})


def test_schema_all_objects_are_closed_and_all_properties_required():
    def inspect(schema):
        if schema["type"] == "object":
            assert schema["additionalProperties"] is False
            assert set(schema["required"]) == set(schema["properties"])
            for child in schema["properties"].values(): inspect(child)
        if schema["type"] == "array": inspect(schema["items"])
    inspect(LAYOUT_SCHEMA)
