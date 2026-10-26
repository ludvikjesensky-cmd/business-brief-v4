# Deep Runner handoff — 2026-10-26

## Current boundary

Bridge is deployed and the exact WSJ Assembler/Indexer/status/search smoke test passed. Persistence remains disabled by both server flag and missing scope. Runtime commit is 848ee5052630555f04213e6bf747f236257571d1. See DEEP_RUNNER.md for receipts and rollback resources.

## Private Chat adapter — prepared, not deployed

Confirmed existing Site: `appgprj_6ad130997e848191822752605e6ab177`, version 6, owner-only custom access, no external visitors. URL: https://business-brief-ingestor.satinyloom128.chatgpt.site . MCP/OAuth resource: https://business-brief-ingestor.satinyloom128.chatgpt.site/mcp . Existing plugin ID: `plugin_asdk_app_sites_8ed4ce3b42248191bfed2a4cafd37c82`.

Repository Python integration already exists at bridge/chat_tools.py with OpenAPI in docs/deep-runner.openapi.json. A tested server-only JS integration module is prepared separately as deep-runner-adapter.mjs. It exports deepRunnerTools, isDeepRunnerTool and callDeepRunner, defaults to plan-only and rejects persist=true. Checks passed for five definitions, default plan, rejected persistence, uncertainty with retained retry UUID, secret redaction and search bounds. This module is not yet part of the published Site.

For the existing TypeScript /mcp route:

1. Open the authoritative existing Site source through Sites source workflow; preserve project ID, MCP capability, access policy and all existing Ingestor tools. The locally inspected historical v6 source at commit 58652309a5720bfa2e25eb29b216e106ff24ac47 contains a Railway BASE; reconcile authoritative source before changes. It is not evidence of current live upstream health.
2. Add the server-only module and import its three exports. Include `...deepRunnerTools` in tools/list. After the existing authenticated Site caller check and before existing Ingestor dispatch, handle `isDeepRunnerTool(name)` with `response(id, await callDeepRunner(name, a, process.env.BRIDGE_PIPELINE_TOKEN))`. For TypeScript, add declarations or port the module without weakening runtime validation. Do not place this secret in client code or model tool arguments.
3. Bind BRIDGE_PIPELINE_TOKEN server-side to the existing authorized WSJ principal credential using a secure operator/Sites secret channel. The value is not supplied in this handoff. Existing Site read/write secrets were not retrieved or changed, and equality with the Hetzner principal is not assumed. If transporting the credential requires user entry, enter it only in the Site runtime-secret UI, never in chat. Use the fixed `https://bridge.businessbrief.cz/deep-runner/v1/tool` endpoint; do not accept caller URLs. Reconcile the existing Ingestor BASE with Hetzner separately while preserving existing Ingestor behavior.
4. Run module/transport tests and Site build, then publish a new owner-private version using the existing Site ID. Verify tools/list exposes the five new tools, status for the exact WSJ identity returns the known receipts, and no secrets or signed URLs appear. This publication has not been performed.
5. The owner opens ChatGPT/Codex Plugins → Personal → Created by you → Business Brief Ingestor and uses Install/Connect if offered. Reuse the existing plugin; do not create a separate MCP app. If already connected and tool names are cached, open a new ordinary Chat and select the existing plugin. Confirm run_assembler, run_indexer, get_pipeline_status, search_index and run_technician appear. Run status first, then exact plan calls with persist=false; inspect COMPLETE result status and stop on review/blocked/unknown. A clean ordinary Chat acceptance remains unperformed.

The current connected plugin in this Codex session exposes existing Ingestor tools only. UI reconnection alone cannot supply Deep Runner until the adapter code and server secret binding are deployed. Technician remains intentionally unavailable.

## Explicit next persist test — NOT AUTHORIZED OR EXECUTED

Only after separate user confirmation for this exact WSJ source/manifest/SHA:

1. Back up env again; add pipeline:persist only to the intended WSJ principal and set BRIDGE_PIPELINE_PERSIST=1. Recreate the same reviewed Bridge image with the existing env/loopback/Caddy boundary. Verify ready.
2. Submit assembler persist=true with a new recorded UUID, poll to COMPLETE/PASS and independently read back every exact article identity/SHA. Stop on NEEDS_REVIEW, BLOCKED or UNKNOWN. This selection already has immutable Article Records from earlier Q020 acceptance, so REPLAYED receipts can be expected; do not overwrite or delete.
3. Only after successful assembler verification, submit indexer persist=true with a separate new recorded UUID. Inspect all post-check receipts and exact DB identities. This selection already has 21 INDEXED versions from the earlier Indexer acceptance. Exact replay should avoid new document embeddings; verify rather than infer.
4. Retry identical request/body/key to test ledger replay, then a new key with identical selection/body to test runtime replay. Compare article/index/chunk counts and identities; no duplicate growth. Retain original UUIDs after timeout; never issue a fresh key as an uncertainty workaround. Query embeddings from search are separately billable.
5. Restore plan-only configuration by removing the server persist flag and persist scope, recreate Bridge, verify ready and PERSIST_DISABLED. A published plan-only JS module deliberately continues rejecting persist=true; changing that requires a reviewed adapter change too. Server-side operator testing can exercise the HTTP contract after confirmation.

No persist flag, persist scope, canonical write, adapter publication or clean Chat acceptance was performed by this rollout. Fast Editorial remains unchanged.
