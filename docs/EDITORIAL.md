# Editorial System — Business Brief v4

## Editorial question
Nejen „co se stalo?“, ale „co v tom autor vidí a proč stojí za to tuto myšlenku přenést?“

## Core distinctions
Fakt, perspektiva autora, syntéza, kontext a komentář Business Briefu nejsou totéž. Rozdílnost FT/WSJ/HB a dalších kvalitních zdrojů je hodnota, nikoli šum k vyhlazení.

Event importance a reading value jsou oddělené veličiny. Známé téma může obsahovat nový argument; velká událost může přinášet málo nové myšlenkové hodnoty.

## Upstream evidence
Editorial workflow nemá začínat z raw PDF ani z neověřeného modelového summary.

Upstream chain:

Technician Source Bundle → Ingestor v2 Page JSONs → Assembler Article Records → Composer topic groupings → optional Translator.

Ingestor může zaznamenat Business Brief relevance, ale finální editorial selection patří až editorial workflow.

## Workflow principle
1. Získat auditovatelné canonical Article Records dnešních vydání.
2. Seskupit související články napříč zdroji bez vyhlazení rozdílů.
3. Objevit kandidátní texty/perspektivy bez předčasného publication decision.
4. Selektivně číst do hloubky tam, kde to přidává hodnotu.
5. Porovnat zdroje a zachovat rozdíly.
6. Vybrat Brief podle čtenářské a informační hodnoty.
7. Ověřit tvrzení/provenance a přiznat nejistotu.
8. Vytvořit Master editorial truth.
9. Adaptovat do kanálů.

Konkrétní počet modelových passů není dogma. Role je odpovědnost, ne nutně agent/API call.

Brief musí být hodnotný sám o sobě. Detail nesmí být financován zamlčením klíčové informace. Detail přidává mechanismus, argumentaci, evidence, nuance a kontinuitu.

Před automatizací se workflow ověřuje na skutečných reference editions. Redakční kvalitu nelze odvodit pouze z unit testů nebo validního JSON.
