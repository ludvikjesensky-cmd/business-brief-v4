# Architecture — Business Brief v4

Architektura odděluje technickou přípravu zdroje, page-level interpretaci, skládání článků, cross-source kompozici, překlad, editorial judgment a publikaci.


## Two independent production branches — D030

Business Brief v4 currently has **two independent branches**. They share the product and source family, but neither is a prerequisite for the other.

### Fast Editorial

```text
complete Reference Editions (FT / WSJ / Handelsblatt)
→ live Chat Editorial Read of each edition
→ provisional Issue Map per edition
→ cross-paper editorial comparison
→ editorial selection / hierarchy
→ Brief
```

Fast Editorial is edition-first and editorial-first. It is optimized for morning understanding and publication judgment. It does **not** require Page JSON, Assembler, Article Records, Indexer, Enrichment, Composer or Memory.

The repository's `fast_editorial.py` / `fast_editorial_worker.py` are historical page-level API automation experiments, not the current Fast Editorial architecture.

### Deep / Memory

```text
Technician
→ ordinary Chat Ingestor
→ immutable Page JSON / explicit edition selection
→ Assembler
→ canonical Article Records
→ Indexer
→ Enrichment / Editorial Memory
→ Detail / research / long-term knowledge
```

Composer D027, if implemented, belongs to this Deep/Memory branch and may group canonical indexed Article Records. It is not the required Cross-Paper stage of Fast Editorial.

### Integration boundary

No required integration is defined yet. Future reuse of Deep/Memory evidence inside Fast Editorial, or promotion of Fast Editorial discoveries into Memory, requires a separate explicit decision and acceptance test. Until then, do not introduce cross-branch dependencies.

## Canonical flow

closed source edition  
→ Technician  
→ validated Source Bundle  
→ Ingestor Access Bridge (authorized evidence access)
→ **Ingestor (ordinary Chat)**
→ Ingestor Access Bridge (validation + verified canonical persistence)
→ one verified Page JSON per source page  
→ accepted Edition Selection Manifest (explicit ID + SHA)
→ Assembler v1 + mandatory assembly post-check (repository implemented; Q020 production acceptance)
→ immutable canonical Article Records in private article-records Storage + operational articles/source-parts index
→ Indexer + mandatory index post-check (derived search layer)
→ Composer + mandatory topic post-check
→ daily-topic-v1 (current-day topics + explicit continuity refs)
→ Selective Deep Read (where recommended and accepted)
→ Editorial Workflow  
→ Master editorial truth  
→ Brief / Detail / channel adaptations

## Technician
Technician je technický gateway: identity, immutable original, SHA/provenance, OCR, page evidence, mechanický split, validace a atomic handoff. Nedělá editorial interpretation.

Jeho output je validovaný source-bundle-v4.

## Ingestor (ordinary Chat)
Ingestor (ordinary Chat) je živá Chat role.

Jeho vstupem je Technician Source Bundle. Zpracovává vždy jednu stránku. Používá obraz stránky a připravenou textovou/evidence vrstvu iterativně a vytváří jeden ověřený Page JSON.

Jeho odpovědností je:
- pochopit obsah a layout konkrétní stránky;
- identifikovat relevantní editorial objects;
- určit titulky, metadata, byline a pokračování;
- rekonstruovat věrohodný source-faithful text přítomný na dané stránce;
- explicitně evidovat nejistoty;
- posoudit relevance v kontextu Scope/Editorial purpose;
- zastavit se po dokončení stránky.

Nevytváří final multi-page Article Record a nespojuje zdroje.

## Ingestor Access Bridge

D018 přijímá úzký HTTP kontrakt v1; samostatná implementace je v `bridge/`, nasazená na Railway a technicky ověřená pro page-1 evidence access z Codex HTTPS klienta. Jediná normativní wire specifikace je [docs/INGESTOR.md §19](../docs/INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1). Bridge bezpečně rozliší current active source, poskytne autorizovaný přístup k privátní evidenci a uloží právě jeden validovaný Page JSON. Runtime je samostatná Railway HTTP služba, oddělená od legacy workeru. PostgreSQL row/session locks doplňuje durable PENDING claim a invoker guards proti změně identity při ztrátě session; podrobnosti v [bridge/README.md](../bridge/README.md).

Nedělá editorial interpretaci, OCR ani assembly. Source UUID v DB/API a SHA identita manifestu mají explicitní ověřenou vazbu. Zápis používá serverem odvozený D017 klíč, RFC8785 JCS/SHA-256, create-if-absent, durable idempotency binding a download verification. Rozdílný canonical obsah vrací 409 bez přepisu; nejistá persistence BLOCKED. Scopes/publication allowlist chrání každý endpoint, credentials zůstávají server-side a signed URLs mají 300 sekund. Kontrakt vyžaduje fencing vůči změnám source identity/readiness při zápisu; neurčuje novou DB tabulku.

## Assembler
Assembler spotřebovává Page JSONy jednoho vydání.

Spojuje části článků přes stránky, řeší continuations a vytváří canonical Article Records. Výsledné články ukládá do Supabase Storage a jejich identity, vztahy, stav a provenance do PostgreSQL.

Assembler nemá znovu interpretovat původní layout stránky. Pokud Page JSON neposkytuje dostatečnou jistotu, výsledek musí jít do review místo hádání.

## Assembler runtime (D029)
The D025 contract now has repository code. `business_brief.assembler` is deterministic and source-faithful; `business_brief.assembler_runtime` loads one explicit accepted selection through the Bridge, independently verifies exact selected Storage bytes/assets, assembles, post-checks and optionally persists only eligible records. The CLI is read-only by default; `--persist` is explicit.

Continuation edges require explicit flags plus a resolvable target. The initial implementation recognizes target/marker labels with a trailing numeric page identity mapped to the selected physical page; multiple incoming candidates on that already-bounded target page may be disambiguated only by deterministic title-token agreement. Unsupported labels/ambiguity fail to NEEDS_REVIEW. No semantic topic similarity or latest-page fallback is used.

Persistence migration creates private `article-records`, `articles` and `article_source_parts`. Storage JSON is canonical authority; DB is an operational/query index. Q020 gates first WSJ read-only/persistent acceptance and any subsequent Indexer handoff.

## Indexer and review loop (D026)
The accepted design adds a rebuildable search layer over persisted Article Records only. Eligibility requires assembly VERIFIED / VERIFIED_WITH_NOTES and post_check PASS; all derived rows bind to exact article_record_sha256. Canonical JSON/full_text and PNG assets remain immutable.

[docs/INDEXER.md](../docs/INDEXER.md) owns paragraph-aware BB-CHUNKING-V1, versioned Cohere BB-EMBEDDING-V1 (embed-v5.0-pro, 1024D, document/query input types, cosine), article/chunk embeddings, pgvector storage, derived tables and index post-check. Hybrid retrieval uses vectors, PostgreSQL full-text relevance and metadata filters; weights remain open. A Czech query can retrieve original English/German evidence in one multilingual space.

Manual workflow returns NEEDS_REVIEW to ordinary Chat source review/correction, explicit immutable revision/selection and Assembler rerun before indexing. A future pipeline runner orchestrates gates and review pauses. This is design, not a deployed Assembler/Indexer or a production run. [SYSTEM](../docs/SYSTEM.md#assembler) owns the D025 Assembler contract and persistence boundary.

## Composer (D027)
Composer is the v4 successor to v3 Cross-Paper Editor, after Indexer and before Selective Deep Read / Editorial Workflow. It groups only the same current-day event/story/problem, not a broad subject, and produces `daily-topic-v1`. Its closed current-day corpus requires assembly VERIFIED / VERIFIED_WITH_NOTES, post_check PASS and a successfully post-checked exact index. Canonical Article Records remain immutable.

Indexer article/chunk embeddings, PostgreSQL full-text and metadata/entities propose candidate relationships; a semantic/model layer may merge, split, retain single-source or request review. Embeddings alone never create topics. Today's groups precede continuity retrieval: **Daily = delta. Memory = context.** Prior references never replace today's coverage.

[docs/COMPOSER.md](../docs/COMPOSER.md) owns deterministic topic identity, technical membership roles, exact article/index provenance, optional supported daily_delta, continuity, Deep Read recommendations, relational operational structures and the mandatory topic post-check. Composer does not perform Deep Read, final selection/importance ranking, Assignment roles, Story Editor framing or Brief writing. Preserve article individuality and importance ≠ reading value. This is D027 design only, not runtime acceptance.

NEEDS_REVIEW returns to Chat article-evidence review, explicit correction and Composer rerun/post-check; BLOCKED integrity failures require repair. A future runner stops at semantic gates. No required v3 Provisional Issue Map layer returns.

## Translator
Translator pracuje až nad spolehlivě sestaveným textem. Je vhodným kandidátem pro API automatizaci, protože jde o řízenou transformaci známého textu, nikoli page-layout interpretation.

## Editorial
Editorial Workflow rozhoduje, co stojí za přenos, jak spojit perspektivy, co číst do hloubky a co publikovat. Completeness a curation zůstávají oddělené.

## Persistence
Supabase PostgreSQL drží identity, relationships, jobs, state, provenance a events.

Supabase Storage drží immutable sources, Technician artefakty, Page JSONy, assembled article artefakty a další validované výstupy.

Railway je worker/runtime a temporary workspace.

## Legacy boundary
Ingestor v1.1 (ingestor-v4-physical-map-v1.1) a Physical Map production path jsou superseded a neaktivní.

Physical Map může zůstat historický/debug artefakt nebo diagnostická evidence, ale není required input Ingestoru v2.0 ani canonical krok pipeline.

Visual Page Map, BODY_FLOW, bbox/overlap matching a block-ID assembly nejsou current architecture.

Acquisition je upstream problém. Technician není downloader/crawler a odstraněný watcher není current komponenta.

## Current extraction and generation boundary
Ordinary Chat uses the private Site v4 adapter for server-side verified image and inline OCR evidence; URLs/tokens never reach the model. Codex is for system development/debugging. See docs/INGESTOR.md §20 for adapter versions, limits and acceptance provenance.

Select primarily relevant articles, with uncertain candidates for review and exceptional irrelevant continuity/review evidence only. Preserve visually validated title/subtitle/byline/text_on_page/continuation; OCR supports the image. Normalize technical layout artifacts only. Do not summarize, paraphrase, translate or invent missing text. Perspective interpretation belongs downstream, not a required per-item object.

New page-ingest-v3 uses producer ingestor-v2.1-chat, instruction 2.1 and directory ingestor-v2.1; v2 and its ingestor-v2.0 key remain immutable compatibility artifacts. Bridge validation and server-side generation mapping are deployed; connected-plugin page-1 content/persistence acceptance passed (CURRENT_STATE/HISTORY). Site v4 already transports the body unchanged and required no redeploy. Auth, JCS, durable binding/fencing, create-if-absent and readback semantics are retained. Assembler must select an explicitly accepted generation and exclude superseded acceptance content, regardless of historical usable_for_assembly=true.

## Article assets — canonical D022
**Text se rekonstruuje. Vizuální artefakty se nepřepisují, ale uchovávají.** `text_on_page` is visually verified continuous article prose. Charts, tables, photos, infographics, illustrations and other visuals are separate article-owned PNG crops, never canonical OCR transcripts. Minimal article fields remain; v4 adds `assets`, without required PerspectiveEvidence or rejected-item inventory.

The new exact generation is `page-ingest-v4` / `ingestor-v2.2-chat` / instruction `2.2` / namespace `ingestor-v2.2`. Keep v2/v3 serialization, keys and production objects immutable. Reuse the existing private `page-ingest` bucket. Canonical key: `page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.2/assets/page-<NNNN>/<asset_id>.png`; sibling Page JSON is `.../ingestor-v2.2/page-<NNNN>.json`. Page JSON carries exact bucket/key/SHA/size/dimensions; no new bucket or client-selected path.

Assets bind ownership (`page_item_id`, page), physical page bbox and authoritative PNG SHA to a logical text anchor (position, auxiliary paragraph index, authoritative surrounding anchor text). Assembler joins prose across pages first, then re-anchors by unique anchor text. A missing/ambiguous match remains `placement_needs_review` / unplaced; never guess from geometry or a stale paragraph index. Physical bbox remains provenance. Editorial may use, interpret or omit visuals while retaining the evidence.

The normative schema, bounds/anchor checks, storage and recovery rules are in docs/INGESTOR.md §21. The bridge now implements authoritative server-side PNG cropping and set-wide fenced create/readback before Page JSON. Text-only submissions may use artifact:null; strict persisted pages contain exact final metadata. Original-request and deterministic target/set bindings preserve source UUID/variant identity and partial-write reconciliation without overwrite/delete. Existing Site v4 generic transport needs no image bytes. CURRENT_STATE records actual deployment/acceptance; implementation alone does not imply production approval.

Historical D022 rollout pin (superseded by the D024 pin in CURRENT_STATE): `b6d465c49dbf546f0ea31876d218121428d495c8`, Railway `4489131f-d578-4062-b88f-40adc3716932` SUCCESS; one page-2 WSJ acceptance with three source-derived chart crops and set-wide verified readback is complete. Existing generic Site v4 required no redeploy; private bucket additively permits JSON/PNG. 226 tests pass. Exact acceptance and bounds are in CURRENT_STATE/HISTORY. Subsequent ordinary-Chat pages 3–10 are reported there with evidence limits; page 6 has a known visual defect. No assembly is evidenced.

## Visual acceptance and immutable correction boundary
D023 / INGESTOR §21.7 requires independent server-equivalent crop preview before visual_checked:true and persistence. Mechanical readback does not detect clipped visuals. D024 / INGESTOR §22 now provides explicit immutable revision snapshots and manifest selection; original defective objects remain retained and excluded. WSJ pages 1–10 now have fresh authoritative readback across their explicit generations; historical canonical page 6 retains its known visual failure. The accepted WSJ manifest now explicitly selects v3 page 1, v4 canonical pages 2–5/7–10 and corrected v4 page-6 r1; no homogeneous all-v4 corpus is claimed.

## Edition selection and immutable revisions (D024)
Assembler accepts exactly one immutable edition-selection-v1 manifest ID + SHA through bridge.selection.assembly_input. It verifies every selected Page JSON and PNG and fails closed on missing/mismatched/unusable/known-defective input. No page-directory scan, latest-generation or latest-revision fallback. Mixed v3/v4/revision selections are explicit. Revision full snapshots use a separate page-revision-v1 wrapper; canonical v2/v3/v4 schemas and objects remain unchanged. INGESTOR §22 is normative. No assembly was run.

## Derived enrichment / knowledge architecture — D028
Canonical article bytes remain untouched. docs/ENRICHMENT.md is the single editorial-enrichment-v1 authority: article and topic annotations, exact SHA/evidence/profile lineage, controlled versus candidate metadata, separate Story Thread/Signal/Trend semantics, explicit review/promotion and durable lifecycle history. COMPOSER's knowledge_links is a bounded projection of that contract, not a parallel design. Daily-topic membership remains concrete and daily-first; broad trend overlap is insufficient.

Memory is SQL metadata + full-text + multilingual Cohere vectors + provenance/time + entities + Story Threads + Signals + Trends + editorial history. Article/Event → Story Thread → Signal → Trend → Analysis/BI is retained. Daily = delta. Memory = context; Memory is primary material for Trend/Analysis products. Source fidelity, event importance and individual reading value remain distinct. Assignment Editor owns inclusion/hierarchy, Story Editor final angle, Deep Read source verification.

Offline enrichment validation and metadata/profile candidate helpers exist. The unapplied candidate-staging SQL migration implements normalized annotations and SHA/run/version-linked candidate relationships, with acceptance deliberately disabled. Q019 gates real upstream article/index FKs, review/promotion/selected-output adapters and topic persistence on the missing physical Assembler/Indexer/Composer structures (Q017/Q018). No source/deployment change.
