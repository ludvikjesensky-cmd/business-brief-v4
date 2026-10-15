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

## Upstream evidence
Editorial workflow nemá začínat z raw PDF ani z neověřeného modelového summary.

Upstream chain:

Technician Source Bundle → Ingestor v2 Page JSONs → Assembler Article Records → Composer topic groupings → optional Translator.

Ingestor může zaznamenat Business Brief relevance a page-level perspective evidence, ale finální editorial selection patří až editorial workflow.

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
