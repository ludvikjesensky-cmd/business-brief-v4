# Deep Runner handoff — 2026-10-27

## Current verified boundary

This document supersedes the 2026-10-26 adapter preparation instructions. The Bridge runner is deployed on Hetzner at runtime commit `848ee5052630555f04213e6bf747f236257571d1`, image `business-brief-bridge:848ee5052630`. The private Site adapter v7 is deployed and its tools were exercised successfully through the connected Chat plugin in a Work conversation. A separate fresh ordinary Chat plan acceptance passed, as reported by the operator and independently verified against both exact server receipts below. Fast Editorial is unchanged.

**Current operational state: plan-only restored.** The operator temporarily activated `BRIDGE_PIPELINE_PERSIST=1` and added `pipeline:persist` to `manual-ingestor` for the authorized WSJ acceptance below, then restored the pre-test configuration/container. The operator reported READY HTTP 200, PERSIST VYPNUTO and PLAN-ONLY OBNOVENO. A subsequent connected-plugin Indexer call with persist=true returned HTTP 403 PERSIST_DISABLED, request `8dc113aa-7289-4b21-a36f-2cf86f6d5bac`; persistence did not start.

Pre-test configuration backup: `/opt/business-brief-v4/.env.pre-persist-test-20261027T070822Z`.
The pre-test container formerly named `business-brief-bridge-pre-persist-20261027T070822Z` was restored as active `business-brief-bridge`. It preserves Chat read/run/search without the persist grant. The tested persist-enabled container and environment were retained under timestamped backup names; only the active container may own loopback port 8080.

## Private adapter and authentication

- Site: `appgprj_6ad130997e848191822752605e6ab177`, version 7, owner-private.
- URL: https://business-brief-ingestor.satinyloom128.chatgpt.site
- MCP: https://business-brief-ingestor.satinyloom128.chatgpt.site/mcp
- Existing plugin: `plugin_asdk_app_sites_8ed4ce3b42248191bfed2a4cafd37c82`.
- Published Site source commit: `eb9b2fa515a916552bf7a688d3fbb462970b5011`.
- Adapter uses `https://bridge.businessbrief.cz`, preserving the existing Ingestor tools and adding run_assembler, run_indexer, get_pipeline_status, search_index, run_technician.
- All runner operations, including status, use existing server-side `BRIDGE_WRITE_TOKEN`; ledger visibility is principal-scoped. Ingestor reads use `BRIDGE_READ_TOKEN`. No new BRIDGE_PIPELINE_TOKEN is required.
- Adapter defaults persist=false, validates explicit selection and UUID retry keys, sanitizes upstream errors, and leaves persist authorization to the Bridge scopes/server flag. It supports explicitly requested persist=true; the older unshipped plan-only module is not the deployed implementation.
- v7 validation at publication: seven transport tests, TypeScript check and production build passed.

Initial v7 calls failed UNAUTHENTICATED because Hetzner only accepted `tannenberg-assembler`. The operator transferred the original Railway BRIDGE_PRINCIPALS directly from their Mac clipboard over SSH into a mode-600 pending file, without exposing tokens to the model. Validated principals `codex-acceptance-read` (source:read) and `manual-ingestor` (source:read, page:write) were added without replacing tannenberg-assembler. All are WSJ-only. manual-ingestor subsequently received pipeline:read/run/search; pipeline:persist was temporary for this test and has now been removed. Site secrets were not read, changed or rotated.

Credential caveat: the existing infrastructure record says Railway secrets had previously been treated as potentially exposed after a provider notification. Reusing original Bridge credentials restores compatibility, but is not evidence of fresh credential rotation or resolution of that earlier concern. A verified secure provisioning/rotation path remains operational follow-up. No supported secret-entry UI was established; do not repeat the earlier unverified UI instructions or ask for tokens in chat.

## Exact accepted selection

- source_id: `603e8242-ffe8-4e1d-a5de-9adb3da4d188`
- manifest_id: `wsj-2026-10-14-selection-r1`
- manifest_sha (HTTP argument): `f78c5339c3f4e406f78645a3c6e3fe3b8f53d89a3919ab6adad4c7e8f29a1d77`

## Plugin acceptance receipts

All IDs below are durable tool request/idempotency IDs, not the per-response transport request_id.

| Operation | Durable request ID | Verified result |
| --- | --- | --- |
| Assembler plan, 2026-10-26 | 4f80f1d4-b89e-4ae2-98d2-f6ad338d22cc | COMPLETE/PASS; 27 items, 21 records, 16 VERIFIED, 5 VERIFIED_WITH_NOTES, zero review/blocked; same-key replay=true |
| Indexer plan, 2026-10-26 | 20bb05c7-679d-4d15-bb8c-d0e59e03b2da | COMPLETE/PASS; 21 eligible, 39 chunks, zero skipped |
| Assembler persist, 2026-10-27 | f61d4dc7-2bb7-405a-84ac-854ab55b12c5 | COMPLETE/PASS; all 21 immutable persistence receipts REPLAYED; same-key API replay=true |
| Indexer persist, 2026-10-27 | 4302b8c7-fb2d-4499-affc-456544c9e3e1 | COMPLETE/PASS; 21 receipts REPLAYED, 39 chunks; same-key API replay=true |
| New-key Indexer persist | 7b01df9a-e416-41fb-abf5-d2d7494ffef8 | COMPLETE/PASS; all 21 exact-version runtime receipts REPLAYED |
| Czech NATO search | d5f92509-ff96-404f-b939-ca523ddd2a3a | COMPLETE/PASS; expected article first, score 0.589623093605046; 5 vector hits, 0 lexical |

One Assembler same-key retry while Indexer was running returned WRITE_IN_PROGRESS (503). After status confirmed completion, retrying that identical Assembler key succeeded. This is observed source-lock enforcement, not a failed assembly or justification to issue new keys after uncertainty.

Direct DB readback joined all 21 Assembler receipts against exact article ID, SHA, bucket, key, byte size and selection: 21 distinct receipts, 21 exact matches. Before/after counts: 21 articles, 21 index runs (all INDEXED), 21 article embeddings, 39 chunks. MD5 comparison fingerprints of complete ordered row JSON, including existing vectors and timestamps, were unchanged:

| Set | Comparison fingerprint |
| --- | --- |
| articles | 3da7d0f863b41670408c49d357fbd2c1 |
| article_index_runs | 8e050e9b9530d0392bdf142d30a65e4b |
| article_embeddings | 927890b2746e30b1aacab1c36d1758bc |
| article_chunks | 39fc72f18e265ae15e79aa27f6e129e1 |

These are comparison fingerprints, not canonical artifact SHA-256 values. The tested indexer_runtime checks replay_if_indexed and performs persisted post-checks before embed calls. All receipts took that replay branch; no new document embedding computation is indicated. This is code/receipt evidence, not independent provider billing telemetry. Search separately performed a billable query embedding. Runner requests create private ledger receipts even when canonical/index data are replayed or persist=false.

Search query: “Jak dronové útoky na lodě prověřují schopnosti NATO?” First result was independently joined to title “Drone Attacks on Ships Test NATO”, article `art-9491140a80efae03a7abca8bd76c7899c20178db7011553da646520e8ce8e16b`, SHA `a095887e661955b4ce97afa4d3bfb0ab10ae5ed5822cc1d4539490feff96f379`. This closes only the previously unconfirmed spot check, not Q017.

run_technician was called through the plugin and correctly returned 409 TECHNICIAN_SOURCE_SCOPED_UNAVAILABLE. No global Technician queue was started.

## Remaining closure

1. DONE: pre-test configuration/container restored; operator readiness/flag/grant checks passed, and the plugin independently returned 403 PERSIST_DISABLED.
2. DONE: operator ran a new ordinary Chat with Business Brief Ingestor, without terminal or credentials. Assembler `9261ada6-abb8-476b-a122-2e5313bd719f` completed at 2026-10-27T07:33:42Z; Indexer `02b9cd60-bd48-417c-a083-f452c2ebfc77` at 07:34:10Z. Both exact server receipts were independently read back as COMPLETE/PASS with persist=false and empty persistence receipts. Assembler: 27 page items, 21 records, 16 VERIFIED, 5 VERIFIED_WITH_NOTES, zero review/blocked, zero persisted. Indexer: 21 rows/eligible, 39 planned chunks, zero skipped/persisted; BB-CHUNKING-V1, BB-EMBEDDING-V1, BB-LEXICAL-TOKENIZER-V1, embed-v5.0-pro, 1024 dimensions. No Search or Technician was run in this fresh Chat.
3. Document the credential-rotation follow-up separately from functional acceptance.
4. Only then proceed to Handelsblatt end-to-end and Czech→German retrieval acceptance. Publication allowlists are currently WSJ-only; do not silently broaden them.
5. Technician source-scoped execution remains separate implementation work. Search still takes the authorized exact-selection subset of global top 100; recall and calibration remain open. Q017 requires a benchmark, latency/cost measurements and Czech→German coverage.
