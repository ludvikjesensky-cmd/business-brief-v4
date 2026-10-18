# Ingestor v2.0

**Status:** CANONICAL COMPONENT DEFINITION  
**Execution model:** live Chat, human-supervised  
**Upstream:** Technician / `source-bundle-v4`  
**Downstream:** Assembler  
**Primary output:** exactly one verified Page JSON per processed source page

## 1. Purpose

Ingestor v2.0 turns one technically prepared publication page into a structured, source-faithful Page JSON.

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
4. previous Chat interpretation.

Previous model output is never source evidence.

When visible page and OCR disagree, inspect the page and resolve from the source whenever possible.

## 4. Scope of one page pass

The Ingestor follows one fixed mental sequence:

**page orientation → item inventory → ownership → relevance/perspective → source-text reconstruction → verification → JSON**

For each requested page:

1. Confirm source, publication, edition and page number.
2. Inspect the complete page before extracting individual items.
3. Build a complete inventory of editorial and non-editorial regions.
4. Identify each editorial item independently and determine ownership/reading order.
5. Judge Business Brief relevance and perspective value for each item.
6. For each relevant item, reconstruct **all source text belonging to that item that is physically present on the current page**.
7. For clearly irrelevant items, preserve the minimum audit inventory required by section 7; full body text is optional.
8. Record page-level perspective evidence only to the extent supported by this page.
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

Use `text_on_page`, not `full_article_text`.

Do not:

- summarize;
- paraphrase;
- translate;
- stylistically improve;
- silently omit text;
- invent transitions;
- infer missing endings;
- complete wording from memory or web knowledge.

OCR may be corrected only when the correction is supported by the visible source.

Line-break hyphenation may be normalized only when visually supported.

If a word or passage cannot be verified, preserve the uncertainty in the Page JSON.

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

### Minimum inventory for irrelevant items

A clearly irrelevant item must still remain auditable. Preserve at minimum, when visible:

- `page_item_id`;
- `item_type`;
- title;
- byline;
- relevance state and reason;
- continuation evidence;
- verification notes where needed.

Full `text_on_page` is optional for clearly irrelevant items unless required for continuity, ambiguity resolution or explicit user review.

Relevance is still not final editorial selection. The Ingestor identifies perspective value; downstream editorial workflow decides what ultimately enters Brief or Detail.

## 8. Page-level perspective evidence

For relevant items, the Ingestor should capture perspective metadata when the current page supports it.

Possible fields include:

- `author_question`;
- `framing`;
- `central_argument`;
- `distinctive_angle`;
- `tensions_or_counterarguments`;
- `open_questions`.

These fields are **page-level evidence**, not a definitive interpretation of the full article.

The Ingestor must distinguish three epistemic layers:

1. **observed_on_page** — directly supported by wording or visible structure on this page;
2. **interpreted_from_page** — a reasonable interpretation of this page, but not a direct quotation or explicit statement;
3. **unresolved_until_assembly** — cannot be determined safely from this page alone and must wait for other article parts.

If a continuation page lacks the headline, opening argument or enough context, do not invent an author question or central argument. Record the perspective as unresolved until assembly.

The Assembler may later combine page-level perspective evidence into article-level perspective metadata, but it must preserve provenance and uncertainty.

## 9. Cross-page boundary

Ingestor v2.0 never assembles multi-page articles.

It records only evidence visible on the current page, including:

- `starts_here`
- `continued_from_previous_page`
- `continues_to_another_page`
- `continuation_marker`
- `continuation_target`

The Assembler resolves cross-page article identity and joins text.

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

The current schema identifier is:

`page-ingest-v2`

Do not invent additional fields outside the contract unless the contract is being deliberately revised.

A page is not complete merely because its JSON appears in Chat. The canonical Page JSON must be durably persisted.

## 12. Persistence contract

The canonical Page JSON artifact belongs in Supabase Storage.

Canonical logical object key:

```
page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.0/page-<NNNN>.json
```

Example:

```
page-ingest/the-wall-street-journal/2026-10-14/<source_sha256>/ingestor-v2.0/page-0001.json
```

The exact Supabase bucket name is operational configuration. The bridge resolves the configured artifact bucket server-side and returns it in the verified receipt; Chat must not invent a bucket name. The normative bridge contract is section 19; implementation/runtime notes are in `bridge/README.md`.

The stored file contains the validated `page-ingest-v2` payload for exactly one source page.

For the same source SHA, Ingestor generation and page number, persistence must be deterministic. A rerun must not silently create a second competing canonical artifact.

PostgreSQL is the operational index, not the primary home of the JSON body. When an implemented operational index exists, it should record source/edition identity, page number, schema version, Ingestor version, Storage key, verification status, artifact hash and timestamps.

Do not create a new database table from Chat unless that table is already part of the implemented system or an explicit schema change is requested.

A successful page pass ends as:

```
interpret page
→ build page-ingest-v2
→ validate structure
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

Ingestor v2.0 is not:

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

Ingestor v2.0 succeeds when:

- the source page has been inspected as a whole;
- relevant editorial items are faithfully represented;
- text is verified against source evidence;
- uncertainty is explicit;
- continuation evidence is preserved;
- output matches `page-ingest-v2`;
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
10. Validate the resulting `page-ingest-v2` payload.
11. Persist it according to section 12.
12. Confirm the durable Storage object key and page status.
13. State any unresolved uncertainty briefly and stop.

A convenient user invocation is:

```
INGESTOR v2.0: process page <N> of <publication/edition>.
```

For example:

```
INGESTOR v2.0: process page 1 of the current READY_FOR_INGESTOR WSJ edition.
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

**Status (2026-10-15): accepted contract; implementation deployed, technical page-1 read acceptance passed from Codex. Production page submission and a separate ChatGPT connector remain unverified.** This section is the single authority for the bridge wire contract. `contracts.py` remains the authority for the Page JSON body. The original contract decision was documentation-only; the subsequent standalone implementation is documented in `bridge/README.md`.

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

Strict Page JSON validation is a bridge requirement, **not an existing dataclass runtime validator**. `PageIngest.to_dict()` defines the field names and nesting, not the Python constructor names: top-level fields are exactly `schema_version`, `producer`, `instruction_version`, `source`, `publication`, `items`, `page_status`, `page_notes`. Require `page-ingest-v2`, `ingestor-v2.0-chat`, `2.0` respectively. `source` is exactly `{source_id:UUID, source_sha256:SHA}`; `publication` is exactly `{publication_id:string, canonical_name:string, edition_date:Date, edition_variant:string, page_no:integer}`.

Every item has exactly the fields/types serialized by `PageItem.to_dict()`: nonempty unique `page_item_id` and nonempty `item_type`; nullable strings `title`, `subtitle`, `kicker`, `byline`, `text_on_page`; required `relevance`, `perspective`, `continuation`, `verification`. Arrays are JSON arrays, never Python tuples. `relevance` requires state `relevant|irrelevant|uncertain` and a nonempty reason. `perspective` requires all nullable scalar fields, list fields and epistemic arrays defined in `PerspectiveEvidence`; specifically `author_question`, `framing`, `central_argument`, `distinctive_angle` are string|null, and `tensions_or_counterarguments`, `open_questions`, `observed_on_page`, `interpreted_from_page`, `unresolved_until_assembly` are string arrays. `continuation` requires three booleans and nullable strings `continuation_marker` and `continuation_target` exactly as `ContinuationEvidence`. `verification` requires `status`, the boolean fields `visual_checked`, `text_layer_checked`, `title_verified`, `boundaries_verified`, `reading_order_verified`, `text_on_page_complete`, plus `byline_verified:boolean|null`, and `notes:string[]`. No omitted defaults or extra fields at any level. `page_notes` is a string array; `items` may be empty for an explicitly verified page with no editorial items, with explanatory page notes.

All integers in this contract reject booleans and fractional values. Validation order is authentication/scope/resource authorization, syntax/shape, live source and bundle identity, page verification consistency, idempotency binding and canonical write. Identity mismatch is 409 `IDENTITY_MISMATCH`; invalid Page JSON types/enums/fields are 422 `PAGE_SCHEMA_INVALID`.

Both page/item statuses use `VERIFIED|VERIFIED_WITH_NOTES|NEEDS_REVIEW|BLOCKED`. A BLOCKED page or item is rejected with 409 `PAGE_BLOCKED`, without canonical write. A NEEDS_REVIEW page may be stored with `usable_for_assembly:false`, and is not a successfully completed verified page pass. Page status must not conceal a worse item status: VERIFIED permits only VERIFIED items; VERIFIED_WITH_NOTES permits VERIFIED/VERIFIED_WITH_NOTES; NEEDS_REVIEW permits any non-BLOCKED item. Non-VERIFIED page/item states require localized nonempty notes. For verified items require visual, text-layer, boundaries and reading-order checks true; require title check when title exists, byline check true when byline exists (null when absent), and complete nonempty text for relevant/uncertain items. Clearly irrelevant items may omit body text and completeness; the bridge preserves this exception. Verified pages must have no unresolved failed required checks. These are mechanical consistency checks of the caller's assertions; the bridge never decides whether prose, relevance or perspective is correct.

### 19.6 Canonical write, hashing and idempotency

Serialize the validated `page` only using RFC 8785 JSON Canonicalization Scheme (JCS), UTF-8, no BOM or trailing newline, no Unicode normalization. SHA-256 of those exact bytes is `artifact_sha256`. Object key is derived server-side:

```text
page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.0/page-<NNNN>.json
```

`NNNN` is zero-padded to four digits. Slugs/date/SHA are validated identity values, not raw path input. The directory `ingestor-v2.0` deliberately differs from producer `ingestor-v2.0-chat`. No variant component is added; if the same key would represent different variant/source UUID identity, refuse with 409 rather than changing this canonical path.

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
