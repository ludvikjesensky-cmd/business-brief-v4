from __future__ import annotations

import pytest

from business_brief.indexer import (
    CHUNK_TARGET_MAX,
    EMBEDDING_DIMENSIONS,
    EMBEDDING_PROFILE,
    IndexerError,
    article_embedding_input,
    chunk_article,
    index_run_id,
    lexical_token_count,
    plan_article,
    validate_embedding,
)


def record(full_text: str) -> dict:
    return {
        "schema_version": "article-record-v1",
        "article_id": "art-" + "a" * 64,
        "title": "Test title",
        "subtitle": "Test subtitle",
        "byline": "Reporter",
        "full_text": full_text,
        "post_check": {"status": "PASS"},
        "assembly": {"status": "VERIFIED"},
    }


def words(count: int, prefix: str) -> str:
    return " ".join(f"{prefix}{i}" for i in range(count))


def test_chunking_is_deterministic_and_profile_bound():
    r = record(words(200, "a") + "\n\n" + words(300, "b"))
    first = plan_article(r, "1" * 64)
    second = plan_article(r, "1" * 64)
    assert first == second
    assert first["embedding_profile"] == EMBEDDING_PROFILE
    assert first["chunk_count"] == 1
    assert first["chunks"][0]["chunk_id"].startswith("chk-")


def test_one_paragraph_overlap_is_applied_when_it_fits():
    text = "\n\n".join([words(400, "a"), words(200, "b"), words(400, "c")])
    chunks = chunk_article(
        article_id="art-" + "a" * 64,
        article_record_sha256="2" * 64,
        full_text=text,
    )
    assert len(chunks) == 2
    assert chunks[0].paragraph_from == 0
    assert chunks[0].paragraph_to == 1
    assert chunks[1].paragraph_from == 1
    assert chunks[1].paragraph_to == 2
    assert chunks[0].text.endswith(words(200, "b"))
    assert chunks[1].text.startswith(words(200, "b"))


def test_long_paragraph_is_split_without_losing_source_bytes():
    paragraph = words(CHUNK_TARGET_MAX * 2 + 1, "x")
    chunks = chunk_article(
        article_id="art-" + "b" * 64,
        article_record_sha256="3" * 64,
        full_text=paragraph,
    )
    assert len(chunks) == 3
    assert all(chunk.fragment_offsets is not None for chunk in chunks)
    assert all(chunk.token_count <= CHUNK_TARGET_MAX for chunk in chunks)
    assert "".join(chunk.text for chunk in chunks) == paragraph


def test_article_embedding_input_is_exact_canonical_projection():
    r = record("Body")
    value = article_embedding_input(r)
    assert '"full_text":"Body"' in value
    assert '"title":"Test title"' in value
    assert "generated summary" not in value


def test_index_run_identity_changes_with_article_record_sha():
    article_id = "art-" + "c" * 64
    assert index_run_id(article_id, "1" * 64) != index_run_id(article_id, "2" * 64)


def test_embedding_validation_requires_exact_finite_dimension():
    good = [0.0] * EMBEDDING_DIMENSIONS
    assert len(validate_embedding(good)) == EMBEDDING_DIMENSIONS
    with pytest.raises(IndexerError):
        validate_embedding([0.0] * (EMBEDDING_DIMENSIONS - 1))
    bad = list(good)
    bad[0] = float("nan")
    with pytest.raises(IndexerError):
        validate_embedding(bad)


def test_tokenizer_counts_unicode_words_and_punctuation_deterministically():
    assert lexical_token_count("Český dotaz: deutsche Wirtschaft.") == 6


def test_ineligible_article_is_rejected():
    r = record("Body")
    r["post_check"]["status"] = "FAIL"
    with pytest.raises(IndexerError):
        plan_article(r, "4" * 64)
