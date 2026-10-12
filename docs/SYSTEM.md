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

**Status:** laboratorní návrh, dílčí ověření stran 5 a 2; není nasazenou produkční architekturou. Kanonický současný stav je v [CURRENT_STATE](../project-memory/CURRENT_STATE.md). Závěry níže vycházejí ze zadání konsolidace a dostupného záznamu konverzace „Stav zpracování WSJ“ (6acd024b-cdb4-83eb-afed-f675034d9dcc); nejde o nový runtime audit ani opakování experimentu. Dostupný záznam podrobně pokrývá stranu 2 a přerušený full-issue test, podrobnosti strany 5 a komprese doplňuje uživatelovo zadání.

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

Pouhý vnější bbox článku nestačí. BODY_FLOW musí explicitně rozdělit tok do oblastí kolem grafů/fotek a určit jejich reading order. V navrhovaném `page-map.json` mají být zóny geometricky přiřaditelné ke stránce; přesný strojový kontrakt, souřadnicový systém a validační pravidla ještě nejsou uzavřeny. Python propojí bboxy textové evidence s oblastmi, aplikuje exclusions a skládá body podle BODY_FLOW; žádné nové sémantické odhady.

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
Strany 5 a 2 jsou proof of concept; neprokazují úplnost vydání, continuations mezi stranami ani obecnost přes publikace. Stav přerušeného testu 26 stran je pouze v CURRENT_STATE, příčina a podmínky opakování v FAILURES/F007. Během těchto experimentů nebyl spuštěn žádný placený Fast Editorial ani OpenAI API; produkční pipeline se neměnila.
