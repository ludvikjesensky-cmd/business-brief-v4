from __future__ import annotations

from business_brief import indexer_runtime as ir


class ReplayStore:
    def select_articles(self, **kwargs):
        return [{"article_id": "art-test", "artifact_sha256": "1" * 64}]

    def load_article_record(self, row):
        return {"article_id": row["article_id"]}

    def replay_if_indexed(self, plan):
        return True


class NoCallEmbedder:
    def embed(self, texts, input_type):
        raise AssertionError("Cohere must not be called for an exact INDEXED replay")


def test_exact_index_replay_skips_embedding_provider(monkeypatch):
    monkeypatch.setattr(
        ir,
        "plan_article",
        lambda record, sha: {
            "article_id": "art-test",
            "article_record_sha256": sha,
            "index_run_id": "idx-test",
            "chunk_count": 2,
            "article_embedding_input": "unused",
            "chunks": [{"text": "a"}, {"text": "b"}],
        },
    )
    report = ir.run(
        source_id="603e8242-ffe8-4e1d-a5de-9adb3da4d188",
        manifest_id="m1",
        manifest_sha256="f" * 64,
        persist=True,
        store=ReplayStore(),
        embedder=NoCallEmbedder(),
    )
    assert report["counts"]["persisted"] == 1
    assert report["persistence"]["receipts"][0]["disposition"] == "REPLAYED"
