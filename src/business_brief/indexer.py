from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from typing import Any, Iterable

ARTICLE_RECORD_SCHEMA = "article-record-v1"
INDEXER_VERSION = "indexer-v1"
TOKENIZER_PROFILE = "BB-LEXICAL-TOKENIZER-V1"
CHUNKING_PROFILE = "BB-CHUNKING-V1"
EMBEDDING_PROFILE = "BB-EMBEDDING-V1"
EMBEDDING_MODEL = "embed-v5.0-pro"
EMBEDDING_DIMENSIONS = 1024
DOCUMENT_INPUT_TYPE = "search_document"
QUERY_INPUT_TYPE = "search_query"
CHUNK_TARGET_MIN = 450
CHUNK_TARGET_MAX = 700
CHUNK_SEPARATOR = "\n\n"

_TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)
_PARAGRAPH_SPLIT_RE = re.compile(r"\n{2,}")


class IndexerError(RuntimeError):
    pass


@dataclass(frozen=True)
class Segment:
    paragraph_index: int
    text: str
    token_count: int
    fragment_from: int | None = None
    fragment_to: int | None = None

    @property
    def fragmented(self) -> bool:
        return self.fragment_from is not None or self.fragment_to is not None


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    chunk_index: int
    paragraph_from: int
    paragraph_to: int
    fragment_offsets: dict[str, int] | None
    text: str
    text_sha256: str
    token_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "chunk_index": self.chunk_index,
            "paragraph_from": self.paragraph_from,
            "paragraph_to": self.paragraph_to,
            "fragment_offsets": self.fragment_offsets,
            "text": self.text,
            "text_sha256": self.text_sha256,
            "token_count": self.token_count,
        }


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def lexical_token_spans(text: str) -> list[tuple[int, int]]:
    return [(match.start(), match.end()) for match in _TOKEN_RE.finditer(text)]


def lexical_token_count(text: str) -> int:
    return len(lexical_token_spans(text))


def split_paragraphs(full_text: str) -> list[str]:
    if not isinstance(full_text, str) or not full_text:
        raise IndexerError("Article Record full_text must be non-empty text")
    paragraphs = _PARAGRAPH_SPLIT_RE.split(full_text)
    if any(paragraph == "" for paragraph in paragraphs):
        raise IndexerError("full_text contains an empty paragraph")
    return paragraphs


def _split_long_paragraph(paragraph: str, paragraph_index: int) -> list[Segment]:
    spans = lexical_token_spans(paragraph)
    if len(spans) <= CHUNK_TARGET_MAX:
        return [Segment(paragraph_index, paragraph, len(spans))]
    segments: list[Segment] = []
    token_start = 0
    char_start = 0
    while token_start < len(spans):
        token_end = min(token_start + CHUNK_TARGET_MAX, len(spans))
        char_end = len(paragraph) if token_end == len(spans) else spans[token_end][0]
        text = paragraph[char_start:char_end]
        count = lexical_token_count(text)
        if not text or count == 0 or count > CHUNK_TARGET_MAX:
            raise IndexerError("long paragraph split failed to make deterministic progress")
        segments.append(
            Segment(
                paragraph_index=paragraph_index,
                text=text,
                token_count=count,
                fragment_from=char_start,
                fragment_to=char_end,
            )
        )
        char_start = char_end
        token_start = token_end
    if "".join(segment.text for segment in segments) != paragraph:
        raise IndexerError("long paragraph split did not preserve exact paragraph bytes")
    return segments


def _chunk_id(
    *,
    article_id: str,
    article_record_sha256: str,
    chunk_index: int,
    paragraph_from: int,
    paragraph_to: int,
    fragment_offsets: dict[str, int] | None,
    text_sha256: str,
) -> str:
    identity = {
        "article_id": article_id,
        "article_record_sha256": article_record_sha256,
        "tokenizer_profile": TOKENIZER_PROFILE,
        "chunking_profile": CHUNKING_PROFILE,
        "chunk_index": chunk_index,
        "paragraph_from": paragraph_from,
        "paragraph_to": paragraph_to,
        "fragment_offsets": fragment_offsets,
        "text_sha256": text_sha256,
    }
    return "chk-" + sha256_bytes(canonical_json(identity))


def chunk_article(
    *,
    article_id: str,
    article_record_sha256: str,
    full_text: str,
) -> list[Chunk]:
    paragraphs = split_paragraphs(full_text)
    units: list[Segment] = []
    for paragraph_index, paragraph in enumerate(paragraphs):
        units.extend(_split_long_paragraph(paragraph, paragraph_index))

    chunk_segments: list[list[Segment]] = []
    current: list[Segment] = []

    def finalize() -> None:
        nonlocal current
        if current:
            chunk_segments.append(current)
            current = []

    for unit in units:
        # A fragment of an exceptionally long paragraph is always its own chunk.
        if unit.fragmented:
            finalize()
            chunk_segments.append([unit])
            continue

        if not current:
            current = [unit]
            continue

        proposed = CHUNK_SEPARATOR.join([segment.text for segment in current] + [unit.text])
        if lexical_token_count(proposed) <= CHUNK_TARGET_MAX:
            current.append(unit)
            continue

        previous = current
        finalize()

        # Exactly one whole-paragraph overlap when it can be included without
        # exceeding the hard upper bound. Otherwise omit overlap to guarantee
        # forward progress.
        overlap = previous[-1]
        candidate = CHUNK_SEPARATOR.join([overlap.text, unit.text])
        if (
            not overlap.fragmented
            and overlap.paragraph_index != unit.paragraph_index
            and lexical_token_count(candidate) <= CHUNK_TARGET_MAX
        ):
            current = [overlap, unit]
        else:
            current = [unit]

    finalize()

    chunks: list[Chunk] = []
    for chunk_index, segments in enumerate(chunk_segments):
        text = CHUNK_SEPARATOR.join(segment.text for segment in segments)
        if not text:
            raise IndexerError("empty chunk")
        token_count = lexical_token_count(text)
        if token_count > CHUNK_TARGET_MAX:
            raise IndexerError("chunk exceeds BB-CHUNKING-V1 hard upper bound")
        paragraph_from = segments[0].paragraph_index
        paragraph_to = segments[-1].paragraph_index
        fragment_offsets = None
        if len(segments) == 1 and segments[0].fragmented:
            fragment_offsets = {
                "paragraph_index": segments[0].paragraph_index,
                "char_from": int(segments[0].fragment_from or 0),
                "char_to": int(segments[0].fragment_to or 0),
            }
        text_sha = sha256_text(text)
        chunks.append(
            Chunk(
                chunk_id=_chunk_id(
                    article_id=article_id,
                    article_record_sha256=article_record_sha256,
                    chunk_index=chunk_index,
                    paragraph_from=paragraph_from,
                    paragraph_to=paragraph_to,
                    fragment_offsets=fragment_offsets,
                    text_sha256=text_sha,
                ),
                chunk_index=chunk_index,
                paragraph_from=paragraph_from,
                paragraph_to=paragraph_to,
                fragment_offsets=fragment_offsets,
                text=text,
                text_sha256=text_sha,
                token_count=token_count,
            )
        )
    if not chunks:
        raise IndexerError("Article Record produced no chunks")
    return chunks


def article_embedding_input(record: dict[str, Any]) -> str:
    value = {
        "title": record.get("title"),
        "subtitle": record.get("subtitle"),
        "byline": record.get("byline"),
        "full_text": record.get("full_text"),
    }
    if not isinstance(value["full_text"], str) or not value["full_text"]:
        raise IndexerError("Article Record lacks full_text")
    return canonical_json(value).decode("utf-8")


def eligible_article_record(record: dict[str, Any]) -> bool:
    return (
        record.get("schema_version") == ARTICLE_RECORD_SCHEMA
        and record.get("assembly", {}).get("status") in {"VERIFIED", "VERIFIED_WITH_NOTES"}
        and record.get("post_check", {}).get("status") == "PASS"
    )


def index_run_id(article_id: str, article_record_sha256: str) -> str:
    identity = {
        "article_id": article_id,
        "article_record_sha256": article_record_sha256,
        "tokenizer_profile": TOKENIZER_PROFILE,
        "chunking_profile": CHUNKING_PROFILE,
        "embedding_profile": EMBEDDING_PROFILE,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
    }
    return "idx-" + sha256_bytes(canonical_json(identity))


def plan_article(record: dict[str, Any], article_record_sha256: str) -> dict[str, Any]:
    if not eligible_article_record(record):
        raise IndexerError("Article Record is not eligible for indexing")
    article_id = record.get("article_id")
    if not isinstance(article_id, str) or not article_id:
        raise IndexerError("Article Record lacks article_id")
    chunks = chunk_article(
        article_id=article_id,
        article_record_sha256=article_record_sha256,
        full_text=record["full_text"],
    )
    representation = article_embedding_input(record)
    return {
        "indexer_version": INDEXER_VERSION,
        "index_run_id": index_run_id(article_id, article_record_sha256),
        "article_id": article_id,
        "article_record_sha256": article_record_sha256,
        "tokenizer_profile": TOKENIZER_PROFILE,
        "chunking_profile": CHUNKING_PROFILE,
        "embedding_profile": EMBEDDING_PROFILE,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "article_embedding_input": representation,
        "article_embedding_input_sha256": sha256_text(representation),
        "chunks": [chunk.to_dict() for chunk in chunks],
        "chunk_count": len(chunks),
    }


def validate_embedding(vector: Iterable[float]) -> list[float]:
    values = [float(value) for value in vector]
    if len(values) != EMBEDDING_DIMENSIONS:
        raise IndexerError(
            f"embedding has {len(values)} dimensions, expected {EMBEDDING_DIMENSIONS}"
        )
    if not all(math.isfinite(value) for value in values):
        raise IndexerError("embedding contains non-finite values")
    return values
