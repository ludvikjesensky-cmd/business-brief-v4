# Ingestor v2.2 — article asset persistence

**Status:** CANONICAL COMPONENT DEFINITION  
**Execution model:** live Chat, human-supervised  
**Upstream:** Technician / `source-bundle-v4`  
**Downstream:** Assembler  
**Primary output:** exactly one verified Page JSON per processed source page

**Rollout boundary:** instruction 2.2 has a server-side asset writer. Deployment and acceptance status are recorded in CURRENT_STATE; schema validity alone does not establish rollout readiness.

## 1. Purpose

Ingestor v2.2 turns one technically prepared publication page into a structured, source-faithful Page JSON.

It exists because reliable page semantics require repeated inspection and correction. It is therefore a live conversational role, not an autonomous API batch worker.

Fundamental unit of work:

```
ONE SOURCE PAGE
→ ONE PAGE JSON
→ STOP
```

The next page begins only after explicit user instruction.

## 2. Required context

Before processing an edition, the Chat acting as Ingestor must read:

1. `PROJECT.md`
2. `project-memory/SCOPE.md`
3. `project-memory/CURRENT_STATE.md`
4. `docs/INGESTOR.md`

Read `docs/EDITORIAL.md` when relevance or downstream editorial meaning is unclear.

Read the current Page JSON contract in `src/business_brief/contracts.py` before emitting output.

The role must understand the purpose of Business Brief before judging relevance.

## 3. Input authority

The canonical input is a valid Technician Source Bundle for the selected edition.

The Source Bundle may provide:

- publication and edition identity;
- source ID and provenance;
- immutable source hash;
- prepared PDF;
- OCR/native text layer;
- page images;
- page-level technical metadata.

Evidence priority:

1. visible source page;
2. Technician page image / technical evidence;
3. prepared text or OCR;
Previous Chat interpretation is excluded from evidence.

Previous model output is never source evidence.

When visible page and OCR disagree, inspect the page and resolve from the source whenever possible.

## 4. Scope of one page pass

The Ingestor follows one fixed mental sequence:

**page orientation → item inventory → ownership → relevance/perspective → source-text reconstruction → verification → JSON**

For each requested page:

1. Confirm source, publication, edition and page number.
2. Inspect the complete page before extracting individual items.
3. Orient over all editorial and non-editorial regions; this working inventory is not a required persisted audit.
4. Identify each editorial item independently and determine ownership/reading order.
5. Judge Business Brief relevance and perspective value for each item.
6. For each relevant item, reconstruct all continuous article prose physically present on this page; preserve associated visuals separately as article assets (§21), never canonical chart/table OCR.
7. Omit clearly irrelevant items unless needed for continuity, ambiguity resolution or explicit review (section 7).
8. Record a short relevance reason; preserve perspective through source text rather than mandatory interpretation fields.
9. Record continuation evidence without assembling other pages.
10. Verify boundaries, reading order, text completeness and uncertainty.
11. Emit exactly one Page JSON matching the current machine contract.
12. Report unresolved uncertainties briefly.
13. STOP.

Do not continue automatically.

The Ingestor must not jump directly to the largest headline. It first understands the page as a whole.

## 5. Editorial item identification

Possible item types include:

- article
- brief
- feature
- column
- editorial
- opinion
- interview
- review
- sidebar
- factbox
- caption
- infographic
- table
- contents_item
- other

Advertisements and page furniture are not editorial items.

For each editorial item, determine as far as the source supports:

- title;
- subtitle/deck;
- kicker;
- byline;
- item type;
- text physically present on the page;
- start/continuation state;
- continuation marker or target;
- relevance;
- verification notes.

Do not infer an article merely from spatial proximity. Ownership and reading order must be checked against the whole page.

## 6. Source-faithful text

For relevant items, reconstruct only the text physically present on the current page.

Use `text_on_page`, not `full_article_text`. Only continuous prose belongs here; preserve associated visuals as PNG assets under §21, without canonical chart/table OCR.

Do not:

- summarize;
- paraphrase;
- translate;
- stylistically improve;
- silently omit text;
- invent transitions;
- infer missing endings;
- complete wording from memory or web knowledge.

OCR is a proposal/supporting evidence; visually validate it against the page image, the primary authority. Technical normalization may join words split across layout lines, remove layout line breaks and excess whitespace, and correct obvious OCR errors only when the image confirms them. Preserve paragraphs and source meaning.

Line-break hyphenation may be normalized only when visually supported.

If a word or passage cannot be verified, localize the uncertainty in verification notes and use NEEDS_REVIEW (or BLOCKED if extraction cannot proceed). Never label unresolved source text VERIFIED or hide it in VERIFIED_WITH_NOTES.

## 7. Relevance

Relevance answers:

> Is this item worth carrying forward into the Business Brief processing pipeline?

It does not answer:

> Will this item be published in the Brief?

The final publication decision belongs downstream.

The Ingestor must not reduce relevance to "is this a big news event?" or even only to "is this business-related?"

A text can be highly relevant because it offers a **distinctive perspective** even when the underlying event is already known.

When judging relevance, explicitly look for:

- a distinctive angle;
- the author's central question;
- the way the publication frames the issue;
- an argument that changes or sharpens understanding;
- a new mental model;
- an unexpected connection;
- a tension, contradiction or dilemma;
- a perspective characteristic of the publication or author;
- material that can move the reader's perception of the topic forward.

The core relevance test is:

> Does this text merely tell us something, or does it help us see the subject differently, more precisely or more deeply?

Preserve three states:

- `relevant`
- `irrelevant`
- `uncertain`

A short reason is required for the relevance judgment.

For a relevant item, the reason should state not only the topic but, where visible from the page, **why the perspective matters**.

### Recall over aggressive filtering

Ingestor is not the final editor. When relevance is genuinely uncertain, prefer **recall over aggressive filtering**.

If an item has plausible business, economic, technological, managerial, geopolitical or perspective value, preserve it for downstream review rather than discarding it prematurely.

Use `uncertain` when the current page is insufficient to make a safe decision.

### Relevant-item selection

Identify articles/editorial items across the whole page, but persist primarily relevant articles. Preserve uncertain candidates for review. Clearly irrelevant items are optional and belong in JSON only when needed for continuity, ambiguity resolution or explicit review; explain that exception in the relevance reason. There is no mandatory audit inventory of rejected items.

What's News digests are navigation/selection evidence, not automatically separate article records. Preserve a digest only when it independently meets relevance or an explicit review need; do not substitute it for the referenced article's body.

## 8. Perspective boundary

Relevance supports selection and requires a short reason. The new minimal contract does not require or serialize PerspectiveEvidence. Preserve the author's argument through faithful source text; article-level interpretation belongs downstream after assembly. The legacy v2 structure remains readable for compatibility only.

## 9. Cross-page boundary

Ingestor v2.2 never assembles multi-page articles.

It records only evidence visible on the current page, including:

- `starts_here`
- `continued_from_previous_page`
- `continues_to_another_page`
- `continuation_marker`
- `continuation_target`

The Assembler resolves cross-page article identity and joins text, then re-anchors assets by unique anchor text (§21.3); ambiguous assets remain unplaced for review.

## 10. Verification

A syntactically valid Page JSON is not automatically trusted.

Each item and page must carry an explicit status:

- `VERIFIED`
- `VERIFIED_WITH_NOTES`
- `NEEDS_REVIEW`
- `BLOCKED`

Verification notes must localize uncertainty.

A confidence number alone is not sufficient evidence.

If the user challenges an extraction, re-inspect the source. Do not defend previous output merely because it was produced earlier.

## 11. Output contract

Each completed page produces exactly one Page JSON.

The machine contract is defined in:

`src/business_brief/contracts.py`

The Markdown defines how the role works. The Python contract defines the exact output structure.

The new asset schema is `page-ingest-v4`, serialized by `PageIngestV4` / `PageItemV4`, producer `ingestor-v2.2-chat`, instruction `2.2` (§21). v2/v3 remain immutable compatibility contracts. The v4 writer rollout and page-2 acceptance are recorded in §21.6; corpus acceptance remains qualified by CURRENT_STATE/F011.

Do not invent additional fields outside the contract unless the contract is being deliberately revised.

A page is not complete merely because its JSON appears in Chat. The canonical Page JSON must be durably persisted.

## 12. Persistence contract

The canonical Page JSON artifact belongs in Supabase Storage.

Canonical logical object key:

```
page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.2/page-<NNNN>.json
```

Example:

```
page-ingest/the-wall-street-journal/2026-10-14/<source_sha256>/ingestor-v2.2/page-0001.json
```

The canonical architecture uses the existing private `page-ingest` bucket; runtime configuration must agree. The bridge resolves the configured artifact bucket server-side and returns it in the verified receipt; Chat must not invent a bucket name. The normative bridge contract is section 19; implementation/runtime notes are in `bridge/README.md`.

The stored file contains the validated `page-ingest-v4` payload for exactly one source page.

For the same source SHA, Ingestor generation and page number, persistence must be deterministic. A rerun must not silently create a second competing canonical artifact.

PostgreSQL is the operational index, not the primary home of the JSON body. When an implemented operational index exists, it should record source/edition identity, page number, schema version, Ingestor version, Storage key, verification status, artifact hash and timestamps.

Do not create a new database table from Chat unless that table is already part of the implemented system or an explicit schema change is requested.

A successful page pass ends as:

```
interpret page
→ build page-ingest-v4
→ validate structure
→ verify every asset crop through the gated writer (§21)
→ persist JSON to Supabase Storage
→ verify durable write
→ report Storage key and page status
→ STOP
```

If persistence fails, the page is not complete. Report the failure and stop. A persisted NEEDS_REVIEW artifact remains review-required, not a completed verified pass; BLOCKED payloads are not canonical writes (section 19).

## 13. Handoff to Assembler

The Page JSON must contain enough page-level truth that Assembler can:

- identify candidate parts of the same article across pages;
- join text in source order;
- preserve provenance;
- detect unresolved ambiguity;
- refuse unsafe assembly when review is required.

Assembler should combine page-level truth.

It should not rediscover page layout.

## 14. Non-goals

Ingestor v2.2 is not:

- Technician;
- OCR preparation;
- Physical Map generator;
- autonomous API page mapper;
- multi-page article assembler;
- cross-publication Composer;
- Translator;
- Assignment Editor;
- Brief writer.

## 15. Legacy

Ingestor v1.1 = `ingestor-v4-physical-map-v1.1`.

Its production role and Physical Map handoff are superseded by D014.

Physical Map, Visual Page Map, BODY_FLOW, bbox/overlap matching and block-ID experiments may remain as historical/debug material only.

## 16. Success criterion

Ingestor v2.2 succeeds when:

- the source page has been inspected as a whole;
- relevant editorial items are faithfully represented;
- text is verified against source evidence;
- uncertainty is explicit;
- continuation evidence is preserved;
- output matches `page-ingest-v4`;
- Assembler can proceed without reinterpreting page layout.


## 17. Chat bootstrap protocol

A fresh Chat must not rely on old conversation context. Before processing a page, it reconstructs the Ingestor role from the repository and the operational Source of Truth.

Bootstrap sequence:

1. Load the Business Brief v4 project through `PROJECT.md`.
2. Read `project-memory/SCOPE.md`.
3. Read `project-memory/CURRENT_STATE.md`.
4. Read this file, `docs/INGESTOR.md`.
5. Read the current Page JSON contract in `src/business_brief/contracts.py`.
6. Resolve the requested publication edition in the operational Source of Truth.
7. Confirm that the selected source is authorized for ingestion and locate its Technician Source Bundle.
8. Resolve the requested page image and supporting prepared text/OCR evidence.
9. Run exactly one page pass according to the rules above.
10. Validate the resulting `page-ingest-v4` payload.
11. Persist it according to section 12.
12. Confirm the durable Storage object key and page status.
13. State any unresolved uncertainty briefly and stop.

A convenient user invocation is:

```
INGESTOR v2.2: process page <N> of <publication/edition>.
```

For example:

```
INGESTOR v2.2: process page 1 of the current READY_FOR_INGESTOR WSJ edition.
```

That short invocation does not replace the bootstrap sequence. It merely selects the source page to process.

## 18. Operational lookup rules

When locating the actual source and artifacts, live operational state has priority over stale Markdown.

Before page interpretation begins, the Chat must establish:

- publication;
- edition date and variant;
- source ID;
- Technician readiness state;
- Source Bundle identity;
- requested page number;
- page image/evidence belonging to that exact source.

If the edition, bundle or page cannot be resolved safely, the run is BLOCKED. Do not guess or silently substitute another source.

## 19. Ingestor Access Bridge — normative HTTP contract v1

**Status (2026-10-16): v1 transport and v3 body/generation extension deployed; earlier ordinary Chat image + inline OCR acceptance passed, and one v3 page-1 production persist through the connected plugin passed with exact readback. See §20 for execution surface and limits.** This section is the single authority for the bridge wire contract. `contracts.py` remains the authority for the Page JSON body. The original contract decision was documentation-only; the subsequent standalone implementation is documented in `bridge/README.md`.

The bridge resolves operational identity, authorizes artifact access, validates one submitted Page JSON and persists it. It performs **no editorial interpretation**, OCR, text repair, relevance judgment, page assembly, model calls or automatic next-page processing. `STORED` attests persistence, not independent verification of editorial truth.

### 19.1 Transport, authorization and common types

- HTTPS only. Every endpoint requires `Authorization: Bearer <bridge_access_token>`. This is a dedicated, high-entropy, revocable bridge credential, never a Supabase secret/service-role key. Server-side credential configuration binds a principal to publication IDs and `source:read` and/or `page:write` scopes. Each request checks both scope and publication authorization, including UUID routes. No authorization from user-editable metadata.
- GET requires `source:read`; POST requires both scopes. Missing/invalid credentials return 401; insufficient scope returns 403. A source/publication outside the principal's allowlist is indistinguishable from an unknown resource (404).
- Supabase credentials stay in server secret storage. Source and output buckets remain private and are explicit deployment configuration (`source_bucket`, `page_ingest_bucket`); absence is 503 `CONFIGURATION_MISSING`. No public buckets, arbitrary object browsing, client-selected buckets/keys, upload URLs or direct client writes.
- JSON responses use `Content-Type: application/json`, `Cache-Control: no-store` and server-generated `X-Request-ID` matching `request_id` in the body. POST requires `Content-Type: application/json`; request body maximum is 5 MiB UTF-8, uncompressed. Reject duplicate JSON keys, invalid UTF-8, NaN/Infinity and trailing content. Unknown fields/query parameters are rejected. Errors never echo tokens, signed URLs, source text or internal exception traces.
- All fields described below are required unless explicitly optional. `null` is allowed only where stated. `UUID` means canonical UUID string; `SHA` is 64 lowercase hexadecimal characters; `Timestamp` is RFC3339 UTC ending in `Z`; `Date` is valid `YYYY-MM-DD`; `page_no` is a 1-based integer, never a boolean, at most 9999. `publication_id` is the canonical `publications.publication_id` slug, not its database UUID. Strings are not silently trimmed or rewritten.
- `SourceIdentity` is exactly `{source_id: UUID, source_sha256: SHA, publication_id: string, canonical_name: string, edition_id: UUID, edition_date: Date, edition_variant: string, page_count: integer, technician_version: string, source_bundle_schema: "source-bundle-v4", source_bundle_sha256: SHA, readiness: "READY_FOR_INGESTOR"}`. `page_count` is positive. `source_bundle_sha256` hashes the exact archived manifest bytes, not reserialized JSON.
- `ArtifactAccess` is exactly `{bucket: string, storage_key: string, media_type: string, sha256: SHA, byte_size: integer, url: string, expires_at: Timestamp}`. Byte size is positive. URLs are read-only HTTPS signed URLs for that exact artifact, fixed TTL 300 seconds from issuance. No transformation or wildcard access. The client checks expiry and downloaded SHA. A renewed GET reauthorizes and returns fresh URLs; expiry alone does not invalidate source identity.

Signed URLs are bearer capabilities: redact them in logs and never persist them in Page JSON. Their validity can outlive revocation of the bridge credential until expiry. An authenticated streaming proxy is an allowable future transport only after an explicit wire-contract revision; v1 returns signed URLs. See [Supabase private downloads](https://supabase.com/docs/guides/storage/serving/downloads) and [Storage access control](https://supabase.com/docs/guides/storage/security/access-control).

### 19.2 Source and bundle identity invariant

For every GET and POST the bridge joins `sources.id` → `sources.edition_id` → `editions.id` → `publications.id`, and `sources.blob_id` → `source_blobs.id`. It requires live `sources.status = READY_FOR_INGESTOR`, `editions.active_source_id = sources.id`, matching contract/version, and a downloadable, structurally valid archived manifest at `sources.source_bundle_path` in the configured source bucket.

Validate manifest publication slug/name, date, variant, SHA, page count and Technician version against those rows. `source_sha256` comes from `source_blobs.sha256`. **The current Technician manifest `source_id` is `sha256:<digest>`, whereas API/Page JSON `source.source_id` is `sources.id` (UUID).** Validate that explicit mapping; never compare the two strings as equal, change the immutable manifest, or infer a database source solely from a filename/hash. Unsupported future manifest identity formats are `BUNDLE_INVALID` until deliberately supported.

Validate manifest `status`, `schema_version`, `original_path`, `prepared_pdf_path`, `ocr.prepared_pdf_path`, `ocr.prepared_sha256`, `page_images`, and parts against `SourceBundle` in `contracts.py`. Exactly one image must exist for every integer page 1..page_count, with positive dimensions and hashes. Prepared path must equal the OCR prepared path; OCR page numbers and part ranges must be in bounds. Resolve only manifest-listed objects under the selected manifest's archive prefix; reject traversal, absolute paths, URL paths and cross-prefix references. The original SHA must equal the blob SHA. Prepared may legitimately be the original PDF when OCR was unnecessary. Metadata listing alone is not proof of downloadable content: hash-check the bytes of the manifest and artifacts offered to the caller, with verified immutable-content caching allowed.

The bridge pins each operation to source UUID, blob SHA, edition, Technician version, manifest key and manifest SHA. It must detect changes before issuing access or committing a write (409 `SOURCE_CHANGED`). It never switches to a newer source during the operation. POST eligibility and identity checks must be serialized with changes to source readiness/active-source/bundle mapping; the implementation must provide a shared locking or equivalent fencing protocol with those changes. A check followed by an unguarded write is insufficient. No long-lived read URL is a write authorization.

### 19.3 GET /ingestor-v2/source/current?publication=...

Request: no body; exactly one required query parameter `publication`, the canonical publication slug (for example `the-wall-street-journal`). Aliases such as `WSJ` are not accepted. No implicit date, timezone, variant or filename guessing.

Selection: within the authorized publication, choose the maximum `edition_date` among editions with a non-null active source. Do not fall back to an older READY edition if the newest active edition is not ready. If that maximum date has multiple variants/editions, return 409 `SOURCE_AMBIGUOUS`; v1 never silently prefers `default`. Require its unique active source to satisfy 19.2. Duplicate/inconsistent mappings are blocked, never resolved with `LIMIT 1` or arrival timestamps. No active edition is 404 `SOURCE_NOT_FOUND`; latest active source not READY is 409 `SOURCE_NOT_READY`.

200 response (exact shape):

```text
{contract_version: "ingestor-access-v1", request_id: UUID,
 status: "READY", selection: {publication: string, rule: "latest-active-edition-date-unique"},
 source: SourceIdentity}
```

This selects the current *available active edition*, not a promise that today's newspaper has arrived. The Chat reports the returned edition date and variant and pins the source UUID/SHA before requesting a page. An explicitly requested different date must not be substituted with this endpoint's result.

### 19.4 GET /ingestor-v2/source/<source_id>/page/<page_no>

Request: no body/query; UUID source and decimal integer page in path. Resolve the exact source using 19.2, never `current` again. Out-of-range page is 404 `PAGE_NOT_FOUND`; malformed UUID/page syntax is 400 `INVALID_REQUEST`.

200 response (exact shape):

```text
{contract_version: "ingestor-access-v1", request_id: UUID, status: "READY",
 source: SourceIdentity, page_no: integer,
 manifest: ArtifactAccess,
 page_image: {artifact: ArtifactAccess, width_px: integer, height_px: integer},
 prepared_evidence: {artifact: ArtifactAccess, pdf_page_no: integer, ocr: OcrInfo},
 original_pdf: ArtifactAccess}
```

`OcrInfo` has exactly the serialized fields of `contracts.py`: `mode:string`, `required:boolean`, `performed:boolean`, `engine:string|null`, `languages:string|null`, `pages_requiring_ocr:integer[]`, `prepared_pdf_path:string`, `prepared_sha256:SHA`. Paths are archived keys, not temporary workspace paths. `pdf_page_no = page_no` in the whole prepared PDF. `manifest` media type is `application/json`; image is `image/png`; prepared/original are `application/pdf`. v1 always supplies the original as an available fallback authority; it may share the prepared artifact when identical. It does not fabricate a separate text sidecar or require Physical Map. The Chat opens the exact PDF page to inspect the prepared text layer; whole-PDF access is evidence access, not authorization to process more pages.

All required artifact access is issued together or the request fails as BLOCKED. Missing or corrupt evidence cannot be replaced by previous model output. The Chat compares the response UUID, SHA, manifest SHA and edition to the pinned selection; mismatch requires stopping and explicit reselection, not automatic retry against another source.

### 19.5 POST /ingestor-v2/page

Required header: `Idempotency-Key: <UUID>`, newly generated per intended submission; preserve it across transport retries. No query parameters. Request body is exactly:

```text
{contract_version: "ingestor-access-v1", source_bundle_sha256: SHA,
 page: PageIngest.to_dict()}
```

The wrapper is transport metadata and is never stored in the canonical artifact. The manifest hash must match the pinned current archived bundle; mismatch is 409 `SOURCE_CHANGED`. `page.source.source_id` selects the exact database source. Apply 19.2 again and require all Page JSON source/publication/date/variant/name/page identity to match, with page within range. The caller cannot set the persistence key or producer generation directory.

Strict Page JSON validation is a bridge requirement, **not an existing dataclass runtime validator**. `PageIngest.to_dict()` defines the field names and nesting, not the Python constructor names: top-level fields are exactly `schema_version`, `producer`, `instruction_version`, `source`, `publication`, `items`, `page_status`, `page_notes`. Accept exactly one generation tuple: (`page-ingest-v2`, `ingestor-v2.0-chat`, `2.0`) or (`page-ingest-v3`, `ingestor-v2.1-chat`, `2.1`) or (`page-ingest-v4`, `ingestor-v2.2-chat`, `2.2`). Mixed tuples are invalid. `source` is exactly `{source_id:UUID, source_sha256:SHA}`; `publication` is exactly `{publication_id:string, canonical_name:string, edition_date:Date, edition_variant:string, page_no:integer}`.

Legacy v2 items have exactly the fields/types serialized by `PageItem.to_dict()`: nonempty unique `page_item_id` and nonempty `item_type`; nullable strings `title`, `subtitle`, `kicker`, `byline`, `text_on_page`; required `relevance`, `perspective`, `continuation`, `verification`. Arrays are JSON arrays, never Python tuples. `relevance` requires state `relevant|irrelevant|uncertain` and a nonempty reason. `perspective` requires all nullable scalar fields, list fields and epistemic arrays defined in `PerspectiveEvidence`; specifically `author_question`, `framing`, `central_argument`, `distinctive_angle` are string|null, and `tensions_or_counterarguments`, `open_questions`, `observed_on_page`, `interpreted_from_page`, `unresolved_until_assembly` are string arrays. `continuation` requires three booleans and nullable strings `continuation_marker` and `continuation_target` exactly as `ContinuationEvidence`. `verification` requires `status`, the boolean fields `visual_checked`, `text_layer_checked`, `title_verified`, `boundaries_verified`, `reading_order_verified`, `text_on_page_complete`, plus `byline_verified:boolean|null`, and `notes:string[]`. No omitted defaults or extra fields at any level within the selected generation. `page_notes` is a string array; `items` may be empty for an explicitly verified page with no editorial items, with explanatory page notes.

For v4, the same minimal fields plus required `assets` are specified in §21; nonempty-assets writes use the implemented writer and acceptance gates there. For v3, `PageItemV3.to_dict()` has the same fields except `perspective` is absent (and rejected as an extra field). All identity, relevance, continuation and verification checks remain unchanged. `subtitle` carries dek/subtitle/perex; absent source metadata is null, never invented. Empty selected-item pages require explanatory page notes. Omitted irrelevant items do not make selected-article text incomplete.

All integers in this contract reject booleans and fractional values. Validation order is authentication/scope/resource authorization, syntax/shape, live source and bundle identity, page verification consistency, idempotency binding and canonical write. Identity mismatch is 409 `IDENTITY_MISMATCH`; invalid Page JSON types/enums/fields are 422 `PAGE_SCHEMA_INVALID`.

Both page/item statuses use `VERIFIED|VERIFIED_WITH_NOTES|NEEDS_REVIEW|BLOCKED`. A BLOCKED page or item is rejected with 409 `PAGE_BLOCKED`, without canonical write. A NEEDS_REVIEW page may be stored with `usable_for_assembly:false`, and is not a successfully completed verified page pass. Page status must not conceal a worse item status: VERIFIED permits only VERIFIED items; VERIFIED_WITH_NOTES permits VERIFIED/VERIFIED_WITH_NOTES; NEEDS_REVIEW permits any non-BLOCKED item. Non-VERIFIED page/item states require localized nonempty notes. For verified items require visual, text-layer, boundaries and reading-order checks true; require title check when title exists, byline check true when byline exists (null when absent), and complete nonempty text for relevant/uncertain items. Clearly irrelevant items may omit body text and completeness; the bridge preserves this exception. Verified pages must have no unresolved failed required checks. These are mechanical consistency checks of the caller's assertions; the bridge never decides whether prose, relevance or perspective is correct.

### 19.6 Canonical write, hashing and idempotency

Serialize the validated `page` only using RFC 8785 JSON Canonicalization Scheme (JCS), UTF-8, no BOM or trailing newline, no Unicode normalization. SHA-256 of those exact bytes is `artifact_sha256`. Object key is derived server-side:

```text
page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.0/page-<NNNN>.json
```

`NNNN` is zero-padded to four digits. Slugs/date/SHA are validated identity values, not raw path input. The server maps v2 to directory `ingestor-v2.0` and v3 to `ingestor-v2.1`, and v4 to `ingestor-v2.2`; callers cannot choose arbitrary directories. The example above is the legacy v2 key. New v3 keys use `ingestor-v2.1` in the same position. All supported page generations use the same fencing, create-if-absent, hashing, binding and readback algorithm. No variant component is added; if the same key would represent different variant/source UUID identity, refuse with 409 rather than changing this canonical path.

- Atomically create-if-absent, content type `application/json`; never blind upsert/overwrite. Concurrent losers read and compare the winning object. Same canonical bytes/identity → safe replay; different content/identity → 409 `CANONICAL_CONFLICT`, preserving existing bytes. Different idempotency keys cannot bypass this rule. Revised editorial output needs a separately authorized future revision protocol; v1 provides none.
- Durably bind `(principal, Idempotency-Key)` to SHA-256 of JCS of the whole request wrapper and target key, atomically claiming it before mutation. Reuse for a different wrapper/target is 409 `IDEMPOTENCY_CONFLICT`. Keep binding for the lifetime of the canonical artifact; do not allow short TTL eviction to permit key reuse. This requires durable operational storage chosen during implementation, not a new table improvised by Chat. Concurrent identical requests may wait or return retryable 503 `WRITE_IN_PROGRESS`.
- After creation or replay, download the stored bytes through Storage, hash them, parse/validate identity and compare exact canonical bytes. Storage metadata, ETag, an upload receipt or listing alone is insufficient. Existing non-JCS/different bytes are a conflict even if JSON is semantically similar. Unreadable or mismatched readback is 503 `PERSISTENCE_UNVERIFIED`; never return STORED. An object may already exist after timeout; retry the same request/key to reconcile, never delete or overwrite it automatically.
- Recheck/fence source eligibility through commit as required by 19.2. Do not modify Technician readiness, active source, source bundle or original. No distributed DB/Storage transaction is assumed. The implementation must recover interrupted claims and writes by readback; any optional index is repairable from verified artifacts and must not falsely mark a page complete.

201 for new object, 200 for verified replay, exact response shape:

```text
{contract_version: "ingestor-access-v1", request_id: UUID, status: "STORED",
 disposition: "CREATED"|"REPLAYED", idempotency_key: UUID,
 source: SourceIdentity, page_no: integer, page_status: PageStatus,
 usable_for_assembly: boolean,
 artifact: {bucket: string, storage_key: string, media_type: "application/json",
            artifact_sha256: SHA, byte_size: integer, serialization: "RFC8785-JCS"},
 verification: {status: "VERIFIED", method: "storage-download-sha256-and-identity",
                stored_sha256: SHA, identity_matches: true, verified_at: Timestamp}}
```

`stored_sha256 = artifact_sha256`; `usable_for_assembly` is true only for VERIFIED/VERIFIED_WITH_NOTES pages. `disposition` reflects this attempt, not a cached earlier 201 response. The Chat reports key, artifact hash, persistence verification and page status, then STOP. NEEDS_REVIEW remains review-required. Storage verification never upgrades the page's editorial status.

### 19.7 Error/status model

Every failure uses this exact envelope; no partial success or HTTP 200 BLOCKED:

```text
{contract_version: "ingestor-access-v1", request_id: UUID, status: "BLOCKED",
 error: {code: string, message: string, retryable: boolean,
         persistence: "NOT_WRITTEN"|"UNKNOWN"|"EXISTING_UNCHANGED",
         details: [{path: string, reason: string}]}}
```

`details` may be empty; paths are JSON pointers or parameter names and contain no submitted text/secrets. `status` is the operation outcome, distinct from source readiness, page status and Storage verification. BLOCKED in this envelope is not a new database source state.

| HTTP | Codes | Retry policy |
| --- | --- | --- |
| 400 | INVALID_REQUEST, INVALID_JSON | Correct request; no write. |
| 401 / 403 | UNAUTHENTICATED / FORBIDDEN | Fix credential/scope; no write. |
| 404 | SOURCE_NOT_FOUND, PAGE_NOT_FOUND | Resolve authorized identity; no write. |
| 409 | SOURCE_AMBIGUOUS, SOURCE_NOT_READY, SOURCE_CHANGED, BUNDLE_INVALID, ARTIFACT_MISSING, ARTIFACT_HASH_MISMATCH, IDENTITY_MISMATCH, PAGE_BLOCKED | Resolve evidence/state explicitly; no automatic source substitution. |
| 409 | CANONICAL_CONFLICT, IDEMPOTENCY_CONFLICT | Existing object/binding unchanged; manual resolution, no overwrite. |
| 413 / 415 | PAYLOAD_TOO_LARGE / UNSUPPORTED_MEDIA_TYPE | Correct request; no write. |
| 422 | PAGE_SCHEMA_INVALID, PAGE_VERIFICATION_INVALID | Correct schema/check consistency; no write. |
| 429 | RATE_LIMITED | Retry same request after Retry-After. |
| 503 | CONFIGURATION_MISSING, UPSTREAM_UNAVAILABLE, WRITE_IN_PROGRESS, PERSISTENCE_UNVERIFIED | Stop page pass; infrastructure recovery or bounded retry. |
| 500 | INTERNAL_ERROR | Stop; correlate request_id, no blind fresh submission. |

Only RATE_LIMITED, UPSTREAM_UNAVAILABLE, WRITE_IN_PROGRESS and PERSISTENCE_UNVERIFIED have `retryable:true`; return `Retry-After` seconds. All other codes have false. `persistence` is NOT_WRITTEN when this attempt definitively did not mutate canonical Storage, EXISTING_UNCHANGED for detected canonical conflicts/replays that fail eligibility, and UNKNOWN whenever write completion/readback cannot be established. Do not claim rollback on failure. Idempotency bindings may exist even when canonical persistence is NOT_WRITTEN. Transport failure without a response is treated as UNKNOWN by the client.

### 19.8 Implementation acceptance gate

Before enabling the first real page, prove authenticated access from the actual Chat integration, private artifact downloads and hash checks, UUID/hash manifest mapping, latest-edition and variant ambiguity behavior, stale/non-ready source rejection and fenced state changes, strict body validation, missing/corrupt evidence handling, identical replay, different-content conflict, concurrent create, reused-key conflict, and recovery after upload/readback timeout. Confirm credentials/URLs are redacted and canonical bytes are re-downloadable. Use one requested page only and STOP; no paid editorial batch, legacy Ingestor resurrection or Assembler implementation is implied.


## 20. Ordinary Chat evidence adapter and rollout

Daily ingestion runs in ordinary Chat through the Business Brief Ingestor plugin:
`resolve_current_source` → `get_page_evidence` (image + OCR) → visually validated relevant-article extraction → validate → persist → STOP.
Codex is for programming, system changes and debugging. It is not the daily ingest execution surface.

The private/only-me Site v4 is https://business-brief-ingestor.satinyloom128.chatgpt.site/ . This adapter is distinct from the Railway HTTP bridge and its signed-artifact wire responses (§19); signed URLs/tokens stay server-side and never reach the model.

Site v3 added server-side page PNG fetch, SHA/identity validation and MCP image content. Site v4 added extraction from the prepared OCR PDF with `unpdf 1.9.0` / PDF.js `6.4.299`, only the requested `pdf_page_no`, PDF limit 24 MiB and extracted text limit 256 KiB, secret sanitization and provenance metadata. Its reported tests cover page isolation, UTF-8, failure, mismatch and no secret leakage. Site adapter source/tests are external to this repository; these are acceptance facts supplied for consolidation, not tests rerun here.

Ordinary Chat read acceptance returned WSJ 2026-10-14 page 1 image 1190×1684 and OCR 14,349 UTF-8 bytes, no warnings or URLs/tokens. Read evidence is therefore verified in ordinary Chat, beyond the earlier Codex HTTPS test. Technical v2 production persistence also passed; its content is superseded (canonical acceptance identity in HISTORY).

Rollout completed on 2026-10-16: bridge commit `1442da050a0b3dcb4a5de9a11611a2b5ec9084c9`, Railway deployment `7d1fa8aa-401d-4a2c-8fe0-5a4804eeb029`, SUCCESS/Online, 1/1 replica. Site v4 (source `5ad1e400d4a8b2a47f73e60de4b98a33a087dd81`, deployment `appgdep_6ad25784d0308191bc1dcdb6869c7145`) is still owner-only. Its write schema and implementation already transport the new page body unchanged, leaving validation to Railway; a mocked transport check confirmed v3 body/idempotency/receipt preservation. No Site change or deployment was needed; read tools were unchanged.

After deployment the connected plugin resolved the exact WSJ 2026-10-14 source and returned page 1 PNG + OCR (14,349 UTF-8 bytes, no warnings). Six relevant article starts were visually compared, locally validated and submitted once with a fresh UUID. Result: STORED/CREATED, VERIFIED_WITH_NOTES, `ingestor-v2.1/page-0001.json`, SHA `bc287714ea5a290833976b7dfec6caf56f09a668e2c0d401c9e317ac246055e6`, 14,568 B, downloaded SHA/identity match, usable_for_assembly=true. Notes preserve visible page-boundary fragments; no off-page text was supplied. Full identity/key is in HISTORY. This pass used Codex's connected MCP plugin, the ordinary-Chat-compatible path; it does not claim a newly observed separate ordinary Chat session. Earlier ordinary Chat read acceptance remains valid historical evidence. Current role instructions are this document plus PROJECT/SCOPE/CURRENT_STATE; the Site performs transport only.

Do not silently convert/rewrite v2 or reuse its idempotency key. Start a fresh submission/key in the new generation; preserve all v2 bytes/bindings. Downstream must select an explicit accepted generation, never mix or automatically fall back to the superseded page. STOP after page 1 was observed; no page 2 or assembly. Full suite: 138 passed; bridge tests: 88 passed. Railway health overview reported Online, no failures or pending work; authenticated resolve/evidence succeeded. The authenticated /health and /ready diagnostic endpoints were not independently called in this rollout.

## 21. Article assets — instruction 2.2 / page-ingest-v4 (D022)

**Text se rekonstruuje. Vizuální artefakty se nepřepisují, ale uchovávají.**

This section extends §19 for the exact tuple `page-ingest-v4` / `ingestor-v2.2-chat` / `2.2`, with server-selected directory `ingestor-v2.2`. v2 and v3 field sets, bytes and keys remain unchanged and readable. Never add assets to existing immutable v3 objects, including production pages 1 and 2. Use a fresh intended-submission key in v4 after a separately authorized rollout. Do not infer rollout readiness from this document or a valid schema.

### 21.1 Prose and visual evidence

`PageItemV4` retains the minimal v3 fields (title, subtitle/dek/perex, kicker, byline, source-faithful `text_on_page`, relevance reason, continuation, verification) and adds required `assets: ArticleAsset[]`, empty when no associated visuals exist. There is no PerspectiveEvidence field and no mandatory inventory of irrelevant items. `text_on_page` is continuous article prose, visually checked against the authoritative page. Do not insert chart/table OCR, axis labels, legends, synthesized descriptions, image placeholders or captions into canonical prose. Preserve paragraphs as `\n\n` boundaries. Source-visible visual titles/captions belong on the asset. A separately selected prose sidebar remains an editorial item; do not misclassify prose as a visual merely to avoid reconstructing it.

An asset is primarily a PNG crop of the exact authoritative Technician page PNG, including the visual's axes/legend/source notes where applicable and excluding neighboring article prose. Never redraw, resample or reconstruct the visual from extracted numbers. Internal OCR may be an optional future derivative, never required, authoritative, or a substitute for the crop. No OCR field is required in this contract.

### 21.2 Exact asset shape and validation

`ArticleAsset.to_dict()` defines all keys below. Optional title/caption/bbox/index/text are represented by null, not omitted; unknown keys are rejected. Asset IDs are lower-case hyphenated slugs, unique across the page and chosen with page/item context, for example `p0002-a02-chart-01`. They do not encode a new article identity.

| Field | Contract |
| --- | --- |
| `asset_id` | Nonempty path-safe slug; no slash, dot, percent escape or traversal. |
| `asset_type` | `chart`, `table`, `photo`, `infographic`, `illustration`, `other`. |
| `page_item_id`, `page_no` | Exact owning enclosing item and source page; asset cannot point to another item/page. |
| `page_anchor` | Exactly `bbox_norm`, `bbox_px`, `source_page_image_sha256`. |
| `text_anchor` | Exactly `position`, `paragraph_index`, `anchor_text`, `status`. |
| `title`, `caption` | Nullable strings, source-visible and visually verified; never inferred interpretations. |
| `artifact` | Exactly `bucket`, `key`, `media_type`, `sha256`, `byte_size`, `width`, `height`. |
| `verification` | Exactly `status`, `visual_checked`, `ownership_verified`, `page_anchor_verified`, `text_anchor_verified`, `notes`. |

`bbox_norm = [x0,y0,x1,y1]` uses the full authoritative PNG, origin top-left, x right, y down. All numbers must be finite, not booleans, in 0..1, with x0<x1 and y0<y1. Optional `bbox_px` uses integer half-open crop bounds in the same unrotated PNG. At crop production the writer derives `[floor(x0*W),floor(y0*H),ceil(x1*W),ceil(y1*H)]`, verifies any supplied pixel bbox against it and source dimensions, and records exact crop width/height; no resizing. This rounding is the sole permitted geometric expansion. `source_page_image_sha256` binds the crop to the exact manifest-listed source PNG. Shape validation alone cannot prove a crop came from that PNG.

Client submission is validated explicitly with `page_schema(..., submission=True)`: `artifact` may be **null** (server-produced metadata) or a complete exact expected artifact. Mixed/partially-null artifact objects are rejected. There are no client image bytes or URLs. Persisted Page JSON uses the default strict `page_schema` and never permits null artifacts. Any supplied complete artifact must equal the server crop result exactly; mismatches return 409 ASSET_ARTIFACT_MISMATCH before writes. The server fills bbox_px when null and exact final artifact metadata after readback.

`artifact.media_type` is `image/png`; SHA is lower-case 64-hex SHA-256 of exact crop bytes, size/width/height are positive integers. If pixel bbox is provided, its extent must equal artifact dimensions. `bucket` must equal the bridge's configured private `page-ingest` output bucket at write time; clients never select an alternative bucket. `key` must equal the canonical server derivation (§21.4), not an arbitrary reference or signed URL.

`verification.status` uses the existing four PageStatus values. The four checks are booleans; notes are strings. VERIFIED / VERIFIED_WITH_NOTES requires all four checks true and anchored placement. A worse asset status must propagate through item and page status; non-VERIFIED states require localized nonempty notes. BLOCKED anywhere prevents canonical page persistence. A placement review requires asset NEEDS_REVIEW, `text_anchor_verified:false`, item/page NEEDS_REVIEW and explanatory notes, keeping `usable_for_assembly:false`. Never mark an unresolved anchor as VERIFIED_WITH_NOTES.

### 21.3 Logical placement and assembly

`position` is `before_paragraph`, `after_paragraph` or `inline_after_anchor`. For paragraph placement, `anchor_text` is an exact source substring within the target paragraph; for inline placement the insertion follows that substring. Paragraph indices are zero-based within the page item's double-newline-delimited `text_on_page`, optional and auxiliary. When supplied on an anchored page asset they must identify the paragraph containing the anchor. `anchor_text` is more authoritative and supports later re-anchoring; it is not an OCR string copied from inside the visual.

`status` is `anchored` or `placement_needs_review`. Anchored placement requires nonempty anchor text occurring exactly once in current item prose. Missing or repeated matches, missing prose or cross-paragraph phrases cannot be silently accepted as anchored. In review state the index and anchor text may be null; keep the physical crop and ownership evidence without inventing a position. A repeated phrase may remain recorded for review.

Assembler selects one explicitly accepted source/generation, joins article prose across pages and resolves continuation identity first. It then finds each asset's anchor in the assembled article; paragraph indices may have shifted. Only a unique supported text match yields placement. Missing or multiple matches remain `placement_needs_review` / unplaced, with original asset ID, ownership, anchor evidence, page bbox and PNG SHA retained. Neither geometric proximity, a stale index nor fuzzy matching may silently decide placement. Assembler does not rewrite source Page JSON or move/rename crops. Ordered assets sharing an insertion point require explicit ordering/review before placement; array order alone is not inferred source order.

### 21.4 Canonical storage and required write semantics

Use the **existing private bucket `page-ingest`**, with the same retention/lifecycle and authorization boundary as Page JSON. No new bucket is required: crops belong to the same immutable source/generation and must survive as long as any referencing Page JSON. The bucket name and the first key component happen to be equal; do not strip that prefix.

```text
bucket: page-ingest
keys:
  page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.2/page-<NNNN>.json
  page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.2/assets/page-<NNNN>/<asset_id>.png
```

Before enabling asset persistence, the bridge writer must:

1. Authenticate existing scopes/publication allowlist and pin source UUID/SHA, bundle SHA, readiness, page PNG SHA and dimensions. Derive bucket/key server-side from validated identity/generation/asset ID. Reject variant/UUID collisions with the existing no-variant namespace.
2. Produce/verify the crop from manifest-listed authoritative PNG bytes, not an arbitrary client image. Verify normalized/pixel bounds, PNG media type, width/height, exact byte size and SHA. Keep visual ownership/meaning verification with Ingestor; server checks cannot establish editorial truth.
3. Bind each intended write durably to request bytes, target and source identity before mutation. Apply the existing session/row fence and crash-surviving PENDING identity guards across create/readback. Binary bytes use direct SHA-256, not JCS; JSON metadata/requests retain RFC8785 JCS.
4. Create-if-absent as `image/png` with no overwrite. Download exact bytes and compare SHA, size, dimensions and source binding on new write and replay. Same bytes/identity replay; different bytes/identity conflict (409). Never replace, delete or silently rename a conflicting crop.
5. Verify every asset and recheck source eligibility through Page JSON commit. Persist Page JSON only after all referenced crops pass durable readback. Page-level STORED must cover the whole referenced set, not merely the JSON. No DB/Storage atomic transaction is assumed: a partial failure may leave immutable orphan crops. Return BLOCKED/UNKNOWN, preserve claims and reconcile with the original request/key; never delete artifacts or advance the page to recover.

Reuse §19 auth, idempotency retention, source fencing, no-overwrite, logging/redaction and conflict/recovery rules. Do not introduce client-chosen paths, bucket credentials, public URLs or a direct Chat-to-Storage bypass. Audit asset ID, parent page/item, PNG SHA, bounds, derived key, byte SHA and readback outcome without source text or secrets. Corrections require a separately authorized future revision protocol, not mutable replacement under v4.

### 21.5 Implemented writer and rollout gate

`POST /ingestor-v2/page` accepts text-only v4 submissions through the existing generic Site/plugin tool. The bridge downloads only the manifest-listed source PNG, verifies its SHA/dimensions, derives the exact §21.2 bbox, and produces RGBA8 PNGs without resampling. Encoding uses filter 0 and explicit stored DEFLATE blocks (no encoder-version-dependent compression), one IHDR/IDAT/IEND; inherited ancillary metadata is excluded and palette transparency is preserved by RGBA conversion. PNG decoding is pinned to Pillow 12.0.0. Limits: source/crop 32 MiB, 40 million source pixels, 32 assets and 64 MiB crop bytes per page; animated/non-PNG sources are rejected. Source and crop downloads are bounded streams.

The existing private bindings table needs no migration. In addition to the principal/request-key binding to original RFC8785 submission bytes, every v4 target reserves `@asset-set-v4` / UUIDv5(NAMESPACE_URL, `business-brief:asset-set-v1:` + page key). Its SHA binds the complete original wrapper, authoritative source identity (including UUID/variant/bundle SHA), and deterministic final artifact metadata. The namespace is reserved from configured auth principals. Both claims commit PENDING before any Storage mutation. The target advisory lock and edition/source/blob/publication row locks span all crop writes/readbacks and Page JSON write/readback. Existing pending guards survive session loss. An empty-assets submission cannot bypass a partially written asset set.

Each crop is uploaded create-if-absent as image/png and exact downloaded bytes, SHA/size/dimensions are checked before the JSON can be written. STORED and VERIFIED binding states are committed only after JSON readback too. Receipt includes `assets` with final metadata and verification for nonempty sets; v2/v3 receipts are unchanged. Retry the **original submission and same key**, including artifact:null when originally submitted. Never substitute the enriched persisted page on retry. Identical new-key replay also works for identical submissions; altered request under the same key is IDEMPOTENCY_CONFLICT. Altered v4 intended target/source/set is ASSET_SET_CONFLICT; existing different crop bytes are ASSET_CONFLICT (409), never overwritten. Complete expected metadata and null submission forms are distinct durable submissions.

A timeout/corrupt new readback returns PERSISTENCE_UNVERIFIED / UNKNOWN; readiness failure after crop writes also reports UNKNOWN. Partial crops remain immutable and original-request reconciliation rechecks all assets. Conflicting asset sets/crops remain fenced PENDING for explicit operator reconciliation; they are never automatically expired/deleted. A JSON conflict may resolve the individual request as CONFLICT while the reserved set stays PENDING. Do not clear either fence without reconciling the entire set. Storage is not a cross-object transaction.

Controlled tests cover one/two assets, pixels and rounding/bounds, source/dimensions/SHA/pixel-bbox/expected-artifact rejection, identical replay, differing-content conflict, concurrent create, interruptions at both asset and page write/readback, second-asset failure, source change before JSON, strict persisted shape, bounded PNG/streams, generic JSON transport, redaction and immutable generation isolation. Deployment remains separately pinned; production acceptance must visually inspect source and crops, verify the exact page receipt and STOP. See CURRENT_STATE for the actual rollout result.

### 21.6 Verified rollout / page-2 acceptance — 2026-10-18
Runtime `b6d465c49dbf546f0ea31876d218121428d495c8` is pinned on Railway deployment `4489131f-d578-4062-b88f-40adc3716932` (SUCCESS). Provisioning now verifies private JSON+PNG capability and at least a 32 MiB finite limit without reducing existing higher/unrestricted limits. The original JSON-only bucket rejected the initial crop; no v4 objects existed, both claims remained PENDING, and the original request/key later reconciled successfully.

The existing private Site v4 required no source change or redeploy: connected-plugin JSON-only submission and enriched receipt passed in Codex, using the ordinary-Chat-compatible path. Exactly WSJ 2026-10-14 page 2 was stored CREATED/VERIFIED_WITH_NOTES with three relevant articles and three visually inspected chart crops, including both bank charts. All text anchors were unique and all artifacts matched independently computed source-derived bytes. Page JSON SHA f271f52b378852b186ee919f39d48983db57d469891bd4fad437107efefed60f, 17165 bytes; set/page bindings VERIFIED, identity_matches=true, usable_for_assembly=true. Exact crop identities/bounds are in HISTORY. 226 tests pass. v2/v3 objects stayed unchanged. STOP after page 2, no assembly; this is not a new separate ordinary Chat session or corpus-wide acceptance.

### 21.7 Normative editorial and independent crop acceptance gate
Text is reconstructed; visual assets are preserved as authoritative crops. Pull quotes are presentation/layout, not new semantic content: never duplicate their extracted wording in canonical prose or create an item/asset for the repeated quote. Distinct boxed prose sidebars remain editorial items. Preserve visually verified internal article subheads in source-faithful prose where semantically part of the article. A visually verified ad-only page may persist as valid v4 with items:[], explanatory page_notes and no article assets; its empty editorial result is canonical and may be usable_for_assembly.

Before setting any asset visual_checked:true and before persisting its page:

1. Verify the authoritative manifest-listed PNG identity and dimensions.
2. Render the proposed crop with §21.2 server-equivalent floor/ceil pixel bounds, without resizing. Inspect every resulting crop independently as its own image; a bbox drawn on the whole page is insufficient.
3. Check all edges, title, axes, legend, source notes and visual extent as applicable, excluding neighboring prose; verify ownership and logical anchor separately.
4. Adjust and re-render/re-preview until complete. If preview or completeness cannot be verified, do not assert visual_checked:true or persist a verified page. Local preview is an acceptance step, not canonical persistence; the production writer must still verify the source-derived crop and final metadata/readback.

This is a manual normative workflow, not a new server-side visual detector or preview endpoint. SHA/readback verifies bytes and identity, not visual/editorial truth. F011 records the immutable page-6 exception: do not consider the edition fully visually accepted or silently correct existing objects. Q014 requires a separately authorized revision/correction protocol. Reported ordinary-Chat coverage and per-page evidence levels are in HISTORY/CURRENT_STATE.
