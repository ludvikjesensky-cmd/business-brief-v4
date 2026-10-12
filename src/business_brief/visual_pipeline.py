"""Local, sequential and resumable Visual Page Map artifact pipeline."""
from __future__ import annotations

import base64
import hashlib
import html
import json
import os
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path

from .visual_assembly import MatchingPolicy, _validate_page, assemble_page
from .visual_continuations import assemble_articles
from .visual_mapper import parse_response
from .visual_page_map import MAPPER_VERSION, PROMPT, VERSION, PageMapError, validate_layout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise PageMapError(f"cannot read JSON artifact: {Path(path).name}") from None


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("wb") as handle:
        handle.write(canonical(data) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())
    temp.replace(path)


@contextmanager
def issue_lock(root):
    """OS lock survives neither crashes nor process termination; no stale lock lease."""
    import fcntl
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".visual-map.lock").open("a") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise PageMapError("another process is using this issue directory") from None
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def page_name(page_no):
    return f"p{page_no:04d}"


def prepare_issue(pdf_path, physical_map_path, root, *, pages=None, width=600, quality=75,
                  prepared_sha256=None):
    import fitz
    root = Path(root)
    if type(width) is not int or not 128 <= width <= 2400 or type(quality) is not int or not 1 <= quality <= 100:
        raise PageMapError("invalid render dimensions/quality")
    physical = load_json(physical_map_path)
    if physical.get("schema_version") not in ("physical-map-v1", "physical-map-v2"):
        raise PageMapError("unsupported Physical Map version")
    for key in ("source_id", "source_sha256"):
        if not isinstance(physical.get(key), str) or not physical[key]:
            raise PageMapError("missing Physical Map source identity")
    source_sha = physical["source_sha256"]
    if len(source_sha) != 64 or any(c not in "0123456789abcdef" for c in source_sha):
        raise PageMapError("invalid Physical Map source SHA-256")
    pdf_bytes = Path(pdf_path).read_bytes()
    prepared_sha = digest(pdf_bytes)
    if prepared_sha != (prepared_sha256 or source_sha):
        raise PageMapError("PDF hash mismatch; for a prepared/OCR derivative supply its verified SHA-256")
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        if doc.is_encrypted:
            raise PageMapError("encrypted PDF is unsupported")
        expected = list(range(1, len(doc) + 1))
        if [p["page_no"] for p in physical["pages"]] != expected:
            raise PageMapError("Physical Map page sequence does not match PDF")
        chosen = expected if pages is None else sorted(pages)
        if not chosen or len(chosen) != len(set(chosen)) or any(type(n) is not int or n not in expected for n in chosen):
            raise PageMapError("invalid/duplicate selected pages")
        settings = {"pdf_sha256": prepared_sha, "physical_map_sha256": digest(canonical(physical)),
                    "source_id": physical["source_id"], "source_sha256": source_sha,
                    "width": width, "jpeg_quality": quality, "page_count": len(doc),
                    "selected_pages": chosen, "renderer": f"PyMuPDF-{fitz.VersionBind}",
                    "coordinate_system": "normalized-top-left-unrotated-page"}
        manifest_path = root / "manifest.json"
        with issue_lock(root):
            if manifest_path.exists():
                manifest = load_json(manifest_path)
                if manifest["settings"] != settings:
                    raise PageMapError("issue directory belongs to different inputs/config; use a new directory")
                verify_issue(root)
                return manifest
            page_meta = []
            # Check all selected pages before writing any renders.
            for n in chosen:
                page, evidence = doc[n - 1], physical["pages"][n - 1]
                _validate_page(evidence)
                if page.rotation != 0:
                    raise PageMapError("rotated PDF requires normalized prepared PDF and matching Physical Map")
                if abs(page.rect.width - evidence["width"]) > 0.01 or abs(page.rect.height - evidence["height"]) > 0.01:
                    raise PageMapError("PDF/Physical Map page dimensions mismatch")
            for n in chosen:
                page = doc[n - 1]
                pix = page.get_pixmap(matrix=fitz.Matrix(width / page.rect.width, width / page.rect.width),
                                      colorspace=fitz.csRGB, alpha=False, annots=False)
                image = pix.tobytes("jpeg", jpg_quality=quality)
                image_path = root / "images" / f"{page_name(n)}.jpg"
                image_path.parent.mkdir(parents=True, exist_ok=True)
                temp = image_path.with_suffix(".tmp")
                temp.write_bytes(image)
                temp.replace(image_path)
                page_meta.append({"page_no": n, "printed_label": page.get_label() or str(n),
                    "width": round(page.rect.width, 3), "height": round(page.rect.height, 3),
                    "image_width": pix.width, "image_height": pix.height,
                    "image_sha256": digest(image), "image_bytes": len(image)})
            manifest = {"schema_version": VERSION, "settings": settings, "pages": page_meta}
            write_json(root / "physical-map.json", physical)
            write_json(manifest_path, manifest)
            return manifest


def verify_issue(root):
    root = Path(root)
    manifest, physical = load_json(root / "manifest.json"), load_json(root / "physical-map.json")
    settings = manifest["settings"]
    if manifest["schema_version"] != VERSION or digest(canonical(physical)) != settings["physical_map_sha256"]:
        raise PageMapError("issue/Physical Map integrity mismatch")
    if physical["source_id"] != settings["source_id"] or physical["source_sha256"] != settings["source_sha256"]:
        raise PageMapError("issue source identity mismatch")
    if [p["page_no"] for p in manifest["pages"]] != settings["selected_pages"]:
        raise PageMapError("issue selected-page mismatch")
    for meta in manifest["pages"]:
        image = root / "images" / f"{page_name(meta['page_no'])}.jpg"
        if not image.is_file() or digest(image.read_bytes()) != meta["image_sha256"]:
            raise PageMapError("render image hash mismatch")
    return manifest, physical


def binding(manifest, meta):
    return {"schema_version": VERSION, "mapper_version": MAPPER_VERSION,
            "source_id": manifest["settings"]["source_id"],
            "source_sha256": manifest["settings"]["source_sha256"],
            "prepared_pdf_sha256": manifest["settings"]["pdf_sha256"],
            "physical_map_sha256": manifest["settings"]["physical_map_sha256"],
            "coordinate_system": manifest["settings"]["coordinate_system"], "page": meta}


def validate_envelope(envelope, manifest, meta):
    if envelope.get("binding") != binding(manifest, meta):
        raise PageMapError("page map belongs to a different source/image/Physical Map")
    validate_layout(envelope["layout"], meta["page_no"])
    if envelope.get("layout_sha256") != digest(canonical(envelope["layout"])):
        raise PageMapError("page map layout hash mismatch")
    return envelope


def map_issue(root, *, maps_dir=None, provider=None, max_api_calls=1):
    root = Path(root)
    if (maps_dir is None) == (provider is None):
        raise PageMapError("choose exactly one: offline maps directory or live provider")
    if type(max_api_calls) is not int or max_api_calls < 1:
        raise PageMapError("max_api_calls must be positive")
    with issue_lock(root):
        manifest, _ = verify_issue(root)
        requested = {"mode": "offline" if maps_dir is not None else "responses",
                     "prompt_sha256": digest(PROMPT.encode()), "mapper_version": MAPPER_VERSION}
        if provider is not None:
            requested.update(model=provider.model, detail=provider.detail, max_output_tokens=provider.max_output_tokens)
        call_count, accepted = 0, []
        for meta in manifest["pages"]:
            n, name = meta["page_no"], page_name(meta["page_no"])
            target, attempt_path = root / "maps" / f"{name}.json", root / "attempts" / f"{name}.json"
            if target.exists():
                envelope = validate_envelope(load_json(target), manifest, meta)
                if envelope["mapper"] != requested:
                    raise PageMapError("mapper config changed; use a new issue directory")
                if maps_dir is not None:
                    imported = load_json(Path(maps_dir) / f"{name}.json")
                    if "binding" in imported:
                        imported = validate_envelope(imported, manifest, meta)["layout"]
                    validate_layout(imported, n)
                    if digest(canonical(imported)) != envelope["layout_sha256"]:
                        raise PageMapError("offline map changed; use a new issue directory")
                accepted.append(n)
                continue
            provenance = {}
            if maps_dir is not None:
                imported = load_json(Path(maps_dir) / f"{name}.json")
                if "binding" in imported:
                    imported = validate_envelope(imported, manifest, meta)["layout"]
                layout = validate_layout(imported, n)
                provenance = {"kind": "offline_supplied_map", "api_called": False}
            else:
                if attempt_path.exists():
                    attempt = load_json(attempt_path)
                    if attempt["mapper"] != requested or attempt["binding"] != binding(manifest, meta):
                        raise PageMapError("attempt provenance/config mismatch")
                    if attempt["status"] != "response_saved":
                        raise PageMapError(f"{name}: prior API attempt unresolved/failed; inspect attempt before explicit rerun in new directory")
                    raw = load_json(root / "responses" / f"{name}.json")
                else:
                    if call_count >= max_api_calls:
                        break
                    attempt = {"binding": binding(manifest, meta), "mapper": requested, "status": "started"}
                    # Durable marker BEFORE network. Crash/timeout never silently triggers a paid retry.
                    write_json(attempt_path, attempt)
                    call_count += 1
                    metadata = {"page_no": n, "image_width": meta["image_width"], "image_height": meta["image_height"],
                        "printed_page_labels": [{"page_no": p["page_no"], "label": p["printed_label"]} for p in manifest["pages"]]}
                    try:
                        raw = provider.generate((root / "images" / f"{name}.jpg").read_bytes(), metadata)
                        write_json(root / "responses" / f"{name}.json", raw)
                    except Exception:
                        write_json(attempt_path, {**attempt, "status": "failed_or_unknown"})
                        raise
                    write_json(attempt_path, {**attempt, "status": "response_saved"})
                layout = parse_response(raw, n)
                provenance = {"kind": "responses", "api_called": True, "response_id": raw.get("id"),
                              "model": raw.get("model", provider.model), "usage": raw.get("usage", {})}
            envelope = {"binding": binding(manifest, meta), "mapper": requested, "provenance": provenance,
                        "layout": layout, "layout_sha256": digest(canonical(layout))}
            write_json(target, envelope)
            accepted.append(n)
        return {"mapped_pages": accepted, "api_calls_this_run": call_count,
                "selected_page_count": len(manifest["pages"]),
                "mapping_complete": len(accepted) == len(manifest["pages"])}


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


def assemble_issue(root, *, policy=None, links=None):
    root, policy = Path(root), policy or MatchingPolicy()
    with issue_lock(root):
        manifest, physical = verify_issue(root)
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
        issue = {"schema_version": "assembled-visual-issue-v1", "source_id": physical["source_id"],
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
