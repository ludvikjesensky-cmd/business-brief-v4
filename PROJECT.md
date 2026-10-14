# Business Brief v4 — Project

**Status:** ACTIVE
**Family:** business-brief
**Generation:** v4
**Repository:** ludvikjesensky-cmd/business-brief-v4

## Purpose
Business Brief zpřístupňuje českému profesionálnímu čtenáři hodnotu kvalitního světového ekonomického a business tisku. Nepřenáší jen události, ale také to, co jejich autoři vidí: otázky, argumenty, perspektivy, rozpory a souvislosti.

Hlavní teze v4: **Není hlavní, na co se díváš. Hlavní je, co vidíš.**

## Read first
Běžné navázání: project-memory/SCOPE.md → project-memory/CURRENT_STATE.md.

Před architektonickou změnou navíc čti ARCHITECTURE.md, DECISIONS.md, FAILURES.md a OPEN_QUESTIONS.md. Pro strategii a návrat ke starším přístupům čti HISTORY.md a LESSONS.md.

Pro práci v roli Ingestoru načti po PROJECT/SCOPE/CURRENT_STATE také docs/INGESTOR.md.

## Detailed docs
- docs/PRODUCT.md — produkt, publikum a hodnoty
- docs/EDITORIAL.md — redakční filozofie a workflow
- docs/SYSTEM.md — technická architektura
- docs/INGESTOR.md — kanonické pracovní instrukce Ingestoru v2.0
- docs/OPERATIONS.md — provoz, observability, náklady a gates
- docs/SOURCES_RIGHTS.md — zdroje, acquisition a právní hranice
- docs/EDITORIAL_MEMORY.md — produktová Editorial Memory; není Project Memory

Původní v4 dokumentace je po migraci zachována v docs.archive/ jako historický zdroj, nikoli kanonická autorita.

## Storage
KNOWLEDGE: toto Repository, zejména PROJECT.md, project-memory/ a docs/.
SOURCE: kód, SQL migrace a kontrakty v Repository; source editions v provozním storage.
PRODUCTION: Railway/Supabase runtime a dočasné workspaces.
ARTIFACTS: validované source, page-ingest a editorial artefakty v Supabase Storage a budoucí publikační výstupy.
OPERATIONAL: Supabase je autoritativní pro jobs, state, provenance, eventy a artefakty; Railway je výpočetní/workspace vrstva.

## Critical rules
Před návrhem starého přístupu čti FAILURES. Nezaměňuj extraction completeness za editorial selection. Neautomatizuj placený modelový workflow před změřeným acceptance testem. Provenance se nesmí ztratit.

Technician připravuje technickou evidenci. Ingestor v2.0 je živá Chat role, zpracovává jednu stránku po druhé a vytváří ověřený JSON pro každou stránku. Ingestor v1.1 / Physical Map production path je superseded a neaktivní. Staré v1–v3 Projects jsou historické zdroje znalosti, ne current code dependencies.
