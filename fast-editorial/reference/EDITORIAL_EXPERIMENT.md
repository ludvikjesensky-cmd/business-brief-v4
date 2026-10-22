# Business Brief v3 — Fast Editorial 10-day Experiment

**Datum:** 29. 9. 2026  
**Stav:** aktivní experimentální protokol  
**Účel:** prakticky ověřit rychlou tvorbu Business Briefu nad trojicí deníků a oddělit ji od hluboké Article/Memory pipeline.

## 1. Hypotéza

Business Brief potřebuje dva různé procesy s jinou definicí úspěchu.

### A. Fast Editorial / Business Brief Production

Cíl:
- rychle pochopit celé vydání;
- zachytit hlavní články a témata;
- porovnat Financial Times, Wall Street Journal a Handelsblatt;
- vybrat témata pro ranní Business Brief;
- provést Deep Read pouze tam, kde je potřebný pro přesnost Briefu;
- publikovat Brief bez čekání na kompletní Memory pipeline.

První discovery mapa je záměrně provisional. Není canonical source truth.

Fast Editorial je **edition-first**. Každý titul vstupuje jako úplná Reference Edition (PDF nebo úplná uspořádaná sada page images). Webový feed nesmí nahradit hranice vydání.

### B. Deep Editorial / Web + Memory Production

Cíl:
- přesná source rekonstrukce;
- Coverage Gate;
- canonical `issue_items`;
- Verified/Normalized Articles;
- enrichment;
- překlad;
- summary;
- chunks;
- Memory;
- webový Detail článku.

Tato větev zůstává založena na frozen v3 source contracts.

## 2. Co zůstává kanonické z v3

Beze změny:
- `bbv3.sources`;
- `bbv3.workflow_runs`, `workflow_steps`, `workflow_events`, `workflow_artifacts`;
- Technician / Physical Map;
- Semantic Mapper / Reconciliation;
- Comparator / Coverage Gate;
- Article Map / Compiler;
- `bbv3.issue_items`;
- `bbv3.articles`;
- `bbv3.article_chunks`;
- Memory-ready gate.

Důležitá hranice:

> `editorial_map_items` jsou redakční hypotézy.  
> `issue_items` jsou canonical položky po Deep source pipeline.

Tyto významy se nesmějí směšovat.

## 3. Datový model Fast Editorial

### `bbv3.editorial_days`

Jeden redakční den experimentu nebo budoucí produkce.

Obsahuje:
- datum;
- `run_mode = experiment | production`;
- `experiment_key`;
- stav dne;
- očekávané publikace;
- metadata.

### `bbv3.editorial_day_sources`

Vazba konkrétního vydání v `sources` na redakční den.

Obsahuje:
- pořadí, v němž vydání přišlo;
- aktuální/frozen Issue Map workflow run;
- `map_status`;
- verzi mapy;
- čas zmrazení;
- souhrnné statistiky.

### `bbv3.editorial_map_items`

Provisional Issue Map jednoho vydání.

Jeden řádek = jeden redakční objekt, typicky článek, komentář nebo rozhovor.

Obsahuje:
- provisional identity;
- pořadí;
- titulek, deck, byline;
- stránky;
- stručný obsah;
- co je dnes nové;
- `priority = core | candidate | low`;
- důvod výběru;
- confidence;
- uncertainties;
- zda je vhodný pro Deep Read / Memory;
- pozdější vazbu na canonical `issue_items`.

Mapa je verzovaná přes `workflow_runs`. Frozen mapa se nepřepisuje. Nový pokus = nový run.

### `bbv3.daily_topics`

Cross-paper vrstva.

Jeden řádek = skutečné téma/příběh dne, nikoli jeden článek.

Obsahuje:
- český pracovní název;
- shrnutí;
- dnešní delta;
- proč je téma důležité;
- `decision = pending | include | reserve | exclude`;
- confidence;
- stav Deep Read.

### `bbv3.daily_topic_items`

M:N vazba mezi tématem a provisional články.

Role zdroje:
- `primary`;
- `supporting`;
- `contrasting`;
- `background`.

### `bbv3.daily_briefs`

Jedna verzovaná podoba Business Briefu.

Obsahuje:
- stav draft/verified/published/superseded;
- vazbu na workflow run;
- případný Markdown artifact;
- kompletní `content_md`.

### `bbv3.brief_items`

Strukturované položky výsledného Briefu.

Každá položka má přímou vazbu na `daily_topic`, takže provenance vede zpět přes všechny zdrojové články až k Reference Edition.

### `bbv3.editorial_notes`

Redakční laboratorní deník a **povinná auditní stopa experimentu**.

Editorial Notes nejsou jen technický log. Musí zachytit i redakční uvažování: co bylo v čísle silné, co bylo obtížné, co změnily další tituly, co se do Briefu dostalo nebo nedostalo a proč, kde vznikla nejistota a co jsme se naučili pro budoucí systém.

Povinné `note_type` pro každý den:
- `issue_map_snapshot` — snapshot frozen Issue Map;
- `process_observation` — bezprostřední poznámka po zpracování vydání;
- `issue_retrospective_detailed` — detailní retrospektiva každého deníku po dokončení dne;
- `cross_paper_map` — témata dne a redakční rozhodnutí;
- `deep_read_summary` — jeden záznam pro každý INCLUDE topic;
- `brief_build_notes` — detailní záznam o tvorbě celého Briefu;
- `day_retrospective` — závěrečný souhrn dne.

`issue_retrospective_detailed` musí minimálně obsahovat:
1. vstup, počet stran, OCR/text-layer stav;
2. způsob Discovery;
3. CORE / CANDIDATE / LOW;
4. charakter čísla a nejsilnější témata;
5. technické/layout problémy a pokračování článků;
6. unikátní redakční přínos titulu;
7. co se změnilo po příchodu dalších titulů;
8. počet INCLUDE/RESERVE topiců, do nichž titul přispěl, a kolikrát byl primární;
9. co se do Briefu nedostalo a proč;
10. quality guardrails a nejistoty;
11. lesson pro architekturu / automatizaci.

`brief_build_notes` musí minimálně obsahovat:
1. funnel issue items → daily topics → INCLUDE/RESERVE → verified Brief;
2. nejdůležitější cross-paper syntézy;
3. proč kvalitní položky zůstaly v RESERVE;
4. co změnil Deep Read;
5. verification guardrails;
6. délku a strukturu Briefu;
7. timing včetně caveatů;
8. použití/nepoužití Memory;
9. co se den naučil o architektuře;
10. otevřené otázky pro další dny.

Další poznatky lze zapisovat jako:
- `missed_article`;
- `false_positive`;
- `changed_decision`;
- `cross_paper_added_context`;
- `deep_read_changed_interpretation`;
- `continuation_problem`;
- `memory_would_help`;
- `automation_candidate`.

Note types nejsou databázově uzavřený enum. Povinný balík výše se ale od Day 1 drží konzistentně.

## 4. Denní protokol

### Krok 1 — první deník

1. Source je evidován v `bbv3.sources`.
2. Vznikne/aktualizuje se `editorial_day`.
3. Source se připojí přes `editorial_day_sources`.
4. Vznikne `workflow_run(role='editorial_discovery')`.
5. LLM projde celé vydání.
6. Zapíše `editorial_map_items`.
7. Vytvoří Markdown Issue Map jako derived artifact.
8. Zapíše Issue-level Editorial Notes.
9. Run se uzavře DONE.
10. `map_status` se nastaví na `frozen` + `frozen_at`.

Po zmrazení se mapa při čtení dalších deníků zpětně neupravuje.

### Krok 2 — druhý a třetí deník

Stejný proces, nezávisle.

Tím vzniknou tři frozen Issue Maps.

### Krok 3 — Cross-Paper Editor

1. Vznikne `workflow_run(role='cross_paper_editor')`.
2. Porovnají se především CORE + CANDIDATE položky.
3. Vytvoří se `daily_topics`.
4. Články se připojí přes `daily_topic_items`.
5. Každý topic dostane include/reserve/exclude.
6. Vznikne Markdown Cross-Paper Map.

### Krok 4 — Deep Read pro Brief

Deep Read se provádí pouze pro témata, kde je potřebný pro kvalitu výsledného Briefu.

Může zahrnovat:
- dohledání pokračování;
- kontrolu celého textu;
- čísla;
- grafy;
- rozdíly mezi zdroji;
- kontrolu argumentace;
- relevantní Memory context.

Deep Read pro Brief není totéž co kompletní canonical Deep/Memory pipeline.

### Krok 5 — Editorial Workflow v1

Po Deep Read se finální Brief nesmí skládat jedním nerozlišeným „synthesis“ krokem.

Použije se kanonický [EDITORIAL_WORKFLOW.md](EDITORIAL_WORKFLOW.md) a jeho pracovní instrukce v [EDITORIAL_PLAYBOOK.md](EDITORIAL_PLAYBOOK.md):

1. Assignment Editor — co patří do vydání a jak velké;
2. Dramaturg — pořadí, rytmus, spojování a hierarchie;
3. Story Editor — fact / angle / tension / Detail promise;
4. Brief Writer — první text podle PRODUCT_MODEL struktury;
5. Detail Editor — kontrola, že Brief nevyčerpal legitimní hodnotu Detailu;
6. Verification Editor — fakta, nejistoty a provenance;
7. Language & Style Editor — čeština, rytmus a poslouchatelnost;
8. Editor-in-Chief — coverage, hierarchy a curiosity gate.

Role jsou redakční průchody, nikoli povinně samostatné technické agenty.

### Krok 6 — Brief

1. Vznikne `daily_brief`.
2. Jednotlivé části se uloží do `brief_items`.
3. Kompletní lidská verze se uloží jako `content_md`.
4. Markdown Business Brief se uloží do `bbv3-derived` a registruje ve `workflow_artifacts`.
5. Po finálním Editor-in-Chief gate se status mění na verified/published.

### Krok 7 — Editorial Notes

Editorial Notes jsou **povinný výstup každého kroku**, ne až závěrečný dovětek.

Po každém deníku vzniknou:
1. `issue_map_snapshot`;
2. `process_observation`.

Po dokončení všech tří titulů a Briefu se ke každému deníku doplní:
3. `issue_retrospective_detailed`.

Na úrovni celého dne vzniknou:
4. `cross_paper_map`;
5. `deep_read_summary` pro každý INCLUDE topic;
6. `brief_build_notes`;
7. `day_retrospective`.

Poznámky musí zachytit nejen technické problémy, ale i změny redakčního úsudku, důvody INCLUDE/RESERVE, quality guardrails, použití Memory, časovou náročnost a otevřené otázky pro další den.

Na konci dne lze z těchto záznamů vytvořit `day-dossier.md`.

## 5. Markdown artifacts

Markdown není canonical databáze. Je lidsky čitelné vykreslení a redakční paměť.

Doporučené cesty v `bbv3-derived`:

```
editorial/YYYY-MM-DD/
  handelsblatt/issue-map-v1.md
  financial-times/issue-map-v1.md
  wall-street-journal/issue-map-v1.md
  cross-paper-map-v1.md
  business-brief-v1.md
  editorial-notes.md
  day-dossier.md
```

Každý uložený artifact se registruje v `bbv3.workflow_artifacts`.

## 6. Vazba Fast → Deep

Pokud pozdější canonical pipeline vytvoří `bbv3.issue_items`, původní provisional item se může propojit přes:

- `editorial_map_items.canonical_issue_item_id`;
- `canonical_match_status`.

Statusy:
- matched;
- split;
- merged;
- not_found;
- false_positive.

Toto je základ budoucího objektivního měření Fast Editorial kvality.

## 7. Co budeme po 10 dnech měřit

Minimálně:
- počet mapovaných článků na vydání;
- CORE/CANDIDATE/LOW;
- podíl CORE/CANDIDATE použitých ve výsledném Briefu;
- kolik témat vzniklo až cross-paper porovnáním;
- kolik rozhodnutí změnil Deep Read;
- kolik článků discovery minulo;
- kolik provisional položek se později ukázalo jako split/merge/false positive;
- kolikrát byla potřeba přesná rekonstrukce;
- kolikrát Memory změnila interpretaci;
- kolik času/práce přinesla každá vrstva.

## 8. Anti-overfitting pravidlo

Během deseti dní se pravidla nemění při každém atypickém vydání.

Nové problémy se zapisují do Editorial Notes.

Změna datového contractu nebo algoritmu se provede až tehdy, když:
- jde o obecný opakující se problém;
- nebo je stávající model objektivně neschopný důležitý případ zachytit.

Jedno zvláštní rozložení jedné stránky není důvodem pro publication-specific hack.

## 9. Bezpečnost a přístup

Fast Editorial tabulky jsou interní server-side data:
- RLS enabled;
- `anon` a `authenticated` bez přístupu;
- CRUD pouze `service_role`;
- stejný model jako ostatní interní tabulky `bbv3`.

## 10. Aktuální stav

K 29. 9. 2026, ověřeno proti Supabase:

### Day 1 — 14 September 2026 — COMPLETE

- 3 frozen Reference Editions;
- 102 provisional editorial items;
- 24 cross-paper topics;
- Brief v1: verified baseline;
- Master Brief v2: verified;
- Editorial Workflow v1 + Editorial Playbook v1 ověřily, že lepší kompozice výrazně zlepšuje hierarchy, rhythm a coverage nad stejným informačním materiálem;
- v databázi existují 2 verified `daily_briefs` pro Day 1.

### Day 2 — 15 September 2026 — COMPLETE

- 3 frozen Reference Editions;
- 112 provisional editorial items;
- 28 cross-paper topics;
- 1 verified Brief;
- Day 2 potvrdil opakovatelnost Fast Editorial konceptu a schopnost pracovat s cross-day continuity / daily delta.

### Day 3 — 16 September 2026 — COLLECTING

- Financial Times: frozen Issue Map, 38 provisional items;
- Wall Street Journal: frozen Issue Map, 38 provisional items;
- Handelsblatt: Reference Edition zatím chybí;
- 0 cross-paper topics;
- 0 Briefs;
- editorial day zůstává správně ve stavu `collecting`.

Day 3 se nesmí počítat jako dokončený třídenní test, dokud nebude přidáno Handelsblatt.

### Known persistence gap

`brief_items` jsou zatím materializované pouze pro Day 1 Brief v1 (13 rows). Day 1 v2 a Day 2 verified Brief existují v `daily_briefs.content_md`, ale jejich structured `brief_items` ještě nejsou doplněné. To je provozní backlog, ne ztráta ověřeného Briefu.

### Experiment pause reason

Experiment byl přerušen kvůli praktickému získání kompletního Handelsblatt vydání, nikoli kvůli selhání Fast Editorial modelu.

Aktuální source-access postup je v [SOURCE_ACQUISITION.md](SOURCE_ACQUISITION.md). Po získání Day 3 Handelsblatt Reference Edition pokračuje experiment stejným protokolem.
