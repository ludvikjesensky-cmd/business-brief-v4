# Editorial System — Business Brief v4

## Editorial question
Nejen:

> Co se stalo?

Ale především:

> Jak o tom tento autor a toto médium přemýšlejí? Co v tom vidí? Jakou otázku si kladou? Jak problém rámují a kam jejich argument vede?

Business Brief nepřenáší pouze událost. Přenáší způsob jejího vidění a pojednání.

## Core distinctions
Fakt, perspektiva autora, perspektiva média, syntéza, kontext a komentář Business Briefu nejsou totéž.

Rozdílnost FT/WSJ/HB a dalších kvalitních zdrojů je hodnota, nikoli šum k vyhlazení.

Event importance a reading value jsou oddělené veličiny. Známé téma může obsahovat nový argument; velká událost může přinášet málo nové myšlenkové hodnoty.

## Perspective value
Text je editorialně hodnotný nejen tehdy, když přináší novou událost, ale také tehdy, když přináší:

- výrazný nebo jedinečný úhel pohledu;
- otázku, která mění způsob, jak problém chápat;
- argument, který posouvá mentální model čtenáře;
- nečekanou souvislost;
- silné rámování;
- rozpor, dilema nebo pochybnost, které nejsou na první pohled zřejmé;
- charakteristický způsob, jakým dané médium téma uchopuje.

Zásadní editorial pravidlo:

> Nekomprimuj text tak, že zachováš fakta, ale ztratíš autora.

Pokud právě autorova otázka, způsob argumentace nebo framing tvoří hlavní hodnotu článku, musí být tato vrstva zachována v dalším zpracování.

## Two editorial contexts — D030

This document serves both product philosophy and downstream editorial judgment, but v4 now has two independent production branches.

**Fast Editorial** starts from complete Reference Editions and live Chat editorial reading. It may create provisional Issue Maps, compare editions cross-paper and build the morning Brief without canonical Article Records, Indexer, Enrichment, Composer or Memory.

**Deep / Memory editorial work** starts from canonical evidence as described below. Its source-reconstruction and knowledge gates must not be imposed on Fast Editorial unless a future explicit decision integrates the branches.

## Upstream evidence — Deep / Memory branch
Deep/Memory editorial workflow nemá začínat z raw PDF ani z neověřeného modelového summary. Toto pravidlo se nevztahuje na Fast Editorial, jehož vstupem je záměrně kompletní Reference Edition čtená live Chat editorem.

Upstream chain:

Technician Source Bundle → Ingestor v2 Page JSONs → Assembler Article Records → Composer topic groupings → optional Translator.

Ingestor zaznamenává krátkou relevance assessment a source-faithful text; rozsáhlá perspective evidence není povinnou page vrstvou. Finální editorial selection a article-level interpretace patří downstream.

Page-level perspective evidence není automaticky finální interpretace článku. Assembler může spojit evidence z více stran; editorial workflow teprve rozhoduje, jakou autorskou otázku, framing a argumentační osu považovat za stabilně podložené na úrovni celého článku.

## Workflow principle
1. Získat auditovatelná canonical Article Records dnešních vydání.
2. Zachovat u každého relevantního textu jeho autorskou otázku, framing, argumentační osu a distinctive angle.
3. Seskupit související články napříč zdroji bez vyhlazení rozdílů.
4. Objevit kandidátní texty/perspektivy bez předčasného publication decision.
5. Selektivně číst do hloubky tam, kde to přidává hodnotu.
6. Porovnat zdroje a zachovat rozdíly.
7. Vybrat Brief podle informační hodnoty i perspective value.
8. Ověřit tvrzení/provenance a přiznat nejistotu.
9. Vytvořit Master editorial truth.
10. Adaptovat do kanálů.

Konkrétní počet modelových passů není dogma. Role je odpovědnost, ne nutně agent/API call.

Brief musí být hodnotný sám o sobě. Detail nesmí být financován zamlčením klíčové informace. Detail přidává mechanismus, argumentaci, evidence, nuance a kontinuitu.

Před automatizací se workflow ověřuje na skutečných reference editions. Redakční kvalitu nelze odvodit pouze z unit testů nebo validního JSON.

## Article assets and placement
D022 preserves charts, tables, photos, infographics and other article visuals as crops of authoritative page PNGs, with article/page ownership and physical/text anchors. `text_on_page` contains visually verified prose, not visual OCR or an inferred interpretation. **Text se rekonstruuje. Vizuální artefakty se nepřepisují, ale uchovávají.** Source-visible titles/captions may accompany the crop; internal OCR is optional noncanonical support.

Assembler joins prose across pages and then re-anchors assets by unique surrounding `anchor_text`; page bbox remains provenance and paragraph index is auxiliary. Missing/ambiguous matches remain `placement_needs_review` / unplaced, never guessed into the article. Editorial decides whether to use, interpret or omit the preserved visual, distinguishing its interpretation from source evidence. Exact contract/storage and implementation gate: INGESTOR.md §21; v2/v3 objects are not rewritten.

## Knowledge handoff — D028
Composer supplies today's evidence-backed signals/delta and bounded editorial-enrichment-v1 knowledge links ([ENRICHMENT.md](ENRICHMENT.md)). Candidates are visible as proposals, not established trends; historical context retains exact reviewed object revisions and source provenance. Assignment Editor chooses inclusion/hierarchy and reading curation, Story Editor final angle, and Deep Read deeper source verification. Enrichment does not equate event importance with article reading value or suppress a distinctive singleton. Daily = delta. Memory = context; Trend/Analysis work uses Memory as primary material and independently reviews its conclusions.
