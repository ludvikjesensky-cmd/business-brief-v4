# Business Brief v4 — New Conversation Handoff

**Status:** AUTHORITATIVE HANDOFF  
**Created:** 3 October 2026  
**Use:** první dokument pro každou novou konverzaci, která má pokračovat ve v4

## Aktuální implementační stav — 9. 10. 2026

Pro pokračování čti nejdříve [PROGRESS_2026-10-09.md](PROGRESS_2026-10-09.md).
WSJ prošel Technicianem, Ingestorem a Fast Editorial do předběžné FROZEN Issue Map:
44 stran, 137 fragmentů, 99 položek. Finální Brief ani úplné pokrytí zakrytého textu
nejsou ověřeny. Další krok je redakční QA včetně strany 15, poté další deníky,
cross-paper selection a Selective Deep Read. Čti také [FAST_EDITORIAL.md](FAST_EDITORIAL.md)
a [INGESTOR.md](INGESTOR.md).

Níže zachovaná zakládající doporučení „nezačínat implementaci“ a „další komponenta
je Ingestor“ popisují historický stav; pro aktuální postup je nahrazuje uvedený
provozní záznam. Produktové a redakční zásady zůstávají platné.

### Provozní změna po prvním testu

WSJ watcher byl na pokyn uživatele zrušen (Railway služba, volume/session,
zdrojové soubory a PR); nepokračovat v jeho obnově. Aktuálně ruční upload PDF.
Další placené Fast Editorial běhy jsou pozastaveny do auditu nákladů a rozpočtu.
Podrobnosti a zbývající historická Git ref jsou v provozním záznamu výše.

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

## 16. Rozhodnutí z 8. října 2026

### Positioning
- Neprodáváme počet zdrojů. Máme **relevantní kvalitní zdroje**, které za čtenáře čteme, vysvětlujeme a zasazujeme do perspektivy.
- Hlavní ranní produkt musí stále dostát jednoduchému slibu: **FT, WSJ a Handelsblatt každé ráno v češtině na vašem stole.**
- Více perspektiv je součást značky. Nehledáme povinný syntetický „správný názor“.

### Portál
- Ambice velkého portálu Detailů zůstává.
- **Brief je časový produkt. Detail je znalostní produkt. Memory je spojovací tkáň.**
- Ne každý ingestovaný článek se stává Detailem.
- Portál má časem organizovat znalost také podle témat, firem, osob, zemí, sektorů a časových vazeb.
- `businessbrief.cz` je současná pracovní doména. Kratší umbrella brand **BRIEF** je možnost, ne podmínka a ne aktuální investiční priorita.

### Rights / transformation
- Zdrojová vrstva může být bohatší než publikační.
- Veřejný produkt nemá zpřístupňovat fulltextovou Article Memory ani fungovat jako náhrada předplatného zdrojových médií.
- Detail je vlastní transformační redakční rekonstrukce s kontextem a odděleným komentářem.
- Před komerčním spuštěním je požadována cílená právní revize workflow.

### Autonomní ráno
- Ranní výroba musí být schopna proběhnout bez přítomnosti člověka.
- Pracovní **TARGET 08:35**, **SLA 08:45 Europe/Prague**.
- FT/HB se zpracovávají předem; WSJ je poslední kritický vstup. Pracovní pozorování: ranní elektronické WSJ bývá dostupné několik minut po 08:00. Dále měřit.
- Povinné koncepty: Publication Gate, self-healing/retry, Event Log, observability, dashboard, exception-only phone alerts.
- Dashboard má jednoduché stavy ⚪ waiting / 🟡 running / 🟢 passed / 🔴 blocked.
- Zdravý provoz nemá spamovat telefon. Tvrdý alert pouze při ohrožení integrity nebo vydání.

### Audio
- Audio je plnohodnotná adaptace Master Briefu, ne TTS webu.
- Potřebuje Audio Adapter a pronunciation layer.
- Cílem je originální rozpoznatelný hlas značky, dlouhodobě neunavující.
- Preferován je jeden konzistentní hlas, ne „AI rádio“.
- Segmentovaná generace audia je preferovaný technický směr kvůli retry, QA, cache a kapitolám.
- ElevenLabs API je kandidát, **nikoli zatím uzamčené rozhodnutí**. Implementační variantu právě ověřuje paralelní Codex práce.

## 17. Nové kanonické dokumenty

Před technickým návrhem čti také:
- `SOURCE_AND_PORTAL_STRATEGY.md`
- `RIGHTS_AND_TRANSFORMATION.md`
- `AUTONOMOUS_MORNING.md`
- `AUDIO.md`

Tyto dokumenty zachycují produktová rozhodnutí, která vznikla po prvním ověření v4 a mají přednost před staršími otevřenými otázkami v tomto handoffu.

## 18. Aktualizované otevřené otázky

Stále otevřené:
- přesná délka a denní variabilita Briefu;
- kolik Detailů denně a jaký Detail selection threshold;
- pricing a free/paid hranice;
- právní stanovisko ke konkrétnímu produkčnímu workflow;
- finální název umbrella portálu;
- finální TTS/voice technologie a licence hlasu;
- přesná automatizační architektura a implementace dashboardu;
- datový model zákaznické Memory;
- pořadí a scope budoucích geografických / sektorových Briefů.

Již **není otevřené**, zda ranní workflow má být schopno autonomie: ano, musí. Není otevřené ani to, zda má audio být mechanické TTS: nemá.


## 19. Technician v4 — první zafixovaná produkční komponenta

Dne 8. října 2026 byla po vědomém přezkoumání v3 zafixována kanonická definice první komponenty produkční pipeline v4: `TECHNICIAN.md`.

Technician v4 je univerzální technická vstupní brána platformy, nikoli komponenta specifická pro FT / WSJ / Handelsblatt.

Kanonický tok:

```
Source Acquirer / manual upload
→ Source Inbox
→ Technician
→ source-bundle-v4
→ Ingestor
```

Klíčová rozhodnutí:
- acquisition není odpovědnost Techniciana;
- Technician je on-demand Railway worker, nikoli permanentní polling daemon;
- webhook/event je wake-up signal, databázová job queue je source of truth;
- po probuzení Technician zpracuje všechny dostupné claimable jobs a poté skončí;
- jobs musí podporovat atomic claim, lease/heartbeat, retry a idempotenci;
- Technician musí umět libovolný, i dříve neznámý titul;
- filename není autorita pro identitu;
- před drahým zpracováním proběhne lightweight IDENTIFY;
- identita se získává kaskádou metadata → native text → lightweight OCR → úzce omezený multimodální fallback;
- fyzická identita je `source_sha256`;
- logická identita vydání je konceptuálně `publication_id + edition_date + edition_variant`;
- stejný SHA se nezpracovává znovu jako nové vydání;
- jiný SHA se stejnou logickou identitou se nesmí automaticky zahodit, jde o edition collision / possible variant;
- originál je immutable;
- OCR patří Technicianovi a vytváří pouze derivative;
- splitting je výhradně mechanický;
- split-PDF byte SHA není correctness gate;
- Ingestor nikdy nesmí vidět rozpracovaný Source Bundle;
- handoff je povolen pouze po validaci a atomic finalize jako `READY_FOR_INGESTOR`.

Hranice role:

> **Technician smí zjistit, co je to za dokument. Nesmí zjišťovat, o čem dokument je.**

Technician tedy může znát titul, datum/variantu vydání, jazyk a fyzické vlastnosti dokumentu. Nesmí vybírat články, určovat témata, důležitost, article boundaries, editorial reading order ani vytvářet Issue Map / Article Records.

Nový kontrakt `source-bundle-v4` bude při implementaci formalizován machine-readable JSON Schema. V3 `source-bundle-v2` zůstává historicky frozen a nebude potichu mutován.

Další komponenta k vědomému převodu z v3 je **Ingestor**.
