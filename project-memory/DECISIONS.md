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


## D016 — ACTIVE — Ingestor zachovává perspective value konzervativně a page-level
**Date:** 2026-10-15.  
**Decision:** Ingestor v2.0 nefiltruje pouze podle event importance nebo tématu. Při nejistotě preferuje recall před agresivním vyřazením a zachovává kandidátní text pro downstream review.

U relevantních textů zachycuje page-level perspective evidence: autorskou otázku, framing, argument, distinctive angle, napětí/protiargumenty a otevřené otázky pouze v rozsahu, který podporuje aktuální stránka. Musí rozlišit observed_on_page, interpreted_from_page a unresolved_until_assembly.

Jasně nerelevantní položky zůstávají minimálně inventarizované kvůli completeness auditu.  
**Reason:** Business Brief nesmí ztratit texty, jejichž hodnota spočívá v perspektivě, a zároveň nesmí z jedné continuation stránky vyrábět definitivní interpretaci celého článku.  
**Consequences:** page-ingest-v2 nese explicitní PerspectiveEvidence; article-level perspective vzniká až po assembly a musí zachovat provenance/uncertainty.
