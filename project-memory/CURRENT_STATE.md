# Current State — Business Brief v4

**Last consolidated:** 2026-10-18

## Current direction
Technician → Source Bundle → ordinary Chat Ingestor (one page, image + OCR) → validated canonical Page JSON → STOP. Assembler, Composer, Translator and Editorial follow only after content acceptance. Codex serves programming, system changes and debugging.

The accepted product correction is relevant-article extraction with source-faithful, visually validated text. There is no mandatory irrelevant-item inventory or mandatory perspective expansion. See D019–D020 and docs/INGESTOR.md.

## Article assets — implemented, deployed and page-2 accepted
D022 is implemented by bounded authoritative server-side PNG cropping, explicit artifact:null submission versus strict final metadata, and set-wide durable/source-fenced create/readback. Existing private page-ingest bucket and v4 namespace ingestor-v2.2; v2/v3 remain immutable. Normative write/recovery details are INGESTOR §21.5.

Bridge runtime is pinned to `b6d465c49dbf546f0ea31876d218121428d495c8`, Railway deployment `4489131f-d578-4062-b88f-40adc3716932` (SUCCESS, 1 replica, iad). PR #8 is stacked after #7; no merge or unrelated service deployment. Site v4 remains unchanged and owner-only. The existing generic tool transported artifact:null v4 JSON and the enriched receipt successfully; no raw image bytes or signed URLs were passed in the write request.

Connected-plugin acceptance in Codex (ordinary-Chat-compatible transport, not a newly observed separate ordinary Chat session) completed exactly WSJ 2026-10-14 page 2: STORED/CREATED, VERIFIED_WITH_NOTES, identity_matches=true, usable_for_assembly=true. Three relevant articles and three chart PNGs (both requested banking charts plus the home-price chart) were visually checked before persistence. Bank continuation retains its visible opening fragment. All three text anchors are unique; no placement guess. Final Page JSON SHA `f271f52b378852b186ee919f39d48983db57d469891bd4fad437107efefed60f`, 17,165 RFC8785 bytes. Exact downloaded PNG SHA/size/dimensions match independent local source-derived expected bytes. Both original-request and deterministic set bindings are VERIFIED. Full canonical keys/crop identities are in HISTORY.

The first attempt encountered the existing bucket's JSON-only MIME restriction, leaving PENDING claims and zero v4 objects. The tested deployment hook additively allowed image/png and raised the bucket limit from 5 to 32 MiB while retaining private access. Retrying the original wrapper and idempotency key completed the same intended write; no claim cleanup or object overwrite/delete. Supabase inspection verified four v4 objects and unchanged v2/v3 object IDs/ETags/sizes/updated_at, including v3 page 2. That acceptance stopped after page 2; the subsequent ordinary-Chat pass is qualified below. No assembly is evidenced.

Recorded #8 validation: 226 tests passed (35 added beyond the 191-test contract baseline); its git diff --check was clean. These tests were not rerun for this documentation-only consolidation. Tested runtime tree 6b6cd891b540b1b3dce0e56f61c71c2f77f3decd exactly matches the published runtime commit. Source PNG SHA 1f85cea3134e033b03f01c312385f6c3e53b07ced165aac7dbcb9b04300b4396, 1190×1684. No DB migration/new bucket or Site redeploy.

## Delivered and accepted
The private/only-me Business Brief Ingestor Site v4 is deployed at https://business-brief-ingestor.satinyloom128.chatgpt.site/ . v3 delivered server-side PNG fetch, SHA/identity validation and MCP image content. v4 adds page-isolated inline OCR text from the prepared PDF, bounded extraction, sanitization and provenance; technical details are in docs/INGESTOR.md §20.

Ordinary Chat get_page_evidence returned WSJ 2026-10-14 page 1 image 1190×1684 + OCR 14,349 UTF-8 bytes without warnings or URL/token leakage. This closes the ordinary Chat read evidence integration gate, beyond the earlier Codex HTTPS acceptance.

The first production v2 page-1 persist passed CREATED, VERIFIED readback and usable_for_assembly=true. Its content model is now product-superseded: irrelevant inventory, separate What's News digest items and excessive perspective metadata. Preserve it unchanged as a technical acceptance artifact; do not treat its transport flag as current content approval. Exact immutable identity is in HISTORY.

These Site/ordinary Chat/persist milestones are user-supplied acceptance evidence consolidated here, not newly executed production checks. Live jobs, health and deployments remain authoritative in operational systems.

## WSJ ordinary-Chat pass — evidence and remaining acceptance
Source: The Wall Street Journal, `2026-10-14/default`, UUID `603e8242-ffe8-4e1d-a5de-9adb3da4d188`, SHA `2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f`, 10 pages. v4 tuple is `page-ingest-v4` / `ingestor-v2.2-chat` / instruction `2.2` / namespace `ingestor-v2.2`.

Evidence checked in this consolidation: canonical memory and PR #8, archived bridge receipts for v3 page 1 and v4 page 2, and the original ordinary-Chat conversation `6acf97b3-4370-83eb-9ec9-a9da736f0e81`. The exposed bridge tools resolve a source/read source-page evidence/persist; they provide no stored Page JSON read/list or receipt lookup endpoint. No fresh production storage inventory or readback was performed. Receipt evidence verifies historical persistence, not present-day object availability. Exact evidence levels and page identities are in HISTORY.

Page 1 has historical v2 acceptance and receipt-backed v3 (`ingestor-v2.1`); no actual v4 page-0001 object was found in available evidence. Page 2 v4 is receipt-backed. Pages 3–10 are reported ordinary-Chat v4 results, with exact JSON keys/SHA/status in the conversation but no raw bridge receipts available here. The reported pass demonstrates repeated read → image/OCR validation → v4 JSON + asset metadata → bridge persist, including empty page, prose sidebar, continuations and photo/map/chart/infographic assets; it is not an independently revalidated corpus. All ten pages are reported processed across generations; a homogeneous all-v4 corpus is NOT established.

**Known open visual defect (F011):** immutable page-6 v4 contains a visually-invalid `About Face` infographic crop, clipped on the left. Its reported technical SHA/readback and usable_for_assembly=true do not override this defect. The edition is NOT fully visually accepted. Quarantine page 6 from accepted downstream input pending an authorized immutable revision/correction protocol (Q014); do not overwrite/delete its JSON or PNG. The approximate wider bbox `[0.335, 0.445, 0.790, 0.810]` is only a manually estimated candidate, not production-writer-verified or canonical.

Every crop must now be independently rendered with server-equivalent bbox rules from the authoritative PNG and previewed as its own image before `visual_checked:true` and persistence (INGESTOR §21.7). Full-page bbox inspection alone is insufficient. Pages 7–10 report this independent preview; it was not replayed here.

## Next gates
1. Review stacked #4 → #5 → #6 → #7 → #8 in dependency order after assessing unrelated main-linked auto-deploys. Runtime stays pinned; documentation pushes do not redeploy it.
2. Obtain authoritative receipts/readback for reported pages 3–10, resolve page-6 visual correction and explicitly select per-page generations before corpus acceptance. No assembly or new ingestion in this consolidation.
3. Resolve Assembler review/identity and shared-insertion ordering policy before downstream implementation. Select an explicitly accepted generation; no assembly was run.

## Inactive and unresolved
Physical Map / Visual Page Map / BODY_FLOW / bbox and block-ID experiments and paid full-edition Fast Editorial remain historical/superseded. Acquisition is unresolved; the removed watcher is not current architecture. Preserve their history in FAILURES/HISTORY. Rights, publication gates and business model remain OPEN_QUESTIONS.

## Local validation for D022
The 191-test contract baseline is extended to 226 passing tests for real PNG crops, source/bbox/metadata identity, bounds/limits, one/two assets, set replay/conflict/concurrency, asset/page interruptions and reconciliation, source change, generic JSON transport and redaction. The six provisioning cases also prove additive MIME/limit changes and privacy/readback gates. No production service is needed for local tests.
