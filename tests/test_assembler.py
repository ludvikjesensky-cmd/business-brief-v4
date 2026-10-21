from __future__ import annotations

import struct

import pytest

from business_brief.assembler import (
    CANONICAL_SEPARATOR,
    IntegrityError,
    article_storage_key,
    assemble,
    canonical_json,
    eligible_for_persistence,
    post_check_article,
    sha256_bytes,
    verify_manifest,
    verify_png_artifact,
    verify_selected_page,
)


SOURCE = {
    "source_id": "603e8242-ffe8-4e1d-a5de-9adb3da4d188",
    "source_sha256": "2" * 64,
    "publication_id": "the-wall-street-journal",
    "canonical_name": "The Wall Street Journal",
    "edition_id": "d09424f1-046d-46ad-98ed-9e638351f5e8",
    "edition_date": "2026-10-14",
    "edition_variant": "default",
}


def item(
    item_id: str,
    title: str,
    text: str,
    *,
    starts: bool = True,
    from_previous: bool = False,
    to_another: bool = False,
    target: str | None = None,
    status: str = "VERIFIED",
    assets: list[dict] | None = None,
) -> dict:
    return {
        "page_item_id": item_id,
        "item_type": "article",
        "title": title,
        "subtitle": None,
        "kicker": None,
        "byline": "Reporter" if starts else None,
        "text_on_page": text,
        "relevance": {"state": "relevant", "reason": "test"},
        "continuation": {
            "starts_here": starts,
            "continued_from_previous_page": from_previous,
            "continues_to_another_page": to_another,
            "continuation_marker": None,
            "continuation_target": target,
        },
        "verification": {
            "status": status,
            "visual_checked": True,
            "text_layer_checked": True,
            "title_verified": True,
            "byline_verified": True if starts else None,
            "boundaries_verified": True,
            "reading_order_verified": True,
            "text_on_page_complete": True,
            "notes": [],
        },
        "assets": assets or [],
    }


def page_doc(page_no: int, items: list[dict], *, schema: str = "page-ingest-v4") -> dict:
    return {
        "schema_version": schema,
        "producer": "ingestor-v2.2-chat" if schema == "page-ingest-v4" else "ingestor-v2.1-chat",
        "instruction_version": "2.2" if schema == "page-ingest-v4" else "2.1",
        "source": {"source_id": SOURCE["source_id"], "source_sha256": SOURCE["source_sha256"]},
        "publication": {
            "publication_id": SOURCE["publication_id"],
            "canonical_name": SOURCE["canonical_name"],
            "edition_date": SOURCE["edition_date"],
            "edition_variant": SOURCE["edition_variant"],
            "page_no": page_no,
        },
        "items": items,
        "page_status": "VERIFIED",
        "page_notes": [],
    }


def selected(page_no: int, doc: dict, *, revision_id: str | None = None):
    kind = "revision" if revision_id else "canonical"
    if revision_id:
        wrapper = {
            "schema_version": "page-revision-v1",
            "revision_id": revision_id,
            "supersedes": {"key": "old", "sha256": "3" * 64},
            "reason": "test",
            "created_by": "test",
            "created_at": "2026-10-21T10:00:00Z",
            "crop_previews": [],
            "page": doc,
        }
        raw = canonical_json(wrapper)
    else:
        raw = canonical_json(doc)
    generation = "ingestor-v2.2" if doc["schema_version"] == "page-ingest-v4" else "ingestor-v2.1"
    key = f"page-ingest/x/{generation}/page-{page_no:04d}.json"
    selection = {
        "page_no": page_no,
        "generation": generation,
        "schema_version": doc["schema_version"],
        "kind": kind,
        "revision_id": revision_id,
        "key": key,
        "sha256": sha256_bytes(raw),
        "page_status": "VERIFIED",
        "usable_for_assembly": True,
        "evidence": {"receipt_id": sha256_bytes(raw), "verified_at": "2026-10-21T10:00:00Z"},
        "selection_reason": None,
    }
    return selection, verify_selected_page(selection, raw)


def manifest(selections: list[dict]):
    source = {**SOURCE, "page_count": len(selections)}
    value = {
        "schema_version": "edition-selection-v1",
        "manifest_id": "fixture-r1",
        "source": source,
        "created_by": "test",
        "created_at": "2026-10-21T10:00:00Z",
        "status": "ACCEPTED_FOR_ASSEMBLY",
        "pages": selections,
    }
    raw = canonical_json(value)
    digest = sha256_bytes(raw)
    verify_manifest(value, raw, digest)
    return value, digest


def test_single_page_article_is_verified_and_deterministic():
    selection, p1 = selected(1, page_doc(1, [item("p1-a", "Alpha Story", "Alpha body.")]))
    m, mh = manifest([selection])
    first = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1])
    second = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1])
    assert first["counts"]["verified"] == 1
    assert first["issues"] == []
    record = first["records"][0]
    assert record["article_id"] == second["records"][0]["article_id"]
    assert record["post_check"]["status"] == "PASS"
    assert record["full_text"] == "Alpha body."
    assert eligible_for_persistence(record)
    assert article_storage_key(record).endswith(f"/{record['article_id']}.json")


def test_cross_page_continuation_uses_explicit_target_and_exact_separator():
    s1, p1 = selected(
        1,
        page_doc(1, [item("p1-a", "Rates Threaten Party for Banks", "First.", to_another=True, target="A2")]),
    )
    s2, p2 = selected(
        2,
        page_doc(2, [item("p2-a", "Banks Log Profits", "Second.", starts=False, from_previous=True)]),
    )
    m, mh = manifest([s1, s2])
    report = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1, p2])
    assert report["issues"] == []
    assert len(report["records"]) == 1
    record = report["records"][0]
    assert record["full_text"] == "First." + CANONICAL_SEPARATOR + "Second."
    assert [p["page_no"] for p in record["source_parts"]] == [1, 2]
    assert record["post_check"]["status"] == "PASS"


def test_title_only_corrobates_candidates_already_bounded_by_explicit_target():
    s1, p1 = selected(
        1,
        page_doc(
            1,
            [
                item("p1-g", "Ambassador to Greece Resigns Amid Allegations", "G1", to_another=True, target="A2"),
                item("p1-c", "Beverly Hills Condo Borrows From Buyers", "C1", to_another=True, target="A2"),
            ],
        ),
    )
    s2, p2 = selected(
        2,
        page_doc(
            2,
            [
                item("p2-c", "Condo Borrows From Buyers", "C2", starts=False, from_previous=True, target="A1"),
                item("p2-g", "Ambassador Resigns", "G2", starts=False, from_previous=True, target="A1"),
            ],
        ),
    )
    m, mh = manifest([s1, s2])
    report = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1, p2])
    assert report["issues"] == []
    assert len(report["records"]) == 2
    bodies = sorted(r["full_text"] for r in report["records"])
    assert bodies == ["C1\n\nC2", "G1\n\nG2"]


def test_ambiguous_continuation_goes_to_review_instead_of_guessing():
    s1, p1 = selected(
        1,
        page_doc(1, [item("p1-a", "Market Update", "Start", to_another=True, target="A2")]),
    )
    s2, p2 = selected(
        2,
        page_doc(
            2,
            [
                item("p2-a", "Update", "One", starts=False, from_previous=True, target="A1"),
                item("p2-b", "Update", "Two", starts=False, from_previous=True, target="A1"),
            ],
        ),
    )
    m, mh = manifest([s1, s2])
    report = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1, p2])
    assert report["counts"]["needs_review"] >= 1
    assert not any(r["full_text"].startswith("Start\n\n") for r in report["records"])


def test_missing_continuation_target_is_review():
    s1, p1 = selected(
        1,
        page_doc(1, [item("p1-a", "Alpha", "Start", to_another=True, target=None)]),
    )
    m, mh = manifest([s1])
    report = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1])
    assert report["records"] == []
    assert report["issues"][0]["status"] == "NEEDS_REVIEW"


def test_item_review_status_is_not_silently_assembled():
    s1, p1 = selected(
        1,
        page_doc(1, [item("p1-a", "Alpha", "Body", status="NEEDS_REVIEW")]),
    )
    m, mh = manifest([s1])
    report = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1])
    assert report["records"] == []
    assert report["issues"][0]["status"] == "NEEDS_REVIEW"


def _asset(anchor: str) -> dict:
    fake_png = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + struct.pack(">II", 1, 1) + b"rest"
    return {
        "asset_id": "asset-1",
        "asset_type": "chart",
        "page_item_id": "p1-a",
        "page_no": 1,
        "page_anchor": {
            "bbox_norm": [0.1, 0.1, 0.2, 0.2],
            "source_page_image_sha256": "4" * 64,
            "bbox_px": [1, 1, 2, 2],
        },
        "text_anchor": {
            "position": "after_paragraph",
            "paragraph_index": 0,
            "anchor_text": anchor,
            "status": "anchored",
        },
        "artifact": {
            "bucket": "page-ingest",
            "key": "asset.png",
            "media_type": "image/png",
            "sha256": sha256_bytes(fake_png),
            "byte_size": len(fake_png),
            "width": 1,
            "height": 1,
        },
        "verification": {
            "status": "VERIFIED",
            "visual_checked": True,
            "ownership_verified": True,
            "page_anchor_verified": True,
            "text_anchor_verified": True,
            "notes": [],
        },
        "title": None,
        "caption": None,
    }


def test_asset_reanchors_only_on_unique_text():
    s1, p1 = selected(
        1,
        page_doc(1, [item("p1-a", "Alpha", "Unique anchor here.", assets=[_asset("Unique anchor")])]),
    )
    m, mh = manifest([s1])
    record = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1])["records"][0]
    assert record["assets"][0]["placement"]["status"] == "placed"
    assert record["assembly"]["status"] == "VERIFIED"


def test_ambiguous_asset_anchor_is_unplaced_and_article_has_notes():
    s1, p1 = selected(
        1,
        page_doc(1, [item("p1-a", "Alpha", "Same anchor. Same anchor.", assets=[_asset("Same anchor")])]),
    )
    m, mh = manifest([s1])
    record = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1])["records"][0]
    assert record["assets"][0]["placement"]["status"] == "placement_needs_review"
    assert record["assembly"]["status"] == "VERIFIED_WITH_NOTES"
    assert record["post_check"]["status"] == "PASS"


def test_post_check_blocks_tampered_full_text():
    s1, p1 = selected(1, page_doc(1, [item("p1-a", "Alpha", "Original")]))
    m, mh = manifest([s1])
    record = assemble(manifest=m, manifest_sha256=mh, selected_pages=[p1])["records"][0]
    record["full_text"] = "Tampered"
    result = post_check_article(record, {1: p1})
    assert result["status"] == "FAIL"
    assert result["expected_full_text_sha256"] != result["actual_full_text_sha256"]


def test_selected_page_hash_mismatch_is_integrity_failure():
    doc = page_doc(1, [item("p1-a", "Alpha", "Body")])
    raw = canonical_json(doc)
    selection = {
        "page_no": 1,
        "generation": "ingestor-v2.2",
        "schema_version": "page-ingest-v4",
        "kind": "canonical",
        "revision_id": None,
        "key": "page.json",
        "sha256": "f" * 64,
        "page_status": "VERIFIED",
        "usable_for_assembly": True,
    }
    with pytest.raises(IntegrityError):
        verify_selected_page(selection, raw)


def test_png_verification_is_byte_and_dimension_bound():
    raw = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + struct.pack(">II", 10, 20) + b"payload"
    artifact = {
        "sha256": sha256_bytes(raw),
        "byte_size": len(raw),
        "width": 10,
        "height": 20,
    }
    verify_png_artifact(raw, artifact)
    with pytest.raises(IntegrityError):
        verify_png_artifact(raw + b"x", artifact)


def test_revision_wrapper_is_verified_without_mutating_page_contract():
    doc = page_doc(1, [item("p1-a", "Alpha", "Body")])
    selection, page = selected(1, doc, revision_id="r1")
    assert selection["kind"] == "revision"
    assert page.revision_id == "r1"
    assert page.page == doc

def test_wsj_page_one_continuation_title_pairs_are_deterministically_resolvable():
    origins = [
        ("p1-banks", "Rates Threaten To Spoil The Party For Banks", "A2"),
        ("p1-greece", "Trump’s Ambassador to Greece Resigns Amid Graft Allegations", "A4"),
        ("p1-condo", "Beverly Hills Condo Borrows From Its Buyers", "A4"),
        ("p1-china", "China’s Weakening Economy Is Creating a Lost Generation", "A10"),
        ("p1-navy", "The Mystery of the Sailor Shaking Up the Navy", "A6"),
        ("p1-park", "Car-Free Oasis Drives San Francisco Backlash", "A10"),
    ]
    destinations = {
        2: [("p2-banks", "Banks Log Profits but Eye Rates")],
        4: [
            ("p4-greece", "Guilfoyle Resigns as Ambassador"),
            ("p4-condo", "Condo Borrows From Buyers"),
        ],
        6: [("p6-navy", "Trump’s Mystery Sailor")],
        10: [
            ("p10-park", "Car-Free Park Drives Backlash"),
            ("p10-china", "China’s Gen Z Is Losing Hope"),
        ],
    }

    selections = []
    pages = []
    s1, p1 = selected(
        1,
        page_doc(
            1,
            [
                item(item_id, title, f"start-{item_id}", to_another=True, target=target)
                for item_id, title, target in origins
            ],
            schema="page-ingest-v3",
        ),
    )
    selections.append(s1)
    pages.append(p1)

    for page_no in range(2, 11):
        incoming = destinations.get(page_no, [])
        doc_items = [
            item(
                item_id,
                title,
                f"end-{item_id}",
                starts=False,
                from_previous=True,
                target="A1",
            )
            for item_id, title in incoming
        ]
        s, p = selected(page_no, page_doc(page_no, doc_items))
        selections.append(s)
        pages.append(p)

    m, mh = manifest(selections)
    report = assemble(manifest=m, manifest_sha256=mh, selected_pages=pages)

    assert report["issues"] == []
    assert len(report["records"]) == 6
    chains = {
        tuple(part["page_item_id"] for part in record["source_parts"])
        for record in report["records"]
    }
    assert chains == {
        ("p1-banks", "p2-banks"),
        ("p1-greece", "p4-greece"),
        ("p1-condo", "p4-condo"),
        ("p1-china", "p10-china"),
        ("p1-navy", "p6-navy"),
        ("p1-park", "p10-park"),
    }

