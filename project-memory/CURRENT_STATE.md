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
Verified on 2026-10-16: default main is 0c3164f3092c14d017285dca68bbfb122bc30de6. PR #4 is open, targets main, head 85b83088f71af1638b4a2416829eb3090c74bd13. PR #5 is open/draft, stacked on #4, head 311a865854a33472b0e78a70b1ee4eae5084cc96. This consolidation is stacked on #5; neither PR has been merged. Their earlier PR descriptions predate subsequent acceptance.

This branch implements page-ingest-v3 / ingestor-v2.1-chat / instruction 2.1 with a separate ingestor-v2.1 canonical namespace. Legacy v2 serialization and storage remain compatible. New bridge/plugin generation support is not yet deployed or production-accepted. No production ingest/persist/deployment is performed by this consolidation.

The standalone Railway bridge has scoped auth, private buckets, direct verified-TLS PostgreSQL sessions, row/session locks, durable PENDING claims and identity guards, create-if-absent and exact JCS readback. See bridge/README.md for recovery. Source Bundle remains source-bundle-v4. The recorded WSJ edition has 10 pages and was prepared by Technician v4.2; this consolidation does not assert new live Technician status.

## Next gates
1. Review/merge the stacked changes in dependency order and deploy bridge + plugin v3 validation/instructions together.
2. On explicit user instruction, accept the simplified content model on real pages (including continuation and a different publication); preserve v2 and select only an explicitly accepted generation downstream.
3. Resolve Assembler review/identity policy, then implement downstream assembly. A dedicated Page JSON index remains conditional on demonstrated need.

## Inactive and unresolved
Physical Map / Visual Page Map / BODY_FLOW / bbox and block-ID experiments and paid full-edition Fast Editorial remain historical/superseded. Acquisition is unresolved; the removed watcher is not current architecture. Preserve their history in FAILURES/HISTORY. Rights, publication gates and business model remain OPEN_QUESTIONS.
