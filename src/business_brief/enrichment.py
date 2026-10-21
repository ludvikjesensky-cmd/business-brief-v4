"""Offline editorial-enrichment-v1 integrity gates; no model, Storage or database I/O.

Callers supply independently read-back Article/Index snapshots. Structural
validation proves binding, not semantic entailment or editorial approval.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime
from hashlib import sha256
import json
import math
import re
import unicodedata

CONTRACT = "editorial-enrichment-v1"
ENRICHMENT_SCHEMA = CONTRACT
ENRICHMENT_PROFILE = "BB-ENRICHMENT-V1"
CATEGORIES = (
    "Politika", "Geopolitika", "Ekonomika", "Energie", "Firmy a průmysl",
    "Technologie", "Finance a trhy", "Osobní finance", "Právo a regulace", "Média", "Ostatní",
)
ENRICHMENT_SYSTEM_PROMPT = """Ground each annotation and dated signal in exact immutable Article Record passages.
Return complete intended article coverage, retaining original source text unchanged.
Topics, tags, entities, geographies and industries describe the current article.
Story Threads track concrete continuing stories; Trends are broad long-term phenomena.
Propose candidates only. Preserve supporting, weakening, contradicting and neutral evidence.
Never establish a Trend from one article/day or promote knowledge by model confidence.
"""
FACETS = frozenset({"topics", "tags", "entities", "geographies", "industries"})
STATUSES = frozenset({"candidate", "needs_review", "accepted", "rejected", "superseded"})
RELATIONS = frozenset({"supports", "weakens", "contradicts", "neutral"})


class EnrichmentError(ValueError):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise EnrichmentError(reason)


def nonempty(value: str) -> bool:
    return isinstance(value, str) and bool(value.strip())


def normalized(value: str) -> str:
    """Lookup suggestion only: never auto-merge entities by label."""
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def digest(value: object) -> str:
    # Versioned internal identity encoding, independent of canonical source JSON.
    data = json.dumps([CONTRACT, value], ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return sha256(data).hexdigest()


@dataclass(frozen=True, order=True)
class ArticleRef:
    article_id: str
    article_record_sha256: str
    bucket: str
    key: str

    def validate(self) -> None:
        require(nonempty(self.article_id) and nonempty(self.key), "missing article identity")
        require(self.bucket == "article-records", "unexpected canonical bucket")
        require(bool(re.fullmatch(r"[0-9a-f]{64}", self.article_record_sha256)), "invalid artifact SHA")


@dataclass(frozen=True)
class IndexRef:
    article: ArticleRef
    index_run_id: str
    embedding_profile: str
    chunking_profile: str

    def validate(self) -> None:
        self.article.validate()
        require(all(nonempty(v) for v in (self.index_run_id, self.embedding_profile, self.chunking_profile)),
                "incomplete index identity")


@dataclass(frozen=True)
class ArticleSnapshot:
    ref: ArticleRef
    full_text: str
    assembly_status: str
    post_check_status: str
    indexes: tuple[IndexRef, ...] = ()


@dataclass(frozen=True)
class Evidence:
    article: ArticleRef
    start: int  # Unicode code-point offsets in immutable full_text, end exclusive
    end: int
    passage_sha256: str
    index: IndexRef | None = None


def validate_evidence(refs: tuple[Evidence, ...], snapshots: dict[ArticleRef, ArticleSnapshot],
                      allowed: frozenset[ArticleRef] | None = None) -> None:
    require(bool(refs) and len(refs) == len(set(refs)), "missing or duplicate evidence")
    for e in refs:
        e.article.validate()
        require(e.article in snapshots, "unknown exact article version")
        require(allowed is None or e.article in allowed, "evidence outside subject membership")
        s = snapshots[e.article]
        require(s.ref == e.article, "snapshot identity mismatch")
        require(s.assembly_status in {"VERIFIED", "VERIFIED_WITH_NOTES"}
                and s.post_check_status == "PASS", "ineligible Article Record")
        require(type(e.start) is int and type(e.end) is int
                and 0 <= e.start < e.end <= len(s.full_text), "invalid evidence range")
        actual = sha256(s.full_text[e.start:e.end].encode("utf-8")).hexdigest()
        require(e.passage_sha256 == actual, "evidence passage SHA mismatch")
        if e.index is not None:
            e.index.validate()
            require(e.index.article == e.article and e.index in s.indexes,
                    "unknown or mismatched exact index")


@dataclass(frozen=True)
class Review:
    reviewer: str
    reviewed_at: str
    reason: str
    evidence: tuple[Evidence, ...]

    def validate(self, snapshots: dict[ArticleRef, ArticleSnapshot]) -> None:
        require(nonempty(self.reviewer) and nonempty(self.reason), "missing explicit review")
        try:
            parsed = datetime.fromisoformat(self.reviewed_at)
            require(parsed.utcoffset() is not None, "review time requires timezone")
        except (ValueError, TypeError) as exc:
            raise EnrichmentError("invalid review time") from exc
        validate_evidence(self.evidence, snapshots)


@dataclass(frozen=True)
class Annotation:
    field: str
    label: str
    term_id: str | None
    evidence: tuple[Evidence, ...]
    confidence: float
    status: str = "candidate"
    review: Review | None = None


@dataclass(frozen=True)
class KnowledgeLink:
    kind: str  # story_thread or trend; candidate label never implies accepted ID
    label: str
    object_id: str | None
    relation: str
    evidence: tuple[Evidence, ...]
    confidence: float
    status: str = "candidate"
    review: Review | None = None
    object_revision_sha256: str | None = None


@dataclass(frozen=True)
class Signal:
    signal_id: str
    description: str
    observed_on: str
    evidence: tuple[Evidence, ...]
    links: tuple[KnowledgeLink, ...]
    confidence: float
    status: str = "candidate"
    review: Review | None = None


@dataclass(frozen=True)
class Enrichment:
    subject_kind: str  # article or daily_topic
    subject_id: str
    members: tuple[ArticleRef, ...]
    producer: str
    producer_version: str
    profile: str
    profile_version: str
    method_version: str
    confidence_method: str
    annotations: tuple[Annotation, ...] = ()
    knowledge_links: tuple[KnowledgeLink, ...] = ()
    signals: tuple[Signal, ...] = ()
    category: str | None = None
    category_evidence: tuple[Evidence, ...] = ()
    contract_version: str = CONTRACT
    topic_output_sha256: str | None = None
    composer_run_id: str | None = None

    @property
    def identity(self) -> str:
        return digest([self.subject_kind, self.subject_id,
                       [vars(m) for m in sorted(self.members)], self.topic_output_sha256,
                       self.producer, self.producer_version, self.profile, self.profile_version])


def validate_state(status: str, review: Review | None,
                   evidence: tuple[Evidence, ...], snapshots: dict[ArticleRef, ArticleSnapshot]) -> None:
    require(status in STATUSES, "invalid review status")
    if status != "candidate":
        require(review is not None, "status transition requires explicit review")
    if review is not None:
        review.validate(snapshots)
        require(set(evidence) <= set(review.evidence), "review does not cover claim evidence")


def validate_confidence(confidence: float) -> None:
    require(type(confidence) in {int, float} and math.isfinite(confidence)
            and 0 <= confidence <= 1, "invalid confidence")


def validate_link(link: KnowledgeLink, snapshots: dict[ArticleRef, ArticleSnapshot],
                  allowed: frozenset[ArticleRef], accepted: dict[tuple[str, str], str]) -> None:
    require(link.kind in {"story_thread", "trend"} and nonempty(link.label), "invalid knowledge kind/label")
    require(link.relation in RELATIONS, "invalid signal relationship")
    validate_evidence(link.evidence, snapshots, allowed)
    validate_confidence(link.confidence)
    validate_state(link.status, link.review, link.evidence, snapshots)
    if link.object_id is not None:
        require(isinstance(link.object_revision_sha256, str)
                and bool(re.fullmatch(r"[0-9a-f]{64}", link.object_revision_sha256)),
                "link requires exact accepted knowledge revision")
        require(accepted.get((link.object_id, link.object_revision_sha256)) == link.kind,
                "link target is not accepted knowledge")
    else:
        require(link.object_revision_sha256 is None, "revision without object ID")
    if link.status == "accepted":
        require(link.object_id is not None, "accepted link requires accepted durable target")


def validate_enrichment(row: Enrichment, *, snapshots: dict[ArticleRef, ArticleSnapshot],
                        terms: dict[tuple[str, str], str], accepted: dict[tuple[str, str], str]) -> None:
    """terms is an explicit taxonomy-version snapshot: (field, ID) -> canonical label.

    accepted is a trusted reviewed snapshot: (object ID, revision SHA) -> kind.
    No candidate/model supplied catalog should be passed as accepted.
    """
    require(row.contract_version == CONTRACT, "unsupported enrichment contract")
    for value in (row.subject_id, row.producer, row.producer_version, row.profile,
                  row.profile_version, row.method_version, row.confidence_method):
        require(nonempty(value), "missing producer/profile/method provenance")
    require(row.subject_kind in {"article", "daily_topic"}, "invalid subject kind")
    require(bool(row.members) and len(set(row.members)) == len(row.members), "invalid member coverage")
    allowed = frozenset(row.members)
    for member in row.members:
        member.validate()
        require(member in snapshots, "unknown member version")
        s = snapshots[member]
        require(s.ref == member and s.assembly_status in {"VERIFIED", "VERIFIED_WITH_NOTES"}
                and s.post_check_status == "PASS", "ineligible member")
    if row.subject_kind == "article":
        require(len(row.members) == 1 and row.subject_id == row.members[0].article_id,
                "article enrichment must bind one exact Article Record")
        require(row.topic_output_sha256 is None and row.composer_run_id is None, "unexpected topic provenance")
    else:
        require(nonempty(row.composer_run_id) and isinstance(row.topic_output_sha256, str)
                and bool(re.fullmatch(r"[0-9a-f]{64}", row.topic_output_sha256)), "missing exact topic output")
        for member in row.members:
            require(bool(snapshots[member].indexes), "topic member lacks accepted index snapshot")
            for index in snapshots[member].indexes:
                index.validate()
                require(index.article == member, "topic member index version mismatch")
    require(row.category is None or row.category in CATEGORIES, "unsupported controlled category")
    if row.category is not None:
        validate_evidence(row.category_evidence, snapshots, allowed)
    else:
        require(not row.category_evidence, "category evidence without category")
    seen = set()
    for a in row.annotations:
        require(a.field in FACETS and nonempty(a.label), "invalid annotation")
        key = (a.field, a.term_id or normalized(a.label))
        require(key not in seen, "duplicate normalized annotation relation")
        seen.add(key)
        if a.term_id is not None:
            require(terms.get((a.field, a.term_id)) == a.label, "unknown controlled term or alias")
        if a.status == "accepted":
            require(a.term_id is not None, "accepted metadata requires normalized catalog ID")
        validate_evidence(a.evidence, snapshots, allowed)
        validate_confidence(a.confidence)
        validate_state(a.status, a.review, a.evidence, snapshots)
    seen_links = set()
    for link in row.knowledge_links:
        key = (link.kind, link.object_id or normalized(link.label), link.relation)
        require(key not in seen_links, "duplicate knowledge link")
        seen_links.add(key)
        validate_link(link, snapshots, allowed, accepted)
    seen_signals = set()
    for signal in row.signals:
        require(nonempty(signal.signal_id) and signal.signal_id not in seen_signals, "duplicate/missing signal ID")
        seen_signals.add(signal.signal_id)
        require(nonempty(signal.description), "signal requires a description")
        try:
            date.fromisoformat(signal.observed_on)
        except (ValueError, TypeError) as exc:
            raise EnrichmentError("signal requires evidence date") from exc
        validate_evidence(signal.evidence, snapshots, allowed)
        validate_state(signal.status, signal.review, signal.evidence, snapshots)
        validate_confidence(signal.confidence)
        for link in signal.links:
            validate_link(link, snapshots, allowed, accepted)
            require(set(link.evidence) <= set(signal.evidence), "signal link evidence not in signal")


def validate_batch(rows: tuple[Enrichment, ...], *, expected: frozenset[ArticleRef],
                   snapshots: dict[ArticleRef, ArticleSnapshot],
                   terms: dict[tuple[str, str], str], accepted: dict[tuple[str, str], str]) -> None:
    """One homogeneous article profile/version per closed run; exact coverage."""
    require(len(expected) == len({m.article_id for m in expected}), "multiple article revisions in run")
    seen: set[ArticleRef] = set()
    profiles = set()
    for row in rows:
        validate_enrichment(row, snapshots=snapshots, terms=terms, accepted=accepted)
        require(row.subject_kind == "article", "article run contains topic enrichment")
        member = row.members[0]
        require(member not in seen, "duplicate article enrichment per run/profile/version")
        seen.add(member)
        profiles.add((row.producer, row.producer_version, row.profile, row.profile_version))
    require(len(profiles) <= 1, "mixed producer/profile versions in run")
    require(seen == expected, "exact article enrichment coverage mismatch")


def validate_promotion(*, kind: str, signals: tuple[Signal, ...], review: Review,
                       snapshots: dict[ArticleRef, ArticleSnapshot]) -> None:
    """Necessary structural minimum; reviewer must assess independent evidence.

    This function does not create or accept an object, or infer a trend by count.
    """
    require(kind in {"trend", "story_thread"}, "invalid promotion kind")
    require(bool(signals) and len({s.signal_id for s in signals}) == len(signals), "missing/duplicate signals")
    review.validate(snapshots)
    articles: set[ArticleRef] = set()
    days = set()
    for signal in signals:
        require(signal.status == "accepted" and nonempty(signal.description), "promotion requires accepted signals")
        validate_evidence(signal.evidence, snapshots)
        validate_confidence(signal.confidence)
        validate_state(signal.status, signal.review, signal.evidence, snapshots)
        try:
            days.add(date.fromisoformat(signal.observed_on))
        except (ValueError, TypeError) as exc:
            raise EnrichmentError("invalid signal date") from exc
        require(set(signal.evidence) <= set(review.evidence), "promotion review misses signal evidence")
        articles.update(e.article for e in signal.evidence)
    if kind == "trend":
        require(len({a.article_id for a in articles}) >= 2 and len(days) >= 2,
                "trend requires multiple articles and evidence dates; never one-article promotion")


@dataclass(frozen=True)
class KnowledgeRevision:
    """Immutable derived object revision, pending Q019 persistence/selection adapter."""
    object_id: str
    kind: str
    label: str
    definition: str
    lifecycle: str
    producer: str
    producer_version: str
    profile: str
    profile_version: str
    signals: tuple[Signal, ...]
    review: Review | None = None
    status: str = "candidate"
    supersedes_sha256: str | None = None

    @property
    def revision_sha256(self) -> str:
        return digest(asdict(self))


def validate_knowledge_revision(revision: KnowledgeRevision, *,
                                snapshots: dict[ArticleRef, ArticleSnapshot]) -> None:
    """Integrity gate only; does not select/persist an accepted revision."""
    for value in (revision.object_id, revision.label, revision.definition, revision.producer,
                  revision.producer_version, revision.profile, revision.profile_version):
        require(nonempty(value), "missing knowledge definition/provenance")
    lifecycle = {
        "story_thread": {"active", "dormant", "resolved", "superseded"},
        "trend": {"emerging", "established", "weakening", "reversed", "dormant", "superseded"},
    }
    require(revision.kind in lifecycle and revision.lifecycle in lifecycle[revision.kind],
            "invalid knowledge kind/lifecycle")
    if revision.supersedes_sha256 is not None:
        require(bool(re.fullmatch(r"[0-9a-f]{64}", revision.supersedes_sha256)), "invalid supersession SHA")
    evidence = tuple(dict.fromkeys(e for signal in revision.signals for e in signal.evidence))
    require(bool(revision.signals), "knowledge revision requires signals")
    validate_state(revision.status, revision.review, evidence, snapshots)
    for signal in revision.signals:
        validate_evidence(signal.evidence, snapshots)
    if revision.status == "accepted":
        require(revision.review is not None, "accepted knowledge requires review")
        validate_promotion(kind=revision.kind, signals=revision.signals,
                           review=revision.review, snapshots=snapshots)
