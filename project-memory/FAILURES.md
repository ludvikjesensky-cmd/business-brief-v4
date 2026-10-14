# Failures — Business Brief v4

## F001 — Rekonstrukce článků z technické/Physical Map
**Origin:** zejména v3.  
**Goal:** z fyzické mapy vydání spolehlivě rekonstruovat články a jejich continuations.  
**Result:** cesta byla křehká, publication/layout dependent a náročná na ověřování; pro ranní produkt nebyla spolehlivým univerzálním základem.  
**Lesson:** Physical Map je evidence, ne semantic truth.  
**2026-10-12 clarification:** opuštěna je inference sémantiky pouze z Physical Map, nikoli její použití jako textové/geometrické evidence. D013 zkouší externí vision mapu; dílčí výsledky a limity jsou v docs/SYSTEM.md. F001 zůstává relevantní.  
**Retry only if:** nová metoda prokáže na malém reálném corpus výrazně lepší spolehlivost/cenu a nevrací projekt k publication-specific patchování.

## F002 — Předčasná složitost pipeline
**Origin:** v1–v3.  
**Result:** technická architektura a množství rolí/dokumentů rostly rychleji než ověřená čtenářská hodnota.  
**Lesson:** architecture follows verified product; role ≠ agent ≠ API call.

## F003 — Fast Editorial full-edition API economics
**Origin:** v4, WSJ 9 Oct 2026.  
**Approach:** page-level model calls + issue synthesis pro celé vydání.  
**Observed:** přibližně USD 7.95 za jediný reálný průchod, kolem 49 requests podle zaznamenaného experimentu.  
**Impact:** nepřijatelné pro rutinní ranní provoz v této podobě.  
**Retry only if:** cost model je předem spočítán a malý acceptance test prokáže přijatelnou cenu při zachování kvality.

## F004 — WSJ automatic watcher/acquisition
**Origin:** v4.  
**Result:** watcher nebyl dostatečně spolehlivý a byl odstraněn z Railway i experimentální větve.  
**Lesson:** acquisition nesmí být skrytý předpoklad downstream pipeline.  
**Retry only if:** existuje nová spolehlivá acquisition capability a je ověřena odděleně.

## F005 — Handoff/status proliferation
**Origin:** v1–v4 documentation.  
**Result:** STATUS, HANDOFF, NEW_CONVERSATION_HANDOFF, V4_HANDOFF, dated PROGRESS a další dokumenty soutěžily o autoritu.  
**Lesson:** jeden PROJECT.md + jeden CURRENT_STATE; history/decisions/failures mají vlastní domovy.

## F006 — Automatizovat před ověřením editorial workflow
**Origin:** zkušenost v2–v4.  
**Result:** technicky funkční automatizace neprokazuje editorial value.  
**Lesson:** nejdřív skutečný referenční den a lidské acceptance, potom škálování.

## F007 — Překrývající se Railway deploye/logy při full-issue render testu
**Date / origin:** 2026-10-12, WSJ 26 stran; dostupný konverzační záznam, ne nový audit Railway.  
**Goal:** rozšířit Visual Page Map ověření na celé vydání.  
**Attempt:** dočasná laboratorní render funkce; po kontaktním listu stran 1–4 render zbývajících stran 5–26 po skupinách.  
**Observed:** více překrývajících se deployů téže funkce, výstup se nevracel čistě a velké base64 logy komplikovaly návrat výsledků. Práce přešla do čekání/opakovaného pollingu a byla uživatelem přerušena. Full-issue validation nebyla dokončena.  
**Cause:** podle pracovního záznamu orchestrace deployů a přenos obrázků přes logy; přesná runtime příčina nebyla při konsolidaci nezávisle ověřena. Není to důkaz selhání semantic layout metody.  
**Cost/risk:** ztracený čas a nejasný stav testu; žádný placený Fast Editorial/OpenAI API nebyl spuštěn, produkční pipeline se neměnila.  
**Retry only if:** ověřit živý stav a zabránit souběhu deployů; sekvenční malé dávky (návrh 4 strany), kompaktní logy a oddělený přenos artefaktů. Render/contact sheet nepovažovat za article assembly validation.

## F008 — Platný layout JSON / vysoké pokrytí bez sémantické správnosti
**Origin:** navazující placené WSJ/HB Visual Page Map testy, protokol2026-10-14.
**Observed:** split narrative do infografiky, crossword contamination, neúplné titulky, pozdní standfirst a nepřesné footprinty; blokové pokrytí tyto chyby neodhalilo. V1.1 opravuje některé role, ale výsledky zůstávají smíšené.
**Lesson:** hodnotit skutečné články a reading order, odděleně od schema valid/full completion. Native HB duplicity navíc vznikají už před vision. Timeout neprokazuje selhání modelu a má neznámý billing.
**Retry only if:** explicitní malý kontrolní vzorek, přesná provenance konfigurace, omezená volání a lidský textový/vizuální audit; ne další plošný běh naslepo. Metriky mají jediný domov v docs/reference-days/visual-map-validation-2026-10-14.md.
