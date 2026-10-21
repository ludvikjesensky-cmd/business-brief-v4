# Business Brief v4 — Project

**Status:** ACTIVE
**Family:** business-brief
**Generation:** v4
**Repository:** ludvikjesensky-cmd/business-brief-v4

## Purpose
Business Brief zpřístupňuje českému profesionálnímu čtenáři hodnotu kvalitního světového ekonomického a business tisku.

Nepřenáší pouze to, co se stalo. Přenáší především **způsob, jakým o tématu konkrétní médium a autor přemýšlejí a píší**: jak problém rámují, jakou otázku kladou, jak vedou argumentaci, na co kladou důraz, co zpochybňují, jaké rozpory vidí a jaké nové souvislosti otevírají.

Cílem není jen informovat, ale přenášet texty a perspektivy, které dokážou měnit, zpřesňovat nebo prohlubovat čtenářovo vnímání tématu.

Hlavní teze v4: **Není hlavní, na co se díváš. Hlavní je, co vidíš.**

## Read first
Běžné navázání: project-memory/SCOPE.md → project-memory/CURRENT_STATE.md.

Před architektonickou změnou navíc čti ARCHITECTURE.md, DECISIONS.md, FAILURES.md a OPEN_QUESTIONS.md. Pro strategii a návrat ke starším přístupům čti HISTORY.md a LESSONS.md.

Pro práci v roli Ingestoru načti po PROJECT/SCOPE/CURRENT_STATE také docs/INGESTOR.md.

## Detailed docs
- docs/PRODUCT.md — produkt, publikum a hodnoty
- docs/EDITORIAL.md — redakční filozofie a workflow
- docs/SYSTEM.md — technická architektura
- docs/INGESTOR.md — kanonické instrukce Ingestoru; §21 article assets / v4 kontrakt a rollout gate (D022)
- docs/INDEXER.md — kanonický design odvozeného search indexu, profily a post-check (D026); implementace zatím neproběhla
- docs/COMPOSER.md — kanonický daily-topic-v1 / Cross-Paper Editor design, provenance a review gates (D027); implementace zatím neproběhla
- docs/OPERATIONS.md — provoz, observability, náklady a gates
- docs/SOURCES_RIGHTS.md — zdroje, acquisition a právní hranice
- docs/ENRICHMENT.md — enrichment-v1, Story Threads/Signals/Trends, provenance a promotion; offline validátory/helpers implementovány, perzistence Q019
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

Business Brief nesmí redukovat zdrojový text na „co se stalo“. Musí zachovat mediální a autorskou perspektivu, otázku, rámování a argumentaci, pokud právě v nich spočívá hodnota textu.

Technician připravuje technickou evidenci. Ingestor (ordinary Chat) je živá Chat role, zpracovává jednu stránku po druhé a vytváří ověřený JSON pro každou stránku. Ingestor v1.1 / Physical Map production path je superseded a neaktivní. Staré v1–v3 Projects jsou historické zdroje znalosti, ne current code dependencies.

## Article assets bootstrap
Read `project-memory/DECISIONS.md` D022 and `docs/INGESTOR.md` §21 for the accepted article-assets model, dual page/text anchors and private `page-ingest` crop layout. v4 is a new immutable generation; v2/v3 stay readable and untouched. The writer was deployed and page-2 acceptance is receipt-backed; full-corpus acceptance remains gated by evidence reconciliation and the page-6 visual defect (CURRENT_STATE, F011). **Text se rekonstruuje. Vizuální artefakty se nepřepisují, ale uchovávají.**
