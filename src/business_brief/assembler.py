from __future__ import annotations

import hashlib
import json
import re
import struct
import unicodedata
from dataclasses import dataclass
from typing import Any, Callable, Iterable



ARTICLE_RECORD_SCHEMA = "article-record-v1"
ASSEMBLER_VERSION = "assembler-v1"
CANONICAL_SEPARATOR = "\n\n"
ELIGIBLE_ITEM_STATUSES = {"VERIFIED", "VERIFIED_WITH_NOTES"}
ELIGIBLE_PAGE_STATUSES = {"VERIFIED", "VERIFIED_WITH_NOTES"}
ASSEMBLY_STATUSES = {"VERIFIED", "VERIFIED_WITH_NOTES", "NEEDS_REVIEW", "BLOCKED"}


class AssemblerError(RuntimeError):
    pass


class IntegrityError(AssemblerError):
    pass


@dataclass(frozen=True)
class SelectedPage:
    page_no: int
    key: str
    sha256: str
    schema_version: str
    generation: str
    kind: str
    revision_id: str | None
    raw: bytes
    page: dict[str, Any]


@dataclass(frozen=True)
class AssemblyIssue:
    status: str
    code: str
    message: str
    item_refs: tuple[tuple[int, str], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "item_refs": [
                {"page_no": page_no, "page_item_id": item_id}
                for page_no, item_id in self.item_refs
            ],
        }


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise IntegrityError("value is not deterministically JSON-serializable") from exc


def strict_json(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IntegrityError("invalid UTF-8 JSON") from exc


def verify_selected_page(selection: dict[str, Any], raw: bytes) -> SelectedPage:
    expected = selection.get("sha256")
    if not isinstance(expected, str) or sha256_bytes(raw) != expected:
        raise IntegrityError("selected page SHA-256 mismatch")
    document = strict_json(raw)
    kind = selection.get("kind")
    if kind == "revision":
        if not isinstance(document, dict) or document.get("schema_version") != "page-revision-v1":
            raise IntegrityError("selected revision wrapper has wrong schema")
        page = document.get("page")
        revision_id = document.get("revision_id")
        if revision_id != selection.get("revision_id"):
            raise IntegrityError("revision identity mismatch")
    elif kind == "canonical":
        page = document
        revision_id = None
    else:
        raise IntegrityError("unsupported selected page kind")
    if not isinstance(page, dict):
        raise IntegrityError("selected page body is missing")
    if page.get("schema_version") != selection.get("schema_version"):
        raise IntegrityError("selected page schema mismatch")
    publication = page.get("publication") or {}
    if publication.get("page_no") != selection.get("page_no"):
        raise IntegrityError("selected page number mismatch")
    if page.get("page_status") not in ELIGIBLE_PAGE_STATUSES:
        raise IntegrityError("selected page is not assembly-eligible")
    if selection.get("usable_for_assembly") is not True:
        raise IntegrityError("selection is not marked usable_for_assembly")
    return SelectedPage(
        page_no=int(selection["page_no"]),
        key=str(selection["key"]),
        sha256=expected,
        schema_version=str(selection["schema_version"]),
        generation=str(selection["generation"]),
        kind=str(kind),
        revision_id=revision_id,
        raw=raw,
        page=page,
    )


def verify_manifest(manifest: dict[str, Any], raw: bytes, expected_sha256: str) -> None:
    if sha256_bytes(raw) != expected_sha256:
        raise IntegrityError("manifest SHA-256 mismatch")
    parsed = strict_json(raw)
    if parsed != manifest:
        raise IntegrityError("manifest bytes differ from bridge assembly input")
    if manifest.get("schema_version") != "edition-selection-v1":
        raise IntegrityError("unsupported selection manifest schema")
    if manifest.get("status") != "ACCEPTED_FOR_ASSEMBLY":
        raise IntegrityError("manifest is not ACCEPTED_FOR_ASSEMBLY")
    pages = manifest.get("pages")
    source = manifest.get("source") or {}
    page_count = source.get("page_count")
    if not isinstance(page_count, int) or not isinstance(pages, list):
        raise IntegrityError("manifest page coverage is invalid")
    if sorted(p.get("page_no") for p in pages if isinstance(p, dict)) != list(range(1, page_count + 1)):
        raise IntegrityError("manifest does not select every physical page exactly once")


def verify_png_artifact(raw: bytes, artifact: dict[str, Any]) -> None:
    if sha256_bytes(raw) != artifact.get("sha256"):
        raise IntegrityError("asset SHA-256 mismatch")
    if len(raw) != artifact.get("byte_size"):
        raise IntegrityError("asset byte size mismatch")
    if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 24:
        raise IntegrityError("asset is not a valid PNG header")
    width, height = struct.unpack(">II", raw[16:24])
    if width != artifact.get("width") or height != artifact.get("height"):
        raise IntegrityError("asset dimensions mismatch")


def _node_key(page_no: int, item_id: str) -> tuple[int, str]:
    return (page_no, item_id)


def _normalize_title(value: str | None) -> set[str]:
    if not value:
        return set()
    text = unicodedata.normalize("NFKD", value.casefold())
    text = "".join(ch if ch.isalnum() else " " for ch in text)
    stop = {
        "the", "a", "an", "of", "to", "for", "from", "on", "in", "and", "as",
        "its", "is", "are", "amid", "with", "at", "by",
    }
    return {token for token in text.split() if len(token) > 1 and token not in stop}


def _target_page_number(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"(\d{1,4})\s*$", value.strip())
    return int(match.group(1)) if match else None


def _title_overlap(left: str | None, right: str | None) -> int:
    return len(_normalize_title(left) & _normalize_title(right))


def _continuation_target_page(item: dict[str, Any]) -> int | None:
    cont = item.get("continuation") or {}
    for value in (cont.get("continuation_target"), cont.get("continuation_marker")):
        page = _target_page_number(value)
        if page is not None:
            return page
    return None


def _incoming_accepts_origin(item: dict[str, Any], origin_page_no: int) -> bool:
    cont = item.get("continuation") or {}
    target = _continuation_target_page(item)
    return target is None or target == origin_page_no


def _resolve_outgoing(
    origin: tuple[int, str],
    nodes: dict[tuple[int, str], dict[str, Any]],
    by_page: dict[int, list[tuple[int, str]]],
) -> tuple[tuple[int, str] | None, str | None]:
    item = nodes[origin]["item"]
    target_page = _continuation_target_page(item)
    if target_page is None:
        return None, "continuation target does not resolve to a physical page number"
    candidates = []
    for key in by_page.get(target_page, []):
        candidate = nodes[key]["item"]
        cont = candidate.get("continuation") or {}
        if cont.get("continued_from_previous_page") is True and _incoming_accepts_origin(candidate, origin[0]):
            candidates.append(key)
    if not candidates:
        return None, f"no incoming continuation candidate on selected page {target_page}"
    if len(candidates) == 1:
        return candidates[0], None

    origin_title = item.get("title")
    scored = [(_title_overlap(origin_title, nodes[key]["item"].get("title")), key) for key in candidates]
    best_score = max(score for score, _ in scored)
    winners = [key for score, key in scored if score == best_score and score > 0]
    if len(winners) == 1:
        return winners[0], None
    return None, f"multiple continuation candidates on selected page {target_page}"


def _source_part(page: SelectedPage, item: dict[str, Any]) -> dict[str, Any]:
    text = item.get("text_on_page")
    if not isinstance(text, str) or not text:
        raise IntegrityError("assembly source part has no text_on_page")
    return {
        "page_no": page.page_no,
        "page_item_id": item["page_item_id"],
        "page_artifact_key": page.key,
        "page_artifact_sha256": page.sha256,
        "text_sha256": sha256_text(text),
    }


def _article_id(
    *,
    source_sha256: str,
    manifest_id: str,
    manifest_sha256: str,
    parts: list[dict[str, Any]],
) -> str:
    identity = {
        "contract": ARTICLE_RECORD_SCHEMA,
        "source_sha256": source_sha256,
        "manifest_id": manifest_id,
        "manifest_sha256": manifest_sha256,
        "parts": [
            {
                "page_no": part["page_no"],
                "page_item_id": part["page_item_id"],
                "page_artifact_sha256": part["page_artifact_sha256"],
                "text_sha256": part["text_sha256"],
            }
            for part in parts
        ],
    }
    return "art-" + sha256_bytes(canonical_json(identity))


def _metadata(items: list[dict[str, Any]]) -> dict[str, Any]:
    origin = next(
        (
            item
            for item in items
            if (item.get("continuation") or {}).get("starts_here") is True
        ),
        items[0],
    )
    def first(field: str) -> Any:
        value = origin.get(field)
        if value is not None:
            return value
        for item in items:
            if item.get(field) is not None:
                return item[field]
        return None
    return {
        "title": first("title"),
        "subtitle": first("subtitle"),
        "byline": first("byline"),
        "item_type": origin.get("item_type") or items[0].get("item_type") or "article",
    }


def _place_assets(items: list[dict[str, Any]], full_text: str) -> tuple[list[dict[str, Any]], bool]:
    out: list[dict[str, Any]] = []
    has_note = False
    for item in items:
        for asset in item.get("assets") or []:
            artifact = asset.get("artifact")
            if not isinstance(artifact, dict):
                raise IntegrityError("persisted v4 asset is missing artifact metadata")
            text_anchor = asset.get("text_anchor") or {}
            anchor_text = text_anchor.get("anchor_text")
            occurrences = full_text.count(anchor_text) if isinstance(anchor_text, str) and anchor_text else 0
            placement: dict[str, Any] = {
                "status": "placement_needs_review",
                "anchor_text": anchor_text,
            }
            if occurrences == 1 and text_anchor.get("status") == "anchored":
                placement = {
                    "status": "placed",
                    "position": text_anchor.get("position"),
                    "anchor_text": anchor_text,
                }
            else:
                has_note = True
            out.append(
                {
                    "asset_id": asset["asset_id"],
                    "asset_type": asset.get("asset_type"),
                    "source_page_no": asset.get("page_no"),
                    "source_page_item_id": asset.get("page_item_id"),
                    "artifact": artifact,
                    "placement": placement,
                    "title": asset.get("title"),
                    "caption": asset.get("caption"),
                }
            )
    return out, has_note


def post_check_article(
    record: dict[str, Any],
    selected_pages: dict[int, SelectedPage],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    texts: list[str] = []
    seen: set[tuple[int, str]] = set()
    ok = True

    for ordinal, part in enumerate(record.get("source_parts") or []):
        key = (part.get("page_no"), part.get("page_item_id"))
        if key in seen:
            ok = False
            checks.append({"check": "source_part_unique", "ordinal": ordinal, "status": "FAIL"})
            continue
        seen.add(key)
        page = selected_pages.get(part.get("page_no"))
        if page is None or page.key != part.get("page_artifact_key") or page.sha256 != part.get("page_artifact_sha256"):
            ok = False
            checks.append({"check": "page_identity", "ordinal": ordinal, "status": "FAIL"})
            continue
        matches = [item for item in page.page.get("items", []) if item.get("page_item_id") == part.get("page_item_id")]
        if len(matches) != 1:
            ok = False
            checks.append({"check": "page_item_identity", "ordinal": ordinal, "status": "FAIL"})
            continue
        text = matches[0].get("text_on_page")
        if not isinstance(text, str) or sha256_text(text) != part.get("text_sha256"):
            ok = False
            checks.append({"check": "source_text_sha256", "ordinal": ordinal, "status": "FAIL"})
            continue
        texts.append(text)
        checks.append({"check": "source_part", "ordinal": ordinal, "status": "PASS"})

    expected = CANONICAL_SEPARATOR.join(texts)
    expected_sha = sha256_text(expected)
    actual = record.get("full_text")
    actual_sha = sha256_text(actual) if isinstance(actual, str) else ""
    if actual != expected:
        ok = False
        checks.append({"check": "full_text_exact", "status": "FAIL"})
    else:
        checks.append({"check": "full_text_exact", "status": "PASS"})

    for asset in record.get("assets") or []:
        placement = asset.get("placement") or {}
        if placement.get("status") != "placed":
            continue
        anchor = placement.get("anchor_text")
        count = expected.count(anchor) if isinstance(anchor, str) and anchor else 0
        status = "PASS" if count == 1 else "FAIL"
        if status == "FAIL":
            ok = False
        checks.append({"check": "asset_anchor_unique", "asset_id": asset.get("asset_id"), "status": status})

    return {
        "status": "PASS" if ok else "FAIL",
        "separator": CANONICAL_SEPARATOR,
        "part_count": len(record.get("source_parts") or []),
        "expected_full_text_sha256": expected_sha,
        "actual_full_text_sha256": actual_sha,
        "checks": checks,
    }


def assemble(
    *,
    manifest: dict[str, Any],
    manifest_sha256: str,
    selected_pages: Iterable[SelectedPage],
) -> dict[str, Any]:
    pages = {page.page_no: page for page in selected_pages}
    source = manifest.get("source") or {}
    if sorted(pages) != list(range(1, int(source.get("page_count", 0)) + 1)):
        raise IntegrityError("selected page set does not match manifest coverage")

    nodes: dict[tuple[int, str], dict[str, Any]] = {}
    by_page: dict[int, list[tuple[int, str]]] = {}
    issues: list[AssemblyIssue] = []
    for page_no in sorted(pages):
        page = pages[page_no]
        by_page[page_no] = []
        for item in page.page.get("items") or []:
            item_id = item.get("page_item_id")
            if not isinstance(item_id, str) or not item_id:
                raise IntegrityError("page item is missing page_item_id")
            key = _node_key(page_no, item_id)
            if key in nodes:
                raise IntegrityError("duplicate page item identity")
            if not isinstance(item.get("text_on_page"), str) or not item.get("text_on_page"):
                issues.append(AssemblyIssue("NEEDS_REVIEW", "ITEM_WITHOUT_TEXT", "page item has no assemblable text", (key,)))
                continue
            nodes[key] = {"page": page, "item": item}
            by_page[page_no].append(key)

    edges: dict[tuple[int, str], tuple[int, str]] = {}
    incoming: dict[tuple[int, str], tuple[int, str]] = {}
    unresolved: dict[tuple[int, str], str] = {}

    for key, node in nodes.items():
        item = node["item"]
        cont = item.get("continuation") or {}
        if cont.get("continues_to_another_page") is not True:
            continue
        target, reason = _resolve_outgoing(key, nodes, by_page)
        if target is None:
            unresolved[key] = reason or "unresolved continuation"
            continue
        if target in incoming:
            unresolved[key] = "continuation target already has another origin"
            unresolved[target] = "continuation has multiple origins"
            continue
        edges[key] = target
        incoming[target] = key

    for key, node in nodes.items():
        item = node["item"]
        cont = item.get("continuation") or {}
        starts_here = cont.get("starts_here")
        from_previous = cont.get("continued_from_previous_page")
        if starts_here is True and from_previous is True:
            unresolved[key] = "continuation flags conflict: starts_here and continued_from_previous_page"
        elif starts_here is False and from_previous is not True:
            unresolved[key] = "continuation flags conflict: non-start item lacks incoming continuation"
        if from_previous is True and key not in incoming:
            unresolved[key] = "incoming continuation has no unique origin"
        status = (item.get("verification") or {}).get("status")
        if status not in ELIGIBLE_ITEM_STATUSES:
            unresolved[key] = f"item verification status is not eligible: {status}"

    visited: set[tuple[int, str]] = set()
    records: list[dict[str, Any]] = []

    for key in sorted(nodes):
        if key in visited or key in incoming:
            continue
        chain: list[tuple[int, str]] = []
        current = key
        local: set[tuple[int, str]] = set()
        while current is not None:
            if current in local:
                unresolved[current] = "continuation cycle detected"
                break
            local.add(current)
            chain.append(current)
            current = edges.get(current)

        visited.update(chain)
        chain_unresolved = [ref for ref in chain if ref in unresolved]
        if chain_unresolved:
            issues.append(
                AssemblyIssue(
                    "NEEDS_REVIEW",
                    "CONTINUATION_UNRESOLVED",
                    "; ".join(sorted({unresolved[ref] for ref in chain_unresolved})),
                    tuple(chain),
                )
            )
            continue

        items = [nodes[ref]["item"] for ref in chain]
        page_objects = [nodes[ref]["page"] for ref in chain]
        parts = [_source_part(page, item) for page, item in zip(page_objects, items)]
        full_text = CANONICAL_SEPARATOR.join(item["text_on_page"] for item in items)
        assets, asset_note = _place_assets(items, full_text)
        metadata = _metadata(items)
        notes: list[str] = []
        if any((item.get("verification") or {}).get("status") == "VERIFIED_WITH_NOTES" for item in items):
            notes.append("one or more source parts are VERIFIED_WITH_NOTES")
        if asset_note:
            notes.append("one or more assets require placement review")
        status = "VERIFIED_WITH_NOTES" if notes else "VERIFIED"

        record = {
            "schema_version": ARTICLE_RECORD_SCHEMA,
            "assembler_version": ASSEMBLER_VERSION,
            "article_id": _article_id(
                source_sha256=source["source_sha256"],
                manifest_id=manifest["manifest_id"],
                manifest_sha256=manifest_sha256,
                parts=parts,
            ),
            "publication": {
                "publication_id": source["publication_id"],
                "canonical_name": source["canonical_name"],
            },
            "edition": {
                "edition_id": source.get("edition_id"),
                "edition_date": source["edition_date"],
                "edition_variant": source["edition_variant"],
            },
            "source": {
                "source_id": source["source_id"],
                "source_sha256": source["source_sha256"],
            },
            "selection": {
                "manifest_id": manifest["manifest_id"],
                "manifest_sha256": manifest_sha256,
            },
            **metadata,
            "full_text": full_text,
            "source_parts": parts,
            "assets": assets,
            "post_check": {},
            "assembly": {
                "status": status,
                "method": "deterministic-continuation-v1",
                "notes": notes,
            },
        }
        record["post_check"] = post_check_article(record, pages)
        if record["post_check"]["status"] != "PASS":
            record["assembly"]["status"] = "BLOCKED"
            record["assembly"]["notes"].append("mandatory deterministic post-check failed")
        records.append(record)

    for key in sorted(nodes):
        if key not in visited:
            issues.append(
                AssemblyIssue(
                    "NEEDS_REVIEW",
                    "ORPHAN_CONTINUATION",
                    unresolved.get(key, "item belongs to a continuation without a chain root"),
                    (key,),
                )
            )

    return {
        "assembler_version": ASSEMBLER_VERSION,
        "manifest_id": manifest["manifest_id"],
        "manifest_sha256": manifest_sha256,
        "source_id": source["source_id"],
        "source_sha256": source["source_sha256"],
        "records": records,
        "issues": [issue.to_dict() for issue in issues],
        "counts": {
            "page_items": len(nodes),
            "article_records": len(records),
            "verified": sum(r["assembly"]["status"] == "VERIFIED" for r in records),
            "verified_with_notes": sum(r["assembly"]["status"] == "VERIFIED_WITH_NOTES" for r in records),
            "blocked": sum(r["assembly"]["status"] == "BLOCKED" for r in records),
            "needs_review": len(issues),
        },
    }


def eligible_for_persistence(record: dict[str, Any]) -> bool:
    return (
        record.get("assembly", {}).get("status") in {"VERIFIED", "VERIFIED_WITH_NOTES"}
        and record.get("post_check", {}).get("status") == "PASS"
    )


def article_storage_key(record: dict[str, Any]) -> str:
    return "/".join(
        [
            record["publication"]["publication_id"],
            record["edition"]["edition_date"],
            record["source"]["source_sha256"],
            record["selection"]["manifest_id"],
            record["article_id"] + ".json",
        ]
    )
