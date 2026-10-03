# Business Brief v4 — New Conversation Handoff

**Status:** AUTHORITATIVE HANDOFF  
**Created:** 3 October 2026  
**Use:** první dokument pro každou novou konverzaci, která má pokračovat ve v4

## 1. Kde projekt stojí

Business Brief v4 byl založen po zásadní produktové a redakční revizi v3.

V3 vyřešila a experimentálně ověřovala mnoho technických problémů: Reference Editions, mapování vydání, Fast Editorial vs Deep Editorial, Article Records, Memory a další pipeline. V průběhu práce se ale ukázalo, že projekt potřebuje přesnější odpověď na otázku **co vlastně vyrábí a proč**.

V4 proto nezačíná kódem. Začíná produktovou a redakční doktrínou.

## 2. Nejdůležitější věty

> **Není hlavní, na co se díváš. Hlavní je, co vidíš.**

> **Dnešní vydání orientuje. Brief otevírá. Detail rozvíjí.**

> **Nepřenášíme jen to, co zahraniční noviny vědí. Přenášíme způsob, jakým o ekonomickém světě přemýšlejí.**

> **Nechceme, aby čtenář odcházel s povinným názorem. Chceme, aby odcházel posunutý.**

## 3. Co Business Brief je

Redakčně vedená česká brána do aktuálních vydání Financial Times, The Wall Street Journal a Handelsblattu.

Z dnešních konkrétních textů vybírá myšlenky, otázky, argumenty, perspektivy, souvislosti, pozorování a mimořádně hodnotné kusy ekonomické žurnalistiky.

Nehledá pouze „nejdůležitější události dne“.

## 4. Co Business Brief není

Není obecné ekonomické zpravodajství, český Reuters/Bloomberg, AI agregátor, univerzální daily summary, produkt maximalizující počet zachycených headline facts ani názorový manuál.

## 5. Základní produkt

### Dnešní vydání
Úplná mapa FT / WSJ / HB. Obsahuje i články nezařazené do Briefu, včetně geopolitiky, rutinních zpráv a dalších částí vydání.

### Brief
Selektivní redakční četba. Má otevírat perspektivy, ne uzavírat témata.

Pracovní dramaturgie:
1. Dobré ráno
2. Co dnes noviny vidí
3. Tři noviny, tři pohledy — volitelné
4. Ještě jsme si všimli
5. Otázky, které nám dnes zůstaly
6. Co dnes ještě stojí za přečtení

### Detail
Prémiová česká redakční rekonstrukce konkrétního článku. Zachovává jeho myšlenkovou konstrukci a podstatný obsah, přidává kontext a jasně oddělený komentář.

### Memory
Podpůrná paměť pro ranní produkt; později může být primárním materiálem Trendů/Analýz.

## 6. Kritická změna oproti dřívějšímu uvažování

Primární tok není:

**událost → topic → syntéza zdrojů**

ale:

**dnešní vydání → konkrétní text → co autor vidí → myšlenka/argument/otázka → redakční výběr → případná syntéza**

Syntéza nesmí vyhladit rozdíl mezi FT, WSJ a HB.

## 7. Cílový čtenář

Nevycházíme z předpokladu, že cílový čtenář už každé ráno čte tři kvalitní zahraniční deníky.

Mnoho čtenářů dnes konzumuje hlavně titulky, sociální sítě, krátké formáty a highlighty. Business Brief má vytvořit cestu od tohoto prostředí ke kvalitnějšímu ekonomickému čtení.

Největší úspěch není „četl méně“, ale „díky Briefu objevil něco, co stojí za hlubší četbu a přemýšlení“.

## 8. Redakční test

U každého kandidátního textu se ptej především:

> **Je v tomto textu něco, co stojí za přenesení do hlavy našeho čtenáře?**

Nemusí být provokativní. Může dokreslit perspektivu, pojmenovat problém, položit dobrou otázku, nabídnout argument, propojit věci, ukázat silný příklad nebo být mimořádně kvalitní žurnalistikou.

## 9. V3 a migrace

Repo v3 je **reference, nikoli šablona**.

Nepřenášet automaticky starou dokumentaci ani architekturu. Převzít pouze prvky, které po vědomém přezkoumání podporují v4.

Pravděpodobně znovu použitelné koncepty:
- Reference Edition;
- úplná Issue Map;
- provenance;
- část Article Record;
- Fast vs Deep zpracování jako technické rozlišení;
- hybridní Memory;
- Master Brief → Web / Email / Audio.

Každý prvek však musí projít v4 product testem.

## 10. Co dělat dál

**Nezačínat ještě rozsáhlou produkční implementaci.**

Doporučený další postup:
1. zrevidovat tuto dokumentaci;
2. vytvořit první ruční Business Brief v4 z jednoho kompletního historického dne, ideálně z již zpracovaných zářijových Reference Editions;
3. vytvořit k němu 1–2 vzorové Detaily;
4. vytvořit návrh úplné stránky „Dnešní vydání“;
5. porovnat výsledek s principy v4;
6. teprve potom navrhnout EDITORIAL_WORKFLOW, datový model a ARCHITECTURE;
7. následně rozhodnout, které části v3 migrovat.

## 11. Doporučené pořadí četby

1. `docs/VISION.md`
2. `docs/PRODUCT_MODEL.md`
3. `docs/EDITORIAL_PHILOSOPHY.md`
4. `docs/BRIEF.md`
5. `docs/DETAIL.md`
6. `docs/TODAYS_EDITIONS.md`
7. `docs/MEMORY.md`
8. tento handoff

## 12. Otevřené otázky

Nejsou ještě definitivně rozhodnuty:
- přesná délka ranního Briefu;
- poměr hlavních bloků a kratších položek;
- kolik Detailů vzniká denně;
- cenový model;
- přesné právní/licenční hranice Detailu;
- zda a kdy přidat další zdroje;
- přesná role The Economist;
- webový informační design;
- datový model v4;
- automatizační architektura;
- které v3 komponenty převzít beze změny.

Tyto otázky se nemají vyřešit abstraktně, pokud je lze lépe rozhodnout na prvním ručně vytvořeném vydání v4.

## 13. Varování pro další konverzace

Nenechat projekt sklouznout zpět k maximalizaci coverage, honbě za „100% správnou mapou“ jako cílem sama o sobě, generickému topic clusteringu, headline summarization, architektuře navržené dříve než redakční produkt ani dojmu, že více automatizace = lepší Brief.

Technologie je prostředek. **Výsledkem musí být četba, která něco otevře v hlavě čtenáře.**


## 14. Stabilní dědictví v1–v3

Před dalším produktovým nebo technickým rozhodnutím čti také:
- `GOALS_AND_VALUES.md`;
- `SCOPE_AND_AUDIENCE.md`;
- `PRODUCT_HERITAGE.md`.

V4 **neruší** historické zásady důvěry, provenance, systematického průchodu celými hlavními vydáními, přirozené češtiny, transformační práce, Memory jako evidence, oddělení faktu / perspektivy / syntézy / komentáře ani ručního ověření před automatizací.

Klíčová reinterpretace úplnosti:

> **Úplnost nese Dnešní vydání. Brief nese redakční výběr.**

Proto se starý „colleague test“ nepoužívá jako povinnost nacpat každý významný text do Briefu. Používá se jako coverage test: významný článek nesmí technicky zmizet a musí být dohledatelný v mapě vydání.

Dlouhodobá produktová rodina zůstává:
- Brief;
- Detail;
- Trendy;
- Analýzy / Business Intelligence;
- pod nimi Memory.

Aktuální v4 však implementačně prioritizuje Dnešní vydání + Brief + Detail + Memory.

Primární publikum zahrnuje manažery, podnikatele, investory a odborníky, ale v4 **nepředpokládá**, že už dnes pravidelně čtou kvalitní zahraniční tisk. Produkt jim k němu má vytvářet cestu.

B2B potenciál zůstává součástí vize: firemní licence, sektorové Briefy, monitoring, Trendy a custom analýzy. Nemá ale předčasně komplikovat první ranní produkt.

Přesný pricing není rozhodnutý. Stabilní je pouze princip, že placená hodnota vzniká hloubkou, pohodlím, kontinuitou a specializací, nikoli umělým zamlčením základních faktů.

## 15. Provozní hodnoty zděděné z v3

Před nákladným nebo destruktivním krokem:
1. přesně definuj požadovanou schopnost;
2. ověř, že navržená cesta ji skutečně poskytuje;
3. odděl ověřené skutečnosti od předpokladů;
4. pojmenuj failure modes;
5. zvaž cenu, kvóty a destruktivní riziko;
6. nejdříve proveď nejmenší reverzibilní test.

Nevytvářet armádu agentů jen proto, že je to možné. Redakční role jsou odpovědnosti, ne nutně procesy nebo API calls.

Technologie je prostředek. **Architektura má následovat ověřený redakční produkt.**
