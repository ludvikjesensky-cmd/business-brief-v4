# Failures — Business Brief v4

## F001 — Rekonstrukce článků z technické/Physical Map
**Origin:** zejména v3.  
**Goal:** z fyzické mapy vydání spolehlivě rekonstruovat články a jejich continuations.  
**Result:** cesta byla křehká, publication/layout dependent a náročná na ověřování; pro ranní produkt nebyla spolehlivým univerzálním základem.  
**Lesson:** Physical Map je evidence, ne semantic truth.  
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
