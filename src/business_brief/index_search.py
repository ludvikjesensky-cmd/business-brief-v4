from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .indexer import EMBEDDING_PROFILE, QUERY_INPUT_TYPE
from .indexer_runtime import CohereEmbedClient, RuntimeErrorIndexer, SupabaseIndexStore


def run(query: str, limit: int = 20) -> dict[str, Any]:
    if not query.strip():
        raise RuntimeErrorIndexer("query must be non-empty")
    if limit < 1 or limit > 100:
        raise RuntimeErrorIndexer("limit must be between 1 and 100")
    store = SupabaseIndexStore.from_env()
    embedder = CohereEmbedClient.from_env()
    vector = embedder.embed([query], QUERY_INPUT_TYPE)[0]
    vector_rows = (
        store.client.rpc(
            "search_article_chunks_vector_v1",
            {
                "query_embedding": vector,
                "match_count": limit,
                "embedding_profile_filter": EMBEDDING_PROFILE,
            },
        )
        .execute()
        .data
        or []
    )
    lexical_rows = (
        store.client.rpc(
            "search_article_chunks_lexical_v1",
            {
                "query_text": query,
                "match_count": limit,
                "embedding_profile_filter": EMBEDDING_PROFILE,
            },
        )
        .execute()
        .data
        or []
    )
    return {
        "query": query,
        "embedding_profile": EMBEDDING_PROFILE,
        "note": "Calibration output: vector and lexical rankings are intentionally separate; no hybrid fusion weights are frozen.",
        "vector": vector_rows,
        "lexical": lexical_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Business Brief v4 Indexer retrieval calibration")
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    try:
        report = run(args.query, args.limit)
    except RuntimeErrorIndexer as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
