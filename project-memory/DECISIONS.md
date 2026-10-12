# Decisions — Business Brief v4

## D001 — ACTIVE — v4 mění hodnotu z pouhé informovanosti na přenos perspektivy
**Decision:** Produkt nepřenáší jen co se stalo, ale co kvalitní autoři v tématu vidí, jak argumentují a co zůstává otevřené.  
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

## D006 — ACTIVE — Physical Map je evidence, ne článek
Ingestor nesmí do fyzické reprezentace vkládat editorial význam.
**Clarification 2026-10-12 (D015):** Ingestor nyní vlastní také oddělenou Visual Page Map. Neutralita se vztahuje na Physical Map; její kontrakt se sémantikou nemění.

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

## D013 — ACTIVE — Sémantický layout určuje vision, Physical Map poskytuje text
**Date:** 2026-10-12.  
**Scope:** přijatý směr laboratorního experimentu, nikoli produkční rollout.  
**Decision:** model mapuje, jak člověk stránku čte, včetně explicitních BODY_FLOW zón a reading order; Python mapu vykonává geometricky nad Physical Map. Nepokračovat v rekonstrukci sémantiky z pouhé geometrie.  
**Reason:** dílčí výsledky stran 5 a 2 přinesly funkční tok textu; přetrvávající chyby jsou zejména na hranicích objektů.  
**Consequences:** zachovat D006 a znalost F001; tento přístup je nová podmínka pro experiment, nikoli popření předchozího failure. Schéma a evidence jsou v [SYSTEM](../docs/SYSTEM.md#visual-page-map--semantic-layout--experiment-wsj-2026-10-12). D007/D011 zůstávají ACTIVE. Implementační kontrakt a konfigurovatelné defaults nyní definuje D014; full-issue kvalita, empirický overlap práh a ekonomika nejsou ověřené.

## D014 — ACTIVE — Lokální kontrakt Visual Page Map v1 a auditovatelné vykonání
**Date:** 2026-10-12.
**Scope:** implementace samostatného experimentálního tooling, žádný produkční rollout.
**Decision:** normalized top-left bboxy, explicitní BODY_FLOW, plné object footprints, jednotlivé block assignments a source/image/layout provenance. Overlap používá union průniků / plochu textového bboxu; pracovní photo default >60 % je nastavitelný a zůstává předmětem acceptance. Cross-page merge vyžaduje schválenou explicitní vazbu a printed cue, ne podobné téma.
**Reason:** reprodukovatelný kontrakt umožňuje testovat geometrii nezávisle na placeném modelu a chrání před ztrátou/duplikací zdrojových bloků.
**Consequences:** sekvenční lokální proces, durable mapy/attempts, žádné automatické placené retries; offline cesta nevyžaduje API. Live API vyžaduje explicitní model/opt-in a limit calls. `all_pages_processed` a `needs_review` jsou odlišné věci. D007/D011 a otevřené Q001/Q009/Q010 zůstávají platné; implementace není potvrzení kvality WSJ ani ceny.

## D015 — ACTIVE — Ingestor tvoří obě mapy, Assembler sestavuje články
**Date:** 2026-10-12.
**Decision:** Visual Page Mapper je interní fáze Ingestoru. Ingestor produkuje Physical Map i Visual Page Map jako oddělené artefakty se společnou proveniencí. Samostatný Assembler tyto mapy vykonává a skládá články; editorial výběr následuje až za ním.
**Reason:** uživatel explicitně upřesnil hranice rolí. Tvorba map patří k ingestion, geometrické sestavení je samostatná auditovatelná odpovědnost. Role nevyžaduje vlastní službu ani API volání.
**Consequences:** lokální `bb-ingestor` nevytváří assembled text a předává `ingestor-output.json`; `bb-assembler` kontroluje identitu/hash map a vykonává deterministické sestavení bez modelových calls. D006 zůstává ACTIVE pro neutrální Physical Map. D013/D014 zůstávají platné jako dělba vision úsudku a geometrického vykonání; mapper už není samostatná top-level role. Produkční queue worker zatím zůstává Physical Map-only a není automaticky přepnut.
