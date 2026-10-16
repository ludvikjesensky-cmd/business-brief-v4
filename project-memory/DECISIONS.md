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

## D011 — ACTIVE — Paid Fast Editorial automation je pozastavena
Po reálném WSJ běhu s nepřijatelným API nákladem se nesmí automaticky plánovat další placené full-edition runs bez cost redesignu a malého acceptance testu.

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
