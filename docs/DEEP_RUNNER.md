# Deep/Memory runner v1

Repository implementation, not a production deployment/acceptance claim.

## Audit and boundary

`bridge/server.py` already authenticates BRIDGE_PRINCIPALS bearer credentials,
checks publication allowlists, conceals unauthorized sources, and sanitizes errors.
`assembler_runtime.run` independently verifies the accepted manifest, selected page
JSON/revisions and PNG bytes twice; persistence is immutable with readback.
`indexer_runtime.run` verifies persisted Article Records and post-checks derived
index writes/replay. These functions are reused directly, without shell execution,
SSH, caller URLs/paths, new credentials, or a parallel web service.

The existing Technician service drains a global inbox and its CLI takes local
paths. Neither supplies a safe authorized source-scoped job claim. The runner
therefore returns `TECHNICIAN_SOURCE_SCOPED_UNAVAILABLE`; it never calls global
wake/drain. Source acquisition/Technician preparation remain operator-controlled.
This is an explicit implementation boundary, not successful Technician execution.
Fast Editorial, Composer, Enrichment, publication and semantic gates are unchanged.

## HTTP tool contract

Authenticated `POST https://bridge.businessbrief.cz/deep-runner/v1/tool` uses the
existing bearer principal configured ONLY in the server-side plugin adapter.
OpenAPI: `docs/deep-runner.openapi.json`. No token, SSH key, Cohere key, database
password or Supabase secret belongs in Chat arguments or model-visible output.
Do not distribute a principal with broader publication access than the user.

Every body requires `contract_version: deep-runner-v1`, operation, explicit
`source_id`, `manifest_id`, `manifest_sha` (lowercase SHA-256). No latest fallback.
Unknown/duplicate fields, invalid media/framing and oversized input are rejected.

| operation | additional fields | scopes in addition to source:read |
| --- | --- | --- |
| assembler | persist: boolean, default false in adapter | pipeline:read, pipeline:run; pipeline:persist for true |
| indexer | persist: boolean, default false in adapter | pipeline:read, pipeline:run; pipeline:persist for true |
| status | none | pipeline:read |
| search | query: 1–2000 chars, limit: 1–20 | pipeline:read, pipeline:search |
| technician | none | returns explicit unavailable |

Run/search require an adapter-generated UUID `Idempotency-Key`. Reuse the SAME key
and exact body after timeout/uncertainty. Changed request bytes under the same
principal/key conflict. A fresh key requests a fresh plan/search. Status needs no
key. It returns the caller's most recent 50 receipts for this exact selection,
including safe result summaries. The accepted manifest is revalidated on every
request, even completed replay/status; authorization precedes execution or lookup.

Runs return 202 promptly; poll status until COMPLETE. COMPLETE means the function
returned, so inspect result.status: PASS, NEEDS_REVIEW or BLOCKED. It is not an
editorial acceptance flag. Do not automatically advance on NEEDS_REVIEW/BLOCKED.
`bridge/chat_tools.py` supplies model-safe definitions and server-side wrappers
for run_assembler, run_indexer, get_pipeline_status, search_index and the explicit
unavailable run_technician. The existing private adapter host injects its secret
transport; no credential argument exists in these tools. Set persist
false unless the user explicitly requests persistence. Never auto-chain across
Ingestor corrections or other human/semantic gates.

The PostgreSQL ledger binds principal/key/request hash and selection. Session
advisory source locks serialize execution across Bridge replicas. Completed
requests replay their stored response without repeating paid calls. A dead worker
can leave RUNNING; UNKNOWN and RUNNING are uncertain, never successful. Retry the
original request/key to reconcile through the existing immutable persistence and
post-checks. Partial article/index writes can exist after failure; never delete or
overwrite them. Incomplete retries may repeat embedding costs; exactly-once billing
is not promised. No automatic process restart recovery or job cancellation exists.
Use bounded operator retries and inspect receipts. Runtime/provider calls retain
their existing timeouts; stop/restart the container for a stuck worker, then retry.

Search uses separate vector/lexical calibration rankings, and filters results to
exact article ID + record SHA in the authorized source/manifest. It returns only
that selection's subset of the global top 100; recall may be incomplete. Query
embedding is billable and requires pipeline:search. No hybrid weights are frozen.

## Hetzner rollout

1. Review and checkout the exact tested commit in `/opt/business-brief-v4`.
2. Back up configuration and apply the additive `add_pipeline_requests` migration
   with the established Supabase migration workflow. Confirm RLS and revoked
   anon/authenticated privileges. Keep bridge_private outside Data API schemas.
   BRIDGE_DATABASE_URL must use the existing owner/service role with table access
   and session semantics; transaction pooling (6543) is unsupported.
3. Build `docker build -f bridge/Dockerfile -t business-brief-bridge:<commit> .`.
   This image adds only the Assembler/Indexer Python adapters and pinned Supabase
   dependency; no OCR system tools are installed. Technician stays unavailable.
4. Retain existing production `.env` mode 600, Caddy and loopback port binding.
   Add `BRIDGE_PIPELINE_ENABLED=1`. Keep `BRIDGE_PIPELINE_PERSIST` unset initially.
   Add pipeline scopes to the intended BRIDGE_PRINCIPALS entry, preserving its
   existing ID/token/publication allowlist and any existing Ingestor scopes.
   SUPABASE_URL, SUPABASE_SECRET_KEY and COHERE_API_KEY stay server-side.
5. Recreate the existing container with the reviewed image and existing `.env`,
   bound `127.0.0.1:8080:8080`; verify local/public authenticated `/ready`.
6. Check missing/invalid auth, disallowed publication, wrong SHA, persist disabled,
   exact Assembler plan and Indexer plan. Poll results; check review counts.
   Enable persistence only for deliberate acceptance, with both server flag and
   pipeline:persist scope. Run accepted WSJ plan → persist → same-key replay and
   fresh-key runtime replay; independently read back exact Storage/DB identities.
   Repeat on Handelsblatt for broader acceptance; Q017 remains open.
7. Configure the existing private Site/plugin adapter server-side to call this
   endpoint. Verify in a clean ordinary Chat that credentials and signed URLs
   never appear in tool arguments/results. This adapter deployment and live
   acceptance are separate from repository tests and are not claimed here.

Rollback: unset BRIDGE_PIPELINE_ENABLED and recreate the prior Bridge image. Retain
the additive ledger and immutable outputs. Do not roll back by deleting articles,
chunks or request bindings. There is no Caddy/DNS/new public port requirement.

## Validation

Run `PYTHONPATH=.:src pytest -q`, PostgreSQL schema checks in CI, and
`git diff --check`. Unit tests use injected boundaries and make no paid calls or
production writes. Live deployment, real concurrency/session-loss and ordinary
Chat acceptance must follow the rollout above.

## Concurrent main consolidation

PR #17 added a separate runner during this implementation. This change supersedes
its listener/principals/DNS contract with the existing Bridge boundary, preserves
its Indexer zero-provider-call exact INDEXED replay fix and regression test, and
keeps the old command fail-closed. There is one deployable runtime/auth boundary.
