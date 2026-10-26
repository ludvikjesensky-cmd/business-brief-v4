from __future__ import annotations

import hmac
import json
import os
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qsl, urlsplit
from uuid import UUID, uuid4

from .assembler import IntegrityError
from .assembler_runtime import RuntimeErrorAssembler, run as run_assembler
from .index_search import run as run_search
from .indexer import IndexerError
from .indexer_runtime import RuntimeErrorIndexer, SupabaseIndexStore, run as run_indexer

RUNNER_CONTRACT = "business-brief-runner-v1"
MAX_BODY = 64 * 1024
WRITE_LOCK = threading.Lock()
MANIFEST_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class RunnerFailure(RuntimeError):
    def __init__(self, code: str, http: int, message: str | None = None):
        super().__init__(message or code)
        self.code = code
        self.http = http
        self.message = message or code


def _require(condition: bool, code: str, http: int, message: str | None = None) -> None:
    if not condition:
        raise RunnerFailure(code, http, message)


def _strict_json(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RunnerFailure("INVALID_JSON", 400) from exc
    _require(type(value) is dict, "INVALID_JSON", 400)
    return value


def _validate_selection(body: dict[str, Any]) -> tuple[str, str, str]:
    _require(
        set(body) == {"source_id", "manifest_id", "manifest_sha256"},
        "INVALID_REQUEST",
        400,
    )
    try:
        source_id = str(UUID(body["source_id"]))
    except (ValueError, TypeError, AttributeError) as exc:
        raise RunnerFailure("INVALID_SOURCE_ID", 400) from exc
    manifest_id = body["manifest_id"]
    manifest_sha = body["manifest_sha256"]
    _require(
        isinstance(manifest_id, str) and bool(MANIFEST_ID_RE.fullmatch(manifest_id)),
        "INVALID_MANIFEST_ID",
        400,
    )
    _require(
        isinstance(manifest_sha, str) and bool(SHA_RE.fullmatch(manifest_sha)),
        "INVALID_MANIFEST_SHA256",
        400,
    )
    return source_id, manifest_id, manifest_sha


def _summary_assembler(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "assembler_version": report.get("assembler_version"),
        "source_id": report.get("source_id"),
        "manifest_id": report.get("manifest_id"),
        "manifest_sha256": report.get("manifest_sha256"),
        "counts": report.get("counts"),
        "persistence": report.get("persistence"),
    }


def _summary_indexer(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "indexer_version": report.get("indexer_version"),
        "source_id": report.get("source_id"),
        "manifest_id": report.get("manifest_id"),
        "manifest_sha256": report.get("manifest_sha256"),
        "profiles": report.get("profiles"),
        "counts": report.get("counts"),
        "skipped": report.get("skipped"),
        "persistence": report.get("persistence"),
    }


def _status(source_id: str, manifest_id: str, manifest_sha256: str) -> dict[str, Any]:
    store = SupabaseIndexStore.from_env()
    articles = store.select_articles(
        source_id=source_id,
        manifest_id=manifest_id,
        manifest_sha256=manifest_sha256,
    )
    article_ids = [row["article_id"] for row in articles]
    runs: list[dict[str, Any]] = []
    for article_id in article_ids:
        rows = (
            store.client.table("article_index_runs")
            .select("index_run_id,article_id,status,expected_chunk_count,actual_chunk_count")
            .eq("article_id", article_id)
            .execute()
            .data
            or []
        )
        runs.extend(rows)
    indexed = [row for row in runs if row.get("status") == "INDEXED"]
    return {
        "source_id": source_id,
        "manifest_id": manifest_id,
        "manifest_sha256": manifest_sha256,
        "articles": len(articles),
        "index_runs": len(runs),
        "indexed_runs": len(indexed),
        "expected_chunks": sum(int(row.get("expected_chunk_count") or 0) for row in indexed),
        "actual_chunks": sum(int(row.get("actual_chunk_count") or 0) for row in indexed),
        "ready_for_search": len(indexed) == len(articles) and bool(articles),
    }


class Application:
    def __init__(self, principals: list[dict[str, Any]]):
        self.principals = principals

    def auth(self, header: str | None, required_scope: str) -> dict[str, Any]:
        principal = None
        if header and header.startswith("Bearer "):
            token = header[7:]
            for candidate in self.principals:
                if hmac.compare_digest(
                    token.encode("utf-8"), candidate["token"].encode("utf-8")
                ):
                    principal = candidate
                    break
        _require(principal is not None, "UNAUTHENTICATED", 401)
        _require(required_scope in principal["scopes"], "FORBIDDEN", 403)
        return principal

    def dispatch(
        self,
        method: str,
        path: str,
        headers: Any,
        read: Any,
    ) -> tuple[int, dict[str, Any]]:
        url = urlsplit(path)
        args = parse_qsl(url.query, keep_blank_values=True)
        _require(not args, "INVALID_REQUEST", 400)

        if url.path == "/ready":
            self.auth(headers.get("Authorization"), "runner:read")
            _require(method == "GET", "INVALID_REQUEST", 400)
            required = [
                "SUPABASE_URL",
                "SUPABASE_SECRET_KEY",
                "INGESTOR_BRIDGE_URL",
                "INGESTOR_BRIDGE_TOKEN",
                "COHERE_API_KEY",
            ]
            missing = [name for name in required if not os.environ.get(name)]
            _require(not missing, "CONFIGURATION_MISSING", 503)
            return 200, {
                "status": "READY",
                "capabilities": {
                    "technician_remote": False,
                    "assembler_plan": True,
                    "assembler_persist": True,
                    "indexer_plan": True,
                    "indexer_persist": True,
                    "status": True,
                    "search": True,
                },
            }

        _require(method == "POST", "INVALID_REQUEST", 400)
        _require(
            headers.get("Content-Type", "").split(";", 1)[0].lower()
            == "application/json",
            "UNSUPPORTED_MEDIA_TYPE",
            415,
        )
        _require(not headers.get("Transfer-Encoding"), "INVALID_REQUEST", 400)
        try:
            length = int(headers.get("Content-Length", ""))
        except ValueError as exc:
            raise RunnerFailure("INVALID_REQUEST", 400) from exc
        _require(0 <= length <= MAX_BODY, "PAYLOAD_TOO_LARGE", 413)
        raw = read(length)
        _require(len(raw) == length, "INVALID_JSON", 400)
        body = _strict_json(raw)

        if url.path == "/v1/search":
            self.auth(headers.get("Authorization"), "runner:read")
            _require(set(body).issubset({"query", "limit"}) and "query" in body, "INVALID_REQUEST", 400)
            query = body["query"]
            limit = body.get("limit", 20)
            _require(isinstance(query, str) and bool(query.strip()), "INVALID_REQUEST", 400)
            _require(type(limit) is int and 1 <= limit <= 100, "INVALID_REQUEST", 400)
            return 200, run_search(query, limit)

        source_id, manifest_id, manifest_sha = _validate_selection(body)

        if url.path == "/v1/status":
            self.auth(headers.get("Authorization"), "runner:read")
            return 200, _status(source_id, manifest_id, manifest_sha)

        if url.path == "/v1/assembler/plan":
            self.auth(headers.get("Authorization"), "runner:read")
            return 200, _summary_assembler(
                run_assembler(
                    source_id=source_id,
                    manifest_id=manifest_id,
                    manifest_sha256=manifest_sha,
                    persist=False,
                )
            )

        if url.path == "/v1/indexer/plan":
            self.auth(headers.get("Authorization"), "runner:read")
            return 200, _summary_indexer(
                run_indexer(
                    source_id=source_id,
                    manifest_id=manifest_id,
                    manifest_sha256=manifest_sha,
                    persist=False,
                )
            )

        if url.path == "/v1/assembler/persist":
            self.auth(headers.get("Authorization"), "runner:write")
            with WRITE_LOCK:
                return 200, _summary_assembler(
                    run_assembler(
                        source_id=source_id,
                        manifest_id=manifest_id,
                        manifest_sha256=manifest_sha,
                        persist=True,
                    )
                )

        if url.path == "/v1/indexer/persist":
            self.auth(headers.get("Authorization"), "runner:write")
            with WRITE_LOCK:
                return 200, _summary_indexer(
                    run_indexer(
                        source_id=source_id,
                        manifest_id=manifest_id,
                        manifest_sha256=manifest_sha,
                        persist=True,
                    )
                )

        raise RunnerFailure("NOT_FOUND", 404)


class Handler(BaseHTTPRequestHandler):
    app: Application | None = None
    protocol_version = "HTTP/1.1"

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(180)

    def log_message(self, *args: Any) -> None:
        pass

    def handle_request(self) -> None:
        request_id = str(uuid4())
        self.close_connection = True
        try:
            _require(
                self.headers.get("X-Forwarded-Proto") == "https",
                "INVALID_REQUEST",
                400,
            )
            for name in (
                "Authorization",
                "Content-Length",
                "Content-Type",
                "X-Forwarded-Proto",
            ):
                _require(
                    len(self.headers.get_all(name, [])) <= 1,
                    "INVALID_REQUEST",
                    400,
                )
            _require(self.app is not None, "CONFIGURATION_MISSING", 503)
            code, body = self.app.dispatch(
                self.command, self.path, self.headers, self.rfile.read
            )
        except RunnerFailure as exc:
            code = exc.http
            body = {
                "status": "BLOCKED",
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "retryable": False,
                },
            }
        except (RuntimeErrorAssembler, IntegrityError, RuntimeErrorIndexer, IndexerError) as exc:
            code = 409
            body = {
                "status": "BLOCKED",
                "error": {
                    "code": "PIPELINE_BLOCKED",
                    "message": str(exc)[:2000],
                    "retryable": False,
                },
            }
        except Exception:
            code = 500
            body = {
                "status": "BLOCKED",
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Internal error",
                    "retryable": False,
                },
            }

        payload = {
            "contract_version": RUNNER_CONTRACT,
            "request_id": request_id,
            **body,
        }
        data = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Request-ID", request_id)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(data)

    do_GET = handle_request
    do_POST = handle_request
    do_PUT = handle_request
    do_DELETE = handle_request


def _load_principals() -> list[dict[str, Any]]:
    raw = os.environ.get("RUNNER_PRINCIPALS", "")
    _require(bool(raw), "CONFIGURATION_MISSING", 503)
    try:
        principals = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RunnerFailure("CONFIGURATION_MISSING", 503) from exc
    _require(type(principals) is list and bool(principals), "CONFIGURATION_MISSING", 503)
    for principal in principals:
        _require(type(principal) is dict, "CONFIGURATION_MISSING", 503)
        _require(
            set(principal) == {"id", "token", "scopes"},
            "CONFIGURATION_MISSING",
            503,
        )
        _require(
            isinstance(principal["id"], str)
            and principal["id"]
            and isinstance(principal["token"], str)
            and len(principal["token"]) >= 43
            and isinstance(principal["scopes"], list)
            and set(principal["scopes"]).issubset({"runner:read", "runner:write"}),
            "CONFIGURATION_MISSING",
            503,
        )
    return principals


def main() -> int:
    Handler.app = Application(_load_principals())
    port = int(os.environ.get("RUNNER_PORT", os.environ.get("PORT", "8090")))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
