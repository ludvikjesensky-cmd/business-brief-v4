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

## 12. Handoff to Assembler

The Page JSON must contain enough page-level truth that Assembler can:

- identify candidate parts of the same article across pages;
- join text in source order;
- preserve provenance;
- detect unresolved ambiguity;
- refuse unsafe assembly when review is required.

Assembler should combine page-level truth.

It should not rediscover page layout.

## 13. Non-goals

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

## 14. Legacy

Ingestor v1.1 = `ingestor-v4-physical-map-v1.1`.

Its production role and Physical Map handoff are superseded by D014.

Physical Map, Visual Page Map, BODY_FLOW, bbox/overlap matching and block-ID experiments may remain as historical/debug material only.

## 15. Success criterion

Ingestor v2.0 succeeds when:

- the source page has been inspected as a whole;
- relevant editorial items are faithfully represented;
- text is verified against source evidence;
- uncertainty is explicit;
- continuation evidence is preserved;
- output matches `page-ingest-v2`;
- Assembler can proceed without reinterpreting page layout.


## 16. Chat bootstrap protocol

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
9. Run exactly one page pass according to sections 3–14.
10. Emit exactly one `page-ingest-v2` JSON, state any unresolved uncertainty briefly, and stop.

A convenient user invocation is:

```
INGESTOR v2.0: process page <N> of <publication/edition>.
```

For example:

```
INGESTOR v2.0: process page 1 of the current READY_FOR_INGESTOR WSJ edition.
```

That short invocation does not replace the bootstrap sequence. It merely selects the source page to process.

## 17. Operational lookup rules

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
