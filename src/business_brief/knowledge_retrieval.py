"""Offline exact-metadata candidate helpers; Q017/Q018 still gate live adapters."""
from dataclasses import dataclass
from itertools import combinations
from .enrichment import ArticleRef, Enrichment, FACETS, IndexRef, require

EMBEDDING_PROFILE = "BB-EMBEDDING-V1"


@dataclass(frozen=True)
class RetrievalHit:
    index: IndexRef
    channel: str
    score: float | None = None


def compatible_hits(hits: tuple[RetrievalHit, ...], *, indexes: frozenset[IndexRef],
                    embedding_profile: str, chunking_profile: str) -> tuple[RetrievalHit, ...]:
    """indexes must be independently post-checked. Scores stay channel-local.

    No language filter: Czech search_query may retrieve EN/DE search_document.
    This checks identity compatibility, not the provider's multilingual quality.
    """
    require(embedding_profile == EMBEDDING_PROFILE, "unsupported embedding profile")
    result = []
    seen = set()
    for hit in hits:
        hit.index.validate()
        require(hit.channel in {"metadata", "full_text", "vector"}, "unknown retrieval channel")
        require(hit.index in indexes, "hit is not a post-checked exact index")
        if (hit.index.embedding_profile, hit.index.chunking_profile) != (embedding_profile, chunking_profile):
            continue
        key = (hit.index, hit.channel)
        if key not in seen:
            result.append(hit)
            seen.add(key)
    return tuple(result)


def metadata_matches(rows: tuple[Enrichment, ...], *, field: str, object_id: str) -> frozenset[ArticleRef]:
    """Input rows must pass validate_enrichment; default filters exclude candidates."""
    require(field in FACETS | {"story_thread", "trend"}, "unknown metadata filter")
    matches = set()
    for row in rows:
        if row.subject_kind != "article":
            continue
        if field in FACETS:
            found = any(a.field == field and a.term_id == object_id and a.status == "accepted"
                        for a in row.annotations)
        else:
            links = row.knowledge_links + tuple(k for s in row.signals if s.status == "accepted" for k in s.links)
            found = any(k.kind == field and k.object_id == object_id and k.status == "accepted" for k in links)
        if found:
            matches.update(row.members)
    return frozenset(matches)


@dataclass(frozen=True)
class CandidateEdge:
    left: ArticleRef
    right: ArticleRef
    reasons: tuple[str, ...]
    requires_semantic_evaluation: bool = True


def metadata_candidates(rows: tuple[Enrichment, ...], *, corpus: frozenset[ArticleRef]) -> tuple[CandidateEdge, ...]:
    """Complement full-text/vectors; broad topic/trend equality creates no edge.

    Accepted entity/geography/industry/thread links suggest pairs for semantic
    review. No output of this helper constitutes daily-topic membership.
    """
    by_article = {}
    for row in rows:
        require(row.subject_kind == "article" and len(row.members) == 1, "expected article enrichment")
        article = row.members[0]
        require(article in corpus, "candidate article outside closed corpus")
        require(article not in by_article, "select one enrichment revision/profile per article")
        keys = {(a.field, a.term_id) for a in row.annotations
                if a.field in {"entities", "geographies", "industries"}
                and a.status == "accepted" and a.term_id is not None}
        keys.update(("story_thread", k.object_id) for k in row.knowledge_links
                    if k.kind == "story_thread" and k.status == "accepted" and k.object_id is not None)
        by_article[article] = keys
    return tuple(CandidateEdge(left, right, tuple(f"{f}:{v}" for f, v in sorted(common)))
                 for left, right in combinations(sorted(by_article), 2)
                 if (common := by_article[left] & by_article[right]))
