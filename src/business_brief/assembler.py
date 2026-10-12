"""Assembler role: deterministic article assembly consuming both Ingestor maps."""
from __future__ import annotations

import base64
import html
from dataclasses import asdict
from pathlib import Path

from .visual_assembly import MatchingPolicy, assemble_page
from .visual_continuations import assemble_articles
from .visual_page_map import PageMapError
from .visual_pipeline import canonical, digest, issue_lock, load_json, page_name, validate_envelope, verify_issue, write_json

def preview_html(image, layout, aspect_ratio):
    """Self-contained image + inspectable zones; article data is always escaped."""
    marks = []
    def rect(box, label, color):
        x0, y0, x1, y1 = (v * 1000 for v in box)
        marks.append(f'<g><title>{html.escape(label)}</title><rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-width="2"/><text x="{x0+2}" y="{y0+12}" font-size="12" fill="{color}">{html.escape(label)}</text></g>')
    for a in layout["articles"]:
        for role in ("headline", "byline", "body_flow"):
            for i, region in enumerate(a[role], 1):
                rect(region["bbox"], f"{a['article_id']}:{role}:{i}", "#0066bb")
        for embedded in a["embedded_objects"]:
            for box in embedded["footprint"]:
                rect(box, embedded["kind"], "#a04000")
            for region in embedded["caption_regions"]:
                rect(region["bbox"], "caption", "#007755")
        for e in a["exclusions"]:
            rect(e["bbox"], e["kind"], "#b00040")
    for e in layout["exclusions"]:
        rect(e["bbox"], e["kind"], "#b00040")
    encoded = base64.b64encode(image).decode("ascii")
    return ('<!doctype html><meta charset="utf-8"><title>Visual Page Map</title>'
            '<style>body{margin:20px;background:#eee;font:16px system-ui}svg{display:block;max-width:100%;height:auto;background:white}text{paint-order:stroke;stroke:white;stroke-width:2px}</style>'
            '<p>Blue: reading zones in explicit order · Brown: embedded objects · Green: captions · Red: exclusions</p>'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="{1000*aspect_ratio}" preserveAspectRatio="none"><image href="data:image/jpeg;base64,{encoded}" width="1000" height="1000" preserveAspectRatio="none"/>'
            + "".join(marks) + '</svg>')


def assemble_issue(root, *, policy=None, links=None, require_ingestor_handoff=False):
    root, policy = Path(root), policy or MatchingPolicy()
    with issue_lock(root):
        manifest, physical = verify_issue(root)
        handoff_path = root / "ingestor-output.json"
        handoff_sha = None
        if handoff_path.exists():
            handoff = load_json(handoff_path)
            if (handoff.get("schema_version") != "ingestor-maps-v1"
                    or handoff.get("producer") != "INGESTOR" or handoff.get("consumer") != "ASSEMBLER"
                    or handoff.get("source_id") != physical["source_id"]
                    or handoff.get("source_sha256") != physical["source_sha256"]
                    or handoff.get("prepared_pdf_sha256") != manifest["settings"]["pdf_sha256"]
                    or handoff.get("page_count") != manifest["settings"]["page_count"]
                    or handoff.get("selected_pages") != manifest["settings"]["selected_pages"]
                    or handoff["physical_map"]["path"] != "physical-map.json"
                    or handoff["physical_map"]["sha256"] != digest((root / "physical-map.json").read_bytes())
                    or handoff["physical_map"]["canonical_sha256"] != manifest["settings"]["physical_map_sha256"]):
                raise PageMapError("Ingestor handoff provenance mismatch")
            present = [p["page_no"] for p in manifest["pages"] if (root / "maps" / f"{page_name(p['page_no'])}.json").exists()]
            if handoff["mapped_pages"] != present or [p["page_no"] for p in handoff["visual_maps"]] != present:
                raise PageMapError("Ingestor handoff map set mismatch; rerun Ingestor")
            complete = present == list(range(1, manifest["settings"]["page_count"] + 1))
            if handoff["all_pages_mapped"] != complete or handoff["status"] != ("READY_FOR_ASSEMBLER" if complete else "PARTIAL"):
                raise PageMapError("Ingestor handoff readiness mismatch")
            for entry in handoff["visual_maps"]:
                expected = f"maps/{page_name(entry['page_no'])}.json"
                if entry["path"] != expected or entry["sha256"] != digest((root / expected).read_bytes()):
                    raise PageMapError("Ingestor handoff Visual Page Map hash mismatch")
            handoff_sha = digest(handoff_path.read_bytes())
        elif require_ingestor_handoff:
            raise PageMapError("Assembler requires ingestor-output.json; run Ingestor first")
        results, missing, usage = [], [], []
        physical_pages = {p["page_no"]: p for p in physical["pages"]}
        for meta in manifest["pages"]:
            n, name = meta["page_no"], page_name(meta["page_no"])
            path = root / "maps" / f"{name}.json"
            if not path.exists():
                missing.append(n)
                continue
            envelope = validate_envelope(load_json(path), manifest, meta)
            result = assemble_page(physical_pages[n], envelope["layout"], policy)
            result["binding"], result["layout_sha256"] = envelope["binding"], envelope["layout_sha256"]
            result["mapper_provenance"] = envelope["provenance"]
            write_json(root / "assembled" / f"{name}.json", result)
            preview = root / "previews" / f"{name}.html"
            preview.parent.mkdir(parents=True, exist_ok=True)
            preview.write_text(preview_html((root / "images" / f"{name}.jpg").read_bytes(), envelope["layout"], meta["image_height"] / meta["image_width"]), encoding="utf-8")
            results.append(result)
            usage.append({"page_no": n, **envelope["provenance"]})
        processed = [p["page_no"] for p in results]
        full = processed == list(range(1, manifest["settings"]["page_count"] + 1))
        totals = {k: sum(p["coverage"][k] for p in results) for k in ("total", "assigned", "excluded", "unmatched", "ambiguous")}
        articles, unresolved = assemble_articles(results, physical["source_sha256"],
            manifest["settings"]["physical_map_sha256"], links)
        issue = {"schema_version": "assembled-visual-issue-v1", "producer": "ASSEMBLER",
            "ingestor_handoff_sha256": handoff_sha, "source_id": physical["source_id"],
            "source_sha256": physical["source_sha256"], "physical_map_sha256": manifest["settings"]["physical_map_sha256"],
            "page_count": manifest["settings"]["page_count"], "processed_pages": processed,
            "missing_selected_pages": missing, "all_pages_processed": full,
            "needs_review": not full or any(p["needs_review"] for p in results),
            "coverage_kind": "physical_block_accounting_not_semantic_completeness",
            "cross_page_merge_status": "reviewed_explicit_links" if links is not None else "not_performed",
            "unresolved_continuations": unresolved,
            "continuation_links_sha256": digest(canonical(links)) if links is not None else None,
            "editorial_selection_status": "not_started", "deep_read_status": "not_started",
            "coverage": totals, "policy": asdict(policy), "usage_by_page": usage,
            "pages": results, "articles": articles}
        write_json(root / "assembled-issue.json", issue)
        return issue
