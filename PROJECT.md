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

Fast Editorial je nyní ve stavu **CANDIDATE READY FOR ACCEPTANCE** po dokončeném Closure Passu.

Předchozí aktivní návrh Fast Editorial byl 2026-10-25 pozastaven a přesunut do:

- `docs/suspended/fast-editorial-pre-greenfield/`

Tyto soubory jsou historický návrh pro srovnání, nikoli současné operating instructions.

Nový Fast Editorial vzniká odděleně v:

- `docs/fast-editorial/FAST_EDITORIAL_START_HERE.md` — hlavní úplné předání know-how novému editorovi
- `docs/fast-editorial/README.md` — orientace v greenfield adresáři
- `docs/fast-editorial/reference/FAST_EDITORIAL_START_HERE_V3_CHAT_SOURCE.md` — nedotčený zdrojový návrh původního v3 Chatu
- `docs/fast-editorial/00_...09_...` — podpůrná rekonstrukční a vývojová reference, nikoli běžný startup

Výchozí mechanický řetězec rekonstruovaný z původního úspěšného v3 Chat experimentu je:

```
Independent Issue Maps
→ Cross-Paper
→ Selective Deep Read
→ eight Editorial Review passes
→ verified Master Brief
```

Nový proces zatím **není canonical**, ale technická a dokumentační Closure specifikace je uzavřená. Hlavním kandidátem je `docs/fast-editorial/FAST_EDITORIAL_START_HERE.md`: úplné předání, které používá zkušenost původního v3 Chatu jako kostru, odstraňuje historickou technickou infrastrukturu a přímo integruje produktový a redakční duch Business Brief v4. Původní rekonstrukční soubory zůstávají referencí pro audit a regresní srovnání.

Do dokončení této rekonstrukce nepoužívej suspended briefingy jako instrukce pro nový Fast Editorial a nevytvářej podle nich další architekturu.

**Fresh Fast Editorial Chat startup:** načti celý `FAST_EDITORIAL_START_HERE.md`, handover contract `docs/fast-editorial/EDITORIAL_HANDOVER.md`, skutečný current state z `fast_editorial.handover_state`, autentické schválené V3 kalibrační Briefy z `docs/fast-editorial/reference/V3_APPROVED_MASTER_BRIEFS.md` a relevantní durable Reference Editions/artefakty. Nový Chat pak stručně vlastními slovy potvrdí hodnotu produktu, aktuální stav, frozen/closed hranice, zděděné opravy a další konkrétní krok; nejde o novou schvalovací bránu.


## Active branches
- **Fast Editorial:** CANDIDATE READY FOR ACCEPTANCE. The previous design is SUSPENDED. `docs/fast-editorial/FAST_EDITORIAL_START_HERE.md` is the current complete handoff candidate combining the proven v3 live-Chat method with the Business Brief v4 editorial purpose. Validate it against authentic historical Briefs and clean-Chat regression tests before declaring it canonical. It must not depend on Deep/Memory infrastructure in this phase.
  - Persistence v1 is implemented in Supabase project `business-brief-v4`, private schema `fast_editorial`; concrete operational Editorial Notes, Issue Maps, Topics, Brief versions, gates and handover state belong there. GitHub holds the method and migrations. See migrations `20261025210000_add_fast_editorial_v1.sql` and `20261025210500_add_fast_editorial_v1_fk_indexes.sql`.
  - Master Editorial Truth is now explicit: each Brief version has canonical `content_json` + human-readable `content_markdown`; channel adaptations live in `fast_editorial.channel_outputs` and may be generated only from a VERIFIED Brief. See migration `20261025212000_add_master_editorial_truth_and_channel_outputs_v1.sql`.
  - Closure Pass 2026-10-25: durable Reference Edition input contract, append-only Editorial Notes, freeze/verification/channel invariants, exact Brief sealing after final gates, authentic Day 1 v2 / Day 2 v1 calibration, handover contract and Publishing boundary are implemented. One genuinely clean-Chat regression remains before canonical status.
- **Deep / Memory:** canonical evidence and long-term knowledge path through Ingestor → Assembler → Article Records → Indexer → Enrichment/Memory. Composer D027 belongs here if implemented.
- Integration between the branches is deliberately unresolved; see D030.

## Detailed docs
- docs/fast-editorial/FAST_EDITORIAL_START_HERE.md — hlavní úplné metodické a redakční předání novému Fast Editorial Chatu; zatím kandidát, ne canonical
- docs/fast-editorial/README.md — orientace, startup model a otevřené validační kroky
- docs/fast-editorial/reference/FAST_EDITORIAL_START_HERE_V3_CHAT_SOURCE.md — nedotčený zdrojový návrh od původního v3 experimentálního Chatu
- docs/fast-editorial/00_...09_... — podpůrná rekonstrukční / vývojová reference, nikoli normální startup surface
- docs/suspended/fast-editorial-pre-greenfield/ — SUSPENDED předchozí návrh; pouze historické srovnání, ne operating instructions
- docs/PRODUCT.md — produkt, publikum a hodnoty
- docs/EDITORIAL.md — redakční filozofie a workflow
- docs/SYSTEM.md — technická architektura; obsahuje kanonický Assembler kontrakt a D029 repository implementation
- docs/INGESTOR.md — kanonické instrukce Ingestoru; §21 article assets / v4 kontrakt a rollout gate (D022)
- docs/INDEXER.md — kanonický kontrakt a implementace odvozeného search indexu (D026/Q017); runtime je nasazen na Hetzneru, WSJ plan/persist/replay prošel, multilingual retrieval calibration pokračuje
- docs/COMPOSER.md — Deep/Memory daily-topic-v1 grouping design inspired by v3 Cross-Paper Editor (D027); není Fast Editorial workflow; implementace zatím neproběhla
- docs/OPERATIONS.md — provoz, observability, náklady a gates
- docs/INFRASTRUCTURE.md — current production infrastructure, Hetzner/Caddy/Docker, DNS, secrets boundary, deploy/recovery and Railway historical boundary\n- docs/RUNNER.md — merged server-side Deep/Memory runner and Chat-facing tool contract; Hetzner deployment/acceptance still pending
- docs/SOURCES_RIGHTS.md — zdroje, acquisition a právní hranice
- docs/ENRICHMENT.md — enrichment-v1, Story Threads/Signals/Trends, provenance a promotion; offline validátory/helpers implementovány, perzistence Q019
- docs/EDITORIAL_MEMORY.md — produktová Editorial Memory; není Project Memory

## Storage
KNOWLEDGE: toto Repository, zejména PROJECT.md, project-memory/ a docs/.
SOURCE: kód, SQL migrace a kontrakty v Repository; source editions v provozním storage.
PRODUCTION: Hetzner/Caddy/Docker runtime; Supabase operational database/storage. Railway is historical provenance, not the current critical runtime.
ARTIFACTS: validované source, page-ingest a editorial artefakty v Supabase Storage a budoucí publikační výstupy.
OPERATIONAL: Supabase je autoritativní pro jobs, state, provenance, eventy a artefakty; Hetzner je current compute/web runtime. Railway již není součást current critical production path.

## Critical rules
Před návrhem starého přístupu čti FAILURES. Nezaměňuj extraction completeness za editorial selection. Neautomatizuj placený modelový workflow před změřeným acceptance testem. Provenance se nesmí ztratit.

Fast Editorial a Deep/Memory jsou podle D030 samostatné větve. Fast Editorial nesmí být podmíněn canonical Article Records, Indexerem, Enrichmentem, Composerem ani Memory, dokud nové explicitní rozhodnutí neurčí jinak.

Business Brief nesmí redukovat zdrojový text na „co se stalo“. Musí zachovat mediální a autorskou perspektivu, otázku, rámování a argumentaci, pokud právě v nich spočívá hodnota textu.

Technician připravuje technickou evidenci. Ingestor (ordinary Chat) je živá Chat role, zpracovává jednu stránku po druhé a vytváří ověřený JSON pro každou stránku. Ingestor v1.1 / Physical Map production path je superseded a neaktivní. Staré v1–v3 Projects jsou historické zdroje znalosti, ne current code dependencies.

## Article assets bootstrap
Read `project-memory/DECISIONS.md` D022 and `docs/INGESTOR.md` §21 for the accepted article-assets model, dual page/text anchors and private `page-ingest` crop layout. v4 is a new immutable generation; v2/v3 stay readable and untouched. The writer was deployed and page-2 acceptance is receipt-backed; full-corpus acceptance remains gated by evidence reconciliation and the page-6 visual defect (CURRENT_STATE, F011). **Text se rekonstruuje. Vizuální artefakty se nepřepisují, ale uchovávají.**
