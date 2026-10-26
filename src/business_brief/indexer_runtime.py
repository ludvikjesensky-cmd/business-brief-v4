from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from supabase import Client, create_client

from .indexer import (
    CHUNKING_PROFILE,
    DOCUMENT_INPUT_TYPE,
    EMBEDDING_DIMENSIONS,
    EMBEDDING_MODEL,
    EMBEDDING_PROFILE,
    INDEXER_VERSION,
    QUERY_INPUT_TYPE,
    TOKENIZER_PROFILE,
    IndexerError,
    canonical_json,
    eligible_article_record,
    plan_article,
    sha256_bytes,
    validate_embedding,
)

ARTICLE_BUCKET = "article-records"


class RuntimeErrorIndexer(RuntimeError):
    pass


class CohereEmbedClient:
    def __init__(self, api_key: str, base_url: str = "https://api.cohere.com"):
        if not api_key:
            raise RuntimeErrorIndexer("COHERE_API_KEY is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    @classmethod
    def from_env(cls) -> "CohereEmbedClient":
        return cls(
            os.environ.get("COHERE_API_KEY", ""),
            os.environ.get("COHERE_API_BASE", "https://api.cohere.com"),
        )

    def _embed_batch(self, texts: list[str], input_type: str) -> list[list[float]]:
        body = canonical_json(
            {
                "model": EMBEDDING_MODEL,
                "input_type": input_type,
                "texts": texts,
                "output_dimension": EMBEDDING_DIMENSIONS,
                "embedding_types": ["float"],
                "truncate": "NONE",
            }
        )
        request = Request(
            f"{self.base_url}/v2/embed",
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Client-Name": "business-brief-v4",
            },
        )
        try:
            with urlopen(request, timeout=120) as response:
                raw = response.read()
                status = response.status
        except HTTPError as exc:
            error = exc.read().decode("utf-8", "replace")[:1000]
            raise RuntimeErrorIndexer(f"Cohere embed failed: HTTP {exc.code} {error}") from exc
        except URLError as exc:
            raise RuntimeErrorIndexer("Cohere embed request failed") from exc
        if status != 200:
            raise RuntimeErrorIndexer(f"Cohere embed failed: HTTP {status}")
        try:
            payload = json.loads(raw.decode("utf-8"))
            vectors = payload["embeddings"]["float"]
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RuntimeErrorIndexer("Cohere returned an invalid embedding response") from exc
        if len(vectors) != len(texts):
            raise RuntimeErrorIndexer("Cohere embedding count mismatch")
        return [validate_embedding(vector) for vector in vectors]

    def embed(self, texts: list[str], input_type: str) -> list[list[float]]:
        if input_type not in {DOCUMENT_INPUT_TYPE, QUERY_INPUT_TYPE}:
            raise RuntimeErrorIndexer(f"unsupported input_type: {input_type}")
        if not texts:
            return []
        vectors: list[list[float]] = []
        for start in range(0, len(texts), 96):
            vectors.extend(self._embed_batch(texts[start : start + 96], input_type))
        return vectors


def _parse_vector(value: Any) -> list[float]:
    if isinstance(value, list):
        return validate_embedding(value)
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise RuntimeErrorIndexer("stored vector is not valid JSON/vector text") from exc
        return validate_embedding(parsed)
    raise RuntimeErrorIndexer("stored vector has an unsupported representation")


class SupabaseIndexStore:
    def __init__(self, client: Client):
        self.client = client

    @classmethod
    def from_env(cls) -> "SupabaseIndexStore":
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SECRET_KEY")
        if not url or not key:
            raise RuntimeErrorIndexer("SUPABASE_URL and SUPABASE_SECRET_KEY are required")
        return cls(create_client(url, key))

    def select_articles(
        self,
        *,
        source_id: str,
        manifest_id: str,
        manifest_sha256: str,
    ) -> list[dict[str, Any]]:
        rows = (
            self.client.table("articles")
            .select("*")
            .eq("source_id", source_id)
            .eq("manifest_id", manifest_id)
            .eq("manifest_sha256", manifest_sha256)
            .order("article_id")
            .execute()
            .data
            or []
        )
        if not rows:
            raise RuntimeErrorIndexer("no persisted Article Records match the explicit selection")
        return rows

    def load_article_record(self, row: dict[str, Any]) -> dict[str, Any]:
        if row.get("storage_bucket") != ARTICLE_BUCKET:
            raise RuntimeErrorIndexer("Article Record points outside article-records bucket")
        try:
            raw = self.client.storage.from_(ARTICLE_BUCKET).download(row["storage_key"])
        except Exception as exc:
            raise RuntimeErrorIndexer(f"cannot download Article Record {row['article_id']}") from exc
        raw = bytes(raw)
        if sha256_bytes(raw) != row.get("artifact_sha256"):
            raise RuntimeErrorIndexer(f"Article Record SHA mismatch: {row['article_id']}")
        try:
            record = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeErrorIndexer(f"Article Record is invalid JSON: {row['article_id']}") from exc
        if record.get("article_id") != row.get("article_id") or not eligible_article_record(record):
            raise RuntimeErrorIndexer(f"Article Record is not eligible: {row['article_id']}")
        return record

    def _run(self, index_run_id: str) -> dict[str, Any] | None:
        rows = (
            self.client.table("article_index_runs")
            .select("*")
            .eq("index_run_id", index_run_id)
            .execute()
            .data
            or []
        )
        return rows[0] if rows else None

    def _set_run(self, plan: dict[str, Any], status: str, *, error: str | None = None, actual: int | None = None) -> None:
        row = {
            "index_run_id": plan["index_run_id"],
            "article_id": plan["article_id"],
            "article_record_sha256": plan["article_record_sha256"],
            "indexer_version": INDEXER_VERSION,
            "tokenizer_profile": TOKENIZER_PROFILE,
            "chunking_profile": CHUNKING_PROFILE,
            "embedding_profile": EMBEDDING_PROFILE,
            "embedding_model": EMBEDDING_MODEL,
            "embedding_dimensions": EMBEDDING_DIMENSIONS,
            "status": status,
            "expected_chunk_count": plan["chunk_count"],
            "actual_chunk_count": actual,
            "article_embedding_input_sha256": plan["article_embedding_input_sha256"],
            "error": error,
            "completed_at": "now()" if status in {"INDEXED", "FAILED"} else None,
        }
        existing = self._run(plan["index_run_id"])
        if existing is None:
            row.pop("completed_at")
            self.client.table("article_index_runs").insert(row).execute()
        else:
            update = {
                "status": status,
                "actual_chunk_count": actual,
                "error": error,
            }
            # Let PostgreSQL assign a real timestamp rather than sending the SQL
            # expression through PostgREST.
            if status in {"INDEXED", "FAILED"}:
                from datetime import datetime, timezone
                update["completed_at"] = datetime.now(timezone.utc).isoformat()
            self.client.table("article_index_runs").update(update).eq(
                "index_run_id", plan["index_run_id"]
            ).execute()

    def _delete_partial(self, plan: dict[str, Any]) -> None:
        for table in ("article_chunks", "article_embeddings"):
            (
                self.client.table(table)
                .delete()
                .eq("article_id", plan["article_id"])
                .eq("article_record_sha256", plan["article_record_sha256"])
                .eq("embedding_profile", EMBEDDING_PROFILE)
                .execute()
            )

    def _post_check(self, plan: dict[str, Any]) -> None:
        embeddings = (
            self.client.table("article_embeddings")
            .select("*")
            .eq("article_id", plan["article_id"])
            .eq("article_record_sha256", plan["article_record_sha256"])
            .eq("embedding_profile", EMBEDDING_PROFILE)
            .execute()
            .data
            or []
        )
        if len(embeddings) != 1:
            raise RuntimeErrorIndexer("index post-check: article embedding count mismatch")
        embedding = embeddings[0]
        if embedding.get("input_sha256") != plan["article_embedding_input_sha256"]:
            raise RuntimeErrorIndexer("index post-check: article embedding input SHA mismatch")
        _parse_vector(embedding.get("embedding"))

        rows = (
            self.client.table("article_chunks")
            .select("*")
            .eq("article_id", plan["article_id"])
            .eq("article_record_sha256", plan["article_record_sha256"])
            .eq("embedding_profile", EMBEDDING_PROFILE)
            .order("chunk_index")
            .execute()
            .data
            or []
        )
        if len(rows) != plan["chunk_count"]:
            raise RuntimeErrorIndexer("index post-check: chunk count mismatch")
        expected = plan["chunks"]
        for index, (row, chunk) in enumerate(zip(rows, expected)):
            if int(row.get("chunk_index")) != index:
                raise RuntimeErrorIndexer("index post-check: non-contiguous chunk indexes")
            for field in (
                "chunk_id",
                "text",
                "text_sha256",
                "paragraph_from",
                "paragraph_to",
                "token_count",
            ):
                if row.get(field) != chunk.get(field):
                    raise RuntimeErrorIndexer(f"index post-check: chunk mismatch in {field}")
            if row.get("fragment_offsets") != chunk.get("fragment_offsets"):
                raise RuntimeErrorIndexer("index post-check: fragment offset mismatch")
            _parse_vector(row.get("embedding"))

    def persist(
        self,
        plan: dict[str, Any],
        *,
        article_embedding: list[float],
        chunk_embeddings: list[list[float]],
    ) -> str:
        if len(chunk_embeddings) != plan["chunk_count"]:
            raise RuntimeErrorIndexer("chunk embedding count mismatch")
        existing = self._run(plan["index_run_id"])
        if existing and existing.get("status") == "INDEXED":
            self._post_check(plan)
            return "REPLAYED"

        try:
            self._set_run(plan, "PENDING")
            self._set_run(plan, "INDEXING")
            self._delete_partial(plan)

            self.client.table("article_embeddings").insert(
                {
                    "article_id": plan["article_id"],
                    "article_record_sha256": plan["article_record_sha256"],
                    "embedding_profile": EMBEDDING_PROFILE,
                    "embedding_model": EMBEDDING_MODEL,
                    "input_type": DOCUMENT_INPUT_TYPE,
                    "input_sha256": plan["article_embedding_input_sha256"],
                    "embedding": article_embedding,
                }
            ).execute()

            chunk_rows = []
            for chunk, vector in zip(plan["chunks"], chunk_embeddings):
                chunk_rows.append(
                    {
                        "chunk_id": chunk["chunk_id"],
                        "article_id": plan["article_id"],
                        "article_record_sha256": plan["article_record_sha256"],
                        "tokenizer_profile": TOKENIZER_PROFILE,
                        "chunking_profile": CHUNKING_PROFILE,
                        "embedding_profile": EMBEDDING_PROFILE,
                        "embedding_model": EMBEDDING_MODEL,
                        "input_type": DOCUMENT_INPUT_TYPE,
                        "chunk_index": chunk["chunk_index"],
                        "paragraph_from": chunk["paragraph_from"],
                        "paragraph_to": chunk["paragraph_to"],
                        "fragment_offsets": chunk["fragment_offsets"],
                        "token_count": chunk["token_count"],
                        "text": chunk["text"],
                        "text_sha256": chunk["text_sha256"],
                        "embedding": vector,
                    }
                )
            self.client.table("article_chunks").insert(chunk_rows).execute()
            self._post_check(plan)
            self._set_run(plan, "INDEXED", actual=plan["chunk_count"])
            return "CREATED"
        except Exception as exc:
            try:
                self._set_run(plan, "FAILED", error=str(exc)[:2000])
            except Exception:
                pass
            raise


def run(
    *,
    source_id: str,
    manifest_id: str,
    manifest_sha256: str,
    persist: bool = False,
    store: SupabaseIndexStore | None = None,
    embedder: CohereEmbedClient | None = None,
) -> dict[str, Any]:
    store = store or SupabaseIndexStore.from_env()
    rows = store.select_articles(
        source_id=source_id,
        manifest_id=manifest_id,
        manifest_sha256=manifest_sha256,
    )
    plans: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for row in rows:
        try:
            record = store.load_article_record(row)
            plans.append(plan_article(record, row["artifact_sha256"]))
        except (RuntimeErrorIndexer, IndexerError) as exc:
            skipped.append({"article_id": row.get("article_id", "?"), "reason": str(exc)})

    receipts: list[dict[str, Any]] = []
    if persist:
        embedder = embedder or CohereEmbedClient.from_env()
        for plan in plans:
            article_vector = embedder.embed(
                [plan["article_embedding_input"]], DOCUMENT_INPUT_TYPE
            )[0]
            chunk_vectors = embedder.embed(
                [chunk["text"] for chunk in plan["chunks"]], DOCUMENT_INPUT_TYPE
            )
            disposition = store.persist(
                plan,
                article_embedding=article_vector,
                chunk_embeddings=chunk_vectors,
            )
            receipts.append(
                {
                    "article_id": plan["article_id"],
                    "index_run_id": plan["index_run_id"],
                    "chunk_count": plan["chunk_count"],
                    "disposition": disposition,
                }
            )

    return {
        "indexer_version": INDEXER_VERSION,
        "source_id": source_id,
        "manifest_id": manifest_id,
        "manifest_sha256": manifest_sha256,
        "profiles": {
            "tokenizer": TOKENIZER_PROFILE,
            "chunking": CHUNKING_PROFILE,
            "embedding": EMBEDDING_PROFILE,
            "model": EMBEDDING_MODEL,
            "dimensions": EMBEDDING_DIMENSIONS,
        },
        "counts": {
            "article_rows": len(rows),
            "eligible": len(plans),
            "skipped": len(skipped),
            "planned_chunks": sum(plan["chunk_count"] for plan in plans),
            "persisted": len(receipts),
        },
        "skipped": skipped,
        "plans": plans if not persist else [],
        "persistence": {"requested": persist, "receipts": receipts},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Business Brief v4 deterministic Indexer")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--manifest-id", required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument(
        "--persist",
        action="store_true",
        help="Call Cohere and persist derived index data. Default plans chunks only.",
    )
    args = parser.parse_args()
    try:
        report = run(
            source_id=args.source_id,
            manifest_id=args.manifest_id,
            manifest_sha256=args.manifest_sha256,
            persist=args.persist,
        )
    except (RuntimeErrorIndexer, IndexerError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not report["counts"]["skipped"] else 3


if __name__ == "__main__":
    sys.exit(main())
