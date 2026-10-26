from __future__ import annotations

import json

import pytest

from business_brief import runner_runtime as rr


TOKEN = "x" * 43
SELECTION = {
    "source_id": "603e8242-ffe8-4e1d-a5de-9adb3da4d188",
    "manifest_id": "wsj-2026-10-14-selection-r1",
    "manifest_sha256": "f" * 64,
}


class Headers(dict):
    def get_all(self, name, default=None):
        return [self[name]] if name in self else (default or [])


def headers(token=TOKEN):
    raw = json.dumps(SELECTION).encode()
    return Headers(
        {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Content-Length": str(len(raw)),
        }
    ), raw


def app(scopes=("runner:read", "runner:write")):
    return rr.Application([{"id": "chat", "token": TOKEN, "scopes": list(scopes)}])


def test_auth_requires_scope():
    with pytest.raises(rr.RunnerFailure) as exc:
        app(("runner:read",)).auth(f"Bearer {TOKEN}", "runner:write")
    assert exc.value.http == 403


def test_selection_validation_is_exact():
    assert rr._validate_selection(dict(SELECTION)) == (
        SELECTION["source_id"],
        SELECTION["manifest_id"],
        SELECTION["manifest_sha256"],
    )
    bad = dict(SELECTION)
    bad["extra"] = True
    with pytest.raises(rr.RunnerFailure):
        rr._validate_selection(bad)


def test_assembler_plan_is_read_only(monkeypatch):
    seen = {}

    def fake_run(**kwargs):
        seen.update(kwargs)
        return {
            "assembler_version": "assembler-v1",
            "source_id": kwargs["source_id"],
            "manifest_id": kwargs["manifest_id"],
            "manifest_sha256": kwargs["manifest_sha256"],
            "counts": {"article_records": 21},
            "persistence": {"requested": False},
        }

    monkeypatch.setattr(rr, "run_assembler", fake_run)
    h, raw = headers()
    code, body = app().dispatch(
        "POST", "/v1/assembler/plan", h, lambda n: raw[:n]
    )
    assert code == 200
    assert seen["persist"] is False
    assert body["persistence"]["requested"] is False


def test_indexer_persist_requires_write_scope():
    h, raw = headers()
    with pytest.raises(rr.RunnerFailure) as exc:
        app(("runner:read",)).dispatch(
            "POST", "/v1/indexer/persist", h, lambda n: raw[:n]
        )
    assert exc.value.http == 403


def test_search_does_not_accept_selection_fields(monkeypatch):
    monkeypatch.setattr(rr, "run_search", lambda query, limit: {"query": query, "limit": limit})
    body = json.dumps({"query": "Čína", "limit": 5}).encode()
    h = Headers(
        {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Content-Length": str(len(body)),
        }
    )
    code, result = app().dispatch("POST", "/v1/search", h, lambda n: body[:n])
    assert code == 200
    assert result == {"query": "Čína", "limit": 5}
