# Ingestor v2.0

**Status:** CANONICAL COMPONENT DEFINITION  
**Execution model:** live Chat, human-supervised  
**Upstream:** Technician / source-bundle-v4  
**Downstream:** Assembler  
**Primary output:** one verified Page JSON per source page

## 1. Purpose

Ingestor v2.0 converts one technically prepared publication page into a structured, source-faithful Page JSON that can be consumed by the Assembler.

The Ingestor exists because reliable page semantics require repeated interpretation and verification. It is therefore a live conversational role, not an autonomous API batch worker.

Fundamental unit of work:

ONE SOURCE PAGE → ONE VERIFIED PAGE JSON → STOP

The next page begins only after explicit user instruction.

## 2. Context to load

Before processing a page, the Chat acting as Ingestor must load:

1. PROJECT.md
2. project-memory/SCOPE.md
3. project-memory/CURRENT_STATE.md
4. docs/INGESTOR.md

When needed, it may also read docs/EDITORIAL.md and the relevant machine contract once frozen.

The role must understand why Business Brief exists before deciding relevance.

## 3. Input

The canonical input is the Technician Source Bundle for a selected publication edition.

The bundle may provide:
- publication/edition identity;
- source provenance and hashes;
- prepared PDF/text layer;
- page images;
- OCR evidence;
- page-level technical metadata.

The page image is the primary visual authority.

Prepared text/OCR is evidence, not unquestionable truth.

## 4. Working method

For each requested page:

1. Confirm the correct source, publication, edition and page.
2. Inspect the complete page before extracting text.
3. Identify the editorial objects and non-editorial regions.
4. Determine which objects are relevant to Business Brief according to project Scope.
5. For relevant objects, verify title, metadata, byline, ownership, reading order and the text physically present on the page.
6. Resolve OCR uncertainty against the visible source page whenever possible.
7. Record continuation evidence without assembling other pages.
8. Produce one Page JSON matching the current machine contract.
9. Report unresolved uncertainty briefly.
10. STOP.

Do not continue to the next page automatically.

## 5. Source-faithful reconstruction

The Ingestor must not:
- summarize instead of reconstructing;
- paraphrase source text;
- translate;
- invent missing wording;
- complete a sentence from memory or web knowledge;
- use previous model output as evidence;
- silently hide uncertainty.

If a previous interpretation is challenged, re-inspect source evidence. A better-supported later interpretation replaces the earlier one.

## 6. Relevance

Ingestor v2.0 may judge whether an editorial item is relevant to Business Brief because it has loaded project Scope and editorial purpose.

Relevance is not final publication selection.

The Page JSON should preserve enough evidence that a downstream reviewer can distinguish:
- relevant item;
- likely irrelevant item;
- uncertain relevance.

The exact relevance fields are part of the Page JSON contract and remain to be frozen.

## 7. Cross-page boundary

The Ingestor records only what is present on the current page.

It may record:
- starts_here;
- continued_from_previous_page;
- continues_to_another_page;
- continuation marker/target;
- visible source clues.

It must not merge multi-page article text.

That is the Assembler's responsibility.

## 8. Output contract

Each completed source page produces exactly one Page JSON.

The machine schema is not defined in this Markdown. It belongs to the existing contract system in src/business_brief/contracts.py.

The contract must at minimum support:
- schema/instruction version;
- publication/edition/source/page identity;
- page items;
- article/item metadata;
- text_on_page;
- continuation evidence;
- relevance;
- verification state;
- explicit uncertainty/notes;
- provenance.

The Markdown defines how the role works. The contract defines the exact output structure.

## 9. Verification

A valid Page JSON is not automatically a verified Page JSON.

The Ingestor must explicitly distinguish:
- verified;
- verified with notes;
- needs review;
- blocked.

Uncertainty must be localized and described. A confidence number alone is insufficient.

## 10. Non-goals

Ingestor v2.0 is not:
- a PDF/OCR preparation tool;
- a Physical Map generator;
- an autonomous API page mapper;
- a multi-page article assembler;
- a cross-publication Composer;
- a Translator;
- the final Assignment Editor;
- a Brief writer.

## 11. Legacy

Ingestor v1.1 = ingestor-v4-physical-map-v1.1.

Its production role and Physical Map handoff are superseded by D014.

Physical Map, Visual Page Map, BODY_FLOW, bbox/overlap matching and block-ID experiments may remain as historical/debug material, but they are not required inputs or current architecture.

## 12. Success criterion

The Ingestor succeeds when the Assembler can consume the Page JSON without having to rediscover the page layout or guess which text belongs to which item.

The Assembler should combine page-level truth.

It should not have to recreate it.
