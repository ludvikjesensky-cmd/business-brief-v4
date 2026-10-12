# System — Business Brief v4

## Boundary
Technická vrstva připravuje evidence. Editorial vrstva interpretuje. Publishing distribuuje schválenou redakční pravdu.

## Technician
Input: uzavřené source edition. Output: validovaný Source Bundle. Odpovědnosti: identity, immutable original, SHA/provenance, container validation, OCR decision/derivative, page renders, mechanical split, manifest, atomic handoff. Žádná editorial interpretace.

## Ingestor
Input: Source Bundle. Output: neutral Physical Map / evidence representation. Odpovědnost je geometrie, text a fyzická struktura, nikoli article/editorial truth.

## Editorial
Fast Editorial prokázal možnost page-level discovery, ale jeho současný full-edition cost profile není přijatelný jako default production architecture. Budoucí editorial design musí respektovat tuto zkušenost.

## Persistence
Supabase PostgreSQL: publications, editions, physical sources/arrivals, jobs, state, provenance, events a další operational entities. Supabase Storage: source inbox/archive a artefakty. Railway: workers a temporary workspace.

## State integrity
Immutable source a provenance jsou first-class. Ready state se nastavuje až po durable uploadu a validaci. Destruktivní cleanup inboxu je poslední krok.

## Observability
Dashboard má číst strukturovaný operational state. Zelený provoz patří na dashboard; alert je pro skutečnou integritu/deadline threat.

## Acquisition
Acquisition je oddělené upstream workflow. Technician není crawler/downloader. Odstraněný watcher není součást current architecture.

## Visual Page Map / semantic layout — experiment WSJ 2026-10-12

**Status:** lokální experimentální implementace v1; není nasazenou produkční architekturou. Původní WSJ experiment má dílčí ověření stran 5 a 2. Kanonický současný stav je v [CURRENT_STATE](../project-memory/CURRENT_STATE.md). Závěry WSJ níže vycházejí ze zadání konsolidace a dostupného záznamu konverzace „Stav zpracování WSJ“ (6acd024b-cdb4-83eb-afed-f675034d9dcc); nejde o nový runtime audit ani opakování experimentu. Dostupný záznam podrobně pokrývá stranu 2 a přerušený full-issue test, podrobnosti strany 5 a komprese doplňuje uživatelovo zadání. Implementační testy jsou samostatná, syntetická evidence.

### Proč nový přístup
Rekonstruovat sémantiku článků pouze z Physical Map jsme opustili: geometrie a textové bloky samy spolehlivě neurčují příslušnost ke článku, pořadí čtení kolem objektů ani oddělení reklamy/pull quote. Heuristiky byly křehké a závislé na konkrétním layoutu (viz F001). Physical Map se zachovává jako zdroj textu a geometrické evidence.

Vision model má mapovat stránku tak, jak ji čte člověk: které oblasti patří k článku, kudy pokračuje tělo a co je vložený objekt nebo cizí obsah. Python tuto sémantickou mapu pouze geometricky vykonává nad Physical Map; nemá znovu hádat článek ani reading order.

### Vstup a kontrakt
Low-res JPEG o šířce 600 px, v testu přibližně 92 KB, stačil pro rozpoznání layoutu na testovaných stranách. Jde o pozorování z tohoto experimentu, nikoli univerzální limit pro všechny publikace. Model nemusí OCRovat body text: ten se bere z Physical Map. Rozlišení pro layout proto nemusí odpovídat rozlišení potřebnému pro OCR.

Zkoušené schéma:

```text
ARTICLE
├── HEADLINE
├── BYLINE
├── BODY_FLOW[]          # explicitní zóny v pořadí čtení
├── EMBEDDED_OBJECTS[]
│   ├── CHART            # plot + axes/legend/labels/notes
│   ├── PHOTO
│   └── PULL_QUOTE
└── EXCLUSIONS[]         # např. reklama a cizí obsah
```

Pouhý vnější bbox článku nestačí. BODY_FLOW musí explicitně rozdělit tok do oblastí kolem grafů/fotek a určit jejich reading order. Strojový kontrakt v1 je nyní implementován v `src/business_brief/visual_page_map.py`; níže je jeho použití a hranice. Python propojí bboxy textové evidence s oblastmi, aplikuje exclusions a skládá body podle BODY_FLOW; žádné nové sémantické odhady.

### Ověření na straně 5
Oba články se podařilo sestavit; reklama i pull quote byly odděleny od těla a explicitní body flow fungoval. Zůstaly drobné hranové chyby Physical Map. Výsledek podporuje dělení sémantického úsudku a geometrického vykonání, ne tvrzení o bezchybné rekonstrukci celého vydání.

### Ověření na straně 2
Komplexnější strana měla podle experimentu 565 textových bloků. Mapa rozpoznala dva hlavní články, dva grafické bloky, velkou fotografii, čtyři briefs, corrections, publikační údaje a spodní foto-blok.

- „Why Higher Bond Yields Aren’t Going Away“: čistý headline a téměř správné tělo. Šest BODY_FLOW oblastí vedlo čtení přes levé sloupce, pod grafy a přes pravé sloupce. Do těla pronikly zbytky grafů (roky/poznámka), protože chart region pokrýval jen kresbu. Nutný je celý vizuální footprint včetně os, legendy, popisků a poznámek.
- „Fed’s Hammack Sees Engine of Inflation on Factory Floor“: hlavní tok přes sloupce kolem fotografie fungoval, ale první řádky tří sloupců pod fotografií byly chybně vyloučeny. Potřebujeme přesnější foto bbox a matching podle skutečného překryvu, nikoli jen středu textového bloku.
- Čtyři briefs byly správně odděleny včetně geografických nadpisů: „Venezuelan Bribe Suspect Arrested“, „Man Charged in Officer’s Death“, „Man Targets His Family, Killing Eight“, „At Least 4 People Die in Hurricane“.
- Corrections a publikační údaje šly oddělit samostatně; u spodního foto-bloku Python vytáhl pouze caption.

Návrh `exclude block only if overlap with photo > 60 %` je kandidát pro ověření, nikoli naměřený nebo schválený univerzální práh. Před implementací je třeba přesně definovat jmenovatel overlap metriky (např. plocha textového bboxu), hraniční pravidla a otestovat zachování prvních řádků pod fotografií.

### Navrhovaný tok a ekonomická hypotéza
`PDF/render → Visual Page Mapper → page-map.json → Python bbox/overlap matching nad Physical Map → assembled article text → editorial selection/deep read`

Levný layout pass pracuje s malým obrázkem a vrací stručnou mapu místo OCR/přepisování všech těl nebo hluboké četby každé stránky. Text skládá Python a dražší úsudek se soustředí na editorial selection a vybrané deep reads. To může výrazně snížit náklad proti současnému Fast Editorial v4.1. Velikost JPEG sama neurčuje cenu modelu; skutečná úspora, tokenový profil, latence a kvalita dosud nebyly změřeny placeným API benchmarkem. Historická cost baseline a gate jsou v [OPERATIONS](OPERATIONS.md).

### Hranice ověření
Strany 5 a 2 jsou proof of concept; neprokazují úplnost vydání, continuations mezi stranami ani obecnost přes publikace. Stav přerušeného testu 26 stran je pouze v CURRENT_STATE, příčina a podmínky opakování v FAILURES/F007. Během původních experimentů ani při implementaci v1 nebyl spuštěn žádný placený Fast Editorial ani OpenAI API; produkční pipeline se neměnila.

## Visual Page Map v1 — implementace a spuštění

### Hranice a moduly
- `visual_page_map.py`: kontrakt, lokální validace a verzovaný vision prompt.
- `visual_mapper.py`: samostatný Responses API adaptér, JPEG input + strict JSON Schema; žádný import/spuštění Fast Editorial.
- `visual_assembly.py`: geometrický matching a pořadí podle BODY_FLOW, zachování přesného textu a block IDs.
- `visual_continuations.py`: pouze explicitně schválené spojování fragmentů s vytištěným page cue.
- `visual_pipeline.py`: verifikace vstupů, render, durable artefakty, resume, coverage a HTML overlay.
- `visual_page_map_cli.py`: CLI `bb-visual-page-map` / `python -m business_brief.visual_page_map_cli`.

Jde o lokální tooling. Nezavádí queue, DB migrace, Railway deployment ani scheduler. Výstup je podklad pro editorial selection/deep read; tyto redakční kroky ani publikování tento nástroj neprovádí.

### Vstupy, souřadnice a matching
Vstupem je ověřený PDF a existující Physical Map v1/v2. Jejich source identity, SHA-256, souvislá posloupnost fyzických stran a rozměry musí souhlasit. Pro OCR/prepared derivát odlišný od originalu je nutné předat jeho ověřený hash ze Source Bundle; original SHA v Physical Map zůstává zachován. Nástroj neposkytuje OCR ani neopravuje text Physical Map. PDF s rotací odmítá: nejdříve připrav normalizovaný PDF a odpovídající Physical Map, aby se nemíchaly souřadnicové rámce.

Layout používá normalized `[x0,y0,x1,y1]` v intervalu 0–1, počátek vlevo nahoře, x doprava a y dolů. Každá body zóna je jeden sloupcový segment. Pořadí array je pořadí čtení, uvnitř zóny se řádky třídí geometricky shora dolů. ID jsou neprázdná a unikátní v rámci stránky; schema odmítá neznámé klíče, neplatné bboxy i NaN/Infinity. Article typ zahrnuje `article`, `brief`, `correction`, `photo`, `utility`.

Footprint objektu může být sjednocení více bboxů; jejich překryv se nepočítá dvakrát. Overlap = plocha průniku footprintu s textovým bboxem / plocha textového bboxu, nikoli IoU ani poloha středu. Výchozí experimentální politika v1: region přijme alespoň 50 %, fotografie vyloučí pouze nad 60 %, ostatní objekty a exclusions nad 50 %. Každý práh je nastavitelný. To jsou pracovní defaults, nikoli empiricky ověřené univerzální hranice. Captions zůstávají zvlášť a nevstupují do body textu.

Blok se přiřadí nejvýše jednou. Dva podobně silné kandidáty (default rozdíl nejvýše 0.05) nástroj označí jako ambiguous a neodhadne vlastníka. Nepokryté bloky, prázdné regiony/položky, nejednoznačnost i modelová nejistota vedou k `needs_review`, včetně dotčených článků. Block accounting není důkaz sémantické úplnosti ani správnosti exclusion.

### Offline průchod
Po instalaci projektu (`pip install -e '.[dev]'`) připrav artefakty; `--pages` lze vynechat pro celé vydání:

```bash
bb-visual-page-map prepare --pdf prepared.pdf --physical-map physical-map.json --output work/visual-issue --pages 2,5
# U odlišného prepared/OCR PDF přidej --prepared-sha256 <ověřený_hash>.
bb-visual-page-map schema > work/layout-schema.json
bb-visual-page-map map --issue-dir work/visual-issue --maps-dir work/reviewed-layouts
bb-visual-page-map assemble --issue-dir work/visual-issue
```

Offline adresář obsahuje `p0002.json`, `p0005.json` atd. Jsou to layout objekty podle schema, nebo dříve uložené map envelopes se shodnou proveniencí. Offline vstup znamená dodanou mapu; neprokazuje, že byla nově ověřena vision modelem. Syntetický integrační příklad vzniká v test fixture `tests/test_visual_pipeline.py`.

### Volitelné placené mapování
Klíč se čte pouze z `OPENAI_API_KEY`; explicitní `--model` musí podporovat image input a strict Structured Outputs. Nevolí se automaticky dražší model ani fallback.

```bash
bb-visual-page-map map --issue-dir work/visual-issue --live --allow-paid \
  --model "$VISUAL_PAGE_MAP_MODEL" --max-api-calls 1 --max-output-tokens 6000 --detail low
bb-visual-page-map assemble --issue-dir work/visual-issue --require-full-issue
```

`--max-api-calls` je limit na jedno spuštění, default 1; opakované spuštění pokračuje dalšími dosud nemapovanými stranami. `--detail low` je konfigurovatelný experimentální default a backend může obraz dále zmenšit; případný přechod na `high` musí být samostatně porovnán kvalitou a cenou. `max_output_tokens` je horní limit, ne cenový rozpočet. Usage/model/response ID se ukládají po stránkách; nástroj netvrdí úsporu v USD bez cenového modelu a reálného měření. Před placeným benchmarkem platí gate z OPERATIONS.

Provider používá [Responses image inputs](https://developers.openai.com/api/docs/guides/images-vision) a [strict Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses). Odesílá obrázek a rozměry/page labels, nikdy tělo Physical Map. Neúplný, odmítnutý nebo neplatný výstup není přijat. Neprobíhají automatické HTTP/model retries.

### Artefakty, resume a review
`manifest.json` váže original/prepared/Physical Map hash a render config. `images/` obsahuje JPEGy; `maps/` page-map envelopes s layout hash, mapper config a proveniencí; `responses/` raw modelové JSON odpovědi; `attempts/` záznamy pokusů; `assembled/` sestavené stránky; `previews/` samostatné HTML overlay; `assembled-issue.json` články/fragmenty, přesný text, odkazy na evidence, usage a coverage report.

Lokální OS lock brání souběžným writerům (macOS/Linux). Přijatá mapa se při resume znovu neplatí. Změna PDF, Physical Map, render config, model/prompt config nebo offline mapy vyžaduje nový issue adresář; nevzniká tiché míchání artefaktů. Záznam pokusu se zapisuje před network call. Po timeoutu/crashi s neznámým billing stavem automatický retry neproběhne; nejdřív prozkoumej attempt a modelový usage. Pokud je odpověď durable uložená, resume ji znovu validuje bez API volání. Do logů se vypisují jen krátká shrnutí, ne obrazy/base64 nebo klíče.

`all_pages_processed` je true pouze pro všechny fyzické strany vydání, nikoli pro vybraný subset. `--require-full-issue` vrátí kód 2, pokud celé vydání není sestavené. Tento příznak neznamená schválenou kvalitu: samostatně kontroluj `needs_review`, nepokryté/ambiguous bloky, exclusions a vizuální náhledy. Coverage sčítá assigned/excluded/unmatched/ambiguous; full-issue error rate vyžaduje lidský reference audit.

### Continuations a editorial handoff
Bez explicitních vazeb jsou položky samostatné page fragmenty. Printed cue mapper uchová, ale podobnost tématu nikdy nespouští merge. Reviewovaný links JSON má `source_sha256`, `physical_map_sha256`, `approved: true` a `links[]` s `from_fragment`, `to_fragment`, `printed_label`. Fragment IDs mají tvar `p0002:a1`; konkrétní lokální article ID čti z mapy. `printed_label` musí přesně souhlasit s cue v jedné z propojovaných položek a ukazovat na druhou fyzickou stranu.

```bash
bb-visual-page-map schema --kind links > work/links-schema.json
bb-visual-page-map assemble --issue-dir work/visual-issue --links work/approved-links.json
```

Neznámé fragmenty, jiné vydání, cykly, duplicitní/větvené vazby, různé typy položek nebo absence printed cue vedou k chybě. Review flag se spojením automaticky nemaže. Issue výstup uchovává fragmenty i složené články a nevyřešené continuations; editorial selection/deep read mají explicitně `not_started`. Otestovaná lokální mechanika nenahrazuje dosud nedokončený WSJ full-issue acceptance test.
