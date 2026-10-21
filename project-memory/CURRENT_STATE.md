# Current State — Business Brief v4

**Last consolidated:** 2026-10-21

## Current direction
Technician → Source Bundle → ordinary Chat Ingestor → immutable canonical Page JSON / explicit full page revisions → Edition Selection Manifest → STOP. No Assembler, Composer, Translator or Editorial run has occurred in this acceptance. Ingestor preserves source-faithful relevant prose and article-owned PNG assets; perspective interpretation remains downstream. Q010 (broader content/publication acceptance) remains open. Q011 is resolved by D025 with a deterministic Assembler policy and frozen logical `article-record-v1` contract.

## Q014/Q015 implemented, deployed and accepted
D024 / INGESTOR §22 implements page-revision-v1 as a separate full-snapshot v4 wrapper, safe source-scoped readback and inventory, and immutable edition-selection-v1. Canonical v2/v3/v4 schemas, keys, request/claim hashes and historical objects remain unchanged. Revision and manifest writes use create-if-absent, exact SHA/readback, durable original-request/target claims and source fencing. Assembler input requires exactly one accepted manifest ID + SHA, re-verifies all selected JSON/PNGs and never scans latest pages.

Bridge pin: `388f2c879ae5d30b9544a08d95b7283a2f4c6fe6`; Railway deployment `fdaf8dfa-5ec9-4706-a5ef-7e15a209610a`, SUCCESS, iad. Tested/published tree `0361481f77a79fb07af9a5d32e17e25a77f02cd5` matched exactly. The acceptance rollout introduced no DB migration or new bucket. The subsequent main merge and legacy cron isolation are recorded below.

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
249 Python tests pass, including 23 new revision/readback/selection tests; Site has 6 passing transport/OCR tests and a successful build. git diff --check is clean. Local canonical manifest/revision bytes match production receipt SHA exactly. Production revision write occurred only after green tests/deployments; full selected-page readback preceded the single accepted manifest write. STOP after manifest; no downstream processing.

## Post-merge handoff (verified 2026-10-18)
GitHub confirms PRs #4–#10 are merged and closed. The ingest handoff is merged into `main` at `d35e963847721b49e5ef3aea71716ea0fb7b2825` (merge PR #10). The older PR #3 remains open/Draft and is separate from this merged stack. Q014/Q015 remain resolved; `wsj-2026-10-14-selection-r1` remains ACCEPTED_FOR_ASSEMBLY with the exact ID/key/SHA above.

Railway confirms the bridge pin/deployment above remains SUCCESS. Before the merge, the unrelated legacy `ingestor` cron was pinned to `a8d6c26e8002c8a4dcad42fce7fa6c5763e65580`; its redeploy `2e44c090-63b8-4b95-b5c6-8e263b14850e` is SUCCESS. Both source pins remain configured; production has no staged changes.

Q011 is resolved by D025 and D029 now implements the deterministic Assembler in the repository. `src/business_brief/assembler.py` builds immutable `article-record-v1` records from one exact accepted manifest, performs continuation resolution, unique-anchor asset placement and mandatory mechanical post-check. `assembler_runtime.py` loads the explicit Bridge assembly-input, independently re-downloads/verifies exact manifest/Page JSON/revision/PNG bytes from private Storage, and provides the `bb-assembler` CLI. Persistence is explicit via `--persist` only.

Migration `20261021130000_add_assembler_articles.sql` defines the private `article-records` bucket plus minimal PostgreSQL `articles` + `article_source_parts` operational indexes. No migration has been applied and no production Article Record has been written. The initial resolver intentionally fails closed when continuation labels cannot safely resolve to selected physical page numbers; title-token agreement only disambiguates candidates already bounded by explicit continuation evidence. Q020 owns real-source acceptance on the accepted WSJ manifest before any Indexer consumption. Broader Q010, rights, acquisition and publication gates remain open.

## Assembler repository implementation (D029; not yet accepted in production)
Branch implementation adds:
- `src/business_brief/assembler.py`: deterministic graph/join logic, article IDs, source-part hashes, asset re-anchoring, post-check and persistence eligibility;
- `src/business_brief/assembler_runtime.py`: Bridge assembly-input adapter, independent Supabase byte verification, immutable Storage persistence + operational DB registration, read-only default CLI;
- `supabase/migrations/20261021130000_add_assembler_articles.sql`: private article-records bucket and article/source-part indexes;
- `tests/test_assembler.py` + `tests/assembler_schema.mjs`: deterministic continuation, ambiguity/review, asset anchor, tamper/hash and SQL/RLS constraints.

The accepted WSJ fixture is expected to exercise six Page-One continuations, including two distinct targets on A4 and two on A10. No real-source Assembler command has yet been run from this branch, so the expected article count/status is not recorded as accepted evidence. Q020 requires read-only real-source inspection before any persistent write.

## PR #14 verification — 2026-10-21
GitHub Actions verification on head `a3d74adaf3275d2de4fdd0b0a0d06930a5cdfc45` passed cleanly: **294 Python tests**, **9 Assembler PostgreSQL/PGlite schema checks**, **14 existing knowledge-schema checks**, plus `py_compile` for assembler.py and assembler_runtime.py.

Review found and fixed two concrete issues before the green run: the initial CI environment omitted the repository root from PYTHONPATH for legacy bridge tests, and the first Assembler migration draft used a malformed dollar-quoted DO block. The migration now uses portable upsert semantics to ensure `article-records` is private; runtime bucket verification also fails closed unless privacy is explicitly false. A dedicated test now covers the exact accepted WSJ Page-One continuation title pairings for A2/A4/A6/A10. No production migration, runtime deployment or Article Record write occurred.

## Q020 live read-only WSJ acceptance — 2026-10-21
Using the exact accepted WSJ 2026-10-14 selection identities, the live immutable page artifacts were read back through the production read-only Ingestor access layer and exercised against the D029 deterministic continuation/asset rules without persistence or production writes.

Selection used:
- manifest_id: `wsj-2026-10-14-selection-r1`
- manifest_sha256: `f78c5339c3f4e406f78645a3c6e3fe3b8f53d89a3919ab6adad4c7e8f29a1d77`
- pages 1–10 exactly as accepted: p1 ingestor-v2.1; p2–5/p7–10 ingestor-v2.2 canonical; p6 revision r1.

Observed result:
- 10 selected pages / 27 page items
- 21 assembled article records
- 16 VERIFIED
- 5 VERIFIED_WITH_NOTES
- 0 NEEDS_REVIEW
- 0 BLOCKED
- all 6 Page-One continuations resolved to the expected selected targets (A2, two A4, A6, two A10)
- 24 ArticleAssets encountered; 24 had exactly one valid authoritative anchor_text placement; 0 placement reviews
- every assembled record passed the mechanical source-order/full_text post-check in the read-only acceptance harness.

No Supabase migration, article-records bucket creation, Article Record persistence, DB row write or deployment occurred.

Important boundary: the available production read-only connector exposes exact immutable Page/Revision readback but does not expose the Bridge `assembly-input` endpoint itself. Therefore this proves live-source compatibility of the deterministic D029 assembly rules against the accepted artifacts, but does not yet prove the deployed `bb-assembler` runtime adapter's end-to-end Bridge/Supabase credential path. Q020 remains open for that final runtime + persistence acceptance.

## Q020 production migration applied; Railway runtime blocked by active platform outage — 2026-10-21
The Assembler persistence migration from main (`20261021130000_add_assembler_articles.sql`) was applied successfully to production Supabase project `tduhlvfsqplckemygjdx`.

Verified after migration:
- `public.articles` exists with RLS enabled and 0 rows;
- `public.article_source_parts` exists with RLS enabled and 0 rows;
- private Storage bucket `article-records` exists with `public=false`;
- no Article Record or source-part row has been written yet.

Supabase advisors show the expected INFO finding that the new RLS tables have no public policies, consistent with the service-role-only design. They also flag an unindexed `articles.publication_id` foreign key as a performance INFO item; this is not a correctness/security blocker for Q020.

The requested Railway Assembler deployment could not be created because Railway is in an active platform-wide incident: new builds/deploys are paused in all regions. Multiple create-service/create-deployment attempts returned `Deploys have been paused temporarily`. Existing Business Brief services remain online. Therefore `bb-assembler --persist`, exact Storage readback and idempotent replay have not run yet; Q020 remains open only on that external deployment gate.

## Indexer design consolidated (D026; not implemented)
The accepted downstream design is Assembler → mandatory assembly post-check → immutable Article Record persistence → Indexer → index post-check. Eligibility requires VERIFIED / VERIFIED_WITH_NOTES plus post_check PASS. NEEDS_REVIEW returns to ordinary Chat source review/correction and Assembler rerun through explicit immutable selection.

[docs/INDEXER.md](../docs/INDEXER.md) owns BB-CHUNKING-V1, first-class BB-EMBEDDING-V1 (Cohere embed-v5.0-pro, 1024D), article/chunk vectors in Supabase pgvector, derived tables, index states and hybrid multilingual retrieval. Canonical Article Records remain untouched. Ranking weights and implementation details remain Q017; broader Editorial Memory remains Q007. A pipeline runner is future orchestration.

Actual acceptance still stops at the accepted WSJ manifest above: no Assembler or Indexer run is claimed. This consolidation adds no runtime code, migration, bucket, Cohere call or deployment. Earlier test counts/deployment pins are historical verified evidence, not newly rerun checks.

## Composer design consolidated (D027; not implemented)
[docs/COMPOSER.md](../docs/COMPOSER.md) now owns the successor to v3 Cross-Paper Editor: closed current-day eligible indexed Article Records → candidate graph → semantic grouping → daily-topic-v1 → mandatory topic post-check → Selective Deep Read → Editorial Workflow. Composer does not select the Brief, allocate editorial roles, perform Deep Read or finalize angle/framing. Article individuality and importance ≠ reading value remain explicit.

Daily = delta. Memory = context: continuity retrieval follows today's grouping and cannot substitute older coverage. The contract defines exact article/index provenance, technical membership roles, deterministic day/member identity, single-source coverage, review statuses and minimal relational structures. NEEDS_REVIEW requires Chat review, recorded correction and Composer rerun; a future runner stops at semantic gates. Q018 owns implementation/calibration gates; Q007 remains broader Editorial Memory.

Actual acceptance still stops at the immutable WSJ selection manifest above. No Assembler, Indexer, Composer, Deep Read or Editorial run is claimed. This update is documentation/contract work only: no runtime implementation, model API calls, migrations, deployments or production data writes.

## Enrichment / hybrid knowledge foundation (D028; repository implementation)
PR #13 continues the existing Composer design with docs/ENRICHMENT.md and daily-topic-v1 knowledge_links. v3 source contracts/code/schema at 933b5c47fb96c97333ff24dda4e7e019486ebbfd were inspected. Retained/adapted/dropped concepts are explicitly mapped there.

Implemented offline Python editorial-enrichment-v1 data types, SHA-bound passage evidence, exact batch coverage/profile uniqueness, controlled/normalized relations, candidate/accepted separation, reviewed promotion minima and metadata/profile retrieval candidate helpers. Synthetic tests validate integrity and boundaries, not model quality or real multilingual recall. No model provider, persistence adapter, live search or semantic Composer grouper is included. The existing PR migration is hardened to nine candidate-staging tables with normalized annotations, required versions/SHA lineage, exact candidate revision FKs, nonempty evidence/date checks, RLS and insert/select-only worker grants. Accepted state is unavailable until Q019.

Assembler physical article tables/runtime now exist repository-side under D029, but are not yet migrated or real-source accepted; Indexer/Composer physical runtimes still do not exist. Q019 must wait for Q020 acceptance plus Q017/Q018 identities before enabling accepted knowledge. Q017/Q018 remain open. Existing production acceptance still stops at the immutable selected WSJ manifest; no Assembler/Indexer/Composer/enrichment production run is claimed. No deployment or production data write.

D028 validation: **281 Python tests passed**, including **32 new enrichment/knowledge tests**; five existing PyMuPDF/SWIG deprecation warnings. Local HTTP tests required localhost socket permission. Markdown relative links/code fences and `git diff --check` passed. The initial older test environment lacked Pillow; the complete suite was rerun in an existing asset-test environment with the required dependencies. The actual SQL migration also passes 14 in-memory PostgreSQL/PGlite integrity and privilege checks; no external database was used. Live upstream adapters, transactional promotion/concurrency and a multilingual provider benchmark remain gated above.

Synchronized with concurrent PR work through c511b018: preserve the existing editorial-enrichment-v1 / BB-ENRICHMENT-V1 names and exact-sidecar Composer-ready requirement. Replace the shallow string-reference validator with the evidence-bound typed API; this is an unfrozen repository contract refinement, not a second parallel enrichment design. Preserve the existing migration path as candidate-only staging rather than granting unsupported accepted knowledge. Prior intermediate implementation remains in Git history.
