import copy
import io
import json
from pathlib import Path
from types import SimpleNamespace

import fitz
import pytest

from business_brief.ingestor import extract_physical_map
from business_brief.visual_mapper import VisualResponsesProvider, parse_response
from business_brief.visual_page_map import LAYOUT_SCHEMA, PageMapError
from business_brief.visual_page_map_cli import main
from business_brief.visual_pipeline import (
    assemble_issue, canonical, digest, issue_lock, load_json, map_issue, prepare_issue, preview_html, write_json,
)

from test_visual_page_map import article, embedded, layout, region


@pytest.fixture
def source(tmp_path):
    pdf = tmp_path / "source.pdf"
    with fitz.open() as doc:
        page = doc.new_page(width=600, height=800)
        page.insert_text((40, 60), "Visual Page Map: synthetic acceptance fixture", fontsize=18)
        page.insert_text((40, 90), "By Test Reporter", fontsize=11)
        page.insert_text((40, 150), "Left column first line.", fontsize=12)
        page.insert_text((40, 170), "Left column second line.", fontsize=12)
        page.insert_text((330, 150), "Right column after the left.", fontsize=12)
        page.insert_text((330, 170), "Exact source text is retained.", fontsize=12)
        page.draw_rect(fitz.Rect(330, 220, 550, 350), color=(.5, .5, .5), fill=(.8, .8, .8))
        page.insert_text((340, 280), "PHOTO", fontsize=20)
        page.insert_text((330, 370), "Separate photo caption.", fontsize=11)
        page.draw_rect(fitz.Rect(40, 440, 550, 530), color=(.5, .1, .1))
        page.insert_text((60, 480), "ADVERTISEMENT", fontsize=18)
        second = doc.new_page(width=600, height=800)
        second.insert_text((40, 60), "Corrections", fontsize=16)
        second.insert_text((40, 100), "This is a separate utility item.", fontsize=12)
        doc.save(pdf)
    sha = digest(pdf.read_bytes())
    bundle = tmp_path / "bundle.json"
    write_json(bundle, {"schema_version": "source-bundle-v4", "status": "READY_FOR_INGESTOR",
        "source_id": "synthetic-fixture", "source_sha256": sha, "page_count": 2,
        "prepared_pdf_path": str(pdf), "ocr": {"prepared_sha256": sha}})
    physical = tmp_path / "physical.json"
    write_json(physical, extract_physical_map(bundle, pdf_path=pdf).to_dict())
    maps = tmp_path / "input-maps"
    write_json(maps / "p0001.json", layout([article(
        headline=[region("headline", [.05, .04, .96, .085])],
        byline=[region("byline", [.05, .09, .5, .12])],
        body_flow=[region("left", [.05, .16, .49, .23]), region("right", [.54, .16, .96, .23])],
        embedded_objects=[embedded("photo", [.54, .27, .93, .44],
            caption_regions=[region("caption", [.54, .44, .96, .48])])])],
        exclusions=[{"region_id": "advertisement", "kind": "advertisement", "bbox": [.05, .54, .94, .67]}]))
    write_json(maps / "p0002.json", layout([article("correction", kind="correction",
        headline=[region("h2", [.05, .04, .9, .09])],
        body_flow=[region("b2", [.05, .10, .9, .15])])], page_no=2))
    return SimpleNamespace(pdf=pdf, physical=physical, maps=maps, sha=sha, root=tmp_path / "issue")


class FakeProvider:
    model, detail, max_output_tokens = "test-model", "low", 6000

    def __init__(self, maps, fail=False):
        self.maps, self.calls, self.fail = maps, [], fail

    def generate(self, image, metadata):
        self.calls.append(metadata)
        assert image.startswith(b"\xff\xd8")
        assert "blocks" not in metadata and "text" not in metadata
        if self.fail:
            raise PageMapError("simulated timeout")
        result = load_json(self.maps / f"p{metadata['page_no']:04d}.json")
        return {"id": "response-" + str(metadata["page_no"]), "status": "completed", "model": self.model,
            "usage": {"input_tokens": 100, "output_tokens": 200},
            "output": [{"content": [{"type": "output_text", "text": json.dumps(result)}]}]}


def test_end_to_end_offline_render_map_assemble_and_idempotent_resume(source):
    manifest = prepare_issue(source.pdf, source.physical, source.root)
    assert manifest["pages"][0]["image_width"] == 600
    assert all(p["image_bytes"] > 0 for p in manifest["pages"])
    assert prepare_issue(source.pdf, source.physical, source.root) == manifest
    assert map_issue(source.root, maps_dir=source.maps)["api_calls_this_run"] == 0
    issue = assemble_issue(source.root)
    assert issue["all_pages_processed"] and not issue["needs_review"]
    body = issue["pages"][0]["articles"][0]["body_text"]
    assert body == "Left column first line.\nLeft column second line.\n\nRight column after the left.\nExact source text is retained."
    assert "ADVERTISEMENT" not in body and "PHOTO" not in body
    assert issue["pages"][1]["articles"][0]["kind"] == "correction"
    assert issue["coverage"]["unmatched"] == 0
    assert map_issue(source.root, maps_dir=source.maps)["mapping_complete"]
    assert assemble_issue(source.root) == issue
    preview = (source.root / "previews/p0001.html").read_text()
    assert "data:image/jpeg;base64," in preview
    assert "body_flow:1" in preview


def test_live_request_budget_and_resume_do_not_recall_accepted_pages(source):
    prepare_issue(source.pdf, source.physical, source.root)
    provider = FakeProvider(source.maps)
    first = map_issue(source.root, provider=provider, max_api_calls=1)
    assert first["mapped_pages"] == [1] and not first["mapping_complete"]
    assert not assemble_issue(source.root)["all_pages_processed"]
    second = map_issue(source.root, provider=provider, max_api_calls=1)
    assert second["mapped_pages"] == [1, 2] and second["mapping_complete"]
    assert len(provider.calls) == 2
    assert map_issue(source.root, provider=provider)["api_calls_this_run"] == 0
    issue = assemble_issue(source.root)
    assert all(p["usage"]["input_tokens"] == 100 for p in issue["usage_by_page"])


def test_unknown_api_attempt_blocks_automatic_paid_retry(source):
    prepare_issue(source.pdf, source.physical, source.root)
    provider = FakeProvider(source.maps, fail=True)
    with pytest.raises(PageMapError, match="timeout"): map_issue(source.root, provider=provider)
    assert load_json(source.root / "attempts/p0001.json")["status"] == "failed_or_unknown"
    with pytest.raises(PageMapError, match="prior API attempt"): map_issue(source.root, provider=provider)
    assert len(provider.calls) == 1


def test_saved_response_can_recover_after_crash_without_api_call(source):
    prepare_issue(source.pdf, source.physical, source.root, pages=[1])
    provider = FakeProvider(source.maps)
    map_issue(source.root, provider=provider)
    (source.root / "maps/p0001.json").unlink()
    assert map_issue(source.root, provider=provider)["api_calls_this_run"] == 0
    assert len(provider.calls) == 1


def test_changed_mapper_configuration_rejected(source):
    prepare_issue(source.pdf, source.physical, source.root)
    provider = FakeProvider(source.maps)
    map_issue(source.root, provider=provider)
    provider.detail = "high"
    with pytest.raises(PageMapError, match="config changed"): map_issue(source.root, provider=provider)
    assert len(provider.calls) == 1


@pytest.mark.parametrize("artifact", ["image", "physical", "layout", "binding"])
def test_corrupt_or_mismatched_artifact_rejected(source, artifact):
    prepare_issue(source.pdf, source.physical, source.root)
    map_issue(source.root, maps_dir=source.maps)
    if artifact == "image":
        (source.root / "images/p0001.jpg").write_bytes(b"corrupted")
    elif artifact == "physical":
        physical = load_json(source.root / "physical-map.json")
        physical["pages"][0]["blocks"][0]["text"] = "altered"
        write_json(source.root / "physical-map.json", physical)
    else:
        path = source.root / "maps/p0001.json"
        saved = load_json(path)
        if artifact == "layout": saved["layout"]["notes"].append("changed")
        else: saved["binding"]["source_id"] = "another-edition"
        write_json(path, saved)
    with pytest.raises(PageMapError): assemble_issue(source.root)


def test_offline_changed_input_does_not_silently_reuse_cached_map(source):
    prepare_issue(source.pdf, source.physical, source.root)
    map_issue(source.root, maps_dir=source.maps)
    changed = load_json(source.maps / "p0001.json")
    changed["notes"].append("a corrected layout")
    write_json(source.maps / "p0001.json", changed)
    with pytest.raises(PageMapError, match="offline map changed"): map_issue(source.root, maps_dir=source.maps)


def test_subset_is_never_reported_as_full_issue(source):
    prepare_issue(source.pdf, source.physical, source.root, pages=[1])
    map_issue(source.root, maps_dir=source.maps)
    issue = assemble_issue(source.root)
    assert issue["processed_pages"] == [1]
    assert not issue["all_pages_processed"] and issue["needs_review"]
    assert main(["assemble", "--issue-dir", str(source.root), "--require-full-issue"]) == 2


def test_hash_and_dimensions_checked_before_render(source):
    with pytest.raises(PageMapError, match="hash mismatch"):
        prepare_issue(source.pdf, source.physical, source.root, prepared_sha256="0" * 64)
    physical = load_json(source.physical)
    physical["pages"][0]["width"] = 700
    write_json(source.physical, physical)
    with pytest.raises(PageMapError, match="dimensions mismatch"):
        prepare_issue(source.pdf, source.physical, source.root)
    assert not (source.root / "images").exists()


def test_prepared_derivative_requires_explicit_verified_sha(source):
    physical = load_json(source.physical)
    physical["source_sha256"] = "0" * 64
    write_json(source.physical, physical)
    with pytest.raises(PageMapError, match="hash mismatch"):
        prepare_issue(source.pdf, source.physical, source.root)
    manifest = prepare_issue(source.pdf, source.physical, source.root, prepared_sha256=source.sha)
    assert manifest["settings"]["source_sha256"] == "0" * 64
    assert manifest["settings"]["pdf_sha256"] == source.sha


def test_no_concurrent_issue_writer(source):
    with issue_lock(source.root):
        with pytest.raises(PageMapError, match="another process"):
            with issue_lock(source.root): pass


def test_invalid_cli_and_live_opt_in_do_not_make_calls(source, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert main(["map", "--issue-dir", str(source.root), "--live", "--model", "test"]) == 1
    assert main(["map", "--issue-dir", str(source.root), "--live", "--allow-paid", "--model", "test"]) == 1


def test_provider_request_is_jpeg_and_schema_constrained_without_physical_text():
    seen = []
    result = layout([])
    def transport(req, timeout):
        seen.append(json.loads(req.data))
        return io.BytesIO(json.dumps({"status": "completed", "output": [
            {"content": [{"type": "output_text", "text": json.dumps(result)}]}]}).encode())
    provider = VisualResponsesProvider("configured-model", allow_paid=True, key="test-secret", transport=transport)
    raw = provider.generate(b"fake-jpeg-bytes", {"page_no": 1, "image_width": 600, "image_height": 800})
    assert parse_response(raw, 1) == result
    body = seen[0]
    assert body["store"] is False
    assert body["text"]["format"]["schema"] == LAYOUT_SCHEMA
    assert body["text"]["format"]["strict"] is True
    image = body["input"][0]["content"][1]
    assert image["detail"] == "low" and image["image_url"].startswith("data:image/jpeg;base64,")
    assert "test-secret" not in json.dumps(body)
    assert "reasoning" not in body  # Provider-neutral: no unsupported effort parameter forced.


@pytest.mark.parametrize("raw", [
    {"status": "incomplete", "output": []},
    {"status": "completed", "output": [{"content": [{"type": "refusal"}]}]},
    {"status": "completed", "output": []},
    {"status": "completed", "output": [{"content": [{"type": "output_text", "text": "not json"}]}]},
])
def test_incomplete_refused_empty_or_invalid_responses_rejected(raw):
    with pytest.raises(PageMapError): parse_response(raw, 1)


def test_preview_escapes_source_identifiers_and_preserves_image_ratio():
    mapped = layout([article("<script>alert(1)</script>", body_flow=[region("b", [0, 0, 1, 1])])])
    result = preview_html(b"image", mapped, 4 / 3)
    assert "<script>" not in result
    assert "&lt;script&gt;" in result
    assert 'height="1333.3333333333333"' in result


def test_rotated_pdf_rejected_before_render(source):
    with fitz.open(source.pdf) as doc:
        doc[0].set_rotation(90)
        pdf = source.pdf.with_name("rotated.pdf")
        doc.save(pdf)
    with pytest.raises(PageMapError, match="rotated PDF"):
        prepare_issue(pdf, source.physical, source.root, prepared_sha256=digest(pdf.read_bytes()))


def test_cli_schema_and_prepare_map_assemble(source, capsys):
    assert main(["schema"]) == 0
    assert json.loads(capsys.readouterr().out) == LAYOUT_SCHEMA
    assert main(["prepare", "--pdf", str(source.pdf), "--physical-map", str(source.physical), "--output", str(source.root)]) == 0
    assert main(["map", "--issue-dir", str(source.root), "--maps-dir", str(source.maps)]) == 0
    assert main(["assemble", "--issue-dir", str(source.root), "--require-full-issue"]) == 0
    summaries = [json.loads(s) for s in capsys.readouterr().out.strip().splitlines()]
    assert summaries[0]["api_calls"] == summaries[1]["api_calls_this_run"] == 0
    assert summaries[-1]["all_pages_processed"] and not summaries[-1]["needs_review"]
