import pytest

from business_brief.assembler import assemble_issue
from business_brief.assembler_cli import main as assembler_main
from business_brief.ingestor import extract_maps
from business_brief.ingestor_cli import main as ingestor_main
from business_brief.physical_map import assert_semantically_neutral
from business_brief.visual_page_map import PageMapError
from business_brief.visual_pipeline import load_json, write_json

from test_visual_pipeline import FakeProvider, source


def ingest(source, **options):
    return extract_maps(source.pdf.parent / "bundle.json", source.root, maps_dir=source.maps, **options)


def test_ingestor_creates_both_maps_without_assembling_articles(source, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Ingestor must never invoke Assembler")
    monkeypatch.setattr("business_brief.assembler.assemble_issue", forbidden)
    handoff = ingest(source)
    assert handoff["producer"] == "INGESTOR" and handoff["consumer"] == "ASSEMBLER"
    assert handoff["status"] == "READY_FOR_ASSEMBLER"
    assert handoff["mapped_pages"] == [1, 2]
    assert handoff["assembly_status"] == "not_started"
    assert handoff["api_calls_this_run"] == 0
    assert not (source.root / "assembled-issue.json").exists()
    assert not (source.root / "assembled").exists()
    assert_semantically_neutral(load_json(source.root / handoff["physical_map"]["path"]))
    assert len(handoff["visual_maps"]) == 2


def test_assembler_consumes_ingestor_handoff_and_both_maps(source):
    handoff = ingest(source)
    result = assemble_issue(source.root, require_ingestor_handoff=True)
    assert result["producer"] == "ASSEMBLER"
    assert result["ingestor_handoff_sha256"]
    assert result["all_pages_processed"]
    assert result["coverage"]["unmatched"] == 0
    assert len(result["articles"]) == 2
    assert load_json(source.root / "ingestor-output.json") == handoff


def test_ingestor_partial_live_maps_resume_without_recalling_completed_page(source):
    provider = FakeProvider(source.maps)
    first = extract_maps(source.pdf.parent / "bundle.json", source.root, provider=provider, max_api_calls=1)
    assert first["status"] == "PARTIAL" and first["mapped_pages"] == [1]
    assert first["needs_review"] and not first["all_pages_mapped"]
    second = extract_maps(source.pdf.parent / "bundle.json", source.root, provider=provider, max_api_calls=1)
    assert second["status"] == "READY_FOR_ASSEMBLER"
    assert len(provider.calls) == 2
    third = extract_maps(source.pdf.parent / "bundle.json", source.root, provider=provider, max_api_calls=1)
    assert third["api_calls_this_run"] == 0
    assert len(provider.calls) == 2


def test_subset_is_partial_handoff_even_when_all_selected_maps_exist(source):
    result = ingest(source, pages=[1])
    assert result["status"] == "PARTIAL" and not result["all_pages_mapped"]
    assert not assemble_issue(source.root, require_ingestor_handoff=True)["all_pages_processed"]


def test_failed_ingestor_rerun_cannot_leave_stale_ready_handoff(source):
    ingest(source)
    changed = load_json(source.maps / "p0001.json")
    changed["notes"].append("changed layout")
    write_json(source.maps / "p0001.json", changed)
    with pytest.raises(PageMapError, match="offline map changed"): ingest(source)
    assert not (source.root / "ingestor-output.json").exists()
    with pytest.raises(PageMapError, match="requires ingestor-output"):
        assemble_issue(source.root, require_ingestor_handoff=True)


@pytest.mark.parametrize("change", ["source", "hash", "readiness", "mapset", "unsafe-path"])
def test_assembler_rejects_invalid_handoff(source, change):
    handoff = ingest(source)
    if change == "source": handoff["source_id"] = "other-edition"
    if change == "hash": handoff["visual_maps"][0]["sha256"] = "0" * 64
    if change == "readiness": handoff["status"] = "PARTIAL"
    if change == "mapset": handoff["mapped_pages"] = [1]
    if change == "unsafe-path": handoff["visual_maps"][0]["path"] = "../other.json"
    write_json(source.root / "ingestor-output.json", handoff)
    with pytest.raises(PageMapError): assemble_issue(source.root, require_ingestor_handoff=True)


def test_role_clis_use_independent_stages(source, capsys):
    assert ingestor_main(["--bundle", str(source.pdf.parent / "bundle.json"), "--output", str(source.root),
                          "--maps-dir", str(source.maps)]) == 0
    assert not (source.root / "assembled-issue.json").exists()
    assert assembler_main(["--issue-dir", str(source.root), "--require-full-issue"]) == 0
    assert (source.root / "assembled-issue.json").exists()


def test_cli_requires_visual_mapping_configuration_and_paid_opt_in(source, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        ingestor_main(["--bundle", str(source.pdf.parent / "bundle.json"), "--output", str(source.root)])
    assert ingestor_main(["--bundle", str(source.pdf.parent / "bundle.json"), "--output", str(source.root),
                          "--live", "--model", "test"]) == 1
    assert not (source.root / "ingestor-output.json").exists()
