# System — Business Brief v4

## Boundary
Technická vrstva připravuje evidence. Ingestor interpretuje konkrétní source page v live conversation. Assembler skládá články. Editorial vrstva rozhoduje o významu a publikaci.

## Technician
Input: uzavřené source edition.

Output: validovaný source-bundle-v4.

Odpovědnosti: identity, immutable original, SHA/provenance, container validation, OCR decision/derivative, page evidence, mechanical split, manifest, atomic handoff. Žádná editorial interpretace.

## Ingestor (ordinary Chat)
Input: Technician Source Bundle.

Execution model: live Chat, human-supervised, page-by-page.

Output: přesně jeden verified Page JSON pro každou dokončenou source page.

Ingestor (ordinary Chat) používá:
- page image jako primární vizuální autoritu;
- prepared text/OCR jako evidence;
- metadata Source Bundle;
- Scope a Editorial purpose pro relevance judgment;
- opakované conversational iterations při nejasnosti.

Nevytváří final multi-page Article Record. Nespojuje více publikací. Neprovádí batch semantic processing přes API.

Po dokončení každé stránky se zastaví.

Stránka je dokončená až po validaci a durable uložení canonical Page JSONu do Supabase Storage podle persistence contractu v docs/INGESTOR.md.

Detail role je v docs/INGESTOR.md.

## Ingestor Access Bridge

Přijatý kontrakt v1, implementovaný v `bridge/` a nasazený jako samostatná Railway HTTP služba: úzká autorizovaná HTTP vrstva mezi live Chat Ingestorem a privátním Supabase Storage. Normativní request/response schémata, validace a chyby jsou pouze v [INGESTOR.md §19](INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1).

- `GET /ingestor-v2/source/current?publication=...` vybírá nejnovější dostupné aktivní vydání jednoznačně; při variantách nebo nepřipraveném zdroji blokuje místo fallbacku.
- `GET /ingestor-v2/source/<source_id>/page/<page_no>` vrací ověřenou identitu a krátkodobé read-only signed URLs pro manifest, obraz, prepared/OCR PDF a originál.
- `POST /ingestor-v2/page` striktně validuje jednu podporovanou generaci `page-ingest-v2/v3/v4`, identitu vůči DB/bundle a ukládá canonical body; v4 assets ověřuje podle §21.

Bridge neinterpretuje obsah, neposuzuje relevanci, neprovádí OCR ani assembly. Databázový source UUID se mapuje na manifest `sha256:<digest>` přes blob/edition vazby, nikoli rovností řetězců. Server odvozuje canonical klíč, zapisuje create-if-absent a ověřuje stažené JCS bytes přes SHA-256 a identitu. Shodný obsah je replay, odlišný obsah 409; žádný silent overwrite. `STORED` je potvrzení persistence, nikoli nezávislý editorial verdikt. NEEDS_REVIEW lze uložit bez assembly eligibility, BLOCKED se canonical neukládá. Durable bindings a source fencing jsou implementované; nejde o samostatný editorial Page JSON index (bridge/README.md).

Samostatná Railway služba `ingestor-access-bridge` prošla technickým page-1 evidence acceptance z Codex HTTPS klienta; Page JSON se v tomto testu neukládal. Ordinary Chat image + inline OCR read acceptance subsequently passed through private Site v4 (docs/INGESTOR.md §20); the first v2 production persist also passed but its content is superseded (HISTORY, D019). Pro deployment, durable fencing a recovery viz [bridge/README.md](../bridge/README.md). Auth principal má scopes a publication allowlist; Supabase secret zůstává jen na serveru.

## Page JSON
Page JSON je nový handoff artefakt mezi Ingestorem a Assemblerem.

Má reprezentovat:
- source/publication/page identity;
- editorial items na stránce;
- title/subtitle/byline/metadata;
- text přítomný na dané stránce;
- starts/continues/continuation evidence;
- relevance;
- verification a explicitní uncertainty;
- provenance k Technician source.

Machine schema je definováno v `src/business_brief/contracts.py` jako legacy `page-ingest-v2`, kompatibilní `page-ingest-v3` (PageIngestV3) a nový `page-ingest-v4` (PageIngestV4; D022).

Legacy v2 canonical Page JSON body patří do Supabase Storage pod logickým klíčem `page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.0/page-<NNNN>.json`. Konkrétní Supabase bucket je operational konfigurace a Chat jej nesmí hádat.

PostgreSQL slouží jako queryable operational index/state/provenance vrstva; primární JSON body zůstává ve Storage. Dedicated page-ingest tabulka se nesmí z Chatu improvizovat, pokud ještě není implementovaná.

## Assembler
Input: Page JSONy jednoho edition/source.

Output: canonical Article Records.

Assembler spojuje části článků napříč stránkami, ale nemá znovu interpretovat page layout. Nejasné případy musí být reviewable.

Article artefakty patří do Supabase Storage; identity, vztahy, provenance a stav do PostgreSQL.

## Composer
Composer pracuje nad Article Records více zdrojů a vytváří topic groupings/dossiers pro články o společném tématu.

Composer není Assignment Editor a nerozhoduje sám o finálním Brief selection.

## Translator
Translator navazuje na sestavené spolehlivé články/topic material. Je vhodným kandidátem pro API automatizaci, protože pracuje s již známým textem.

## Editorial
Editorial Workflow pracuje až nad spolehlivým obsahovým základem. Rozlišuje fakta, perspektivy autorů, cross-source synthesis, kontext a Business Brief commentary.

## Persistence
Supabase PostgreSQL: publications, editions, physical sources/arrivals, jobs, state, provenance, relations a další operational entities.

Supabase Storage: source inbox/archive, Technician artifacts, Page JSONs, assembled article artifacts a další validované artefakty.

Railway: workers a temporary workspace.

## State integrity
Immutable source a provenance jsou first-class. Ready state se nastavuje až po durable uploadu a validaci. Destruktivní cleanup inboxu je poslední krok.

## Observability
Dashboard má číst strukturovaný operational state. Zelený provoz patří na dashboard; alert je pro skutečnou integritu/deadline threat.

## Acquisition
Acquisition je oddělené upstream workflow. Technician není crawler/downloader. Odstraněný watcher není součást current architecture.

## Legacy: Ingestor v1.1 / Physical Map
ingestor-v4-physical-map-v1.1, physical-map.json jako povinný production handoff, Visual Page Map, BODY_FLOW, bbox/overlap matching a block-ID article assembly jsou superseded.

Jejich kód může dočasně zůstat v repository kvůli historii, testům nebo diagnostice, ale nesmí být považován za current production architecture.

Historické důvody a podmínky případného návratu jsou v project-memory/FAILURES.md a DECISIONS.md.

## Current extraction and generation boundary
Ordinary Chat uses the private Site v4 adapter for server-side verified image and inline OCR evidence; URLs/tokens never reach the model. Codex is for system development/debugging. See docs/INGESTOR.md §20 for adapter versions, limits and acceptance provenance.

Select primarily relevant articles, with uncertain candidates for review and exceptional irrelevant continuity/review evidence only. Preserve visually validated title/subtitle/byline/text_on_page/continuation; OCR supports the image. Normalize technical layout artifacts only. Do not summarize, paraphrase, translate or invent missing text. Perspective interpretation belongs downstream, not a required per-item object.

New page-ingest-v3 uses producer ingestor-v2.1-chat, instruction 2.1 and directory ingestor-v2.1; v2 and its ingestor-v2.0 key remain immutable compatibility artifacts. Bridge v3 validation and server-side generation mapping were deployed and page-1 acceptance passed on 2026-10-16 (CURRENT_STATE/HISTORY); this does not establish v4 asset support. Auth, JCS, durable binding/fencing, create-if-absent and readback semantics are retained. Assembler must select an explicitly accepted generation and exclude superseded acceptance content, regardless of historical usable_for_assembly=true.

## Article assets — canonical D022
**Text se rekonstruuje. Vizuální artefakty se nepřepisují, ale uchovávají.** `text_on_page` is visually verified continuous article prose. Charts, tables, photos, infographics, illustrations and other visuals are separate article-owned PNG crops, never canonical OCR transcripts. Minimal article fields remain; v4 adds `assets`, without required PerspectiveEvidence or rejected-item inventory.

The new exact generation is `page-ingest-v4` / `ingestor-v2.2-chat` / instruction `2.2` / namespace `ingestor-v2.2`. Keep v2/v3 serialization, keys and production objects immutable. Reuse the existing private `page-ingest` bucket. Canonical key: `page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.2/assets/page-<NNNN>/<asset_id>.png`; sibling Page JSON is `.../ingestor-v2.2/page-<NNNN>.json`. Page JSON carries exact bucket/key/SHA/size/dimensions; no new bucket or client-selected path.

Assets bind ownership (`page_item_id`, page), physical page bbox and authoritative PNG SHA to a logical text anchor (position, auxiliary paragraph index, authoritative surrounding anchor text). Assembler joins prose across pages first, then re-anchors by unique anchor text. A missing/ambiguous match remains `placement_needs_review` / unplaced; never guess from geometry or a stale paragraph index. Physical bbox remains provenance. Editorial may use, interpret or omit visuals while retaining the evidence.

The normative schema, bounds/anchor checks, storage and recovery rules are in docs/INGESTOR.md §21. The bridge now implements authoritative server-side PNG cropping and set-wide fenced create/readback before Page JSON. Text-only submissions may use artifact:null; strict persisted pages contain exact final metadata. Original-request and deterministic target/set bindings preserve source UUID/variant identity and partial-write reconciliation without overwrite/delete. Existing Site v4 generic transport needs no image bytes. CURRENT_STATE records actual deployment/acceptance; implementation alone does not imply production approval.

Current deployed v4 pin: `b6d465c49dbf546f0ea31876d218121428d495c8`, Railway `4489131f-d578-4062-b88f-40adc3716932` SUCCESS; one page-2 WSJ acceptance with three source-derived chart crops and set-wide verified readback is complete. Existing generic Site v4 required no redeploy; private bucket additively permits JSON/PNG. 226 tests pass. Exact acceptance and bounds are in CURRENT_STATE/HISTORY. Subsequent ordinary-Chat pages 3–10 are reported there with evidence limits; page 6 has a known visual defect. No assembly is evidenced.

## Visual acceptance and immutable correction boundary
D023 / INGESTOR §21.7 requires independent server-equivalent crop preview before visual_checked:true and persistence. Mechanical readback does not detect clipped visuals. Current bridge immutability provides no editorial revision protocol: retain defective originals, require Q014 for authorized corrections and explicit downstream supersession/selection. WSJ page 1 is evidenced as v2/v3, page 2 as v4; pages 3–10 are reported v4 with page-6 visual failure. No homogeneous all-v4 or fully visually accepted corpus is established.
