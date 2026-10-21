import pytest

from business_brief.enrichment import (
    ENRICHMENT_PROFILE,
    ENRICHMENT_SCHEMA,
    EnrichmentError,
    stable_id,
    topic_membership_has_concrete_evidence,
    validate_article_enrichment,
    validate_trend_promotion,
)

def _payload():
    aid = "a-1"
    sha = "1" * 64
    refs = ["a-1#p1"]
    signal_id = stable_id("sig", aid, sha, "VW zvyšuje úsporný cíl", "supports", refs)
    return {
        "schema_version": ENRICHMENT_SCHEMA,
        "profile": ENRICHMENT_PROFILE,
        "producer": "test",
        "articles": [{
            "article_id": aid,
            "article_record_sha256": sha,
            "category": "Firmy a průmysl",
            "topics": ["Volkswagen", "nákladové škrty"],
            "tags": ["VW", "automotive"],
            "entities": [{"name": "Volkswagen", "type": "company"}],
            "geographies": ["Německo"],
            "industries": ["automotive"],
            "story_thread_candidates": [{
                "label": "Volkswagen restructuring 2026",
                "relation": "new development",
                "evidence_refs": refs,
                "confidence": 0.9,
            }],
            "trend_candidates": [{
                "label": "restrukturalizace evropského autoprůmyslu",
                "relation": "supports",
                "evidence_refs": refs,
            }],
            "signals": [{
                "signal_id": signal_id,
                "description": "VW zvyšuje úsporný cíl",
                "polarity": "supports",
                "target_kind": "trend",
                "target_ref_or_label": "restrukturalizace evropského autoprůmyslu",
                "evidence_refs": refs,
            }],
        }],
    }

def test_exact_article_sha_binding_and_coverage():
    payload = _payload()
    validate_article_enrichment(payload, expected_articles={"a-1": "1" * 64})
    with pytest.raises(EnrichmentError):
        validate_article_enrichment(payload, expected_articles={"a-1": "2" * 64})
    with pytest.raises(EnrichmentError):
        validate_article_enrichment(payload, expected_articles={"a-1": "1" * 64, "a-2": "2" * 64})

def test_signal_requires_evidence():
    payload = _payload()
    payload["articles"][0]["signals"][0]["evidence_refs"] = []
    with pytest.raises(EnrichmentError):
        validate_article_enrichment(payload, expected_articles={"a-1": "1" * 64})

def test_signal_id_is_deterministic():
    payload = _payload()
    payload["articles"][0]["signals"][0]["signal_id"] = "sig-wrong"
    with pytest.raises(EnrichmentError):
        validate_article_enrichment(payload, expected_articles={"a-1": "1" * 64})

def test_one_article_cannot_promote_accepted_trend():
    rows = [{
        "article_id": "a-1",
        "article_record_sha256": "1" * 64,
        "evidence_refs": ["a-1#p1"],
    }]
    with pytest.raises(EnrichmentError):
        validate_trend_promotion(signal_rows=rows, accepted_status="accepted")

def test_multi_article_trend_promotion_can_pass_validation():
    rows = [
        {"article_id": "a-1", "article_record_sha256": "1" * 64, "evidence_refs": ["a-1#p1"]},
        {"article_id": "a-2", "article_record_sha256": "2" * 64, "evidence_refs": ["a-2#p3"]},
    ]
    validate_trend_promotion(signal_rows=rows, accepted_status="accepted")

def test_broad_shared_trend_is_not_topic_membership_evidence():
    assert not topic_membership_has_concrete_evidence(["trend", "industry", "entity"])
    assert topic_membership_has_concrete_evidence(["trend", "same_event"])
