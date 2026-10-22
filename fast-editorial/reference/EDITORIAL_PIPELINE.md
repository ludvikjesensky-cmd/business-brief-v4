# Business Brief v3 — Editorial & Memory Pipeline

**Datum:** 29. 9. 2026  
**Stav:** dvě paralelní redakční cesty; Fast Editorial experiment aktivní

Tento dokument přenáší relevantní redakční a Memory koncepty z Business Brief v2 do robustnější source architektury v3.

## 1. Základní princip

> **Fast Editorial vybírá a syntetizuje. Deep Editorial ověřuje a buduje Memory.**

Od 27. 9. 2026 nejsou ranní Business Brief a Memory jedna lineární pipeline.

### Fast Editorial / Business Brief Production

```
Reference Edition
(PDF nebo úplná uspořádaná sada page images)
→ Editorial Discovery
→ Provisional Issue Map
→ freeze mapy každého titulu
→ Cross-source Topics
→ Selective Deep Read
→ Editorial Workflow v1
→ Business Brief
```

Cílem je rychlý, kvalitní ranní produkt. Provisional mapa není canonical source truth a nesmí se ukládat do `issue_items`.

### Deep Editorial / Web + Memory Production

```
Reference Edition
→ Source Adapter / Technician
→ Physical Map
→ Semantic Map
→ Reconciliation
→ Comparator / Coverage Gate
→ Article Map
→ Compiler
→ Text Normalizer
→ Relevance + Disposition
→ ADVANCE only
→ Metadata
→ Full Czech Translation
→ Czech Summary
→ Story Threads
→ Chunks
→ Memory-ready Gate
→ Hybrid Memory
```

> **Coverage patří canonical source vrstvě. Provisional relevance může vzniknout už ve Fast Editorial, ale canonical relevance/disposition zůstává až za ověřenou rekonstrukcí.**

## 2. Relevance a disposition jsou dvě oddělené otázky

`relevance`:
- `relevant`;
- `not_relevant`;
- `uncertain`.

`disposition`:
- `advance`;
- `exclude`;
- `watch`.

Povinné mapování:
- relevant → advance;
- not_relevant → exclude;
- uncertain → watch.

Relevance je široká vstupní brána. Neurčuje, zda článek skončí ve finálním ranním Briefu.

Neexistuje kvóta relevantních článků.

Rutinní sport, kulturní recenze, recepty, lifestyle, celebrity a entertainment bez významného business/economic přesahu se typicky vyřazují. Sportovní liga, média, kultura nebo entertainment s významným ekonomickým, regulatorním, transakčním či tržním dopadem mohou být relevantní.

## 3. Metadata

Plný enrichment běží pouze nad `advance` články.

Každý relevantní Article Record dostává:
- jednu `category`;
- `topics[]`;
- `trends[]`;
- `story_thread_candidates[]`;
- `tags[]`;
- `entities[]`;
- `geographies[]`;
- `industries[]`.

### Trend vs story thread

**Trend** = široký dlouhodobější fenomén.

Příklad:
`restrukturalizace evropského autoprůmyslu`

**Story thread** = konkrétní pokračující příběh, firma, politika nebo událost.

Příklad:
`Mercedes-Benz: restrukturalizace evropské výroby`

Trendy pomáhají tematickému přehledu. Story threads slouží k časové kontinuitě a Memory retrievalu.

## 4. Překlad a summary

Originální text je kanonický zdroj pravdy.

Každý relevantní článek má:
- source-language original;
- úplný interní český překlad `body_cs`;
- samostatný stručný český `summary_cs`.

Překlad a summary se nesmějí směšovat.

Translation provenance:
- status;
- model/producer;
- version;
- hash vstupního source textu.

Plný český překlad je interní pracovní vrstva, ne automaticky veřejný publikační obsah.

## 5. Article Archive

V Supabase jsou nově oddělené:

### `bbv3.issue_items`
Kompletní redakční klasifikace článkových položek:
- article identity;
- page refs;
- relevance;
- disposition;
- reason;
- relevance domains.

### `bbv3.articles`
Pouze relevantní / `advance` články pro další redakční práci:
- originální clean text;
- Czech full translation;
- Czech summary;
- metadata;
- trends;
- story threads;
- provenance/status.

### `bbv3.article_chunks`
Chunky pro hybridní retrieval:
- original;
- cs;
- pořadí;
- page refs;
- hash.

## 6. Hybrid Memory

Memory není jen vector database.

Používáme tři vrstvy:

1. **SQL metadata**  
   Přesné filtrování podle zdroje, data, category, industry, geography, entity, trend nebo story thread.

2. **Full-text**  
   Přesné názvy, fráze a termíny. Indexujeme originál i českou pracovní verzi.

3. **Vectors**  
   Sémantická podobnost přes různé formulace a jazyky.

Cílem je hybridní ranking.

Memory není pouze vector RAG. RAG je retrieval mechanismus nad širší znalostní vrstvou, která zahrnuje structured metadata, provenance, entity, story threads, signals, trends a editorial history.

## 7. Embeddings

Embedding model musí být multilingual.

Před produkčním vektorováním musí benchmark ověřit:
- český dotaz → anglický článek;
- český dotaz → německý článek;
- anglický článek → tematicky podobný německý článek.

Výchozí preference:
- embedding primárně originálních chunků;
- neembeddingovat slepě originál i českou verzi paralelně;
- dvojí vektorování zavést jen pokud benchmark prokáže přínos.

Embeddings nejsou podmínkou `memory-gate-v1`.

## 8. Memory-ready gate

Vydání není hotové proto, že workflow doběhlo.

`memory-gate-v1` ověřuje:
- proběhl disposition všech článků;
- každý `advance` item má Article Archive record;
- žádný `exclude/watch` item nemá Article Archive record;
- existuje čistý originální text;
- existuje verified Czech translation;
- existuje verified Czech summary;
- enrichment je verified;
- existují original chunks;
- existují Czech chunks.

Teprve potom je vydání `memory_status = ready`.

Embeddings jsou v této verzi gate nepovinné.

## 9. Daily editorial layer

Daily editorial layer nyní existuje ve dvou režimech.

### Fast daily layer

Po zmrazení tří provisional Issue Maps:

1. cross-source clustering do `daily_topics`;
2. určení dnešní delty;
3. include / reserve / exclude;
4. selektivní Deep Read;
5. Editorial Workflow v1 podle `docs/EDITORIAL_WORKFLOW.md`;
6. vlastní česká kompozice a verification uvnitř oddělených redakčních průchodů;
7. finální Editor-in-Chief gate;
8. publikace Briefu.

Memory je zde podpůrný kontext, nikoli blokující prerequisite.

### Deep / Memory daily layer

Po Memory-ready lze stejné téma dále obohatit o:
- hybrid Memory retrieval;
- story continuity;
- webový Article Detail;
- přesnější dlouhodobé vazby;
- pozdější opravy a retrospektivu.

> **Daily = delta. Memory = context.**

Relevantní článek není totéž jako článek, který se musí objevit ve finálním Briefu.

Stejně tak importance of event není totéž jako reading value of article. Hlavní news stories mohou být nejlépe obslouženy cross-paper syntézou, zatímco curated vrstva `Ještě stojí za pozornost` doporučuje texty, které stojí za skutečný čas čtenáře kvůli argumentu, reportingu, objevnosti nebo interpretaci.

## 10. Co se mění proti původnímu v3 směru

Původní v3 předpokládala, že ranní Brief počká na kompletní canonical rekonstrukci a Memory-ready všech zdrojů.

Desetidenní experiment tento předpoklad dočasně ruší pro Fast Editorial.

Zachováváme ale jeho nejcennější část:
- canonical source coverage zůstává podmínkou Deep/Memory vrstvy;
- `issue_items` a `articles` se neplní provisional odhady;
- Fast mapy mají vlastní datový model;
- pozdější propojení provisional → canonical umožní kvalitu objektivně změřit.

Detailní protokol je v `docs/EDITORIAL_EXPERIMENT.md`.


## 11. Translation Worker v1

Překlad už není ruční Chat krok. Produkční překladová vrstva je `translation-worker-v1`.

Princip:
- vstupem je kompletní sada ADVANCE článků;
- každý článek je samostatný API request;
- requesty běží řízeně paralelně;
- výchozí concurrency je 8;
- výchozí model je `gpt-6-luna`;
- při opakovaném problému se konkrétní článek eskaluje na `gpt-6-sol`;
- standardní processing tier je default; Fast lze zapnout konfigurací;
- Structured Outputs vynucují `article_id + body_cs`;
- publication-neutral completeness check hlídá prázdný, extrémně krátký/dlouhý nebo zkolabovaný text;
- retry se týká pouze chybného článku;
- celý translation stage je DONE jen při 100% pokrytí;
- podezřelý článek vede na NEEDS_REVIEW, ne k tichému přijetí.

CLI:
`bb-translate --input enriched-articles.json --output article-translation-v1.json --report translation-report.json`

Issue Runner:
`bb-issue-run --auto-translate`

API překlad dostává status `translated`, nikoli `verified`. Verification zůstává samostatný QA krok před Memory-ready gate.

Batch API je budoucí archivní/nízkonákladová cesta. Pro ranní produkci zůstává default standardní Responses API s paralelizací.
