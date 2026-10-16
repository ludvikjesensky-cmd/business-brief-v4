# Ingestor Access Bridge

The normative wire contract is `docs/INGESTOR.md §19` from PR #4. This is a separate HTTP service, with no worker/model/OCR/editorial imports. Build from the repository root using `bridge/Dockerfile`.

## Runtime

Required server variables:

- `BRIDGE_DATABASE_URL`: direct PostgreSQL connection; port 6543 transaction pooling is not supported. The runtime overrides TLS parameters with `verify-full` and the bundled official Supabase Root 2021 CA.
- `SUPABASE_URL`, `SUPABASE_SECRET_KEY`: server only; Railway references the existing Technician variables.
- `BRIDGE_SOURCE_BUCKET=source-archive`, `BRIDGE_PAGE_INGEST_BUCKET=page-ingest`: explicitly configured, private buckets. `python -m bridge.provision` creates the configured output bucket if absent and rejects public buckets.
- `BRIDGE_PRINCIPALS`: server-only JSON array of objects with exactly `id`, `token`, `scopes`, `publications`. Tokens must have at least 256 bits of randomness. Production principals authorize only `the-wall-street-journal`; the acceptance principal has only `source:read`, and the manual principal has both scopes. Revoke by removing its entry and redeploying. Never pass Supabase credentials to a client.
- Railway provides `PORT` and terminates HTTPS. Public requests require `X-Forwarded-Proto: https`. `/health` and `/ready` require the same bridge bearer credential; readiness checks DB/migration and both private buckets. Railway's unauthenticated healthcheck must not be configured against these authenticated routes.

## Write fence and recovery

The service locks edition -> source -> blob -> publication rows in the same edition/source order as Technician finalization. A session advisory lock serializes the canonical target across the durable-claim transaction and the write/readback transaction. It retains row locks across Storage create-if-absent, download and exact canonical-byte verification.

Row locks alone do not protect an in-flight HTTP upload if the DB session dies. The private `bindings` table therefore commits a PENDING claim before Storage mutation; invoker triggers reject identity/readiness changes for its source, edition, blob and publication. The guard survives a dead process without lease expiry. VERIFIED/CONFLICT is committed only after readback resolves the attempt. A matching retry reacquires locks and reconciles the existing object. Claims are not evicted. The table is operational state, not a Page JSON index.

An unresolved PENDING claim intentionally blocks identity changes. Operators must retry the original request/idempotency key and verify Storage before clearing it; do not delete claims or expire fences to unblock a stale writer. Never overwrite or delete a canonical artifact automatically. A lost session after a create/readback returns UNKNOWN. The original canonical bytes and UUID/variant identity are compared on every replay.

## Verification

```
python -m pip install -r bridge/requirements.txt pytest
PYTHONPATH=.:src python -m pytest -q tests/test_bridge.py
```

`python -m bridge.db_checks` is an explicit deployment diagnostic: competing PostgreSQL sessions verify that the live source row stays locked through simulated write/readback phases, and all four pending-claim triggers are checked inside a transaction that rolls back. It does not write Storage, modify retained source state, or create Page JSON. It is not a routine application endpoint.

`python -m bridge.acceptance <local-read-credential-json> <redacted-report-path>` uses only GET against HTTPS, downloads exactly page-1 evidence plus its required whole PDFs/manifest, checks downloaded SHA/size, pinned UUID/SHA/bundle identity and expiry, and writes a report without credentials or signed URLs. It never posts a Page JSON or interprets source prose. This diagnostic checks only the Codex HTTPS client. The subsequent ordinary Chat acceptance was performed separately through the Site adapter; see below.

The DB CA came from the URL in Supabase's official Studio `custom-content.json`. SHA-256 certificate fingerprint: `807025ad50d4ed219d2c9c7d299c004f824eb00cf7f65afef607d07b72e6cafa`.

## Subsequent acceptance and v3 extension
The earlier Codex-only read limitation is closed: ordinary Chat read acceptance passed through the private Business Brief Ingestor Site v4 with image + inline OCR and no URL/token leakage. The Site adapter is external to this repository; version/limits/test provenance are documented in docs/INGESTOR.md §20. First production v2 persistence also passed, but its content is product-superseded (HISTORY/D019).

This branch accepts both exact generation tuples: page-ingest-v2 / ingestor-v2.0-chat / 2.0 and page-ingest-v3 / ingestor-v2.1-chat / 2.1. v3 omits perspective and maps to ingestor-v2.1; v2 serialization and namespace remain unchanged. All fencing, auth, JCS, readback, no-overwrite and idempotency semantics above apply unchanged. This extension has not been deployed/production-accepted: update the plugin validator/instructions together before new content acceptance. Never migrate by overwriting v2 or reusing its intended-submission key. No production requests are needed for local verification.
