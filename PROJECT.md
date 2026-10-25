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

Fast Editorial používá tři samostatné role / mentální režimy a single-entry briefingy, nikoli nutně tři samostatné konverzace. Pro běžný startup načti pouze briefing přidělené role a její vstupy; širší Project Memory ani čtvrtý workspace dokument nejsou potřeba:

- `docs/FAST_EDITORIAL_CHAT.md` = Issue Editor + jedno kompletní vydání → frozen Issue Map + povinné Editorial Notes → **STOP**.
- `docs/CROSS_PAPER_CHAT.md` = Cross-Paper Editor + 3 frozen Issue Maps (FT, WSJ, HB) a jejich Editorial Notes → Daily Topics / Cross-Paper Map + povinné Editorial Notes → **STOP**.
- `docs/NEWSROOM_CHAT.md` = Newsroom Editor + Daily Topics, Cross-Paper Notes, relevantní Deep Read a uncertainties → Master Brief, podpůrné artefakty a day retrospective → **STOP**.

**One day, one Editorial Chat. Multiple explicit roles. Frozen artifacts between roles.** Výchozí produkční model je jeden kontinuální Editorial Chat pro celý den: postupně nezávisle zpracuje FT, WSJ a HB, poté Cross-Paper a Newsroom. Uvedené tři soubory jsou role/mental-mode briefings. Jeden Chat může role projít postupně, ale každá další role vyžaduje explicitní nové zadání a explicitní načtení příslušného briefingu; dokončení předchozí role samo o sobě pokračování neopravňuje. Každé další vydání vyžaduje vlastní explicitní zadání Issue Editora. Hard STOP ukončuje aktuální roli / mentální režim, ne nutně celou konverzaci; po Master Briefu končí role Newsroom. Každý briefing samostatně obsahuje mission, redakční principy, workspace contract a vlastní hard STOP.

Kontinuita paměti Chatu je žádoucí, ale redakční nezávislost každé Issue Map je procesní pravidlo. Issue Editor posuzuje pouze aktuální vydání; ani při tvorbě WSJ/HB mapy nesmí předčasně syntetizovat cross-paper pohled nebo nechat předchozí tituly určovat její úsudek. Každá mapa se zmrazí před dalším vydáním. Frozen FT mapu nelze zpětně měnit po četbě WSJ/HB; pozdější poznatky patří do downstream artefaktů. Uložené artefakty jsou zdrojem explicitního stavu, verzí a rozhodnutí i při pokračování ve stejné konverzaci.

Samostatné Chaty zůstávají povolené pro paralelizaci, regresní testy nebo když kontext naroste, ale nejsou výchozí produkční model.

## Active branches
- **Fast Editorial:** independent edition-first morning editorial workflow inherited from the successful v3 experiment. Current task: reconstruct and port the live Chat Issue Map → cross-paper → Brief workflow. It must not depend on Deep/Memory infrastructure in this phase.
- **Deep / Memory:** canonical evidence and long-term knowledge path through Ingestor → Assembler → Article Records → Indexer → Enrichment/Memory. Composer D027 belongs here if implemented.
- Integration between the branches is deliberately unresolved; see D030.

## Detailed docs
- docs/FAST_EDITORIAL_CHAT.md — single entrypoint pouze pro Issue Editora; jedno vydání → frozen Issue Map → STOP
- docs/CROSS_PAPER_CHAT.md — single entrypoint pro Cross-Paper Editora; 3 frozen Issue Maps → Daily Topics → STOP
- docs/NEWSROOM_CHAT.md — single entrypoint pro Newsroom Editora; Daily Topics + Deep Read → Master Brief → STOP
- docs/PRODUCT.md — produkt, publikum a hodnoty
- docs/EDITORIAL.md — redakční filozofie a workflow
- docs/SYSTEM.md — technická architektura; obsahuje kanonický Assembler kontrakt a D029 repository implementation
- docs/INGESTOR.md — kanonické instrukce Ingestoru; §21 article assets / v4 kontrakt a rollout gate (D022)
- docs/INDEXER.md — kanonický design odvozeného search indexu, profily a post-check (D026); implementace zatím neproběhla
- docs/COMPOSER.md — Deep/Memory daily-topic-v1 grouping design inspired by v3 Cross-Paper Editor (D027); není Fast Editorial workflow; implementace zatím neproběhla
- docs/OPERATIONS.md — provoz, observability, náklady a gates
- docs/INFRASTRUCTURE.md — current production infrastructure, Hetzner/Caddy/Docker, DNS, secrets boundary, deploy/recovery and Railway historical boundary
- docs/SOURCES_RIGHTS.md — zdroje, acquisition a právní hranice
- docs/ENRICHMENT.md — enrichment-v1, Story Threads/Signals/Trends, provenance a promotion; offline validátory/helpers implementovány, perzistence Q019
- docs/EDITORIAL_MEMORY.md — produktová Editorial Memory; není Project Memory

Původní v4 dokumentace je po migraci zachována v docs.archive/ jako historický zdroj, nikoli kanonická autorita.

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
