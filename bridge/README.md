# Ingestor Access Bridge

The normative wire contract is `docs/INGESTOR.md §19` from PR #4. This is a separate HTTP service, with no worker/model/OCR/editorial imports. Build from the repository root using `bridge/Dockerfile`.

## Runtime

Required server variables:

- `BRIDGE_DATABASE_URL`: direct PostgreSQL connection; port 6543 transaction pooling is not supported. The runtime overrides TLS parameters with `verify-full` and the bundled official Supabase Root 2021 CA.
- `SUPABASE_URL`, `SUPABASE_SECRET_KEY`: server only; Railway references the existing Technician variables.
- `BRIDGE_SOURCE_BUCKET=source-archive`, `BRIDGE_PAGE_INGEST_BUCKET=page-ingest`: explicitly configured, private buckets. `python -m bridge.provision` creates the configured output bucket if absent, rejects public buckets, additively enables JSON/PNG and raises a smaller finite upload limit to 32 MiB (preserving unrestricted/higher limits and other MIME types), then verifies readback.
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

The deployed v3 revision accepts both exact generation tuples: page-ingest-v2 / ingestor-v2.0-chat / 2.0 and page-ingest-v3 / ingestor-v2.1-chat / 2.1. v3 omits perspective and maps to ingestor-v2.1; v2 serialization and namespace remain unchanged. All fencing, auth, JCS, readback, no-overwrite and idempotency semantics above apply unchanged. The extension was deployed on 2026-10-16, pinned to 1442da050a0b3dcb4a5de9a11611a2b5ec9084c9, Railway deployment 7d1fa8aa-401d-4a2c-8fe0-5a4804eeb029 (SUCCESS/Online). Site v4 already transports arbitrary page bodies; no Site source change or redeploy was necessary. One connected-plugin v3 page-1 persist passed with exact JCS SHA/identity readback; see CURRENT_STATE/HISTORY. Never migrate by overwriting v2 or reusing its intended-submission key. No production requests are needed for local verification.

## Article-assets v4 contract boundary (D022)
This branch adds `page-ingest-v4` / `ingestor-v2.2-chat` / `2.2`, mapped server-side to `ingestor-v2.2`. v2/v3 serialized shapes and keys are unchanged. `bridge.validation.asset_key` derives source/generation/page-bound PNG keys; schema validation checks asset ownership, metadata, bbox and exact unique text anchors, and verification propagates asset review/blocking status to item/page.

Architecture reuses `BRIDGE_PAGE_INGEST_BUCKET=page-ingest` (private), with keys `page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.2/assets/page-<NNNN>/<asset_id>.png`. Page JSON is its sibling `.../ingestor-v2.2/page-<NNNN>.json`. Contract details and required crop write semantics are exclusively in docs/INGESTOR.md §21.

The server-side writer accepts artifact:null or complete exact expected metadata in v4 submissions, crops only the authoritative manifest PNG, and fills persisted metadata after exact create-if-absent/readback verification. The ordinary Chat tool remains text JSON. See INGESTOR §21.5 for limits, deterministic PNG encoding, reserved durable set binding and full recovery semantics. No DB migration, new bucket, public URL or client image upload is required. v2/v3 objects and bindings remain untouched.

Both original-request and deterministic target/set claims stay PENDING across partial failures. Retry original payload/key; do not replace artifact:null with enriched output on retry. ASSET_SET_CONFLICT / ASSET_CONFLICT are explicit 409s and do not overwrite or clear fences automatically. A partial set cannot produce canonical successful JSON. Set identity includes source UUID/variant/bundle and exact final artifacts.

Local validation: `PYTHONPATH=.:src python -m pytest -q`; deployment/acceptance evidence is in CURRENT_STATE/HISTORY. Keep Railway pinned to the tested runtime commit, preserving the open PR chain and unrelated main-linked services.

## v4 rollout and acceptance — 2026-10-18
Pinned runtime `b6d465c49dbf546f0ea31876d218121428d495c8`, deployment `4489131f-d578-4062-b88f-40adc3716932`, SUCCESS. 226 tests pass. Existing Site v4 transported text-only v4 submission/receipt without change or redeploy. Exactly WSJ 2026-10-14 page 2 was created with three source-PNG chart crops, all exact SHA/size/dimensions and page identity readback verified, both bindings VERIFIED, usable_for_assembly=true. Initial JSON-only bucket failure was reconciled using the original request/key after the additive provision fix. See CURRENT_STATE/HISTORY for canonical identities. No page 3, assembly, migration, merge or historical object mutation.

## Corpus and editorial acceptance boundary
The page-2-only scope above describes that rollout acceptance. Subsequent ordinary-Chat pages 3–10 are reported in HISTORY, with no raw receipts or stored-object lookup available to this consolidation. The exposed source-page GET returns source evidence, not persisted ingest output. Do not use POST replay as a read/list substitute. Page 1 remains evidenced v2/v3; do not infer all-v4 coverage.

Before visual_checked:true/persist, independently render and preview every crop from the authoritative PNG with writer-equivalent bbox rounding (INGESTOR §21.7, D023). Technical readback does not detect clipping. F011 records the page-6 About Face defect; its immutable originals remain untouched and corpus visual acceptance is incomplete. The bridge has no editorial revision endpoint/protocol; Q014 must resolve correction and supersession before an authorized production fix.

## Revision / selection extension
INGESTOR §22 defines immutable full-snapshot page-revision-v1, source-scoped readback/inventory and edition-selection-v1. New endpoints retain existing scopes, private storage, source/durable fences and create-if-absent. Readback returns final Page JSON and independently downloaded PNG receipts without signed capabilities. Private Site adds get_page_artifact/list_ingested_pages and explicit revision/manifest writer transport. Future Assembler must use assembly-input with exactly one manifest ID/SHA; it never discovers latest pages. Existing v2/v3/v4 request bytes and claim hashes are unchanged. Deployment and operational acceptance are recorded separately in CURRENT_STATE.
