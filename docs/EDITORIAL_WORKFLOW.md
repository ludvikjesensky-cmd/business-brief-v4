# Editorial Workflow v4

**Status:** CANONICAL  
**Produkt:** Business Brief v4  
**Účel:** převést úplné dnešní vydání FT, WSJ a Handelsblattu do ranního Briefu, který současně orientuje, otevírá perspektivy a neunavuje.

## 1. Proč má v4 osm redakčních průchodů

Business Brief v4 není ani agregátor zpráv, ani sbírka chytrých komentářů.

Musí současně splnit dvě různé potřeby čtenáře:

1. **Informační bezpečí:** po Briefu nemá zjistit, že mu unikla zásadní věc z dnešních FT, WSJ nebo Handelsblattu.
2. **Intelektuální hodnota:** nemá pouze vědět, co se stalo. Má si odnést několik myšlenek, argumentů, perspektiv nebo otázek, které stojí za přemýšlení.

Proto oddělujeme úplnost, výběr, dramaturgii, psaní, hloubku, verifikaci, jazyk a finální odpovědnost.

Osm průchodů neznamená osm agentů ani osm API volání. Jsou to **osm odlišných redakčních odpovědností a kontrolních bran**. Technická implementace může některé průchody spojit, ale nesmí ztratit jejich funkci.

Základní vztah produktu:

> **Dnešní vydání orientuje v úplnosti. Brief orientuje a otevírá. Detail rozvíjí. Čtenář si ponechává úsudek.**

A základní pravidlo Briefu:

> **Jedna myšlenka, jedno místo.**

Žádné téma, argument ani pointa se v Briefu nesmí opakovat jen proto, aby byla nejprve v souhrnu, potom v hlavní části a nakonec v doporučení.

---

# 2. Vstup do workflow

Workflow začíná až ve chvíli, kdy máme dostatečně spolehlivou mapu dnešních vydání.

Minimální vstupy:

- Reference Edition FT
- Reference Edition WSJ
- Reference Edition Handelsblatt
- úplná nebo dostatečně ověřená Issue Map každého titulu
- Article Records / metadata dostupných článků
- případný Deep Read u kandidátů, kde mapa nestačí
- provenance: odkud každé tvrzení pochází
- Memory jako podpůrný kontext, nikoli jako náhrada dnešních vydání

**Reference Edition určuje, co dnešní noviny jsou. Web pomáhá vybrané články číst, ověřovat a rozšiřovat.**

V4 nemá začínat topic clusteringem. Primární redakční jednotkou je:

> **konkrétní článek → jeho myšlenka / perspektiva / argument → případné propojení s jinými články**

Cross-paper topic vzniká až poté, co rozumíme jednotlivým textům.

---

# 3. Výstupy workflow

Workflow vytváří minimálně tři artefakty:

### RAW MASTER
První úplná verze Briefu po výběru a napsání. Je zachována pro audit a srovnání.

### MASTER BRIEF VERIFIED
Finální redakčně a fakticky ověřený Brief.

### EDITORIAL LOG
Stručný záznam zásadních rozhodnutí:
- co bylo zařazeno do radaru
- co bylo vybráno jako perspektiva
- co zůstalo pouze v Dnešních vydáních
- co bylo odstraněno kvůli opakování
- kde byla interpretace oslabena nebo opravena
- které články byly doporučeny k Detailu

Díky tomu lze zpětně rozlišit **technický miss**, **redakční omission** a **vědomé dramaturgické rozhodnutí**.

---

# 4. PASS 1 — ASSIGNMENT EDITOR
## Co dnes musíme vědět a co stojí za přemýšlení?

### Úkol
Assignment Editor projde dnešní vydání jako celek a rozdělí materiál podle jeho funkce pro čtenáře.

Neptá se pouze:

> Co je dnes nejdůležitější?

Ptá se:

> Co musí čtenář vědět, aby byl orientovaný?  
> Co stojí za přenesení do jeho hlavy jako myšlenka?  
> Co je kvalitní, ale může zůstat v Dnešních vydáních?

### Každá položka dostane disposition

**RADAR**  
Zásadní událost nebo změna, kterou čtenář potřebuje znát, ale která nevyžaduje hlubší rozvinutí v Briefu.

**PERSPECTIVE**  
Článek nebo pohled s výraznou transfer value: argument, otázka, konstrukce, pozorování nebo perspektiva, která stojí za rozvinutí.

**CROSS-PAPER CANDIDATE**  
Dva nebo tři články sledují stejnou věc, ale každý v ní vidí něco odlišného. Kandidát na „Tři noviny, tři pohledy“.

**NOTICE**  
Menší, ale chytrá, překvapivá nebo užitečná myšlenka vhodná do krátkého oddechového bloku.

**DETAIL CANDIDATE**  
Text s vysokou čtenářskou hodnotou, který stojí za hlubší českou rekonstrukci. Může současně být PERSPECTIVE.

**EDITION ONLY**  
Patří do úplné mapy dnešních novin, ale ne do Briefu.

### Výběrové otázky
- Je to důležité pro orientaci?
- Přináší text něco víc než událost samotnou?
- Je v něm myšlenka, kterou si čtenář může pamatovat večer?
- Je článek intelektuálně nebo reportážně výjimečný?
- Je relevantní pro ekonomiku, firmy, management, technologie, trhy nebo ekonomickou společnost?
- Přináší jiný pohled než ostatní texty?
- Má cenu přenést právě tento způsob vidění do češtiny?

### Tvrdé pravidlo
Velikost události sama nerozhoduje o délce v Briefu.

> **Velikost události rozhoduje o tom, zda ji musíme vidět. Čtenářská a myšlenková hodnota rozhoduje o tom, kolik prostoru jí dáme.**

### Gate
Po Pass 1 nesmí existovat zásadní událost dne, která není buď v RADAR, PERSPECTIVE, nebo vědomě označena jako EDITION ONLY s důvodem.

---

# 5. PASS 2 — DRAMATURG
## Jak z výběru vytvořit ranní zážitek, ne seznam?

### Úkol
Dramaturg skládá **mentální rytmus Briefu**.

Neoptimalizuje počet článků. Optimalizuje pozornost posluchače.

### Typická dramaturgie

**Dobré ráno**  
Krátký lidský vstup. Ne obsah Briefu před Briefem.

**Radar / Co dnes potřebujete vědět**  
Krátká orientační vrstva. Obsahuje pouze témata, ke kterým se Brief už nevrátí.

**Hlavní perspektivy**  
Obvykle několik nejsilnějších myšlenek dne. Počet není kvóta.

**Tři noviny, tři pohledy**  
Pouze pokud rozdíl perspektiv sám vytváří hodnotu.

**Krátké objevy / Ještě jsme si všimli**  
Několik kratších myšlenek, které mění tempo.

**Doporučení ke čtení**  
Lidské zakončení a pozvání k Detailu nebo originálu.

Sekce nejsou povinné každý den. **Stabilní je dramaturgická funkce, ne formulář.**

### Dramaturg hlídá
- střídání těžších a lehčích témat
- změnu délky a tempa
- aby za sebou nebylo několik textů se stejnou konstrukcí
- aby se Brief postupně neproměnil v nekonečný proud položek
- aby žádná část nebyla pouze „další informace“
- aby konec přinesl uvolnění, ne další nálož faktů

### NO-REPEAT GATE
Dramaturg vytváří mapu témat a point.

> **Jedna myšlenka, jedno místo.**

Pokud je téma v radaru, nesmí být později hlavním textem. Pokud je hlavní text doporučen k Detailu, závěrečné doporučení ho znovu nepřevypráví.

Odkaz není opakování. Nové převyprávění stejné pointy ano.

### Délka
Neexistuje pevný limit minut ani slov.

> **Každá další minuta musí přinést něco nového.**

Deset nudných minut je příliš mnoho. Patnáct dobrých minut může být v pořádku.

---

# 6. PASS 3 — STORY EDITOR
## Zachovali jsme to, co autor skutečně viděl?

### Úkol
Story Editor pracuje s každým vybraným článkem zvlášť a chrání jeho intelektuální konstrukci před zploštěním.

U každé PERSPECTIVE rekonstruuje:

1. Co se stalo?
2. Co v tom autor vidí?
3. Jaký je jeho hlavní argument?
4. Jak k němu dochází?
5. Jaké důkazy, čísla nebo příklady jsou pro něj podstatné?
6. Co je na textu jiné než na běžném zpravodajství o tématu?
7. Co zůstává otevřené?

### Anti-flattening test
Pokud lze výslednou položku zaměnit za obecný titulek typu:
- „AI mění práci“
- „Evropa má problém s autoprůmyslem“
- „Solár roste“
- „USA mají vysoký dluh“

pak jsme pravděpodobně ztratili to nejcennější.

Story Editor hledá formulaci typu:

> „Gig economy možná není jen typ práce, ale tlumič pracovního trhu. Co se stane, když automatizujeme i tento tlumič?“

### Cross-paper pravidlo
Články se nesmějí sloučit jen proto, že pojednávají o stejné události.

Nejprve:
- FT vidí X
- WSJ vidí Y
- HB vidí Z

Teprve potom lze vytvořit syntézu.

> **Rozdíl perspektiv je informace, nikoli šum k odstranění.**

### Gate
Každý hlavní text musí mít jasně identifikovatelnou transfer value. Pokud ji nemá, vrací se do RADAR, NOTICE nebo EDITION ONLY.

---

# 7. PASS 4 — BRIEF WRITER
## Napiš to tak, aby to člověk chtěl poslouchat

### Úkol
Brief Writer vytváří RAW MASTER.

Píše pro chytrého, časově vytíženého člověka, nikoli pro databázi ani výroční zprávu.

### Hlas
Business Brief má působit jako:

> **ranní rozhovor s mimořádně dobře připraveným člověkem, který prošel tři kvalitní noviny a vypráví, co v nich našel.**

Ne jako:
- tisková agentura
- školní výklad
- investiční memo
- seznam anotací
- AI summary

### Jazyk
Preferujeme:
- přirozenou češtinu
- konkrétní slovesa
- různou délku vět
- přímé formulace
- občasné oslovení posluchače
- přirozené přechody
- prostor pro jednoduchou větu po složitém argumentu

Lidské přechody mohou být například:
- „Teď něco úplně jiného.“
- „Tady stojí za to na chvíli zůstat.“
- „A ještě jedna nenápadná věc.“
- „Tohle je jeden z textů, které se snadno přehlédnou.“
- „Pokud máte dnes ještě patnáct nebo dvacet minut…“

Nesmějí se však stát novou šablonou.

### Anti-template pravidlo
Ne každý text musí mít:
**fakt → překvapení → hlubší význam → velká otázka.**

Jeden text může skončit otázkou. Jiný číslem. Jiný argumentem autora. Jiný prostým pozorováním.

> **Ne každý odstavec potřebuje intelektuální gong.**

### Otázky
Otázka je dobrá pouze tehdy, pokud skutečně otevírá problém.

Nevyrábíme otázky proto, že v4 „má být přemýšlivá“.

### RAW MASTER
Po tomto průchodu se verze uloží a už se nepřepisuje beze stopy. Slouží jako kontrolní bod pro měření hodnoty dalších redakčních průchodů.

---

# 8. PASS 5 — DEPTH & DETAIL EDITOR
## Otevírá Brief dost, ale nevyprázdnil Detail?

### Úkol
Depth & Detail Editor kontroluje hranici mezi Briefem a Detailem.

Brief má čtenáři umožnit pochopit:
- proč text stojí za pozornost
- jaká je jeho hlavní myšlenka
- dost argumentu, aby nebyl teaserem bez obsahu

Nemá však rekonstruovat celý článek.

### Test
Po přečtení Briefu se ptáme:

> Rozumím, proč je článek zajímavý?

Ano.

> Vím už prakticky všechno, co mi může Detail nabídnout?

Pokud ano, Brief zašel příliš daleko.

### Detail candidate test
Silný Detail typicky obsahuje další hodnotu:
- plnou argumentační strukturu
- důkazy a data
- reportážní materiál
- příklady
- protiargumenty
- nuance
- kontext
- českou redakční interpretaci

### Doporučení ke čtení
Závěr nesmí opakovat obsah hlavního textu.

Stačí lidské doporučení:

> „Pokud máte dnes ještě patnáct nebo dvacet minut na jeden text, my bychom sáhli po…“

A krátké vysvětlení, které nepřevypráví pointu znovu.

---

# 9. PASS 6 — VERIFICATION EDITOR
## Je všechno pravda a víme, co je čí tvrzení?

### Úkol
Verification Editor kontroluje fakta, provenance, míru jistoty a hranici mezi zdrojem a naší interpretací.

### Povinné rozlišení

**SOURCE CLAIM**  
Co tvrdí původní článek nebo citovaný člověk.

**FACTUAL CORE**  
Co lze považovat za ověřený fakt.

**AUTHOR PERSPECTIVE**  
Co je argument nebo interpretace autora FT/WSJ/HB.

**BB SYNTHESIS**  
Co vzniklo naším propojením více zdrojů.

**BB COMMENTARY / QUESTION**  
Co je naše vlastní interpretace nebo otázka.

Tyto vrstvy nemusí být ve veřejném textu označeny štítky, ale musí být v redakčním procesu rozlišitelné.

### Kontroluje se
- číslo
- jednotka
- měna
- datum
- osoba a funkce
- kauzalita
- citace
- stav návrhu vs přijaté rozhodnutí
- interní scénář vs veřejná prognóza
- fakt vs očekávání
- fakt vs naše inference
- aktuálnost
- zda syntéza nepřekračuje zdroje

### Zásada
V4 si dovoluje více interpretace než v3. Proto musí mít **ještě ostřejší provenance**.

> **Čtenář smí dostat naši myšlenku. Nesmí ji omylem považovat za tvrzení Financial Times.**

### Gate
Nejistota se neskrývá stylistickou sebejistotou. Pokud něco nevíme, text to musí přiznat nebo tvrzení odstranit.

---

# 10. PASS 7 — LANGUAGE, HUMANITY & AUDIO EDITOR
## Zní to jako člověk?

### Úkol
Tento průchod se neprovádí pouze očima.

Brief se musí **číst nahlas nebo simulovat jako mluvený poslech**.

Editor hledá kognitivní únavu.

### Kontroluje
- příliš dlouhé věty
- nahromadění čísel
- business žargon
- abstraktní podstatná jména
- několik těžkých pasáží za sebou
- monotónní strukturu odstavců
- opakované rétorické figury
- příliš mnoho otázek
- příliš mnoho „point“
- mechanické přechody
- chybějící lidské nadechnutí

### Humanity pass
Ptáme se:

> Mluvíme ještě k člověku, nebo už jen zpracováváme obsah?

Lidskost neznamená familiárnost ani podcastové žvanění.

Má změkčit kognitivní náročnost:
- přirozeným přechodem
- jednoduchou větou
- občasným oslovením
- změnou tempa
- přiznáním redakční preference
- doporučením typu „my bychom dnes sáhli po…“

### Audio test
Ideální kontrolní otázka:

> **Dokážu to poslouchat při cestě do práce bez potřeby vracet se o odstavec zpět?**

Pokud ne, text může být příliš hutný, i když je napsaný správně.

### NO-BOREDOM TEST
Délka sama o sobě není chyba.

Chybou je minuta, během níž:
- se nic nového nedozvím
- slyším stejnou pointu podruhé
- text stojí na místě
- musím nést příliš mnoho detailů, které nikam nevedou

---

# 11. PASS 8 — EDITOR-IN-CHIEF
## Chtěl bych to zítra znovu?

### Úkol
Editor-in-Chief neprovádí další stylistické leštění. Posuzuje Brief jako celý produkt.

### Osm finálních otázek

1. **ORIENTATION**  
   Vím po Briefu, co zásadního se dnes děje?

2. **TRANSFER VALUE**  
   Odnesl jsem si několik myšlenek, které bych bez těchto novin neměl?

3. **NO REPEAT**  
   Zazněla každá myšlenka opravdu jen jednou?

4. **SOURCE IDENTITY**  
   Cítím rozdíl mezi FT, WSJ a Handelsblattem, nebo jsme z nich vyrobili jednu agenturu?

5. **RHYTHM**  
   Má Brief změny tempa, nebo mě postupně unavuje?

6. **HUMANITY**  
   Mám pocit, že mi někdo noviny vypráví, nebo že zpracovávám dokument?

7. **TRUST**  
   Je jasné, co je fakt, co pohled autora a co naše interpretace?

8. **RETURN TEST**  
   **Kdyby mi tohle někdo každé ráno deset až patnáct minut vyprávěl cestou do práce, chtěl bych ho zítra poslouchat znovu?**

Pokud poslední odpověď není přesvědčivé ano, Brief není hotový.

### Editor-in-Chief smí
- odstranit celý text
- přesunout položku do Dnešních vydání
- zkrátit radar
- vrátit text Story Editorovi
- odmítnout chytrou, ale přehnanou interpretaci
- odstranit otázku
- změnit pořadí
- vyžádat nový Deep Read
- vrátit Brief do kteréhokoli předchozího passu

Publikace není devátý pass. Je výsledkem schválení.

---

# 12. Doporučená struktura finálního Briefu

Není to pevná šablona. Je to výchozí dramaturgie.

1. **Dobré ráno**  
   Krátký lidský vstup.

2. **Co dnes potřebujete vědět**  
   Radar. Několik zásadních věcí, které už se dále neopakují.

3. **Co dnes stojí za přemýšlení**  
   Několik hlavních perspektiv. Každá může mít jinou délku a konstrukci.

4. **Tři noviny, tři pohledy**  
   Pouze pokud rozdíl perspektiv vytváří skutečnou hodnotu.

5. **Ještě jsme si všimli**  
   Krátké, stravitelné objevy a myšlenky.

6. **Pokud máte ještě patnáct nebo dvacet minut…**  
   Jedno až několik skutečně dobrých doporučení k Detailu nebo originálnímu článku.

Neexistuje povinný počet položek.

> **Ne více obsahu. Více hodnoty z obsahu, který jsme vybrali.**

---

# 13. Co se změnilo proti v3

### v3
Primární otázka:
> Jak spolehlivě vytvořit kvalitní ranní přehled z úplných vydání FT, WSJ a Handelsblattu?

Typická redakční jednotka:
> topic

Hlavní hodnota:
> orientace, úplnost, minimum pro informovanost

Riziko:
> velmi dobrý briefing se může postupně stát únavným proudem informací a rozpustit osobitost původních článků.

### v4
Primární otázka:
> Jak českému čtenáři přinést to nejhodnotnější z dnešního myšlení FT, WSJ a Handelsblattu a přitom zachovat informační bezpečí?

Primární redakční jednotka:
> konkrétní článek a jeho perspektiva / myšlenka

Hlavní hodnota:
> orientace + intelektuální transfer + chuť pokračovat do Detailu

Ochranné mechanismy:
- úplnost nese Dnešní vydání
- radar nese informační bezpečí
- hlavní Brief nese perspektivu
- Detail nese hloubku
- NO-REPEAT gate chrání před nudou
- Humanity & Audio pass chrání před kognitivní únavou

---

# 14. Kanonické principy workflow

> **Úplnost nese Dnešní vydání. Brief nese redakční výběr.**

> **Jedna myšlenka, jedno místo.**

> **Velikost události rozhoduje o tom, zda ji musíme vidět. Myšlenková a čtenářská hodnota rozhoduje o prostoru.**

> **Článek → perspektiva → případné propojení. Nikoli články → topic → generický souhrn.**

> **Rozdíl perspektiv je informace.**

> **Brief otevírá. Detail rozvíjí.**

> **Každá další minuta musí přinést něco nového.**

> **Délka není problém. Nuda a kognitivní únava jsou problém.**

> **Ne každý text potřebuje pointu nebo otázku.**

> **Čtenář nemá mít pocit, že zpracovává informace. Má mít pocit, že mu někdo dobře vybral a vypráví dnešní noviny.**

> **Nechceme čtenáři říkat, co si má myslet. Chceme mu dát víc toho, s čím může přemýšlet.**

---

# 15. Praktický referenční test

Referenční den 14. 9. 2026 uchováváme ve třech stavech:

1. **v3 VERIFIED** — kontrolní skupina: velmi kvalitní briefing.
2. **v4 RAW MASTER** — první prototyp nové dramaturgie bez osmi průchodů.
3. **v4 VERIFIED** — výsledek tohoto workflow.

Porovnání RAW → VERIFIED má ukázat, jakou konkrétní hodnotu přidává každý redakční pass.

Teprve workflow, které prokazatelně zlepšuje referenční dny, má smysl automatizovat.

---

# 16. Jednovětá definice

> **Editorial Workflow v4 převádí úplné dnešní vydání tří novin do Briefu, který čtenáři nic zásadního nenechá uniknout, ale svou největší pozornost věnuje tomu, co stojí za to vidět, pochopit a promýšlet.**
