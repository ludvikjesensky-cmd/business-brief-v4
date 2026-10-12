import pytest

from business_brief.visual_continuations import assemble_articles
from business_brief.visual_page_map import PageMapError


def fragment(identity, body, cues):
    return {"fragment_id": identity, "headline": [], "byline": [], "kind": "article",
            "body_text": body, "continuations": cues, "needs_review": True}


@pytest.fixture
def issue():
    cue = {"direction": "to", "page_no": 2, "printed_label": "Continued on A2"}
    pages = [{"page_no": 1, "articles": [fragment("p0001:a", "First page.", [cue])]},
             {"page_no": 2, "articles": [fragment("p0002:b", "Second page.", [])]}]
    links = {"source_sha256": "source-sha", "physical_map_sha256": "physical-sha", "approved": True,
             "links": [{"from_fragment": "p0001:a", "to_fragment": "p0002:b", "printed_label": "Continued on A2"}]}
    return pages, links


def test_reviewed_printed_continuation_assembles_in_explicit_order(issue):
    pages, links = issue
    articles, unresolved = assemble_articles(pages, "source-sha", "physical-sha", links)
    assert len(articles) == 1
    assert articles[0]["body_text"] == "First page.\n\nSecond page."
    assert articles[0]["fragment_ids"] == ["p0001:a", "p0002:b"]
    assert articles[0]["join_status"] == "reviewed_explicit_links"
    assert articles[0]["needs_review"]  # Joining alone is not editorial acceptance.
    assert not unresolved


def test_similar_fragments_are_never_merged_without_links(issue):
    pages, _ = issue
    articles, unresolved = assemble_articles(pages, "source-sha", "physical-sha")
    assert len(articles) == 2 and len(unresolved) == 1


@pytest.mark.parametrize("mutation", ["unapproved", "source", "physical", "unknown", "no-cue", "duplicate", "cycle"])
def test_unsafe_links_rejected(issue, mutation):
    pages, links = issue
    if mutation == "unapproved": links["approved"] = False
    if mutation == "source": links["source_sha256"] = "another-edition"
    if mutation == "physical": links["physical_map_sha256"] = "another-map"
    if mutation == "unknown": links["links"][0]["to_fragment"] = "missing"
    if mutation == "no-cue": links["links"][0]["printed_label"] = "same topic"
    if mutation == "duplicate": links["links"].append(links["links"][0].copy())
    if mutation == "cycle":
        pages[1]["articles"][0]["continuations"] = [{"direction": "to", "page_no": 1, "printed_label": "A1"}]
        links["links"].append({"from_fragment": "p0002:b", "to_fragment": "p0001:a", "printed_label": "A1"})
    with pytest.raises(PageMapError): assemble_articles(pages, "source-sha", "physical-sha", links)
