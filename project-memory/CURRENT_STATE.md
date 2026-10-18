# Current State — Business Brief v4

**Last consolidated:** 2026-10-18

## Current direction
Technician → Source Bundle → ordinary Chat Ingestor (one page, image + OCR) → validated canonical Page JSON → STOP. Assembler, Composer, Translator and Editorial follow only after content acceptance. Codex serves programming, system changes and debugging.

The accepted product correction is relevant-article extraction with source-faithful, visually validated text. There is no mandatory irrelevant-item inventory or mandatory perspective expansion. See D019–D020 and docs/INGESTOR.md.

## Article assets — implemented, deployed and page-2 accepted
D022 is implemented by bounded authoritative server-side PNG cropping, explicit artifact:null submission versus strict final metadata, and set-wide durable/source-fenced create/readback. Existing private page-ingest bucket and v4 namespace ingestor-v2.2; v2/v3 remain immutable. Normative write/recovery details are INGESTOR §21.5.

Bridge runtime is pinned to `b6d465c49dbf546f0ea31876d218121428d495c8`, Railway deployment `4489131f-d578-4062-b88f-40adc3716932` (SUCCESS, 1 replica, iad). PR #8 is stacked after #7; no merge or unrelated service deployment. Site v4 remains unchanged and owner-only. The existing generic tool transported artifact:null v4 JSON and the enriched receipt successfully; no raw image bytes or signed URLs were passed in the write request.

Connected-plugin acceptance in Codex (ordinary-Chat-compatible transport, not a newly observed separate ordinary Chat session) completed exactly WSJ 2026-10-14 page 2: STORED/CREATED, VERIFIED_WITH_NOTES, identity_matches=true, usable_for_assembly=true. Three relevant articles and three chart PNGs (both requested banking charts plus the home-price chart) were visually checked before persistence. Bank continuation retains its visible opening fragment. All three text anchors are unique; no placement guess. Final Page JSON SHA `f271f52b378852b186ee919f39d48983db57d469891bd4fad437107efefed60f`, 17,165 RFC8785 bytes. Exact downloaded PNG SHA/size/dimensions match independent local source-derived expected bytes. Both original-request and deterministic set bindings are VERIFIED. Full canonical keys/crop identities are in HISTORY.

The first attempt encountered the existing bucket's JSON-only MIME restriction, leaving PENDING claims and zero v4 objects. The tested deployment hook additively allowed image/png and raised the bucket limit from 5 to 32 MiB while retaining private access. Retrying the original wrapper and idempotency key completed the same intended write; no claim cleanup or object overwrite/delete. Supabase inspection verified four v4 objects and unchanged v2/v3 object IDs/ETags/sizes/updated_at, including v3 page 2. STOP after page 2: no page 3 or assembly.

226 tests pass (35 added beyond the 191-test contract baseline); git diff --check clean. Tested runtime tree 6b6cd891b540b1b3dce0e56f61c71c2f77f3decd exactly matches the published runtime commit. Source PNG SHA 1f85cea3134e033b03f01c312385f6c3e53b07ced165aac7dbcb9b04300b4396, 1190×1684. No DB migration/new bucket or Site redeploy.

## Delivered and accepted
The private/only-me Business Brief Ingestor Site v4 is deployed at https://business-brief-ingestor.satinyloom128.chatgpt.site/ . v3 delivered server-side PNG fetch, SHA/identity validation and MCP image content. v4 adds page-isolated inline OCR text from the prepared PDF, bounded extraction, sanitization and provenance; technical details are in docs/INGESTOR.md §20.

Ordinary Chat get_page_evidence returned WSJ 2026-10-14 page 1 image 1190×1684 + OCR 14,349 UTF-8 bytes without warnings or URL/token leakage. This closes the ordinary Chat read evidence integration gate, beyond the earlier Codex HTTPS acceptance.

The first production v2 page-1 persist passed CREATED, VERIFIED readback and usable_for_assembly=true. Its content model is now product-superseded: irrelevant inventory, separate What's News digest items and excessive perspective metadata. Preserve it unchanged as a technical acceptance artifact; do not treat its transport flag as current content approval. Exact immutable identity is in HISTORY.

These Site/ordinary Chat/persist milestones are user-supplied acceptance evidence consolidated here, not newly executed production checks. Live jobs, health and deployments remain authoritative in operational systems.

## Earlier v3 rollout (historical evidence)
Verified on 2026-10-16: default main is 0c3164f3092c14d017285dca68bbfb122bc30de6. PR dependency chain remains open: #4 → main, #5 → #4, #6 → #5. Ancestor checks pass; all three have no submitted reviews or inline review threads. No PR was merged during rollout. Deploying only the bridge from a pinned reviewed/tested commit avoids triggering unrelated main-linked Railway services, including the historical ingestor cron.

Bridge commit 1442da050a0b3dcb4a5de9a11611a2b5ec9084c9 is deployed and pinned on Railway: deployment 7d1fa8aa-401d-4a2c-8fe0-5a4804eeb029, SUCCESS/Online, 1/1 replica. It accepts page-ingest-v3 / ingestor-v2.1-chat / instruction 2.1 in ingestor-v2.1, preserving v2. Site v4 required no change: its generic body transport already supports v3, verified with a mocked write-transport check and the real receipt. Site remains owner-only, source 5ad1e400d4a8b2a47f73e60de4b98a33a087dd81, deployment appgdep_6ad25784d0308191bc1dcdb6869c7145.

Post-deploy connected-plugin resolve and page-1 image/OCR passed for the pinned WSJ 2026-10-14 source. Six visually checked article starts were persisted once: STORED/CREATED, VERIFIED_WITH_NOTES, 14,568 JCS bytes, SHA bc287714ea5a290833976b7dfec6caf56f09a668e2c0d401c9e317ac246055e6, ingestor-v2.1/page-0001.json. Download readback matched SHA and identity; usable_for_assembly=true. Notes preserve unfinished page-boundary sentences/words, not unresolved source uncertainty. No page 2, assembly, v2 overwrite/deletion or migration. Full canonical key is in HISTORY. Tests: 138 passed; diff check clean.

The earlier v3 workflow remains compatible; the current instruction 2.2 runtime/asset acceptance is recorded above. This rollout acceptance ran in Codex through the same connected MCP tools; it is not a newly observed separate ordinary-Chat session. Earlier ordinary Chat image/OCR acceptance remains distinct evidence.

The standalone Railway bridge has scoped auth, private buckets, direct verified-TLS PostgreSQL sessions, row/session locks, durable PENDING claims and identity guards, create-if-absent and exact JCS readback. See bridge/README.md for recovery. Source Bundle remains source-bundle-v4. The recorded WSJ edition has 10 pages and was prepared by Technician v4.2; this consolidation does not assert new live Technician status.

## Next gates
1. Review stacked #4 → #5 → #6 → #7 → #8 in dependency order after assessing unrelated main-linked auto-deploys. Runtime stays pinned; documentation pushes do not redeploy it.
2. Further pages/publications and continuation/content corpus acceptance require explicit instruction. Only one v4 page was accepted here.
3. Resolve Assembler review/identity and shared-insertion ordering policy before downstream implementation. Select an explicitly accepted generation; no assembly was run.

## Inactive and unresolved
Physical Map / Visual Page Map / BODY_FLOW / bbox and block-ID experiments and paid full-edition Fast Editorial remain historical/superseded. Acquisition is unresolved; the removed watcher is not current architecture. Preserve their history in FAILURES/HISTORY. Rights, publication gates and business model remain OPEN_QUESTIONS.

## Local validation for D022
The 191-test contract baseline is extended to 226 passing tests for real PNG crops, source/bbox/metadata identity, bounds/limits, one/two assets, set replay/conflict/concurrency, asset/page interruptions and reconciliation, source change, generic JSON transport and redaction. The six provisioning cases also prove additive MIME/limit changes and privacy/readback gates. No production service is needed for local tests.
