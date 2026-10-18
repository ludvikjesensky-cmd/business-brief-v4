# Architecture — Business Brief v4

Architektura odděluje technickou přípravu zdroje, page-level interpretaci, skládání článků, cross-source kompozici, překlad, editorial judgment a publikaci.

## Canonical flow

closed source edition  
→ Technician  
→ validated Source Bundle  
→ Ingestor Access Bridge (authorized evidence access)
→ **Ingestor (ordinary Chat)**
→ Ingestor Access Bridge (validation + verified canonical persistence)
→ one verified Page JSON per source page  
→ Assembler  
→ canonical Article Records  
→ Composer  
→ Topic Dossiers / cross-source groupings  
→ Translator  
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

## Composer
Composer pracuje nad canonical Article Records více publikací. Seskupuje články, které se týkají společného tématu nebo příběhu, a vytváří topic dossier. Není to ještě finální editorial selection.

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

Current deployed v4 pin: `b6d465c49dbf546f0ea31876d218121428d495c8`, Railway `4489131f-d578-4062-b88f-40adc3716932` SUCCESS; one page-2 WSJ acceptance with three source-derived chart crops and set-wide verified readback is complete. Existing generic Site v4 required no redeploy; private bucket additively permits JSON/PNG. 226 tests pass. Exact acceptance and bounds are in CURRENT_STATE/HISTORY. Subsequent ordinary-Chat pages 3–10 are reported there with evidence limits; page 6 has a known visual defect. No assembly is evidenced.

## Visual acceptance and immutable correction boundary
D023 / INGESTOR §21.7 requires independent server-equivalent crop preview before visual_checked:true and persistence. Mechanical readback does not detect clipped visuals. Current bridge immutability provides no editorial revision protocol: retain defective originals, require Q014 for authorized corrections and explicit downstream supersession/selection. WSJ page 1 is evidenced as v2/v3, page 2 as v4; pages 3–10 are reported v4 with page-6 visual failure. No homogeneous all-v4 or fully visually accepted corpus is established.
