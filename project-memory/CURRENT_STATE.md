# Current State — Business Brief v4

**Last consolidated:** 2026-10-16

## Current direction
Technician → Source Bundle → ordinary Chat Ingestor (one page, image + OCR) → validated canonical Page JSON → STOP. Assembler, Composer, Translator and Editorial follow only after content acceptance. Codex serves programming, system changes and debugging.

The accepted product correction is relevant-article extraction with source-faithful, visually validated text. There is no mandatory irrelevant-item inventory or mandatory perspective expansion. See D019–D020 and docs/INGESTOR.md.

## Delivered and accepted
The private/only-me Business Brief Ingestor Site v4 is deployed at https://business-brief-ingestor.satinyloom128.chatgpt.site/ . v3 delivered server-side PNG fetch, SHA/identity validation and MCP image content. v4 adds page-isolated inline OCR text from the prepared PDF, bounded extraction, sanitization and provenance; technical details are in docs/INGESTOR.md §20.

Ordinary Chat get_page_evidence returned WSJ 2026-10-14 page 1 image 1190×1684 + OCR 14,349 UTF-8 bytes without warnings or URL/token leakage. This closes the ordinary Chat read evidence integration gate, beyond the earlier Codex HTTPS acceptance.

The first production v2 page-1 persist passed CREATED, VERIFIED readback and usable_for_assembly=true. Its content model is now product-superseded: irrelevant inventory, separate What's News digest items and excessive perspective metadata. Preserve it unchanged as a technical acceptance artifact; do not treat its transport flag as current content approval. Exact immutable identity is in HISTORY.

These Site/ordinary Chat/persist milestones are user-supplied acceptance evidence consolidated here, not newly executed production checks. Live jobs, health and deployments remain authoritative in operational systems.

## Repository and rollout boundary
Verified on 2026-10-16: default main is 0c3164f3092c14d017285dca68bbfb122bc30de6. PR dependency chain remains open: #4 → main, #5 → #4, #6 → #5. Ancestor checks pass; all three have no submitted reviews or inline review threads. No PR was merged during rollout. Deploying only the bridge from a pinned reviewed/tested commit avoids triggering unrelated main-linked Railway services, including the historical ingestor cron.

Bridge commit 1442da050a0b3dcb4a5de9a11611a2b5ec9084c9 is deployed and pinned on Railway: deployment 7d1fa8aa-401d-4a2c-8fe0-5a4804eeb029, SUCCESS/Online, 1/1 replica. It accepts page-ingest-v3 / ingestor-v2.1-chat / instruction 2.1 in ingestor-v2.1, preserving v2. Site v4 required no change: its generic body transport already supports v3, verified with a mocked write-transport check and the real receipt. Site remains owner-only, source 5ad1e400d4a8b2a47f73e60de4b98a33a087dd81, deployment appgdep_6ad25784d0308191bc1dcdb6869c7145.

Post-deploy connected-plugin resolve and page-1 image/OCR passed for the pinned WSJ 2026-10-14 source. Six visually checked article starts were persisted once: STORED/CREATED, VERIFIED_WITH_NOTES, 14,568 JCS bytes, SHA bc287714ea5a290833976b7dfec6caf56f09a668e2c0d401c9e317ac246055e6, ingestor-v2.1/page-0001.json. Download readback matched SHA and identity; usable_for_assembly=true. Notes preserve unfinished page-boundary sentences/words, not unresolved source uncertainty. No page 2, assembly, v2 overwrite/deletion or migration. Full canonical key is in HISTORY. Tests: 138 passed; diff check clean.

Daily ordinary Chat workflow is technically ready through the existing plugin with current PROJECT/SCOPE/CURRENT_STATE/INGESTOR context. This rollout acceptance ran in Codex through the same connected MCP tools; it is not a newly observed separate ordinary-Chat session. Earlier ordinary Chat image/OCR acceptance remains distinct evidence.

The standalone Railway bridge has scoped auth, private buckets, direct verified-TLS PostgreSQL sessions, row/session locks, durable PENDING claims and identity guards, create-if-absent and exact JCS readback. See bridge/README.md for recovery. Source Bundle remains source-bundle-v4. The recorded WSJ edition has 10 pages and was prepared by Technician v4.2; this consolidation does not assert new live Technician status.

## Next gates
1. Review/merge #4 → #5 → #6 in dependency order after considering main-linked service auto-deploy effects. Bridge remains pinned; documentation-only pushes do not redeploy it.
2. On explicit user instruction, accept the simplified content model on real pages (including continuation and a different publication); preserve v2 and select only an explicitly accepted generation downstream.
3. Resolve Assembler review/identity policy, then implement downstream assembly. A dedicated Page JSON index remains conditional on demonstrated need.

## Inactive and unresolved
Physical Map / Visual Page Map / BODY_FLOW / bbox and block-ID experiments and paid full-edition Fast Editorial remain historical/superseded. Acquisition is unresolved; the removed watcher is not current architecture. Preserve their history in FAILURES/HISTORY. Rights, publication gates and business model remain OPEN_QUESTIONS.
