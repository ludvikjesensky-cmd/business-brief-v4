from dataclasses import replace
from hashlib import sha256
import pytest
from business_brief.enrichment import (
    Annotation, ArticleRef, ArticleSnapshot, Enrichment, EnrichmentError, Evidence,
    IndexRef, KnowledgeLink, KnowledgeRevision, Review, Signal, validate_batch, validate_enrichment, validate_promotion, validate_knowledge_revision,
)
from business_brief.knowledge_retrieval import RetrievalHit, compatible_hits, metadata_candidates, metadata_matches


@pytest.fixture
def data():
    refs = tuple(ArticleRef(f"a{i}", str(i)*64, "article-records", f"edition/{i}.json") for i in (1, 2))
    texts = ("Mercedes mění výrobu. Original English evidence.", "Volkswagen investiert in Deutschland.")
    indexes = tuple(IndexRef(r, f"index{i}", "BB-EMBEDDING-V1", "BB-CHUNKING-V1") for i, r in enumerate(refs))
    snapshots = {r: ArticleSnapshot(r, t, "VERIFIED", "PASS", (idx,)) for r, t, idx in zip(refs, texts, indexes)}
    evidence = tuple(Evidence(r, 0, len(t), sha256(t.encode()).hexdigest(), idx) for r, t, idx in zip(refs, texts, indexes))
    rows = tuple(Enrichment("article", r.article_id, (r,), "chat", "1", "BB-ENRICHMENT", "1", "manual-v1", "ordinal-v1") for r in refs)
    return refs, snapshots, evidence, rows


def review(evidence):
    return Review("editor", "2026-10-21T12:00:00+02:00", "checked source evidence", evidence)


def check(row, snapshots, terms=None, accepted=None):
    validate_enrichment(row, snapshots=snapshots, terms=terms or {}, accepted=accepted or {})


def signal(evidence, day="2026-10-20", sid="s1"):
    return Signal(sid, "new evidence", day, evidence, (), .8, "accepted", review(evidence))


def test_exact_coverage_identity_and_source_immutability(data):
    refs, snapshots, _, rows = data
    before = dict(snapshots)
    validate_batch(rows, expected=frozenset(refs), snapshots=snapshots, terms={}, accepted={})
    assert snapshots == before
    assert rows[0].identity == replace(rows[0]).identity
    assert rows[0].identity != replace(rows[0], producer_version="2").identity


@pytest.mark.parametrize("mode", ["duplicate", "missing", "extra", "mixed"])
def test_bad_coverage(data, mode):
    refs, snapshots, _, rows = data
    bad = {"duplicate": rows+(rows[0],), "missing": rows[:1], "extra": rows,
           "mixed": (rows[0], replace(rows[1], profile_version="2"))}[mode]
    with pytest.raises(EnrichmentError):
        validate_batch(bad, expected=frozenset(refs[:1] if mode == "extra" else refs), snapshots=snapshots, terms={}, accepted={})


def test_artifact_sha_binding(data):
    refs, snapshots, _, rows = data
    wrong = replace(refs[0], article_record_sha256="f"*64)
    with pytest.raises(EnrichmentError, match="unknown member"):
        check(replace(rows[0], members=(wrong,)), snapshots)
    assert rows[0].identity != replace(rows[0], members=(wrong,)).identity


@pytest.mark.parametrize("change", ["sha", "range", "index", "article", "empty"])
def test_exact_evidence(data, change):
    _, snapshots, evidence, rows = data
    e = evidence[0]
    bad = {"sha": (replace(e, passage_sha256="0"*64),), "range": (replace(e, end=999),),
           "index": (replace(e, index=evidence[1].index),), "article": evidence[1:], "empty": ()}[change]
    with pytest.raises(EnrichmentError):
        check(replace(rows[0], annotations=(Annotation("topics", "Výroba", None, bad, .7),)), snapshots)


def test_explicit_review_controlled_ids_and_entity_dedup(data):
    _, snapshots, evidence, rows = data
    a = Annotation("entities", "Mercedes-Benz", "mercedes", evidence[:1], 1, "accepted")
    terms = {("entities", "mercedes"): "Mercedes-Benz"}
    with pytest.raises(EnrichmentError, match="explicit review"):
        check(replace(rows[0], annotations=(a,)), snapshots, terms)
    a = replace(a, review=review(evidence[:1]))
    row = replace(rows[0], annotations=(a,))
    check(row, snapshots, terms)
    for bad in (replace(row, annotations=(a, a)), replace(row, annotations=(replace(a, label="unknown alias"),)),
                replace(row, category="invented")):
        with pytest.raises(EnrichmentError):
            check(bad, snapshots, terms)
    a = replace(a, term_id=None, status="candidate", review=None)
    with pytest.raises(EnrichmentError, match="duplicate normalized"):
        check(replace(row, annotations=(a, replace(a, label=" MERCEDES-BENZ "))), snapshots)


def test_candidate_vs_accepted_knowledge(data):
    _, snapshots, evidence, rows = data
    link = KnowledgeLink("trend", "Auto restructuring", None, "supports", evidence[:1], 1)
    check(replace(rows[0], knowledge_links=(link,)), snapshots)
    with pytest.raises(EnrichmentError, match="accepted durable target"):
        check(replace(rows[0], knowledge_links=(replace(link, status="accepted", review=review(evidence[:1])),)), snapshots)
    with pytest.raises(EnrichmentError, match="not accepted knowledge"):
        check(replace(rows[0], knowledge_links=(replace(link, object_id="candidate-id", object_revision_sha256="a"*64),)), snapshots)


@pytest.mark.parametrize("relation", ["supports", "weakens", "contradicts", "neutral"])
def test_signal_counterevidence(data, relation):
    _, snapshots, evidence, rows = data
    link = KnowledgeLink("trend", "x", None, relation, evidence[:1], .6)
    check(replace(rows[0], signals=(replace(signal(evidence[:1]), links=(link,)),)), snapshots)


def test_signals_require_evidence_and_dates(data):
    _, snapshots, evidence, rows = data
    for bad in (replace(signal(evidence[:1]), evidence=()), replace(signal(evidence[:1]), observed_on="yesterday"),
                replace(signal(evidence[:1]), links=(KnowledgeLink("trend", "x", None, "supports", evidence[1:], .8),))):
        with pytest.raises(EnrichmentError):
            check(replace(rows[0], signals=(bad,)), snapshots)


def test_no_one_article_or_same_day_trend_promotion(data):
    _, snapshots, evidence, _ = data
    s1, s2 = signal(evidence[:1]), signal(evidence[1:], "2026-10-21", "s2")
    for signals in ((s1,), (s1, replace(s2, observed_on=s1.observed_on)),
                    (s1, replace(s2, evidence=evidence[:1], review=review(evidence[:1]))),
                    (s1, replace(s2, status="candidate"))):
        with pytest.raises(EnrichmentError):
            validate_promotion(kind="trend", signals=signals, review=review(evidence), snapshots=snapshots)
    validate_promotion(kind="trend", signals=(s1, s2), review=review(evidence), snapshots=snapshots)
    validate_promotion(kind="story_thread", signals=(s1,), review=review(evidence[:1]), snapshots=snapshots)


def test_topic_output_and_member_binding(data):
    refs, snapshots, _, rows = data
    topic = replace(rows[0], subject_kind="daily_topic", subject_id="topic1", members=refs,
                    topic_output_sha256="a"*64, composer_run_id="run1")
    check(topic, snapshots)
    for bad in (replace(topic, topic_output_sha256=None), replace(topic, composer_run_id=None), replace(topic, members=(refs[0], refs[0]))):
        with pytest.raises(EnrichmentError):
            check(bad, snapshots)
    with pytest.raises(EnrichmentError):
        check(topic, {r: replace(s, indexes=()) for r, s in snapshots.items()})


def test_multilingual_profile_compatibility(data):
    _, snapshots, evidence, _ = data
    indexes = frozenset(s.indexes[0] for s in snapshots.values())
    hits = tuple(RetrievalHit(e.index, "vector", .5) for e in evidence)
    assert compatible_hits(hits, indexes=indexes, embedding_profile="BB-EMBEDDING-V1", chunking_profile="BB-CHUNKING-V1") == hits
    wrong = replace(hits[0].index, embedding_profile="old")
    assert compatible_hits((RetrievalHit(wrong, "vector"),), indexes=indexes | {wrong}, embedding_profile="BB-EMBEDDING-V1", chunking_profile="BB-CHUNKING-V1") == ()
    with pytest.raises(EnrichmentError):
        compatible_hits((RetrievalHit(wrong, "vector"),), indexes=indexes, embedding_profile="BB-EMBEDDING-V1", chunking_profile="BB-CHUNKING-V1")


def test_shared_broad_trend_never_forces_daily_topic(data):
    refs, snapshots, evidence, rows = data
    enriched = tuple(replace(r, annotations=(Annotation("topics", "Automotive", "auto", (e,), .9, "accepted", review((e,))),),
                            knowledge_links=(KnowledgeLink("trend", "Restructuring", "trend1", "supports", (e,), .9, "accepted", review((e,)), "b"*64),))
                     for r, e in zip(rows, evidence))
    for r in enriched:
        check(r, snapshots, {("topics", "auto"): "Automotive"}, {("trend1", "b"*64): "trend"})
    assert metadata_matches(enriched, field="trend", object_id="trend1") == frozenset(refs)
    assert metadata_candidates(enriched, corpus=frozenset(refs)) == ()
    entities = tuple(replace(r, annotations=(Annotation("entities", "Group", "group", (e,), .8, "accepted", review((e,))),)) for r, e in zip(enriched, evidence))
    edges = metadata_candidates(entities, corpus=frozenset(refs))
    assert len(edges) == 1 and edges[0].requires_semantic_evaluation
    candidates = tuple(replace(r, annotations=tuple(replace(a, status="candidate", review=None) for a in r.annotations)) for r in entities)
    assert metadata_matches(candidates, field="entities", object_id="group") == frozenset()
    assert metadata_candidates(candidates, corpus=frozenset(refs)) == ()


@pytest.mark.parametrize("status", ["NEEDS_REVIEW", "BLOCKED"])
def test_ineligible_article_rejected(data, status):
    refs, snapshots, _, rows = data
    snapshots[refs[0]] = replace(snapshots[refs[0]], assembly_status=status)
    with pytest.raises(EnrichmentError, match="ineligible"):
        check(rows[0], snapshots)


@pytest.mark.parametrize("confidence", [float("nan"), float("inf"), -.1, 1.1, True])
def test_bad_confidence(data, confidence):
    _, snapshots, evidence, rows = data
    a = Annotation("tags", "test", None, evidence[:1], confidence)
    with pytest.raises(EnrichmentError, match="confidence"):
        check(replace(rows[0], annotations=(a,)), snapshots)


def test_review_provenance_and_category_evidence(data):
    _, snapshots, evidence, rows = data
    check(replace(rows[0], category="Technologie", category_evidence=evidence[:1]), snapshots)
    with pytest.raises(EnrichmentError):
        check(replace(rows[0], category="Technologie"), snapshots)
    a = Annotation("tags", "test", "test", evidence[:1], .8, "accepted", review(evidence[:1]))
    terms = {("tags", "test"): "test"}
    for bad_review in (replace(a.review, reviewer=""), replace(a.review, reviewed_at="2026-10-21"),
                       replace(a.review, evidence=evidence[1:])):
        with pytest.raises(EnrichmentError):
            check(replace(rows[0], annotations=(replace(a, review=bad_review),)), snapshots, terms)


def test_durable_revision_lifecycle_and_acceptance(data):
    _, snapshots, evidence, _ = data
    revision = KnowledgeRevision("trend1", "trend", "Auto restructuring", "European automotive sector",
                                 "emerging", "chat", "1", "BB-ENRICHMENT", "1",
                                 (signal(evidence[:1]), signal(evidence[1:], "2026-10-21", "s2")),
                                 review(evidence), "accepted")
    validate_knowledge_revision(revision, snapshots=snapshots)
    assert revision.revision_sha256 == replace(revision).revision_sha256
    assert revision.revision_sha256 != replace(revision, lifecycle="weakening").revision_sha256
    for bad in (replace(revision, lifecycle="resolved"), replace(revision, review=None),
                replace(revision, signals=revision.signals[:1]), replace(revision, producer_version="")):
        with pytest.raises(EnrichmentError):
            validate_knowledge_revision(bad, snapshots=snapshots)


def test_links_pin_exact_accepted_revision(data):
    _, snapshots, evidence, rows = data
    link = KnowledgeLink("story_thread", "Factory restructuring", "thread1", "supports", evidence[:1],
                         .8, "accepted", review(evidence[:1]), "a"*64)
    check(replace(rows[0], knowledge_links=(link,)), snapshots, accepted={("thread1", "a"*64): "story_thread"})
    for bad in (replace(link, object_revision_sha256=None), replace(link, object_revision_sha256="b"*64)):
        with pytest.raises(EnrichmentError):
            check(replace(rows[0], knowledge_links=(bad,)), snapshots, accepted={("thread1", "a"*64): "story_thread"})
