# Decisions — Business Brief v4

## D001 — ACTIVE — v4 mění hodnotu z pouhé informovanosti na přenos perspektivy
**Decision:** Produkt nepřenáší jen co se stalo. Přenáší především způsob, jakým o tématu konkrétní médium a autor přemýšlejí a píší: jejich otázku, framing, argumentaci, důrazy, pochybnosti, rozpory a jedinečný úhel pohledu.

Relevantní může být i text bez zásadně nové události, pokud nabízí perspektivu, která mění, zpřesňuje nebo prohlubuje čtenářovo vnímání tématu.

Business Brief nesmí komprimovat zdroj tak, že zachová fakta, ale ztratí autora nebo charakteristický pohled média.  
**Origin:** v4 Vision / Editorial Philosophy.

## D002 — ACTIVE — Completeness a curation jsou oddělené vrstvy
**Decision:** Dnešní vydání nese systematickou coverage; Brief může legitimně vybírat. Extraction miss je chyba, editorial omission může být rozhodnutí.  
**Origin:** dědictví v1 + reinterpretace v4.

## D003 — ACTIVE — Provenance je součást produktu
Každé významné tvrzení/výstup musí být dohledatelný ke zdroji a transformacím.

## D004 — ACTIVE — Supabase je operational memory/archive; Railway je workshop
Databáze/storage drží autoritativní state a artefakty. Railway filesystem je dočasný.

## D005 — ACTIVE — Technician zůstává čistě technický
OCR a fyzická příprava patří Technicianovi; semantic/editorial interpretation ne.

## D006 — SUPERSEDED — Physical Map je evidence, ne článek
Původní rozhodnutí oddělovalo fyzickou reprezentaci od semantic truth. Tento princip zůstává historicky správný, ale Physical Map už není required production layer. Superseded by D014.

## D007 — ACTIVE — Automatizace následuje po ručním/levném ověření
Placené nebo autonomní workflow se nepouští do produkčního rytmu bez acceptance testu ceny, času a kvality.

## D008 — ACTIVE — Jedna redakční pravda, více adaptací
Text, web, e-mail a audio vycházejí ze stejného editorial masteru; kanál mění formu, ne fakta/hierarchii/jistotu.

## D009 — ACTIVE — Memory podporuje dnešek, nenahrazuje ho
Dnešní vydání je primární. Editorial Memory přidává kontinuitu, deduplikaci a kontext.

## D010 — ACTIVE — Watcher není součástí v4
Automatický WSJ watcher byl odstraněn. Acquisition se musí řešit explicitně jinou cestou.

## D011 — ACTIVE — Page-level API automatizace Fast Editorialu je pozastavena
Po reálném WSJ běhu s nepřijatelným API nákladem se nesmí automaticky plánovat další placené full-edition page-level API runs bez cost redesignu a malého acceptance testu.

Toto rozhodnutí **není selháním ani pozastavením Fast Editorial jako redakčního modelu**. Týká se konkrétní automatizační implementace `fast-editorial-v4.1`, která prováděla modelové volání nad jednotlivými stranami a následnou syntézu. Úspěšný v3 Fast Editorial byl primárně live Chat/editorial workflow nad kompletními Reference Editions a zůstává platným produktovým dědictvím.

## D012 — ACTIVE — v1–v3 jsou dědictví, ne current code dependencies
Relevantní principy, decisions, failures a lessons se přenášejí do v4 Project Memory; staré implementace se nenačítají jako skryté závislosti.

## D013 — SUPERSEDED — Sémantický layout určuje vision, Physical Map poskytuje text
**Date:** 2026-10-12.  
**Decision:** Vision mapuje page layout a Python skládá text nad Physical Map.  
**Status:** experimentální směr byl opuštěn po dalších pokusech; nenahrazuje jej jiný autonomous semantic mapper. Superseded by D014.

## D014 — ACTIVE — Ingestor v2.0 je live Chat page-by-page workflow
**Date:** 2026-10-14.  
**Decision:** Ingestor v1.1 (ingestor-v4-physical-map-v1.1) a Physical Map production path jsou neaktivní. Nový Ingestor v2.0 je živá Chat role nad Technician Source Bundle. Zpracovává přesně jednu stránku po druhé a vytváří jeden ověřený Page JSON na stránku. Po každé stránce se zastaví a další iterace pokračuje až na pokyn uživatele.  
**Reason:** Jednorázové API/automatizované semantic passes a následné heuristické assembly nebyly dostatečně spolehlivé a vyžadují opakované interpretační iterace. Live conversation umožňuje opakovaně zkontrolovat obraz, text a předchozí hypotézy bez toho, aby předchozí model output fungoval jako evidence.  
**Consequences:** Physical Map není required input. Page JSON je nový handoff kontrakt směrem k Assembleru. Přesný contract se má definovat v existujícím contract systemu v src/business_brief/contracts.py. Ingestor v2.0 není autonomous API worker.

## D015 — ACTIVE — Assembler navazuje až na ověřené Page JSONy
**Date:** 2026-10-14.  
**Decision:** Assembler spojuje page-level části článků napříč stranami a vytváří canonical Article Records. Ukládá article artefakty do Supabase Storage a strukturovanou identitu/provenance/state do PostgreSQL.  
**Reason:** Page interpretation a cross-page assembly jsou odlišné odpovědnosti.  
**Consequences:** Assembler nesmí znovu hádat page semantics, pokud jsou Page JSONy nejisté; takový případ jde do review.


## D016 — SUPERSEDED by D019 — Ingestor zachovává perspective value konzervativně a page-level
**Date:** 2026-10-15.
**Decision:** Ingestor v2.0 nefiltruje pouze podle event importance nebo tématu. Při nejistotě preferuje recall před agresivním vyřazením a zachovává kandidátní text pro downstream review.

U relevantních textů zachycuje page-level perspective evidence: autorskou otázku, framing, argument, distinctive angle, napětí/protiargumenty a otevřené otázky pouze v rozsahu, který podporuje aktuální stránka. Musí rozlišit observed_on_page, interpreted_from_page a unresolved_until_assembly.

Jasně nerelevantní položky zůstávají minimálně inventarizované kvůli completeness auditu.  
**Reason:** Business Brief nesmí ztratit texty, jejichž hodnota spočívá v perspektivě, a zároveň nesmí z jedné continuation stránky vyrábět definitivní interpretaci celého článku.  
**Consequences:** page-ingest-v2 nese explicitní PerspectiveEvidence; article-level perspective vzniká až po assembly a musí zachovat provenance/uncertainty.


## D017 — ACTIVE — Page JSON je durable Storage artefakt; Chat output sám nestačí
**Date:** 2026-10-15.
**Decision:** Canonical `page-ingest-v2` body se ukládá do Supabase Storage. Logický object key je `page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.0/page-<NNNN>.json`. Konkrétní bucket je operational konfigurace a nesmí být v Chatu hádán.

Page pass je dokončen teprve po validaci JSONu, durable write a ověření identity uloženého objektu. Vypsání JSONu pouze do konverzace není canonical persistence.

PostgreSQL slouží jako operational index/state/provenance vrstva. Dedicated page-ingest tabulka se nemá improvizovat před implementací; do té doby je autoritativním artefaktem JSON ve Storage.  
**Reason:** Assembler potřebuje stabilní, auditovatelný a znovu načitatelný handoff mezi Chat Ingestorem a downstream workflow.  
**Consequences:** Ingestor musí po každé stránce reportovat Storage key a page status; při persistence failure se stránka nepovažuje za dokončenou a workflow se zastaví.


## D018 — ACTIVE — Ingestor Access Bridge je úzký autorizovaný transport a persistence boundary
**Date:** 2026-10-15.
**Decision:** Přijímáme design kontraktu `ingestor-access-v1` v [docs/INGESTOR.md §19](../docs/INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1). Tři endpointy jsou `GET /ingestor-v2/source/current?publication=...`, `GET /ingestor-v2/source/<source_id>/page/<page_no>` a `POST /ingestor-v2/page`. Bridge rozlišuje jednoznačné nejnovější aktivní vydání bez fallbacku na starší READY source, autorizuje read-only evidence access a validuje/persistuje právě jeden `page-ingest-v2`. Nedělá editorial interpretaci, OCR, model calls ani assembly.

**Reason:** Referencovaný první acceptance pokus narazil na chybějící Chat ↔ private Storage přístup. DB metadata nejsou přístup k obsahu ani potvrzení durable write.

**Consequences:** D017 canonical path zůstává beze změny. UUID source v DB/API se explicitně mapuje na SHA identitu Technician manifestu. Server-side credential/scopes/publication allowlist a 300s signed URLs chrání privátní bucket; Supabase secret se Chatu neposkytuje. Zápis je create-if-absent nad RFC8785 JCS bytes, s SHA-256/readback identity verification a durable idempotency binding. Odlišný obsah/identita na stejném klíči je 409, nikoli overwrite; BLOCKED se canonical neukládá, NEEDS_REVIEW lze uložit bez assembly eligibility. Implementace musí zajistit fencing vůči změnám readiness/active source/bundle mapping.

Preferujeme budoucí malou samostatnou Railway HTTP službu. Toto rozhodnutí nepředstavuje implementaci, deploy, nový DB schema ani obnovení legacy Ingestoru. Přesná schémata a error model se neduplikují do dalších dokumentů. Acceptance gate je v §19.8; první skutečný page pass zůstává ruční, jedna strana a STOP.

## D019 — ACTIVE — Relevant source-faithful page extraction
**Date:** 2026-10-16.
**Decision:** Supersedes D016's mandatory irrelevant inventory and perspective expansion. Identify items over the whole page, persist primarily relevant articles plus uncertain candidates; include irrelevant items only for continuity, ambiguity resolution or explicit review. Preserve title, subtitle/dek/perex, byline, text_on_page and continuation with technical identity/verification. Relevance needs a short reason, not mandatory PerspectiveEvidence. What's News is not automatically a separate article.
**Reason:** Page truth must serve downstream reading/assembly, without unnecessary interpretation. OCR proposes; the image verifies. Only technical layout/hyphenation/spacing normalization and visually confirmed OCR corrections are allowed. No summary, paraphrase, translation, stylistic rewrite or invented text. Unverifiable text requires localized uncertainty and NEEDS_REVIEW/BLOCKED.
**Consequences:** Perspective value remains editorial purpose; faithful text carries it into downstream interpretation. Completeness concerns selected article text, not mandatory inventory of every rejected item.

## D020 — ACTIVE — New generation without overwriting v2
**Date:** 2026-10-16.
**Decision:** Extend the existing contract system with PageItemV3/PageIngestV3: page-ingest-v3, ingestor-v2.1-chat, instruction 2.1. Preserve v2 classes and strict validation. Derive v3 Storage keys with ingestor-v2.1 in place of ingestor-v2.0. The first v2 page remains a superseded technical acceptance artifact, never silently rewritten. D017 remains active for durable storage, with its path retained for v2 and extended here for v3.
**Reason:** Existing canonical create-if-absent forbids content replacement; schema, instructions and producer must move together.
**Consequences:** Same auth/fencing/JCS/hash/idempotency/readback/conflict semantics and HTTP endpoints. New generation requires a new intended-submission idempotency key. No automatic migration, deletion, v2 fallback or mixing generations in assembly. Deploy bridge/plugin support together and accept new content separately; this decision is implemented locally, not proof of production rollout.

## D021 — ACTIVE — Ordinary Chat daily ingest; Codex system work
**Date:** 2026-10-16.
**Decision:** Daily workflow is resolve_current_source → get_page_evidence (image + inline OCR) → visually validated relevant-article extraction → validate → persist → STOP in ordinary Chat through the plugin. Codex handles programming, system changes and debugging.
**Reason:** Ordinary Chat evidence acceptance now passed; earlier Codex-only integration limitation is closed.
**Consequences:** Technical persistence acceptance is distinct from source-content approval. Site URLs/tokens are fetched server-side and never returned to the model. One accepted page does not establish full-corpus quality.

## D022 — ACTIVE — Article assets, dual anchors and immutable v4 generation
**Date:** 2026-10-18.
**Decision:** **Text se rekonstruuje. Vizuální artefakty se nepřepisují, ale uchovávají.** `text_on_page` contains only source-faithful continuous article prose visually checked against the page. Charts, tables, photos, infographics, illustrations and other article visuals are separate `ArticleAsset` records owned by a `page_item_id` on a source page. Preserve a crop of the authoritative page PNG; internal OCR/extraction is neither required nor canonical evidence. Source-visible title/caption may be recorded separately when verified.

Each asset has a physical `page_anchor` (normalized bbox, source PNG SHA, optional reproducible pixel bbox) and a logical `text_anchor` (position, optional zero-based paragraph index and authoritative surrounding `anchor_text`). Assembler first joins article text, then re-anchors assets by unique anchor text. Paragraph indices may change during assembly; page geometry remains audit/provenance only. Missing/ambiguous anchors become `placement_needs_review` / unplaced; never guess placement.

**Storage decision:** Reuse the existing private `page-ingest` bucket, not a new bucket. Within it the canonical object key is `page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.2/assets/page-<NNNN>/<asset_id>.png`. The repeated `page-ingest` is intentional: bucket and object-key prefix are distinct. Page JSON is the sibling `.../ingestor-v2.2/page-<NNNN>.json` and carries exact bucket/key/SHA/size/dimensions. Keep auth, lifecycle, provenance and fenced writes under the same bridge boundary; never upload directly from Chat or grant bucket access. Keys are derived server-side; asset writes must be create-if-absent with SHA-256, exact download readback, source fencing, durable idempotency and no overwrite. No production configuration change is made here.

**Generation:** `page-ingest-v4` / `ingestor-v2.2-chat` / instruction `2.2` / namespace `ingestor-v2.2`, implemented in the existing contracts.py. Minimal v3 article fields remain, plus required `assets` array; no mandatory PerspectiveEvidence or irrelevant-item inventory. D017/D020 remain active for historical v2/v3 paths and immutable compatibility. Existing production v3 pages 1 and 2 (page 2 reported by the user; not independently inspected here) must never be rewritten or migrated in place.

**Reason:** Visual meaning depends on geometry, axes and relationships that OCR does not faithfully preserve; two anchors retain both source evidence and usable article placement without polluting prose.

**Consequences / implementation boundary:** §21 of docs/INGESTOR.md is normative. The follow-up implementation adds bounded source-PNG cropping, deterministic PNG encoding, explicit artifact:null submission versus strict persisted metadata, reserved deterministic durable target/set binding, fenced asset+JSON create/readback and original-request reconciliation. No DB migration/new bucket or client binary transport is needed. Deployment and single-page acceptance are separate verified milestones in CURRENT_STATE/HISTORY; the original consolidation itself performed no production writes. Existing v2/v3 remain immutable.

## D023 — ACTIVE — Independent crop preview before visual acceptance
**Date:** 2026-10-18.
**Decision:** Each asset crop must be rendered from the authoritative page PNG with server-equivalent §21.2 geometry and independently previewed as its own image before visual_checked:true and page persistence. Inspect the full visual footprint and article ownership; full-page bbox inspection does not satisfy this gate.
**Reason:** F011 exposed a clipped infographic despite successful technical readback.
**Consequences:** INGESTOR §21.7 and OPERATIONS govern the manual acceptance gate. No preview endpoint or immutable revision protocol is implied by this decision; unavailable crop preview blocks visual acceptance. Existing defective immutable artifacts require Q014 resolution.

## D024 — ACTIVE — Immutable full page revisions and explicit edition selection
**Date:** 2026-10-18.
**Decision:** Q014/Q015 mechanism uses page-revision-v1 wrappers around full v4 snapshots, with explicit canonical supersedes key/SHA, reason/author/time and crop preview hashes. Canonical objects remain immutable. Source-scoped readback verifies Page JSON and every PNG without signed capabilities. edition-selection-v1 records exactly one selected artifact for every physical page, including intentional heterogeneous generations. Assembler accepts one explicit manifest ID/SHA and independently verifies all selected bytes; no latest fallback. ACCEPTED_FOR_ASSEMBLY requires verified, usable, non-defective selections.
**Reason:** Immutable ingest history and authoritative downstream selection have different responsibilities. Technical readback does not resolve visual defects.
**Consequences:** INGESTOR §22 is normative. Same durable source fences/idempotency/no-overwrite apply. Protocol implementation alone does not close page-6 remediation or operational corpus acceptance; CURRENT_STATE records those gates. Q010/Q011 remain separate.


## D025 — ACTIVE — Deterministic Assembler review policy and Article Record contract
**Date:** 2026-10-19.  
**Decision:** Assembler is a deterministic transformation over exactly one immutable `edition-selection-v1` manifest identified by `manifest_id + sha256`. It re-verifies every selected Page JSON and referenced asset byte-for-byte before assembly and never scans for latest generations/revisions.

Assembler may join page-level parts automatically only when continuation evidence yields exactly one valid chain within the selected edition. Explicit continuation markers/targets and page start/continue flags are authoritative. Title/byline agreement and adjacent-page ordering may corroborate an already unique chain, but similarity, topic, layout proximity or model inference must never create a join by themselves. Zero or multiple valid continuation candidates produce `NEEDS_REVIEW`; missing/mismatched selected bytes, blocked input or broken provenance produce `BLOCKED`. A single-page article with no continuation ambiguity may assemble directly.

Text assembly preserves source order and source-faithful prose. It must not summarize, paraphrase, translate, repair missing source text or reinterpret page layout. A mandatory deterministic post-check reconstructs the expected `full_text` from the exact ordered `text_on_page` source parts using one canonical separator, recomputes every part hash and the final text hash, and verifies that every selected source part is used exactly once in the declared order. The stored `full_text` must be byte-for-byte equal to that reconstructed text. Any mismatch, omission, duplication, reordering or hash failure is `BLOCKED`, not an editorial review case. After prose assembly, each v4 ArticleAsset is re-anchored against the assembled text using its authoritative `anchor_text`. Exactly one match permits placement. Zero or multiple matches produce an unplaced asset with `placement_needs_review`; geometry and paragraph index are provenance/support only and must not force placement.

The canonical Article Record contract is `article-record-v1`. Required logical fields are: deterministic `article_id`; publication/edition/source identity; exact selection manifest identity; article metadata (`title`, optional `subtitle`, optional `byline`, `item_type`); `full_text`; ordered `source_parts[]` carrying page number, page item ID, selected Page JSON key/SHA and text SHA; `assets[]` carrying the original asset identity/artifact plus resolved placement state and source ownership; and `assembly` carrying `status`, method and notes. Status is one of `VERIFIED`, `VERIFIED_WITH_NOTES`, `NEEDS_REVIEW`, `BLOCKED`. Article Records are immutable artifacts in Supabase Storage; PostgreSQL holds queryable identity, relationships, provenance and state.

**Persistence:** Use a dedicated private Supabase Storage bucket `article-records`. Canonical key: `<publication_id>/<edition_date>/<source_sha256>/<manifest_id>/<article_id>.json`. Article Record bytes use deterministic canonical JSON, create-if-absent, SHA-256 and exact download readback; an existing different object at the same key is a conflict, never an overwrite. Article assets remain immutable references to their existing `page-ingest` PNGs and are not copied into the article bucket.

PostgreSQL is an operational/query index, not the canonical article body. The minimal implementation creates `articles` and `article_source_parts`: `articles` stores deterministic article identity, source/edition/publication + manifest identity, title/byline/item type, assembly/post-check status, Storage bucket/key/SHA/size and timestamps; `article_source_parts` stores ordered provenance for every page part (`article_id`, ordinal, page number, page item ID, selected Page JSON key/SHA and text SHA). Full article prose remains canonical in Storage. Embeddings/chunks are a later derived Indexer layer, not Assembler persistence.

**Reason:** Cross-page joining should be reproducible and auditable. Page interpretation already happened in Ingestor; Assembler must not become a second semantic/layout model or hide ambiguity behind heuristics.

**Consequences:** Q011 is resolved. Initial implementation should be ordinary deterministic code, with any future model-assisted review kept outside canonical automatic assembly. The first acceptance target is the already accepted WSJ 2026-10-14 selection. This decision defines policy/contract only; it does not implement or run Assembler.

## D026 — ACTIVE — Indexer is a derived, rebuildable multilingual search layer
**Date:** 2026-10-21.
**Decision:** Immutable Storage Article Records remain canonical. Indexer accepts only persisted records with assembly VERIFIED / VERIFIED_WITH_NOTES and post_check PASS, bound by exact article_record_sha256. It creates article-level and paragraph-aware chunk-level embeddings plus PostgreSQL full-text projections; it never summarizes, translates, rewrites or mutates canonical records.

BB-CHUNKING-V1 targets roughly 450–700 tokens, whole paragraphs where possible, one-paragraph overlap, deterministic chunk identity and text SHA-256. BB-EMBEDDING-V1 is first-class versioned configuration: Cohere embed-v5.0-pro, 1024 dimensions, search_document for documents, search_query for queries, cosine similarity and shared multilingual space. Supabase/Postgres pgvector vector(1024) is the vector store. Logical derived tables are article_embeddings, article_chunks and article_index_runs, with PENDING / INDEXING / INDEXED / FAILED states and mandatory index post-check.

**Reason:** Search must be rebuildable independently of canonical evidence, with Czech queries able to retrieve English/German source text and every result traceable to its immutable version.
**Consequences:** [docs/INDEXER.md](../docs/INDEXER.md) is the single detailed Indexer contract. Hybrid retrieval combines vectors, PostgreSQL full-text relevance and metadata filters; weights remain open. Manual workflow includes Chat review/correction and Assembler rerun for NEEDS_REVIEW before indexing; a future runner only orchestrates these gates. This is design acceptance, not runtime, schema, bucket, provider-call or deployment evidence. Q007 remains broader; Q016 resolves the search-layer choice and Q017 records remaining implementation/ranking details.

## D027 — ACTIVE — Composer creates current-day daily topics before editorial selection
**Date:** 2026-10-21.
**Decision:** Composer succeeds v3 Cross-Paper Editor between Indexer and Selective Deep Read / Editorial Workflow. It consumes a closed current-day set of persisted Article Records with assembly VERIFIED / VERIFIED_WITH_NOTES, post_check PASS and successful exact-version indexing. Hybrid Indexer retrieval proposes candidate relationships; a semantic/model layer merges, splits, retains single-source topics or sends ambiguity to review. Only the same current-day event/story/problem belongs together; broad subject/entity similarity and embeddings alone cannot establish a topic.

The output is `daily-topic-v1`, with deterministic day/member-version identity, working title and topic identity, individually preserved articles with technical roles and membership evidence, coverage, continuity/prior refs, optional provenance-backed daily_delta, Deep Read recommendation, confidence/method/status and exact article/index provenance. Technical membership roles are primary / same_event / follow_up / background_today / adjacent, never Assignment roles such as lead / coverage / curated.

**Memory:** Daily = delta. Memory = context. Form today's groups first; only then retrieve older indexed articles/topics for continuity. Historical references never substitute for today's articles or inflate coverage.
**Boundary:** Composer does not perform Deep Read, choose final inclusion/importance/space, finalize angle/story framing or write the Brief. Preserve importance of event ≠ reading value of article and article individuality inside groups. No required v3 Provisional Issue Maps return.
**Persistence/gates:** Logical operational structures are editorial_days, daily_topics, daily_topic_articles, daily_topic_memory_refs and composer_runs; canonical Article Records remain unchanged. Mandatory topic post-check validates exact identities/SHA/index eligibility, coverage, membership explanations, memory targets and claim provenance. VERIFIED / VERIFIED_WITH_NOTES may proceed; NEEDS_REVIEW returns to Chat article-evidence review, explicit correction and Composer rerun/post-check; BLOCKED integrity failures require repair. A future runner must stop at semantic gates.
**Reason:** Retain v3's useful clustering/editorial boundary while using v4's verified canonical evidence, multilingual retrieval and precise provenance.
**Consequences:** [docs/COMPOSER.md](../docs/COMPOSER.md) is the single detailed Composer contract. Q018 tracks Composer implementation/calibration; Q019 tracks enrichment/knowledge acceptance. D028 subsequently adds offline validators/helpers and an unapplied candidate-staging migration. No Composer runtime, model call, deployment or production write is implied.

## D028 — ACTIVE — Preserve v3 enrichment as derived editorial knowledge
**Date:** 2026-10-21.
**Decision:** docs/ENRICHMENT.md is the single versioned editorial-enrichment-v1 authority. Retain v3 topics/trends/story_thread_candidates/tags/entities/geographies/industries, controlled category and hybrid Memory intent; adapt free trend strings to evidence-bearing candidates or reviewed durable links. Keep Story Thread, Signal and Trend distinct. Article/Event → Story Thread → Signal → Trend → Analysis/BI remains the knowledge chain. A Trend cannot be established by one article/day; promotion is an explicit reviewed operation, never Composer's responsibility.

**Boundary:** Immutable Article Record bytes stay canonical; rebuildable enrichment binds article_record_sha256 and producer/profile/version. daily-topic-v1 gains bounded knowledge_links. SQL metadata/full-text/vector/provenance/time/editorial history are first-class; Daily = delta. Memory = context, with Memory primary for Trend/Analysis. Controlled metadata, candidates and reviewed accepted relations remain separate. Editorial ownership and importance ≠ reading value remain unchanged.

**Implementation:** Offline validators and exact metadata/profile candidate helpers plus tests are implemented. No physical upstream articles/index/topic tables exist; the existing PR migration is hardened to candidate staging, with normalized annotations and enforced run/version/SHA lineage, RLS and no accepted state. Q019 gates upstream FKs, immutable review/output selection and transactional promotion; local PostgreSQL tests cover staging integrity and privileges. Q017/Q018 and real-source acceptance remain open. No v3 advance-only gate, bilingual Memory-ready prerequisite, Fast Editorial or Provisional Issue Map is reintroduced. No model call, deployment or production data write.

## D030 — ACTIVE — Fast Editorial a Deep/Memory jsou dvě nezávislé větve
**Date:** 2026-10-22.

**Decision:** Business Brief v4 drží Fast Editorial a Deep/Memory jako dvě samostatné větve se samostatnými vstupy, workflow, acceptance gates a provozními artefakty. V aktuální fázi mezi nimi není required dependency ani povinný handoff.

**Fast Editorial** navazuje na ověřený v3 desetidenní experiment. Je edition-first a editorial-first: kompletní Reference Edition → live Chat Editorial Read → provisional Issue Map → cross-paper editorial comparison → editorial selection → Brief. Jeho cílem je rychle pochopit celé vydání, jeho těžiště, jednotlivé texty, jejich reading value a vztahy napříč FT / WSJ / Handelsblatt. Nemá čekat na canonical Article Records, Indexer, Enrichment, Composer ani Memory.

**Deep/Memory** zůstává evidence-first větev pro přesnou rekonstrukci a dlouhodobou znalost: Technician → ordinary Chat Ingestor → immutable Page JSON / selection → Assembler → canonical Article Records → Indexer → Enrichment / Memory. Composer D027 patří do této větve jako případné seskupování canonical indexed Article Records; není nástupcem celého Fast Editorial workflow a není bránou pro ranní Brief.

**Historical code:** `src/business_brief/fast_editorial.py` a `fast_editorial_worker.py` jsou historický automatizační experiment z 9. 10. 2026. Zachovávají užitečný Issue Map contract a některé editorial principy, ale jejich Physical Map / `ingestor_jobs` / page-level paid API runtime je superseded a nesmí být považován za současnou Fast Editorial implementaci.

**Reason:** v3 prokázala hodnotu Fast Editorial jako rychlého redakčního čtení kompletních vydání. v4 současně prokázala lepší cestu pro přesný Deep Read a canonical evidence. Jejich předčasné spojení znovu vytváří zbytečné technické dependency a posouvá ranní Brief za pomalou Deep pipeline.

**Consequences:** Nejbližší Fast Editorial práce nejprve rekonstruuje a přenese ověřený v3 workflow do v4 jako samostatnou větev. Integrace s canonical Article Records, Composerem nebo Memory je samostatná budoucí otázka a nesmí být předpokládána v současném návrhu.

## D029 — ACTIVE — Deterministic Assembler is implemented repository-side
**Date:** 2026-10-21.
**Decision:** Implement the D025 Assembler as deterministic Python code over exactly one explicit accepted edition-selection-v1 manifest. The runtime takes source UUID + manifest ID + manifest SHA, calls only the Bridge assembly-input endpoint for the selected handoff, then independently downloads and verifies the exact manifest bytes, every selected canonical/revision Page JSON and every referenced PNG from private Storage before assembly.

Continuation joins require explicit continuation evidence. The initial resolver accepts target/marker labels whose trailing page number maps to one selected physical page. If that target page contains multiple incoming continuation items, normalized title-token agreement may only corroborate one candidate already bounded by the explicit continuation evidence; it never creates an edge from topic/title similarity alone. Missing target mapping, zero/multiple candidates, ties, ineligible item verification, multi-origin conflicts or cycles become NEEDS_REVIEW. Unsupported publication page-label schemes fail closed pending a versioned resolver.

Article Record construction is source-faithful: exact text_on_page joined only with the frozen "\n\n" separator, deterministic article_id from source/manifest/ordered-part identities, immutable source-part hashes and v4 asset references. Asset placement requires one unique anchor_text occurrence; otherwise placement_needs_review is retained. Mandatory post-check independently re-resolves every declared part against the selected Page JSON set, recomputes text hashes and expected full_text, verifies final SHA equality and every claimed placed anchor. Post-check failure is BLOCKED.

Persistence is implemented but not deployed. Only VERIFIED / VERIFIED_WITH_NOTES records with post_check PASS may be written. Canonical bytes go create-if-absent to private article-records and are read back exactly; same bytes replay idempotently, different bytes conflict. PostgreSQL articles + article_source_parts are operational/query indexes only. Migration 20261021130000_add_assembler_articles.sql creates the bucket/tables/RLS; bb-assembler is explicit and read-only unless --persist is supplied.

**Reason:** D025 was already frozen, while Q019 and the Indexer need stable physical Article Record identities. A deterministic implementation can now be tested on the accepted WSJ manifest without introducing semantic automation or weakening provenance.

**Consequences:** Repository implementation exists in src/business_brief/assembler.py and assembler_runtime.py with unit/schema tests. No migration has been applied, no Railway service deployed and no production Article Record written yet. Q020 is the acceptance/deployment gate. Q019 may now depend on the real Assembler schema once Q020 confirms it rather than inventing a parallel article catalog.
