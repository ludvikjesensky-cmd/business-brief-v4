# Current State — Business Brief v4

**Last consolidated:** 2026-10-22


## Production infrastructure migration — 2026-10-22

Current production compute/web runtime is **Hetzner**, not Railway. Canonical operational detail is in [docs/INFRASTRUCTURE.md](../docs/INFRASTRUCTURE.md).

- Host: `tannenberg-prod-01`, IPv4 `46.225.32.16`, Ubuntu 26.04.1 LTS.
- Caddy is the public HTTPS gateway.
- `bridge.businessbrief.cz` terminates at Caddy and reverse-proxies to the Bridge container on `127.0.0.1:8080`.
- `businessbrief.cz` is served as a static site from `/var/www/businessbrief.cz`; source lives in private repo `ludvikjesensky-cmd/business-brief-web-v2`.
- Supabase remains authoritative PostgreSQL/Storage.
- The Hetzner-side production environment is `/opt/business-brief-v4/.env`, mode 600; secrets are not stored in Git.
- Following the Railway Variables security notification received by the operator, secrets previously stored there were treated as potentially exposed and rotated where applicable.
- Current `INGESTOR_BRIDGE_URL` is `https://bridge.businessbrief.cz`.
- Railway deployment IDs/pins below are historical provenance only and no longer establish current runtime health.

### Q020 real-source acceptance on Hetzner — COMPLETE

Accepted WSJ source `603e8242-ffe8-4e1d-a5de-9adb3da4d188`, manifest `wsj-2026-10-14-selection-r1`, SHA `f78c5339c3f4e406f78645a3c6e3fe3b8f53d89a3919ab6adad4c7e8f29a1d77`.

Read-only Assembler result:
- 27 page items;
- 21 Article Records;
- 16 VERIFIED;
- 5 VERIFIED_WITH_NOTES;
- 0 NEEDS_REVIEW;
- 0 BLOCKED;
- persistence not requested; 21 eligible, 0 persisted.

The first explicit `--persist` run wrote the eligible immutable Article Records and returned `CREATED` receipts. Repeating the exact same `--persist` command returned `REPLAYED` for the same records, confirming idempotent same-key/same-bytes persistence rather than duplicate creation.

Public website `https://businessbrief.cz/` returned 200. Public authenticated Bridge readiness returned HTTP/2 200 with `status: READY`. The Assembler container also reached the same public Bridge endpoint and received 200. Q020 is therefore accepted for this exact manifest/runtime.



## Indexer Q017 implementation and first live acceptance — 2026-10-26
PR #16 was merged into `main` at `47227d97cfdb3ec7f4b9d54d9839a9482b67a4b3` after green CI. Indexer v1 is implemented: deterministic BB-CHUNKING-V1 with frozen BB-LEXICAL-TOKENIZER-V1, Cohere `embed-v5.0-pro` / 1024D direct v2 API integration with `truncate=NONE`, pgvector/full-text derived tables, exact-version run states and post-check, explicit `bb-indexer` plan/persist CLI and `bb-search` calibration output with separate vector/lexical rankings.

Supabase production migration `add_indexer_v1` is applied. Production verification: pgvector 0.8.2; `article_index_runs`, `article_embeddings` and `article_chunks` have RLS enabled; vector and lexical retrieval RPCs are SECURITY INVOKER, unavailable to anon/authenticated and executable by service_role.

Hetzner was updated from `main` and the Docker image rebuilt. Exact WSJ source/manifest used for Q020 was then passed through Indexer. Read-only plan: 21 article rows, 21 eligible, 0 skipped, 39 planned chunks, no persistence. First explicit `--persist`: 21 receipts with CREATED. Identical rerun: 21 REPLAYED. Direct Supabase readback after replay: 21 index runs, 21 INDEXED, 21 article embeddings, 39 chunks covering all 21 articles; no duplicate growth.

Initial Czech→English semantic retrieval spot checks also passed across distinct topics: bank rates/profits, U.S. defense startups in Taiwan, and Chinese economic stagnation/Gen Z. In the Taiwan and China tests the expected article occupied the top vector positions; lexical ranking was empty for the Czech query against English source text, as expected. This is strong preliminary multilingual evidence but not final Q017 closure.

Q017 remains OPEN because Czech→German acceptance on Handelsblatt, a predeclared multilingual acceptance set, latency/cost measurement and final retrieval calibration are still pending. Hybrid fusion weights remain deliberately unfrozen.

## Current direction
D030 now separates the project into two independent branches.

**Fast Editorial:** current priority is to reconstruct and port the proven v3 edition-first live Chat workflow into v4 as an independent morning editorial path. The existing `fast-editorial-v4.1` page-level API worker is historical/superseded automation evidence, not the target implementation. Fast Editorial must not depend on Assembler, Indexer, Enrichment, Composer or Memory in this phase.

**Deep / Memory:** accepted source selection remains Technician → Source Bundle → ordinary Chat Ingestor → immutable canonical Page JSON / explicit full page revisions → Edition Selection Manifest → Assembler/post-check → immutable Article Records. Production Assembler acceptance and the first live Indexer plan/persist/replay acceptance have occurred on the exact accepted WSJ manifest; Composer, Translator and Editorial production runs have not. Ingestor preserves source-faithful relevant prose and article-owned PNG assets; perspective interpretation remains downstream. Q010 remains open. Q011 is resolved by D025 with deterministic Assembler policy and frozen logical `article-record-v1` contract.

## Q014/Q015 implemented, deployed and accepted
D024 / INGESTOR §22 implements page-revision-v1 as a separate full-snapshot v4 wrapper, safe source-scoped readback and inventory, and immutable edition-selection-v1. Canonical v2/v3/v4 schemas, keys, request/claim hashes and historical objects remain unchanged. Revision and manifest writes use create-if-absent, exact SHA/readback, durable original-request/target claims and source fencing. Assembler input requires exactly one accepted manifest ID + SHA, re-verifies all selected JSON/PNGs and never scans latest pages.

Historical D024 Railway Bridge pin: `388f2c879ae5d30b9544a08d95b7283a2f4c6fe6`; Railway deployment `fdaf8dfa-5ec9-4706-a5ef-7e15a209610a`, SUCCESS, iad. Tested/published tree `0361481f77a79fb07af9a5d32e17e25a77f02cd5` matched exactly. The acceptance rollout introduced no DB migration or new bucket. The subsequent main merge and legacy cron isolation are recorded below.

Private/only-me Site version 6: source `58652309a5720bfa2e25eb29b216e106ff24ac47`; deployment `appgdep_6ad5259db29c8191aee9f97bc8c8896f`, succeeded; https://business-brief-ingestor.satinyloom128.chatgpt.site . Adds get_page_artifact/list_ingested_pages and explicit revision/manifest tools. Existing plugin sessions may cache the original three tool names: resolve_current_source now also returns the ingest inventory; get_page_evidence includes a stored_page_readback text block for every exact available generation/revision on that page. The original generic persist_page_ingest transport also recognizes explicit page-revision-v1 / edition-selection-v1 envelopes inside body.page and routes them to the dedicated bridge endpoints. Those compatibility paths were exercised through the connected plugin, without credentials/signed URLs reaching the model. New standalone tool names were not separately invoked in this cached Codex session; no newly observed separate ordinary Chat session is claimed.

## WSJ 2026-10-14 accepted selection
Source UUID `603e8242-ffe8-4e1d-a5de-9adb3da4d188`, source SHA `2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f`, bundle SHA `e14e274810bbde45f738d94ca4a93f3eacefffb32bbb2221b259e2777a84e74d`, default variant, 10 physical pages. Fresh new-path readback verified all selected Page JSONs and 24 PNGs. Pages 3–10 canonical key/SHA/status exactly match #9 HISTORY; no discrepancies. Inventory confirms v2/v3 page 1, v3/v4 page 2 and v4 canonical pages 3–10; no v4 page 1. Selection is deliberately heterogeneous.

Manifest `wsj-2026-10-14-selection-r1`, **ACCEPTED_FOR_ASSEMBLY**, exact key:
`page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/edition-selection/wsj-2026-10-14-selection-r1.json`

SHA `f78c5339c3f4e406f78645a3c6e3fe3b8f53d89a3919ab6adad4c7e8f29a1d77`, 6,534 RFC8785 bytes, STORED/VERIFIED. Every page is explicitly selected: page 1 v3 canonical; pages 2–5 v4 canonical; page 6 v4 revision r1; pages 7–10 v4 canonical. Exact per-page SHA/status/receipt timestamps and asset identities are recorded in the immutable manifest/readbacks; HISTORY records the mapping. The edition is eligible as explicitly selected input, not homogeneous all-v4 and not evidence of cross-publication quality.

## Page-6 remediation (F011 resolved for selected revision)
Canonical page-6 SHA `d8672242e2cf88e51518c824c4ffceefbcfd524eb07a50d33a6611e2af4531ef` remains byte-identical and is explicitly blocked from accepted selection. New `ingestor-v2.2/revisions/page-0006/r1/page.json`: SHA `28fb43b41dec104745307204356bb758fa1c2f3044edc1e2688570865638d066`, 18,942 bytes, VERIFIED_WITH_NOTES, exact downloaded JSON + both PNG identities verified. Reason: `incomplete infographic crop`; lineage identifies original canonical key/SHA.

Authoritative source page PNG SHA `05b849e71ecbc45c252f48b1e657e11b6a4e3cae0b004fe8f1f64f4f909f5916`, 1190×1684. Standalone writer-equivalent inspection selected infographic bbox `[0.360,0.453,0.671,0.779]`, pixels `[428,762,799,1312]`, 371×550, 816,878 bytes, SHA `db6cd769e5c1a23f285e611b04faafc6bf89cfec07b285fb969a22084bbaf3c6`. The earlier estimated candidate was not used blindly.

Required standalone preview also exposed an independently clipped/contaminated Army photo. Following the user's evidence-based exception, r1 corrects its bbox to `[0.150,0.101,0.459,0.248]`, pixels `[178,170,547,418]`, 369×248, 366,389 bytes, SHA `7a975a9d6d88859683f8db2d99bf7663046eeb234a60161233cf166a561653c9`. All page text, anchors, article fields and non-crop metadata compare unchanged. Original JSON and both original PNGs remain historical artifacts, separately read back unchanged. Every revision crop was independently previewed before write; technical readback remains distinct from visual judgment.

## Validation and next boundary
249 Python tests pass, including 23 new revision/readback/selection tests; Site has 6 passing transport/OCR tests and a successful build. git diff --check is clean. Local canonical manifest/revision bytes match production receipt SHA exactly. Production revision write occurred only after green tests/deployments; full selected-page readback preceded the single accepted manifest write. This 2026-10-18 validation stopped after manifest; Q020 subsequently passed on 2026-10-22 as recorded above.

## Post-merge handoff (verified 2026-10-18)
GitHub confirms PRs #4–#10 are merged and closed. The ingest handoff is merged into `main` at `d35e963847721b49e5ef3aea71716ea0fb7b2825` (merge PR #10). The older PR #3 remains open/Draft and is separate from this merged stack. Q014/Q015 remain resolved; `wsj-2026-10-14-selection-r1` remains ACCEPTED_FOR_ASSEMBLY with the exact ID/key/SHA above.

Historical verification on 2026-10-18 confirmed the Railway bridge pin/deployment above as SUCCESS. Before the merge, the unrelated legacy `ingestor` cron was pinned to `a8d6c26e8002c8a4dcad42fce7fa6c5763e65580`; its redeploy `2e44c090-63b8-4b95-b5c6-8e263b14850e` is SUCCESS. Both source pins were configured at that historical check; this is not a current Hetzner deployment claim.

Q011 is resolved by D025 and D029 now implements the deterministic Assembler in the repository. `src/business_brief/assembler.py` builds immutable `article-record-v1` records from one exact accepted manifest, performs continuation resolution, unique-anchor asset placement and mandatory mechanical post-check. `assembler_runtime.py` loads the explicit Bridge assembly-input, independently re-downloads/verifies exact manifest/Page JSON/revision/PNG bytes from private Storage, and provides the `bb-assembler` CLI. Persistence is explicit via `--persist` only.

Migration `20261021130000_add_assembler_articles.sql` defines the private `article-records` bucket plus minimal PostgreSQL `articles` + `article_source_parts` operational indexes. The Assembler persistence path is now production-accepted for the exact WSJ manifest above; immutable Article Records were created and an immediate identical replay returned REPLAYED. The initial resolver intentionally fails closed when continuation labels cannot safely resolve to selected physical page numbers; title-token agreement only disambiguates candidates already bounded by explicit continuation evidence. Q020 is resolved for this exact accepted WSJ manifest; Indexer implementation is live and has passed WSJ plan/persist/replay, while Q017 multilingual calibration remains open. Broader Q010, rights, acquisition and publication gates remain open.

## Assembler repository implementation (D029; Q020 accepted for selected WSJ manifest)
Branch implementation adds:
- `src/business_brief/assembler.py`: deterministic graph/join logic, article IDs, source-part hashes, asset re-anchoring, post-check and persistence eligibility;
- `src/business_brief/assembler_runtime.py`: Bridge assembly-input adapter, independent Supabase byte verification, immutable Storage persistence + operational DB registration, read-only default CLI;
- `supabase/migrations/20261021130000_add_assembler_articles.sql`: private article-records bucket and article/source-part indexes;
- `tests/test_assembler.py` + `tests/assembler_schema.mjs`: deterministic continuation, ambiguity/review, asset anchor, tamper/hash and SQL/RLS constraints.

The accepted WSJ fixture is expected to exercise six Page-One continuations, including two distinct targets on A4 and two on A10. Real-source Assembler acceptance is complete on Hetzner for the exact accepted WSJ manifest: 21 Article Records (16 VERIFIED, 5 VERIFIED_WITH_NOTES, 0 NEEDS_REVIEW, 0 BLOCKED), followed by CREATED persistence receipts and REPLAYED receipts on identical rerun.

## PR #14 verification — 2026-10-21
GitHub Actions verification on head `a3d74adaf3275d2de4fdd0b0a0d06930a5cdfc45` passed cleanly: **294 Python tests**, **9 Assembler PostgreSQL/PGlite schema checks**, **14 existing knowledge-schema checks**, plus `py_compile` for assembler.py and assembler_runtime.py.

Review found and fixed two concrete issues before the green run: the initial CI environment omitted the repository root from PYTHONPATH for legacy bridge tests, and the first Assembler migration draft used a malformed dollar-quoted DO block. The migration now uses portable upsert semantics to ensure `article-records` is private; runtime bucket verification also fails closed unless privacy is explicitly false. A dedicated test now covers the exact accepted WSJ Page-One continuation title pairings for A2/A4/A6/A10. No production migration, runtime deployment or Article Record write occurred.

## Indexer design and runtime (D026/Q017)
The accepted downstream design is Assembler → mandatory assembly post-check → immutable Article Record persistence → Indexer → index post-check. Eligibility requires VERIFIED / VERIFIED_WITH_NOTES plus post_check PASS. NEEDS_REVIEW returns to ordinary Chat source review/correction and Assembler rerun through explicit immutable selection.

[docs/INDEXER.md](../docs/INDEXER.md) owns BB-CHUNKING-V1, first-class BB-EMBEDDING-V1 (Cohere embed-v5.0-pro, 1024D), article/chunk vectors in Supabase pgvector, derived tables, index states and hybrid multilingual retrieval. Canonical Article Records remain untouched. Runtime implementation and exact-version persistence/replay are now live. Q017 now tracks remaining multilingual retrieval calibration, latency/cost and hybrid weighting; broader Editorial Memory remains Q007. A pipeline runner is future orchestration.

Current accepted runtime includes the Assembler Q020 run plus Indexer plan/persist/replay over the same 21 WSJ Article Records, with 39 chunks and direct Supabase readback. Initial Czech→English retrieval spot checks passed; Czech→German and full Q017 calibration remain open. Earlier test counts/deployment pins are historical verified evidence, not newly rerun checks.

## Deep/Memory Composer design consolidated (D027; not implemented)
[docs/COMPOSER.md](../docs/COMPOSER.md) owns a Deep/Memory grouping layer inspired by v3 Cross-Paper Editor: closed current-day eligible indexed Article Records → candidate graph → semantic grouping → daily-topic-v1 → mandatory topic post-check → Selective Deep Read → Editorial Workflow. Composer does not select the Brief, allocate editorial roles, perform Deep Read or finalize angle/framing. Article individuality and importance ≠ reading value remain explicit.

Daily = delta. Memory = context: continuity retrieval follows today's grouping and cannot substitute older coverage. The contract defines exact article/index provenance, technical membership roles, deterministic day/member identity, single-source coverage, review statuses and minimal relational structures. NEEDS_REVIEW requires Chat review, recorded correction and Composer rerun; a future runner stops at semantic gates. Q018 owns implementation/calibration gates; Q007 remains broader Editorial Memory.

Current accepted runtime includes Assembler Q020 and first live Indexer acceptance on the exact WSJ manifest. No Composer, Deep Read or Editorial production run is claimed. This update is documentation/contract work only: no runtime implementation, model API calls, migrations, deployments or production data writes.

## Enrichment / hybrid knowledge foundation (D028; repository implementation)
PR #13 continues the existing Composer design with docs/ENRICHMENT.md and daily-topic-v1 knowledge_links. v3 source contracts/code/schema at 933b5c47fb96c97333ff24dda4e7e019486ebbfd were inspected. Retained/adapted/dropped concepts are explicitly mapped there.

Implemented offline Python editorial-enrichment-v1 data types, SHA-bound passage evidence, exact batch coverage/profile uniqueness, controlled/normalized relations, candidate/accepted separation, reviewed promotion minima and metadata/profile retrieval candidate helpers. Synthetic tests validate integrity and boundaries, not model quality or real multilingual recall. No model provider, persistence adapter, live search or semantic Composer grouper is included. The existing PR migration is hardened to nine candidate-staging tables with normalized annotations, required versions/SHA lineage, exact candidate revision FKs, nonempty evidence/date checks, RLS and insert/select-only worker grants. Accepted state is unavailable until Q019.

Assembler physical article tables/runtime under D029 are accepted for the exact WSJ manifest through Q020 on Hetzner, including immutable persistence and replay. Indexer/Composer physical runtimes remain unimplemented; Q019 still requires Q017/Q018 identities and its own knowledge acceptance. No Indexer/Composer/enrichment production run is claimed. The D028 validation below is historical offline evidence, not a rerun during this consolidation.

D028 validation: **281 Python tests passed**, including **32 new enrichment/knowledge tests**; five existing PyMuPDF/SWIG deprecation warnings. Local HTTP tests required localhost socket permission. Markdown relative links/code fences and `git diff --check` passed. The initial older test environment lacked Pillow; the complete suite was rerun in an existing asset-test environment with the required dependencies. The actual SQL migration also passes 14 in-memory PostgreSQL/PGlite integrity and privilege checks; no external database was used. Live upstream adapters, transactional promotion/concurrency and a multilingual provider benchmark remain gated above.

Synchronized with concurrent PR work through c511b018: preserve the existing editorial-enrichment-v1 / BB-ENRICHMENT-V1 names and exact-sidecar Composer-ready requirement. Replace the shallow string-reference validator with the evidence-bound typed API; this is an unfrozen repository contract refinement, not a second parallel enrichment design. Preserve the existing migration path as candidate-only staging rather than granting unsupported accepted knowledge. Prior intermediate implementation remains in Git history.
