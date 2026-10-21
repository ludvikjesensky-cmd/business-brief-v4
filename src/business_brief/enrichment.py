from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable

ENRICHMENT_SCHEMA = "editorial-enrichment-v1"
ENRICHMENT_PROFILE = "BB-ENRICHMENT-V1"
CATEGORIES = (
    "Politika", "Geopolitika", "Ekonomika", "Energie", "Firmy a průmysl",
    "Technologie", "Finance a trhy", "Osobní finance", "Právo a regulace",
    "Média", "Ostatní",
)
POLARITIES = {"supports", "weakens", "contradicts", "neutral"}
KNOWLEDGE_LIFECYCLE = {"candidate", "accepted", "rejected", "retired"}

class EnrichmentError(ValueError):
    pass

def stable_id(prefix: str, *parts: Any) -> str:
    raw = json.dumps(parts, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"{prefix}-" + hashlib.sha256(raw).hexdigest()[:24]

def _strings(value: Any, field: str, *, minimum: int = 0, maximum: int = 50) -> list[str]:
    if not isinstance(value, list):
        raise EnrichmentError(f"{field} must be a list")
    cleaned: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise EnrichmentError(f"{field} must contain non-empty strings")
        cleaned.append(item.strip())
    if len(cleaned) != len(set(cleaned)):
        raise EnrichmentError(f"{field} must not contain duplicates")
    if not minimum <= len(cleaned) <= maximum:
        raise EnrichmentError(f"{field} count out of range")
    return cleaned

def _evidence_refs(value: Any, field: str) -> list[str]:
    return _strings(value, field, minimum=1, maximum=50)

def _validate_candidate(row: Any, field: str) -> None:
    if not isinstance(row, dict):
        raise EnrichmentError(f"{field} entries must be objects")
    label = row.get("label")
    if not isinstance(label, str) or not label.strip():
        raise EnrichmentError(f"{field}.label is required")
    relation = row.get("relation")
    if not isinstance(relation, str) or not relation.strip():
        raise EnrichmentError(f"{field}.relation is required")
    _evidence_refs(row.get("evidence_refs"), f"{field}.evidence_refs")
    confidence = row.get("confidence")
    if confidence is not None and (not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1):
        raise EnrichmentError(f"{field}.confidence must be between 0 and 1")

def _validate_signal(row: Any, article_id: str, article_sha: str) -> None:
    if not isinstance(row, dict):
        raise EnrichmentError("signals entries must be objects")
    desc = row.get("description")
    if not isinstance(desc, str) or not desc.strip():
        raise EnrichmentError("signal description is required")
    if row.get("polarity") not in POLARITIES:
        raise EnrichmentError("invalid signal polarity")
    refs = _evidence_refs(row.get("evidence_refs"), "signals.evidence_refs")
    expected_id = stable_id("sig", article_id, article_sha, desc.strip(), row.get("polarity"), refs)
    supplied = row.get("signal_id")
    if supplied is not None and supplied != expected_id:
        raise EnrichmentError("signal_id is not deterministic for its evidence")
    target_kind = row.get("target_kind")
    if target_kind is not None and target_kind not in {"story_thread", "trend"}:
        raise EnrichmentError("invalid signal target_kind")

def validate_article_enrichment(payload: dict[str, Any], *, expected_articles: dict[str, str]) -> None:
    if payload.get("schema_version") != ENRICHMENT_SCHEMA:
        raise EnrichmentError("unsupported enrichment schema")
    if payload.get("profile") != ENRICHMENT_PROFILE:
        raise EnrichmentError("unsupported enrichment profile")
    if not isinstance(payload.get("producer"), str) or not payload["producer"].strip():
        raise EnrichmentError("producer is required")
    rows = payload.get("articles")
    if not isinstance(rows, list):
        raise EnrichmentError("articles must be a list")
    actual: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise EnrichmentError("article enrichment row must be an object")
        aid = row.get("article_id")
        if not isinstance(aid, str) or not aid or aid in actual:
            raise EnrichmentError("invalid or duplicate article_id")
        actual.add(aid)
        if aid not in expected_articles:
            raise EnrichmentError(f"unexpected article_id {aid}")
        sha = row.get("article_record_sha256")
        if sha != expected_articles[aid]:
            raise EnrichmentError(f"article_record_sha256 mismatch for {aid}")
        if row.get("category") not in CATEGORIES:
            raise EnrichmentError(f"unsupported category for {aid}")
        _strings(row.get("topics"), "topics", minimum=1, maximum=8)
        _strings(row.get("tags"), "tags", minimum=1, maximum=20)
        _strings(row.get("geographies"), "geographies", maximum=20)
        _strings(row.get("industries"), "industries", maximum=20)
        entities = row.get("entities")
        if not isinstance(entities, list):
            raise EnrichmentError("entities must be a list")
        seen_entities: set[tuple[str, str | None]] = set()
        for entity in entities:
            if not isinstance(entity, dict) or not isinstance(entity.get("name"), str) or not entity["name"].strip():
                raise EnrichmentError("entity name is required")
            etype = entity.get("type")
            if etype is not None and (not isinstance(etype, str) or not etype.strip()):
                raise EnrichmentError("entity type must be a non-empty string")
            key = (entity["name"].strip(), etype.strip() if isinstance(etype, str) else None)
            if key in seen_entities:
                raise EnrichmentError("duplicate entity")
            seen_entities.add(key)
        for field in ("story_thread_candidates", "trend_candidates"):
            values = row.get(field)
            if not isinstance(values, list):
                raise EnrichmentError(f"{field} must be a list")
            for candidate in values:
                _validate_candidate(candidate, field)
        signals = row.get("signals")
        if not isinstance(signals, list):
            raise EnrichmentError("signals must be a list")
        for signal in signals:
            _validate_signal(signal, aid, sha)
    if actual != set(expected_articles):
        missing = sorted(set(expected_articles) - actual)
        raise EnrichmentError(f"article coverage mismatch missing={missing}")

def validate_trend_promotion(*, signal_rows: Iterable[dict[str, Any]], accepted_status: str = "accepted") -> None:
    rows = list(signal_rows)
    if accepted_status not in KNOWLEDGE_LIFECYCLE:
        raise EnrichmentError("invalid trend lifecycle status")
    if accepted_status != "accepted":
        return
    if len(rows) < 2:
        raise EnrichmentError("accepted trend requires at least two signals")
    article_versions = {
        (row.get("article_id"), row.get("article_record_sha256"))
        for row in rows
        if row.get("article_id") and row.get("article_record_sha256")
    }
    if len(article_versions) < 2:
        raise EnrichmentError("accepted trend cannot be promoted from one article version")
    for row in rows:
        _evidence_refs(row.get("evidence_refs"), "trend signal evidence_refs")

def topic_membership_has_concrete_evidence(evidence_kinds: Iterable[str]) -> bool:
    concrete = {
        "same_event", "same_story", "same_concrete_problem", "explicit_relation",
        "fulltext_match", "chunk_match",
    }
    return bool(concrete.intersection(set(evidence_kinds)))
