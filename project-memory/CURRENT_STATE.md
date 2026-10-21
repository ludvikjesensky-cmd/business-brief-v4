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

Q011 is now resolved by D025. The Assembler contract is now closed at the design level: deterministic `article-record-v1`, mandatory post-check, dedicated private `article-records` bucket with canonical `<publication_id>/<edition_date>/<source_sha256>/<manifest_id>/<article_id>.json` keys, and minimal PostgreSQL `articles` + `article_source_parts` operational indexes. The next planned implementation step is a deterministic Assembler over the explicit Edition Selection Manifest ID + SHA, producing immutable `article-record-v1` outputs; ambiguous joins or asset placement become review states rather than guesses. Every assembled article must also pass the mandatory mechanical post-check: exact source-part SHA verification, exactly-once ordered part usage, byte-for-byte reconstruction of `full_text` with canonical `\n\n` separators, final text SHA equality, and validation of every claimed asset placement. Post-check integrity failure is BLOCKED. No Assembler implementation or run is part of this contract freeze. Broader Q010, rights, acquisition and publication gates remain open. Legacy Physical Map, autonomous semantic ingest and paid full-edition Fast Editorial remain historical/superseded; see FAILURES/HISTORY.

## Indexer design consolidated (D026; not implemented)
The accepted downstream design is Assembler → mandatory assembly post-check → immutable Article Record persistence → Indexer → index post-check. Eligibility requires VERIFIED / VERIFIED_WITH_NOTES plus post_check PASS. NEEDS_REVIEW returns to ordinary Chat source review/correction and Assembler rerun through explicit immutable selection.

[docs/INDEXER.md](../docs/INDEXER.md) owns BB-CHUNKING-V1, first-class BB-EMBEDDING-V1 (Cohere embed-v5.0-pro, 1024D), article/chunk vectors in Supabase pgvector, derived tables, index states and hybrid multilingual retrieval. Canonical Article Records remain untouched. Ranking weights and implementation details remain Q017; broader Editorial Memory remains Q007. A pipeline runner is future orchestration.

Actual acceptance still stops at the accepted WSJ manifest above: no Assembler or Indexer run is claimed. This consolidation adds no runtime code, migration, bucket, Cohere call or deployment. Earlier test counts/deployment pins are historical verified evidence, not newly rerun checks.
