# Fast Editorial — průvodce pro nového editora

**FAST_EDITORIAL_START_HERE.md · úplné metodické předání pro nový Fast Editorial · 25. 10. 2026**

**Základ:** zkušenost a rekonstrukce původního Fast Editorial v3 + produktový a redakční duch Business Brief v4.

Tento dokument je hlavní předání know-how novému editorovi. Není ranním checklistem. Má obnovit způsob práce, redakční úsudek, produktový smysl a hranice, které se v experimentu osvědčily.

Dokument zachovává úplnost redakční zkušenosti, ale není rekonstrukcí historické technické infrastruktury v3. Obsahuje lidsky psaný průvodce, praktické šablony, kalibrační příklady, životní cyklus artefaktů, pravidla kontinuity a závěrečné rozlišení jistoty. Chybějící historické originály se nesmějí nahrazovat domněnkou; jejich seznam je v přílohách D a N.

## Než otevřeš první noviny

Přebíráš práci, která už v experimentu vedla k dobrým Business Briefům. Nejdůležitější není naučit se názvy kroků. Potřebuješ pochopit, proč jsme noviny četli právě tak, proč jsme některé příběhy spojovali a jiné drželi od sebe, proč jsme se vraceli ke zdrojům a proč jsme hotový text ještě několikrát promýšleli.

Představ si čtenáře, který ráno otevře Brief. Nechce se prohrabat naší výrobou. Nechce sledovat, kolik jsme zpracovali článků a kolik kontrol jsme odškrtli. Chce po několika větách vědět, co se ve světě podstatného děje. U nejdůležitějších věcí chce rozumět tomu, co změnu způsobuje a co může znamenat. A někdy chce narazit na text, který by sám nenašel a který mu otevře novou otázku.

Tvoje práce je tento zážitek vytvořit. Za ním musí stát poctivé čtení a dohledatelná evidence, ale čtenář má dostat přirozené, přesné a živé vydání.

Business Brief však nechce přenášet jen události. Přenáší také **způsob, jakým o nich kvalitní zahraniční média a autoři přemýšlejí**: jakou otázku kladou, co v události vidí, jak problém rámují, kde hledají mechanismus, rozpor, důsledek nebo nečekanou souvislost.

> **Není důležité, na co se díváš, ale co vidíš.**

Pokud český čtenář událost už zná, ale díky Business Briefu v ní uvidí něco, co by jinak přehlédl, produkt splnil svůj účel.

Tento průvodce proto začíná u úsudku. Technické struktury najdeš dále. Čti jej jako vysvětlení od kolegy, který ti předává svůj stůl: co na něm leží, proč to tam je, kde se už jednou spletl a na co si máš dát pozor.

### Co tento dokument skutečně ví

Podkladem je dostupná historie experimentu Fast Editorial v3, následná rekonstrukce a diskuse o předání. Nejsou použity pozdější procesní verze. Nemáme zde úplné původní PDF, celé mapy ani celé finální Briefy. Máme konkrétní zprávy o průběhu a rozhodnutích, včetně oprav a výsledků.

Aby tě text nezahltil výhradou v každém odstavci, platí toto rozlišení pro celý dokument:

- **Doložená zkušenost** jsou popsané události experimentu, názvy použitých průchodů a poznámek, zaznamenané výsledky a příklady oprav.
- **Předávaná redakční praxe** je srozumitelná rekonstrukce toho, jak tento způsob práce zopakovat. Výklad rozhodovacích situací a vyplněné vzory nejsou doslovným historickým Playbookem.
- **Současná produktová a redakční doktrína Business Briefu** je vědomá vrstva v4. Nejde o tvrzení, že všechny tyto principy byly ve v3 explicitně pojmenované, ale o dnešní definici toho, jakou hodnotu má Fast Editorial vytvářet.
- **Technická implementace** je oddělená otázka. Logické struktury v tomto dokumentu jsou pracovní kontrakty pro předání, ne povinnost obnovovat historickou technickou infrastrukturu v3.

Čísla z experimentu v příkladech slouží k vysvětlení redakčního rozhodování. Nejsou aktuálními zprávami ani nově ověřenými fakty pro publikaci. Vyplněné ukázky poznámek níže jsou didaktické rekonstrukce, nikoli export originálních řádků.

## Jak se v průvodci orientovat

1. Co dělá dobrý Brief a jak se díváme na noviny.
2. Jak číst vydání a rozpoznávat hodnotu článků.
3. Co je mapa a proč ji zmrazujeme.
4. Jak vznikají skutečné denní příběhy v Cross-Paper.
5. Kdy a jak se vracet do hloubky.
6. Jak osm redakčních pohledů promění podklady v text.
7. Jak poznat, že vydání funguje.
8. Jak zapisovat Editorial Notes, aby nesly zkušenost.
9. Jak řešit obtížné situace a obnovit práci.
10. Jak zachovat kontinuitu mezi dny a při předání.
11. Praktické šablony, historie experimentu a předání.

Praktické přílohy: **A** šest struktur; **B** ukládání na checkpointech; **C** doložené výsledky; **D** potřebné originální podklady; **E** startovací zadání; **F** rada editorovi; **G** celý den krok za krokem; **H** úplný slovník polí; **I** životní cyklus artefaktů; **J** přenos živého kontextu; **K** pravomoci osmi editorů; **L** stavba a rozsah Briefu; **M** kontrola všech hlavních oblastí; **N** závěrečné sebehodnocení A/B/C.

Aktuální stav rozpracované práce patří do EDITORIAL_HANDOVER.md. Tento dokument vysvětluje metodu a mění se při vědomé změně metody, nikoli po každém novém vydání.

---

## 1. Jaký Brief se snažíme vytvořit

### Čtenář má získat orientaci a porozumění

Umět vyjmenovat události není totéž jako rozumět dni. Představ si pět zpráv o výnosech dluhopisů, sazbách, zadlužení firem, rozpočtech a hypotékách. Můžeš z nich udělat pět korektních výtahů. Čtenář se dozví pět věcí, ale nemusí uvidět, že růst ceny kapitálu prochází různými částmi ekonomiky.

Na druhou stranu je nemůžeš bez rozmyslu slepit do obecného tvrzení „všechno zdražuje“. Tím bys zahodil rozdílné mechanismy, časové horizonty a důkazy. Dobrý Brief hledá míru: společnou souvislost vysvětlí a důležité rozdíly zachová.

Právě mezi těmito dvěma chybami pracuje redakční úsudek. Příliš roztříštěné vydání nechá syntézu na čtenáři. Příliš uhlazené vydání mu nabídne přesvědčivý, ale zjednodušený příběh.

### Nejen co se stalo, ale co v tom noviny vidí

Business Brief není překladač ani soupis zpráv. U hodnotného textu se ptej: co autor vidí, jakou otázku si klade, jak problém rámuje, na čem staví argument, co komplikuje snadný závěr a co zůstává otevřené.

FT, WSJ a Handelsblatt mohou popisovat stejnou událost, ale vidět jiné příčiny, rizika, vítěze a poražené, historické paralely nebo strategické otázky. Tyto rozdíly nejsou šum k vyhlazení. Často jsou samotnou hodnotou produktu.

> **Nekomprimuj text tak, že zachováš fakta, ale ztratíš autora.**

Kontrolní otázka: kdyby autor originálu četl naše zpracování, poznal by v něm svou otázku a argument, nebo jen data, která použil?

### Event importance a reading value nejsou totéž

Sleduj dvě odlišné veličiny. **Event importance** říká, jak významná je samotná událost. **Reading value** říká, jak hodnotný je konkrétní text pro čtenářovo přemýšlení. Velká událost může mít rutinní článek. Menší téma může obsahovat mimořádný argument, interview, analýzu nebo mentální rámec.

Při výběru se proto neptej jen „Je to důležité?“, ale také:

> **Ztratil by český čtenář zajímavý způsob vidění světa, kdybychom tento text vynechali?**

### Důležitost není jen velikost titulku

Velký titulek je informace o tom, co zdůrazňuje daná redakce. Ber ho vážně. Ale i krátký text uvnitř čísla může popisovat podstatnou změnu. A dlouhá analýza nemusí být dnešním hlavním příběhem, přestože může být výborná pro kuraci.

Hledej, co se změnilo, komu na tom záleží, jak to funguje a zda článek přináší něco, co stojí za čtenářův čas. „Je to o velké firmě“ není úplná odpověď. „Je to originální“ také nestačí, pokud originalita nemá pro produkt význam.

Původní v3 experiment neměl v dostupném záznamu přesnou personu. Současný Business Brief však cílí především na českého manažera, podnikatele, investora, odborníka nebo profesně zvídavého člověka, který nemá čas systematicky číst FT, WSJ a Handelsblatt, ale chce rozumět nejen událostem, nýbrž i argumentům, otázkám a perspektivám. Nevymýšlej mu další socioekonomické vlastnosti, které produkt nedefinuje.

### Brief má být velkorysý k času čtenáře

Nenuť čtenáře odhadovat, proč mu nějakou informaci dáváš. Nestačí napsat, že se něco stalo a „má to zásadní důsledky“. Vysvětli jeden konkrétní důsledek nebo přesný mechanismus, pokud jej zdroje podporují.

Přitom nevysvětluj každému tématu celý svět od začátku. Krátká věta může stačit tam, kde jde o coverage. Hlavní příběh si zaslouží více prostoru, protože bez něj by čtenář nepochopil změnu.

Přirozený jazyk není povrchnost. Přesnost nemusí znít akademicky. Když se ti pointa nedaří říct srozumitelně, vrať se k otázce, zda jí skutečně rozumíš.

### Čtenář má dostat perspektivu, ne povinný názor

Business Brief může vysvětlovat, porovnávat a hodnotit redakční přínos. Nemá tři noviny slít do jedné syntetické doktríny ani čtenáři vnucovat jediný správný závěr. Když se kvalitní zdroje dívají na stejnou věc jinak, může být právě tento rozdíl tím nejcennějším.

Dobrá četba nemusí vždy nejistotu zmenšit. Někdy je pokrok, že čtenář vidí více relevantních možností, ostřejší napětí nebo lepší otázku.

> **Nechceme, aby čtenář odcházel s povinným názorem. Chceme, aby odcházel posunutý.**

### Coverage safety net

Zájem o originální perspektivy nesmí vytlačit hlavní zprávy dne. Čtenář potřebuje jistotu, že výběr je záměrný, nikoli náhodně neúplný. Hlavní události proto mohou být pokryté stručně, i když jejich články nepřinášejí mimořádnou reading value.

> **Main news can be brief. Distinctive journalism deserves depth.**

### Curiosity má vycházet z obsahu

Čtenářskou zvědavost nevyvoláváme zadržováním odpovědi. Pokud text ví, proč je problém důležitý, řekne to. Další čtení má nabídnout hloubku, nikoli teprve základní vysvětlení slibu z titulku.

Například finanční role Nvidie může otevřít otázku, jak se v AI ekonomice propojuje zákazník, dodavatel a financování. Nemusíme předstírat tajemství. Stačí přesně ukázat zajímavý mechanismus a jeho omezení.

Reading recommendation je samostatná redakční funkce. Pokud článek stojí za hlubší pozornost, řekni čtenáři **proč**: jakou perspektivu, otázku, argument nebo zkušenost mu další čtení přinese. Kurace není zbytkový koš.

> **Nechceme čtenáře od čtení odvádět. Chceme mu pomoci poznat, co opravdu stojí za jeho čas.**

### Úplnost je závazek při čtení, selekce při vydávání

Není v pořádku vyrobit dobrý text z několika náhodně otevřených článků a tvrdit, že jsme zmapovali číslo. Je ale správné po úplném prohlédnutí vybrat jen část obsahu do výsledku.

Při čtení dlužíš vydání pozornost. Při psaní dlužíš čtenáři výběr. Tento rozdíl drž od prvního dne.

## 2. Jeden Chat jako souvislý editor

Síla experimentu spočívala v návaznosti. Tentýž Chat prošel vydání, pamatoval si jejich rozdíly, vytvořil topics, vracel se ke zdrojům a psal. Když narazil na nepřesnost, mohl opravit nejen izolované číslo, ale i svůj výklad celého příběhu.

Osm redakčních rolí jsou různé otázky kladené jedné společné práci. Není nutné z nich vyrábět osm oddělených agentů. To by změnilo způsob práce, který tu předáváme.

Živá paměť je užitečná, ale nemůže být jediným nositelem podstatných informací. Co musí přežít ztrátu kontextu, zapiš: zdrojové odkazy, výběr, významné nejistoty, změny interpretace a kanonické výsledky. Co je jen pracovní formulace nebo drobná stylistická volba, nemusí mít vlastní objekt.

Není cílem zachytit celý vnitřní proces přemýšlení. Zapisuj stručné důvody rozhodnutí, důkazy a dopady. Další editor potřebuje pochopit výsledek úsudku, ne číst každou dočasnou odbočku.

Když přebíráš práci, rozliš dvě věty: „předchozí Chat oznámil, že je mapa frozen“ a „načetl jsem frozen mapu a zkontroloval její stav“. Obě mohou být pravdivé, ale nejsou totožné.

## 3. První vydání: nejprve zjisti, co skutečně držíš

Před čtením identifikuj titul, celé datum a konkrétní vydání. Den experimentu není náhradou kalendářního data. Rok neodvozuj ze současného data. Pokud se ti dostane druhá varianta téhož čísla, nejprve ověř, zda je to duplikát, jiné vydání či opravený soubor.

Zaregistruj zdroj a pořadí příjmu, teprve potom začni mapovat. Day 2 začal WSJ, Day 3 FT. Pořadí je skutečnost, kterou zaznamenáš; není to žebříček důvěryhodnosti ani předepsaná dramaturgie.

Zjisti počet stran a kvalitu textové vrstvy. Extrahovaný text, který míchá sloupce a sousední články, není spolehlivý jen proto, že jde kopírovat. U textových PDF kontroluj layout tam, kde potřebuješ oddělit články, doplnit pokračování nebo přiřadit číslo správnému textu.

U obrazového PDF čti z renderů. V experimentu se FT o 18 stranách procházelo vizuálně bez OCR celého čísla. Z toho neplyne zákaz OCR za všech okolností. Plyne z toho, že plné OCR nebylo podmínkou Fast Editorial. Nečitelnou konkrétní pasáž musíš získat čitelně, pokud na ní závisí rozhodnutí.

Pokud první vizuální preflight proběhl před registrací runu, zaznamenej to. Ve v3 se taková odchylka u FT přiznala. Přesný audit znamená pravdivý záznam, nikoli uměle dokonalou časovou osu.

## 4. Jak číst celé číslo a neztratit se v něm

### Čti s otevřeným výběrem

Na prvních stranách si můžeš udělat představu o charakteru čísla. Nedovol, aby se z ní stal předčasný filtr. Když titulní strana zdůrazňuje AI a sazby, stále musíš projít průmysl, banky, obchod a ostatní relevantní části.

U každého článku si zkus říct dvě odlišné věty: co tvrdí a proč může být důležitý. Druhá věta nesmí být jen přepsaný titulek. „Výnosy rostou“ je obsah. „Dražší financování se přenáší do rozhodování firem“ může být redakční význam, pokud to článek skutečně dokládá.

### Dbej na hranice článku

Teaser na titulní straně a pokračování uvnitř nejsou dva objekty. Dva sousední články na jedné stránce nejsou jeden objekt. Krátký box může být součástí vysvětlení hlavního článku, ale může také nést samostatný relevantní příspěvek. Rozhodni podle obsahu a zaznamenej vazbu, pokud by ji další editor nemusel poznat.

Zvlášť pozor na články, které extrakce spojí přes několik sloupců. Číselný údaj z vedlejšího textu může vytvořit velmi věrohodnou chybu.

### Žánr je součást evidence

Zpráva, interview, FT View, Opinion a Lex mohou přinášet hodnotu, ale jiným způsobem. Názor ekonoma nebo manažera může být důležitý signál. Nemění se tím v nezávisle doložený fakt.

U interview odděl to, co respondent oznamuje, od toho, jak vysvětluje svět a co slibuje. Výrok o budoucnosti označ jako očekávání či záměr. U komentáře nepředpokládej, že všechna jeho faktická východiska jsou již ověřena pro naše vlastní tvrzení.

### Nezahrnutí také potřebuje orientaci

Reklamní přílohy a partner content nepřeváděj do běžné editorial mapy. Tabulkové tržní stránky nejsou automaticky sbírkou samostatných článků. V experimentu se kontrolovaly i arts stránky, ale kulturní recenze nebyly zařazeny do businessové mapy.

Nemusíš vytvářet záznam každé vynechané reklamy. Stačí v závěru vydání uvést, které typy nebo rozsahy stran byly zkontrolované a nezahrnuté. „Nezahrnuto“ musí být odlišitelné od „nepřečteno“.

## 5. Jak rozpoznávat relevantní články

Následující rozlišení je praktická rekonstrukce úsudku, nikoli původní bodovací rubrika. Jeho účelem je pomoci ti všimnout si hodnoty, ne přidělit každému textu matematické skóre.

### Co z článku musíš pochopit

U editorialně významného textu se pokus určit nejen „co tvrdí“, ale také:

- jakou otázku si autor klade;
- jak téma rámuje;
- jakou argumentační osu vede;
- co považuje za podstatné;
- jaké důkazy, příklady nebo osoby používá;
- kde připouští protiargument nebo nejistotu;
- co je na textu nové, překvapivé nebo charakteristické pro dané médium;
- co by český čtenář bez tohoto textu pravděpodobně neviděl.

Není-li autorova otázka nebo argument bezpečně rozpoznatelný, nevymýšlej jej. Označ potřebu hlubšího čtení.

### Co může dát článku vysokou hodnotu

**Nová skutečnost s významným dopadem.** Událost mění situaci pro trh, odvětví, stát nebo důležitou skupinu lidí. Potřebuješ vědět, co je skutečně nové a co je již známé pozadí.

**Mechanismus, který dosud nebyl vidět.** Text vysvětluje, proč se něco děje. Day 3 WSJ o skladbě kupujících Treasuries byl zajímavý právě tím, že mohl přidat mechanismus za známý pohyb výnosů.

**Přenos z jedné oblasti do druhé.** Cena ropy se může proměnit v náklad domácností, pricing firem nebo inflační tlak. Přenos ale musí být podložený; nesmíš jej odvodit pouze z toho, že dvě věci nastaly zároveň.

**Konkrétní případ širší změny.** Malý případ může být výmluvný, pokud zdroj vysvětluje jeho reprezentativnost. Jedna zajímavá firma sama nedokládá trend celého odvětví.

**Silná strategická otázka.** Interview, analýza nebo dlouhý text mohou ukázat rozhodování s dlouhodobými důsledky. Nemusejí být leadem; mohou být výbornou kurací.

**Důležitá protiváha.** Text může komplikovat příběh, který ostatní zdroje líčí příliš hladce. Jeho hodnota může spočívat právě v omezení naší vlastní teze.

### Event importance, reading value a CORE/CANDIDATE/LOW

Event importance a reading value drž odděleně. CORE/CANDIDATE/LOW je pracovní priorita uvnitř samostatně čteného vydání, která má zohlednit obojí i charakter konkrétního čísla. Není to matematický součet ani finální publication decision.

### CORE, CANDIDATE a LOW

CORE používej pro objekty, bez kterých by samostatný obraz vydání ztratil významnou část své businessové hodnoty. Může to být velká událost, silný mechanismus nebo mimořádný původní příspěvek. CORE není synonymum titulní strany.

CANDIDATE je relevantní článek, jehož konečné využití záleží na denním obrazu, přínosu vůči jiným zdrojům a prostoru. Není to slabší známka kvality psaní novin. Může se později stát důležitou částí hlavního topicu.

LOW je relevantní objekt s nižší předběžnou prioritou pro tento produkt a toto vydání. Nemá být zásobníkem všeho, co zůstalo na stránce. Reklama či irelevantní obsah nemusí být v mapě vůbec.

U hraničního případu napiš krátce důvod: „relevantní, ale zatím především firemní událost bez doloženého širšího dopadu“ je užitečnější než neurčité „středně důležité“.

### Co dělat, když si nejsi jistý

Jestli nevíš, co článek říká, ještě jsi jej dostatečně nepochopil: dočti potřebnou pasáž. Jestli víš, co říká, ale nevíš, jak důležitý bude v dnešním celku, může zůstat CANDIDATE. Jestli je nejasná konkrétní metrika či rozsah, zapiš otázku pro Deep Read; rozhodnutí o prioritě nepředstírej jako ověření všech detailů.

Nedávej CORE jen proto, že by ti bylo líto článek ztratit. Od toho máš mapu, CANDIDATE a později RESERVE. Záznam zachovává možnost návratu bez povinnosti publikovat.

### Dlouhodobá hodnota není úkolem této fáze

Původní experiment evidoval také Memory candidate, ale nový Fast Editorial je na této vrstvě záměrně nezávislý na Deep / Memory infrastruktuře. Pokud si všimneš strukturálně významného textu, můžeš jeho dlouhodobou hodnotu stručně poznamenat v Editorial Notes nebo handoveru, ale nevytvářej tím nový povinný workflow ani technickou závislost.

## 6. Issue Map: co musí uchovat a co nemá předstírat

Mapa má umožnit pozdější srovnání a návrat ke zdroji. Nemá být prvním návrhem celého Briefu. Dobrá položka zachytí identitu článku, jeho vlastní pointu, redakční hodnotu a důležité otázky.

U textu s vyšší perspective value musí mapa zachovat i to, **jak autor nebo médium problém vidí**: jeho otázku, frame nebo argumentační osu. Ne každý článek potřebuje dlouhý interpretační zápis; ale tam, kde právě perspektiva tvoří hodnotu, nesmí při mapování zmizet.

Když napíšeš jen „AI / významné / CORE“, další editor z toho nic nezíská. Když napíšeš dlouhý obecný esej o AI, ztratíš konkrétní článek. Hledej přiměřenou prostřední úroveň: několik přesných vět a spolehlivý lokátor.

Lokátor musí člověka nebo další Chat dovést na stejné místo. Pokud se liší fyzická strana PDF a tištěné číslo stránky, uchovej obě, když je znáš. Záznam „strana 8“ bez určení souboru není dostatečný. Původní titulek nepočešťuj tak, že jej potom nepůjde identifikovat; pracovní český název může být vedle něj.

Závěr vydání má říct, jaké bylo jeho redakční těžiště, čím přispělo, co zůstává nejisté a které objekty musí zůstat odlišitelné. Počty jsou kontrola konzistence, ne hlavní obsah závěru.

Freeze znamená: samostatné čtení tohoto vydání je uzavřeno a jeho původní úsudek uchován. Další noviny nesmějí přepsat to, co jsme viděli nezávisle. Oprava objektivní chyby je možná, ale zřetelně a s uchováním původního snapshotu. Tento opravný mechanismus je naše praktické doporučení pro přenos, nikoli doložená původní technická funkce.

Po freeze pošli uživateli stručný stav: titul je hotový, co jej charakterizuje, případné podstatné omezení a co následuje. Nepředstírej již hotové denní závěry.

## 7. Druhé a třetí vydání: nezávislost při zachované paměti

Předchozí titul nelze z živého kontextu vymazat a není to potřeba. Důležitá je disciplína rozhodnutí. Při čtení nového čísla nevynechávej článek proto, že podobný už znáš. Právě rozdíly v podání mohou být později cenné.

Naopak nehledej za každou cenu potvrzení oblíbeného tématu z prvního titulu. Pokud druhé noviny přinášejí jiný silný příběh, dovol jim jej ukázat. Počet zmínek není jediným měřítkem důležitosti.

V tomto kroku ještě nerozhoduj „FT je primary a WSJ supporting“. To jsou role v konkrétním Daily Topic, který vznikne až při Cross-Paper. Značka novin nemá stálou roli pro všechny příběhy.

Po každém titulu proveď stejné uzavření a freeze. Třetí vydání není jen doplněk ke dvěma předchozím. Má dostat stejnou možnost přinést vlastní hodnotu.

## 8. Cross-Paper: hledání příběhu pod články

Teď poprvé smíš z trojice vydání vytvářet společný obraz dne. Máš již dostatek podkladů, abys rozhodoval, které podobnosti něco znamenají a které jsou jen slovní.

Cross-Paper nemá hledat společné minimum. Ptej se také: **na co se všechny zdroje dívají a co každý z nich vidí jinak?** Syntéza je dobrá tehdy, když rozdíly a souvislosti zviditelní, ne když je uhladí do průměru.

### Začni otázkou, nikoli složkou

Topic „AI“ je příliš široký. Topic „jak bezpečnostní rizika mění kapitálový závod AI“ už pojmenovává napětí. Ještě musíš ověřit, že jej zdroje skutečně nesou.

Stejná událost je přirozený důvod ke spojení, ale není jediný. Články mohou společně vysvětlovat mechanismus, například přenos vyšší ceny kapitálu. Nemusíš však spojit všechny dopady do jednoho topicu už zde. Můžeš zachovat samostatné topics a propojit je až dramaturgicky.

### Rozliš tři druhy vztahu

**Popisují totéž.** Vyber hlavní nosný zdroj, ostatní přidají doplnění či nezávislé potvrzení, pokud skutečně jsou nezávislé.

**Doplňují se.** Jeden text přináší událost, druhý mechanismus nebo důsledek. Pojmenuj, co přidává každý, a nevydávej nově vytvořenou souvislost za citát některého z nich.

**Jsou příbuzné, ale samostatné.** Bezpečnost AI, financování Nvidií a dostupnost datacenter se mohou objevit v jedné dramaturgické oblasti, aniž tvoří jeden Daily Topic.

Slučování musí čtenáři něco vysvětlit. Pokud jen šetří počet řádků v úložiště, nemá redakční důvod.

### Role zdrojů jsou konkrétní

Primary nese jádro konkrétního příběhu. Supporting přidává důkaz nebo aspekt. Contrasting upozorňuje na relevantní odlišný výklad či protitlak. Background poskytuje kontext. Ke každé vazbě přidej krátké vysvětlení příspěvku; samotná role je příliš chudá pro pozdější obnovení úsudku.

Tři články citující stejný podklad nejsou automaticky tři nezávislá potvrzení. Je-li jejich společný původ patrný, zachovej jej v poznámce. Toto je doporučení pro práci s evidencí, nikoli tvrzení o konkrétním incidentu experimentu.

### Rozpor nejprve rozlož

Ptáš se na stejný čas, stejné období, stejný segment, stejnou metriku a stejnou míru jistoty? Porovnáváš stav při uzávěrce s intradenní hodnotou? Celý trh s vybranými firmami? Schválený závazek s uvažovaným maximem?

Teprve když tyto rozdíly nevysvětlují nesoulad, máš skutečný rozpor. Pak jej vyřeš návratem ke zdrojům, nebo jej transparentně ponech jako nejistotu. Nevybírej pohodlnější údaj jen proto, že lépe sedí do titulku.

### INCLUDE, RESERVE, EXCLUDE

INCLUDE je rozhodnutí, že topic patří do další hlavní redakční práce. Neurčuje ještě jeho konečnou délku ani sekci. RESERVE je relevantní materiál, který nyní není hlavní volbou, ale může posloužit coverage, kuraci či změně výběru. EXCLUDE znamená vědomě nepoužít v tomto dni; důvod může být nízká relevance, duplicita či nedostatečný podklad.

Nepotřebuješ vytvořit topic pro každý článek jen proto, aby se všechny položky mapy „spotřebovaly“. Mapa je širší než denní výběr. Pokud však vypadne významný CORE příspěvek, měl bys umět říct proč.

Při hraničním rozhodnutí znovu použij dvojí test: co musí čtenář vědět kvůli orientaci a co by ztratil z hlediska způsobu vidění, kdybychom text vynechali. Silný single-source text může být INCLUDE právě kvůli reading value; počet titulů není náhradou úsudku.

Při hraničním rozhodnutí formuluj důvod, který by pochopil druhý editor: „obsahově silné, ale nepřináší nový denní posun; vhodné pro kuraci“ je použitelný důvod. „Nesedí“ nikoli.

## 9. Selective Deep Read: kdy přesně nastává

Hlavní soustředěný krok nastává po Cross-Paper a před psaním. V Day 2 jím prošlo všech dvanáct INCLUDE topics. Už v Issue Mapách se označovali pravděpodobní kandidáti, ale konečná fronta vycházela z denního výběru.

To neznamená, že předtím nesmíš dočíst nejasnou pasáž. Pro správnou identifikaci článku nebo jeho pointy se ke zdroji vrať okamžitě. A neznamená to, že po tomto kroku už nikdy neotevřeš PDF. Verification i běžná editorská práce mohou vyvolat další návrat.

| Situace | Co udělat |
| --- | --- |
| Nevíš, ke kterému článku patří odstavec | Vyjasnit hned při čtení; neodkládat chybnou identitu |
| Článek je srozumitelný, ale možná potřebuje přesná čísla | Zapsat otázku a kandidaturu pro Deep Read |
| Cross-Paper vybral INCLUDE | Prověřit potřebné zdrojové články před Editorial |
| Při psaní vznikne nové faktické tvrzení | Doložit jej před použitím; neopírat se jen o paměť |
| RESERVE se přesune do hlavního příběhu | Doplnit odpovídající hlubší ověření |
| RESERVE se použije krátce v coverage | Ověřit přesně to, co bude tvrzeno; nevydávat to za hotový plný Deep Read |
| Jazyková změna zesílí tvrzení | Znovu prověřit dotčený claim |
| Detail vyžaduje jinou hloubku | Nepředstírat, že Brief Deep Read automaticky pokryl celý Detail |

### Co znamená číst do hloubky

Otevři nosný článek a relevantní podpůrné články. Nevybírej jen větu, která potvrzuje tezi. Přečti okolí čísel, omezení, atribuce a závěr. U syntézy více zdrojů ověř také přechod mezi nimi: skutečně podporují společný mechanismus?

Před čtením si můžeš napsat známé otázky. Po čtení se zeptej, co tě překvapilo a co jsi předtím přehlédl. Tím chráníš druhou funkci Deep Read: hledání chyby, kterou sis ještě neuměl položit jako otázku.

Přidej ještě jednu kontrolu: **neztratila naše dosavadní syntéza právě to, co bylo na původním textu intelektuálně cenné?** Deep Read může napravit nejen chybný fakt nebo mechanismus, ale i příliš ploché zacházení s autorovou otázkou, argumentem či nejistotou.

### Kdy je hotovo

Máš dostatečně jasné, co topic tvrdí, o které zdroje se opírá, jaký je rozsah tvrzení a co zůstává nejisté. Zásadní nevyřešený problém nemůže zmizet pod statusem done. Můžeš dokončit review se závěrem, že claim nelze použít nebo že topic má jít do rezervy; to ale není faktické schválení původní verze.

Jestli zdroj potřebný pro nosné tvrzení není dostupný, přesně pojmenuj mezeru. Nepřeváděj starší konverzační hlášení nebo obecnou znalost do údajně nového ověření.

### Co jsme se naučili na konkrétních případech

Toyota: problém nebyl v nesprávně opsaném čísle, ale v rozsahu věty. Červenec u evropských soukromých zákazníků není celoroční evropský trh. Dobrá poznámka musí tuto hranici přenést až do finálního titulku.

Defence-tech: zdroje mohly být jednotlivě dobře přečtené, ale společný rámec „soukromý kapitál“ neseděl na Rusko. Oprava změnila interpretaci, nikoli jen detail. To je důvod, proč Deep Read prověřuje také syntézu.

Nvidia: dostupné prostředky, možná výše garancí a názor „too big to fail“ jsou tři různé druhy tvrzení. Velké číslo a známé jméno nesmějí přeskočit podmínky a atribuci.

Belgie: atraktivní titulek o návratu k jádru se musí vejít do skutečného technického a vyjednávacího stavu. Restartovatelnost reaktorů a rozdělení nákladů nejsou podružné výjimky, pokud mění podstatu zprávy.

## 10. Přechod do Editorial: přestaň jen spravovat podklady

Po Deep Read už máš materiál pro vydání. Je čas rozhodnout, jak jej čtenáři předáš. Ne každému topicu patří samostatný miničlánek. Ne všechno, co jsi obtížně ověřil, musí zůstat v hlavním textu.

Nepřipoutej se k nákladům své práce. Dlouhé ověřování není redakční argument pro dlouhou položku. Může skončit jednou přesnou větou, která čtenáři ušetří nedorozumění.

Osm průchodů dělej skutečně postupně nad společným vývojem textu. Na konci nesepisuj zpětně osm fiktivních kontrol jen proto, aby vznikla kompletní sada poznámek.

## 11. Assignment Editor: z čeho má dnešní vydání být

Podívej se na celý den a navrhni jeho obsahové zadání. Které věci čtenář nesmí minout? Co potřebuje vysvětlení? Co stačí krátce zaznamenat? Co je zajímavé další čtení?

Záměrně odděl **coverage** a **reading value**. Velká událost může dostat krátké, přesné pokrytí. Menší text s mimořádným argumentem nebo perspektivou může dostat výraznou kuraci či větší prostor. Nevyžaduj, aby jeden žebříček řešil obě funkce.

Vycházej z topics po Deep Read a z rezervy. Znovu neprovádíš nezávislé mapování novin; rozhoduješ o využití již pochopeného materiálu. Pokud se objeví mezera, vrať se k mapám a zdrojům.

Výsledek má být srozumitelný i bez otevřených podkladových artefaktů: „dnes vysvětlíme cenu kapitálu a její přenos, fyzické limity ropy, napětí v AI a novou ekonomiku obrany; ostatní významné události pokryjeme kratší vrstvou“. To je obsahové zadání, nikoli ještě hotový text.

V poznámce zachyť hlavní výběr, funkci důležitých vedlejších témat, případně co zůstalo v rezervě a proč. Pokud využiješ reserve nad dosavadní úroveň ověření, doplň zdrojovou práci. Automatické INCLUDE pro každý CORE neexistuje.

## 12. Dramaturg: dej vydání tvar

Představ si průchod čtenáře celým textem. Co uvidí nejdřív? Kde musí zpomalit? Kde potřebuje zrychlit? Nevyčerpá první dlouhá položka všechnu pozornost? Nenásledují za sebou tři podobné příběhy, které si čtenář začne plést?

Hierarchie se vytváří pořadím, délkou, přesností úvodu a množstvím vysvětlení. Nestačí dát všem stejný blok a prvnímu přidat označení „hlavní“.

V Day 2 vznikly čtyři vrcholy a sedm hlavních jednotek. Dramaturg spojil sazby s dopady do bilancí a rozpočtů a západní AI safety s čínským paradoxem. Nvidia a fyzická infrastruktura zůstaly odlišitelné. To je konkrétní zkušenost, nikoli příkaz vyrábět každý den stejnou kompozici.

Pokud dvě témata propojíš, uchovej jejich původní identity a zdrojové vazby. Nemusíš kvůli tomu zpětně přepsat Cross-Paper ani frozen mapy. V textu však nesmí vzniknout kauzalita, kterou zdroje nepodporují.

V dramaturgické poznámce popiš pořadí, vrcholy, spojení a účel kratších vrstev. Není třeba plánovat každou větu.

## 13. Story Editor: najdi přesnou pointu

U každé hlavní jednotky si polož otázku: co by měl čtenář umět po přečtení říct vlastními slovy? Pokud odpověď zní jen „je to důležité téma“, příběh ještě nemáš.

U textů s vysokou perspective value se ptej také: **jaký způsob vidění má po přečtení zůstat v hlavě?** Pointa nemusí být jen „co se stalo“. Může být v tom, jak autor přesouvá otázku, komplikuje běžný rámec nebo ukazuje mechanismus, který v české debatě nebývá vidět.

Úhel není ozdobný titulek. Je to vybraná cesta materiálem. U Treasury může být úhlem překročení hranice, změna kupujících nebo přenos do financování. Nevybírej je podle atraktivity slov, ale podle toho, co dnes přibylo a co nesou zdroje.

Příběh nemusí obsahovat konflikt dvou osob. Může jít o napětí mezi ambicí a fyzickou kapacitou, mezi investicemi a rizikem nebo mezi krátkodobým pohybem a dlouhodobou strukturou. Nenutíš každému textu stejné dramatické schéma.

Zapiš pointu, why_now, hlavní mechanismus a hranici tvrzení. Pokud nedokážeš formulovat úhel bez přesahu přes zdroje, zúž jej nebo se vrať k Deep Read.

## 14. Brief Writer: napiš čtenáři text, který lze číst

Teď už nepíšeš poznámky pro sebe. Píšeš člověku, který neviděl tvoje tabulky. V úvodu mu dej orientaci. V hlavních příbězích vysvětli změnu a význam. V kratších položkách nezdržuj. Kuraci zdůvodni konkrétní hodnotou textu.

Piš inteligentně, ale ne akademicky; zvědavě, ne vševědoucně; sebevědomě ve výběru, skromně v soudech. Rozlišuj fakt, interpretaci autora a vlastní syntézu Business Briefu. Nenuť čtenáři jeden správný názor tam, kde kvalitní zdroje nechávají prostor pro více rozumných interpretací.

Nezačínej každou položku stejným obecným úvodem. Neopakuj u každé „co to znamená pro byznys“, pokud můžeš význam přirozeně vysvětlit v jedné větě. Různé příběhy potřebují různou stavbu.

Termín použij, když pomáhá přesnosti, a vysvětli jej tam, kde je to potřeba. „Hyperscaler“ není zakázané slovo, ale nesmí být náhradou za pochopení toho, o kterých firmách a obchodních modelech mluvíš.

Pozor na drobná slova: „už“, „stále“, „poprvé“, „zůstává“, „všichni“, „musí“. Často do textu propašují historické, kvantitativní nebo kauzální tvrzení, které žádná tabulka čísel nekontrolovala.

Nevkládej do čtenářského textu provozní značky CORE, INCLUDE nebo PASS. Podkladová struktura je pro redakci. Čtenářská struktura je pro porozumění.

Draft ulož jako jednu konkrétní verzi. Nestačí napsat do poznámky, že „draft vznikl“. Musí existovat text, ke kterému se další kontrola vztahuje.

## 15. Detail Editor: dej Briefu plnou hodnotu a zachovej hloubku

Ptej se, zda čtenář po Briefu chápe pointu a zda případné další čtení nabízí něco skutečného navíc. Pokud musí otevřít Detail, aby se dozvěděl, co se vlastně stalo, Brief neposkytl slíbenou hodnotu. Pokud už Brief vyčerpal všechny argumenty, důkazy a výjimky, pravděpodobně je příliš dlouhý nebo vztah k Detailu není dobře promyšlený.

Strong Detail value znamená, že téma má další podstatnou hloubku. Sufficient znamená, že rozvinutí má smysl, i když není dominantní. Weak je signál k přehodnocení rozsahu či umístění. Toto je výklad zaznamenaných kategorií, nikoli doložený přesný historický scoring.

Nevyráběj cliffhanger jen proto, aby přechod do Detailu vypadal lákavě. Napiš, co může hlubší čtení vysvětlit: finanční strukturu, rozdílné scénáře, technické limity, rozdělení rizik.

Brief a Detail jsou komplementární produkty. Brief musí dát skutečné porozumění. Detail přidává argumentační strukturu, evidence, nuance, příklady a protiargumenty. **Nikdy nezhoršuj Brief proto, aby vznikl důvod kliknout dál.**

Tento pass neposkytuje důkaz, že Detail již existuje. Nevytvářej link na neexistující obsah a neoznamuj hotovou sadu Detailů pouze podle hodnocení jejich potenciálu.

## 16. Verification Editor: ověř, co je opravdu napsáno

Vrať se k textu jako k novému objektu. Přesně přečtené zdroje se mohly během psaní proměnit v nepřesné tvrzení. Kontroluj nejen čísla, ale také čas, podmínky, rozsah, atribuci a implikace.

Treasury je učebnicový případ: Deep Read rozlišil maximum 5,012 % a close 4,96 %. Přesto watchlist naznačil, že výnos může „zůstat“ nad 5 %. Správná čísla v podkladu tedy nezabránila chybné větě. Oprava se týkala slovesa a předpokládaného stavu.

Při kontrole si označ nosná tvrzení a přiřaď je k podkladům. Nemusíš vytvářet novou tabulku pro každou větu, pokud to stávající provenance umožňuje. Musíš ale dokázat ukázat, odkud klíčový claim pochází.

Jestli je věta vlastní syntézou, zkontroluj jednotlivé opory i oprávněnost propojení. Citace za odstavcem nesmí zakrýt fakt, že zdroj podporuje jen jeho první polovinu.

Výsledek poznámky má být konkrétní: které problémy byly nalezeny, jak se opravily a zda něco zůstává. „Všechno ověřeno“ bez vztahu k textové verzi a bez popisu rozsahu je slabý audit.

## 17. Language & Style Editor: nech text znít přirozeně

Přečti hlavní jednotky jako souvislé čtení nahlas. Nemáš-li zvukový výstup, udělej textovou kontrolu rytmu a nepředstírej provedenou audio zkoušku. V experimentu byl read-aloud test hlášen 7/7; není doložen přesný technický protokol.

Hledej příliš dlouhé věty, abstraktní podstatná jména, doslovné anglické obraty a opakované závěry. Krátit lze i přeskládáním věty, nejen vypouštěním informací.

Nesmaž „podle zdrojů“, „může“, „v červenci“ nebo „u soukromých zákazníků“, pokud tato slova nesou skutečnou hranici tvrzení. Plynulejší chybná věta není jazykové zlepšení.

Když jazyková úprava změní věcný význam, vrať dotčené místo do Verification. Když mění jen slovosled nebo odstraní zbytečné opakování, není potřeba znovu otevírat celý proces.

## 18. Editor-in-Chief: rozhodni o celku

Odlož na chvíli pocit, kolik práce už bylo hotovo. Posuzuj text, který dostane čtenář. Má den jasnou mapu? Jsou vrcholy skutečně vidět? Neztratila se důležitá událost mezi oblíbenými tématy? Nezní všechny odstavce stejně? Je text důvěryhodný a stojí za čtení?

Poslední editor může schválit bez zásahu. V Day 1 to tak proběhlo. Změna není dokladem pečlivosti sama o sobě.

Polož si také kontrolní otázku „mrtvolky článku“: **poznal by autor původního textu v našem zpracování svou otázku a argument, nebo jsme zachovali jen data?** Pokud zmizelo právě to, kvůli čemu stál text za pozornost, vrať jej k Story / Writer / Deep Read podle příčiny.

Pokud něco nefunguje, pojmenuj konkrétní problém a vrať jej tam, kde jej lze opravit. Chybějící podstatné téma patří k výběru; plochá hierarchie k dramaturgii; nepřesná pointa ke Story nebo Deep Read; nesprávné tvrzení k Verification. Není nutná rozsáhlá automatická návratová matice.

Po opravě znovu posuď dotčené vlastnosti. Finální PASS musí patřit skutečně poslední verzi textu, ne předchozímu draftu.

## 19. Jak číst finální brány

**Coverage:** Nechybí věc, jejíž nepřítomnost by zkreslila dnešní obraz? Neznamená to publikovat celou mapu. Významná vedlejší událost může být vyřešena krátce. V Day 1 se tak zachovala témata mimo leady.

**Hierarchy:** Je jasné, co má čtenář opravdu pochopit a co pouze zaznamenat? Otestuj první věty a délkové váhy. Pokud by šlo položky libovolně přeházet bez ztráty smyslu, může být dramaturgie slabá.

**Curiosity:** Nabízí text otázku nebo souvislost, která stojí za další pozornost? Nevyvolává jen neurčitý dojem, že se děje něco „zásadního“?

**Trust:** Neskrývá přesvědčivý jazyk nejistotu, názor či omezení? Odpovídá jistota formulace kvalitě zdroje?

**Product fit:** Dostává čtenář Business Brief, který mu pomůže orientovat se, nebo technickou zprávu o našem zpracování, soupis výtahů či přetíženou analýzu?

**90-second test:** Dá rychlý průchod textem mapu dne? V Day 1 byla výslovně popsána orientace po prvních pěti větách. Přesný měřicí protokol není doložen. Neměň tento test na nepodložený požadavek přečíst celý Brief za devadesát sekund.

Při neúspěchu nepiš jen FAIL. Uveď, co jej způsobuje a jaká změna je potřebná. Při úspěchu stačí stručné důvody, které ukážou skutečné posouzení.

K historicky doloženým branám přidej současné produktové testy Business Briefu:

**Perspective:** Přežil tam, kde na něm záleželo, autorův nebo mediální způsob vidění?

**Difference:** Ukázala cross-paper syntéza skutečné rozdíly a souvislosti, místo aby je vyhladila nebo uměle vyráběla?

**Reader autonomy:** Dáváme čtenáři kvalitní argumenty a perspektivy bez vnuceného závěru?

**Time respect:** Šetří text pozornost tím, že vybírá, nebo jen mechanicky zkracuje?

**Life:** Působí vydání jako živá redakční práce, nebo jako uniformní AI digest?


## 20. Jak může výsledné vydání působit

Přesné názvy sekcí musíme ověřit z autentických finálních Briefů. Následující vysvětlení jejich možných funkcí není tvrzením, že existoval závazný sedmisekční template.

„Dobré ráno“ může čtenáře uvést do dne. Nemá to být dlouhá obecná úvaha před zprávami. „Dnes v kostce“ může rychle zpřístupnit denní mapu. Pokud obě části říkají totéž, stačí funkci spojit nebo zkrátit.

„Hlavní příběhy“ nesou vysvětlení. Ne každý musí mít stejný počet odstavců. „Ještě potřebujete vědět“ chrání coverage a dává důležitým vedlejším věcem přiměřený prostor.

„Čísla dne“ mají smysl jen tehdy, když číslo něco osvětluje. Bez jednotky, období a kontextu je dekorací. Není nutné opakovat číslo z hlavního příběhu jen kvůli naplnění sekce.

„Co sledujeme“ má pojmenovat otevřenou otázku či další rozhodující vývoj. Nepředstírej budoucí datum nebo očekávanou událost, kterou zdroje nedávají. „Budeme sledovat situaci“ nic konkrétního nepřidává.

„Co dnes ještě stojí za přečtení“ vysvětluje hodnotu doporučeného textu. Kurace není zbytková hromádka. Rooftop solar a private equity v Day 1 měly vlastní místo, aniž byly násilně povýšeny na leady.

Tato vrstva je pro Business Brief first-class editorial function. U doporučení nestačí říct, že je článek „zajímavý“. Řekni, jakou otázku, argument, perspektivu, reporting nebo mentální rámec čtenář získá, když mu věnuje další čas.

## 21. Editorial Notes: napiš kolegovi, co by jinak nevěděl

Dobrá poznámka je krátké předání rozhodnutí. Představ si, že se za týden někdo zeptá: proč jsme spojili tyto články, proč jsme vybrali tento úhel a co nám zabránilo napsat širší tvrzení? Poznámka má odpovědět bez nutnosti znovu absolvovat celou konverzaci.

Nejde o dlouhé vysvětlování každé myšlenky. Potřebuješ identitu rozhodnutí, důvod, oporu, změnu a dopad. U passu bez změny napiš, co bylo kontrolováno a proč výsledek obstál.

### Kdy poznámku uložit

Ulož ji při uzavření příslušného kroku, dokud máš důvod rozhodnutí čerstvý. U významné opravy ji vytvoř rovnou, ne až při denní retrospektivě. Retrospektiva má shrnout zkušenost, nikoli dodatečně vymyslet audit, který během práce neexistoval.

Je-li zápis zablokovaný technicky, uchovej připravený obsah a označ jej jako nezapsaný. Nezaměň stav textu za stav persistence. Uživatel může vědět, že je redakční práce hotová, ale zápis čeká.

### Jak podrobná má být

Rutinní kontrola může být stručná. Změna společného rámce si zaslouží více prostoru. Není potřeba stejná délka poznámek pro všechny topics. Věta „opraveno“ je málo; deset odstavců o triviálním překlepu je zbytečně mnoho.

### Vyplněný příklad: změna interpretace

> **Typ:** deep_read_summary, téma Toyota/VW.  
> **Před čtením:** Topic naznačoval obecné předběhnutí Volkswagenu.  
> **Zjištění:** Předběhnutí se týká července u evropských soukromých zákazníků. Kumulativní období leden–červenec má jiné pořadí.  
> **Rozhodnutí:** Zúžit topic a budoucí titulek. INCLUDE zachovat.  
> **Důvod:** Zpráva zůstává relevantní, ale širší formulace není podložena.  
> **Dopad:** Zachovat období a prodejní kanál při každém pozdějším zkrácení.  
> **Evidence:** V reálném zápisu doplnit skutečné article ID a lokátor pasáže. V tomto rekonstruovaném příkladu nejsou dostupné.

### Vyplněný příklad: proč neslučovat

> **Typ:** cross_paper_map, rozhodnutí o AI topics.  
> **Rozhodnutí:** Fyzickou dostupnost infrastruktury a finanční roli Nvidie držet jako samostatné topics.  
> **Důvod:** Jedna otázka se týká provozní dostupnosti kapacity, druhá financování a koncentrace rizika. Společné označení AI nevyjadřuje jeden mechanismus.  
> **Dopad:** Mohou sousedit nebo být dramaturgicky propojené, ale zachovají vlastní pointu a provenance.  
> **Evidence:** Doplnit konkrétní source links z denního výběru.

### Vyplněný příklad: kontrola bez zásahu

> **Typ:** editor_in_chief_review_v1, konkrétní verze Briefu.  
> **Zjištění:** Úvod dává mapu dne, vrcholy mají zřetelnou váhu a vedlejší coverage nepřetěžuje hlavní čtení. Ověření nezanechalo nevyřešený nosný claim.  
> **Rozhodnutí:** Schválit beze změn.  
> **Důvod:** Další zásah nemá identifikovaný redakční přínos.  
> **Brány:** U každé uvést stručný skutečný důvod PASS, nikoli automaticky vložit tento příklad.  
> **Reference:** Přesná uložená verze textu.

### Vyplněný příklad: technická odchylka

> **Typ:** process_observation.  
> **Událost:** Redakční draft vznikl, ale zápis se neuchoval.  
> **Dopad:** Kanonická persistence PASS 4 nebyla dokončená; navazující stav nelze zatím vydávat za uložený.  
> **Náprava:** Zapsat připravený obsah správně a ověřit výsledný záznam.  
> **Redakční dopad:** Pokud text zůstává stejný, neopakovat výběr témat jen kvůli chybě zápisu.

### Přehled poznámek podle okamžiku

| Okamžik | Historicky používané označení | Co má zachovat |
| --- | --- | --- |
| Freeze vydání | issue_map_snapshot | Samostatný výsledek čtení a mapu |
| Odchylka nebo poučení | process_observation | Co nastalo, dopad a nápravu |
| Cross-Paper | cross_paper_map | Syntézu, rozlišení, výběr, provenance a frontu |
| Deep Read topicu | deep_read_summary | Co bylo čteno, zjištěno a omezeno |
| Významné interpretační změny | deep_read_changed_interpretation | Před/po, důvod a dopad |
| Assignment | editorial_selection_v1 | Obsahové zadání a využití témat |
| Dramaturgie | dramaturgy_plan_v1 | Pořadí, váhy, spojení a rytmus |
| Story | story_angles_v1 | Pointy, why_now a hranice |
| Writer | master_brief_draft_v1 | Draft nebo jednoznačný odkaz na něj |
| Detail | detail_gap_review_v1 | Vztah pointy Briefu k další hloubce |
| Verification | verification_review_v1 | Kontrolovaný text, opravy a zbývající problémy |
| Language | language_style_review_v1 | Jazykové zásahy a čitelnost |
| Chief | editor_in_chief_review_v1 | Finální úsudek a brány |
| Významné textové stavy | master_brief_claim_verified_v1; master_brief_language_edited_v1 | Přesné snapshoty textu |
| Uzavření dne | issue_retrospective_detailed; brief_build_notes; day_retrospective | Co jsme se naučili o čtení, tvorbě a dni |
| Časová návaznost | memory_would_help | Konkrétní případ, kde paměť pomáhá, a otevřenou úvahu |

Názvy jsou doložené z hlášení. Bez načtení schématu nelze říct, zda jsou uloženy jako note_type, title nebo jiná hodnota. Suffix _v1 není sám o sobě číslo kanonické verze celého Briefu.

## 22. Rozhodování v obtížných situacích

### Důležité téma stojí na slabém podkladu

Odděl důležitost od ověřitelnosti. Velká relevance nezlepší kvalitu evidence. Zjisti, zda lze napsat užší, dobře doloženou větu. Pokud nejde ověřit samotná pointa, neposouvej téma jako jistý hlavní příběh. Zapiš důvod a potřebný podklad.

### Jediný titul má výborný text

Nečekej na umělé potvrzení jeho existence v ostatních novinách. Posuď význam, zdrojovou kvalitu a přesnost. Single-source příběhy byly v Day 2 součástí INCLUDE. Zachovej atribuci tam, kde zdroj přináší exkluzivní nebo sporné tvrzení.

### Dva zdroje se skutečně neshodnou

Po kontrole času, rozsahu a metriky může rozpor zůstat. Nesnaž se jej vyřešit průměrem nebo výběrem líbivějšího čísla. Je-li podstatný pro pointu, vrať se ke zdrojům nebo popiš odlišná tvrzení s atribucí. Není-li možné vytvořit poctivou stručnou formulaci, claim nepoužij.

### Nový fakt zpochybní hotový topic

Uprav pracovní topic a zapiš změnu. Freeze samostatné Issue Mapy není zákaz poznání. Znamená uchovat původní samostatný úsudek; nová denní interpretace patří do topicu a poznámek.

### Zjistíš chybějící článek po freeze

Neprohlašuj, že tam byl celou dobu. Zaznamenej doplnění a důvod. Pokud ovlivňuje coverage či výběr, znovu posuď dotčené rozhodnutí. Původní snapshot zachovej. Jde o doporučenou opravu, nikoli historicky doložený konkrétní incident.

### Vydání je příliš dlouhé

Nezačni slepým zkrácením každé položky o stejné procento. Nejprve znovu posuď hierarchii: co musí být hlavní, co může být coverage a co patří do kurace. Potom odstraň opakování a nadbytečné vysvětlování. Až nakonec řeš jednotlivá slova.

### Vydání je správné, ale nudné

Nepřidávej silnější přídavná jména. Hledej konkrétní změnu, paradox nebo důsledek, který text ztratil. Možná jsou úhly příliš obecné nebo všechny položky mají stejný rytmus. Vrať se ke Story a dramaturgii.

### Uživatel chce všech osm passů najednou

Proveď je postupně bez zbytečných zastávek. V Day 2 to bylo výslovně zadáno. Nezaměň to za sloučení všech kontrol do jednoho neověřitelného tvrzení na konci. Jestli uživatel chce postupovat po jednom, respektuj to. Pauza není redakční role.

### Uživatel změní rozsah dne

Zachovej dokončené artefakty a jasně uveď nové zadání. Nesnaž se změnu maskovat jako původní plán. Pokud má být Brief jen ze dvou titulů, nelze jej popisovat jako standardní dokončenou třízdrojovou práci.

### Otevíráš článek na webu místo původního vydání

Webová verze může být novější nebo obsahově odlišná. Pokud ji uživatel povolil a použiješ ji, označ původ a časový rozdíl. Nenahrazuj jí potichu evidenci z historického PDF. Pro rekonstrukci experimentu mají přednost tehdejší konkrétní podklady.

### Chybí rok, zdrojový soubor nebo identifikátor

Nedoplňuj jej odhadem. Pojmenuj přesnou mezeru a dohledávej ji v autorizovaných podkladech. Z dnešního data nelze odvodit rok experimentálního čísla. ID není text, který si editor smí vymyslet podle titulku.

## 23. Časová kontinuita bez předurčení nového dne

V experimentu jsme si uvědomili, že horizontální spojení tří novin funguje lépe než formalizovaná osa přes čas. Uživatel upozornil na Treasury a vznikla poznámka memory_would_help. Nový povinný temporal pass ale zaveden nebyl.

Nes si z předchozího dne poslední ověřený stav, to, co jsme čtenáři už vysvětlili, a otevřené otázky. Při samostatném čtení dnešních vydání nepoužívej tento seznam jako objednávku leadů. Nový den může mít jiné těžiště.

Po freeze map zvaž, zda jde o pokračování, zesílení, obrat, nový mechanismus nebo pouhé opakování. Nepiš „pokračuje trend“ jen proto, že se téma objevilo dvakrát. Pokud souvislost znáš pouze z konverzační paměti, ověř ji před konkrétním publikovaným srovnáním.

Zkušenost s Treasury ukazuje možnou návaznost: cena kapitálu a blízkost hranice; intradenní překročení; další otázka struktury kupujících a přenosu do hypoték. Smyslem není znovu každý den vysvětlovat všechno, ale přesně říct, co dnešní zdroje přidaly.

## 24. Jak zacházet s koncem Chatu

Nespoléhej na to, že bude čas napsat dokonalé poslední předání. Ukládej dokončené artefakty průběžně a při denní retrospektivě obnov stručnou předávací poznámku. Nejlepší přechod je mezi dny nebo po uzavřeném kroku.

Novému Chatu předej tři druhy informace: tento způsob práce, autentické výsledky jako měřítko a aktuální stav s otevřenými příběhy. Přesný vnitřní kontext předchozího Chatu přenést nelze, ale lze obnovit pracovní porozumění.

Nepředávej pouze stále kratší souhrn souhrnu. Udržuj odkazy na skutečné mapy, texty, poznámky a zdroje. Při rozpracovaném dni musí být zřejmé, které části už byly ověřeny a které ne.

Po načtení má nový Chat stručně vyjádřit, co přebírá a co udělá dál. Nejde o nový gate ani povinné čekání na potvrzení, pokud má dost podkladů a zadání. Je to kontrola, že nezaměnil například dvě frozen mapy za dokončený Cross-Paper.

## 25. Co nepřidávat jen pro pocit úplnosti

Tento dlouhý průvodce má být bohatý vysvětlením, nikoli počtem povinností. Nepřeváděj každý jeho odstavec na pole, check-box nebo samostatný workflow run.

Nepotřebujeme skóre každého článku, kvótu témat, povinný konflikt v každém příběhu, stejné délky poznámek ani povinný zásah posledního editora. Nepotřebujeme samostatného agenta pro každou roli. Nepotřebujeme trendový objekt jen proto, že se něco objevilo dvakrát.

Potřebujeme spolehlivou identitu zdrojů, nezávislé mapy, poctivou syntézu, návrat ke zdrojům, čitelný text, skutečné kontroly a důvody zásadních rozhodnutí. Když přibývající administrativa začne bránit čtení a úsudku, vrať se k tomu, čemu má sloužit.

Stejně tak nepřidávej obsahové stereotypy jen proto, že vypadají redakčně: generické „proč je to důležité“, povinný konflikt, automatické manažerské implikace, tři zdroje jako podmínku významu nebo umělý závěr tam, kde článek nechává produktivní nejistotu.

---

# Praktická příloha: struktury a provozní orientace

Následující část soustředí šablony na jedno místo. Jsou to logické kontrakty pro přenos práce a pro dohledatelnost zdrojů. Nejsou databázovým schématem ani povinností používat konkrétní úložiště. Žádná ukázková hodnota není existujícím ID.

## A. Šest základních struktur

### Issue Map item

```yaml
item_id: "stabilní identita v rámci dne / artefaktu"
issue_id: "identita vydání"
source:
  file_ref: "dohledatelný zdroj"
  pdf_pages: []
  printed_pages: []
  continuation_locator: null
headline_original: ""
working_label_cs: ""
author: ""
genre: "news | analysis | interview | opinion | editorial | lex | other"
article_point: "co tvrdí tento článek, nikoli celý sektor"
author_view:
  question: ""
  frame: ""
  argument_or_angle: ""
what_is_new_or_useful: ""
event_importance: "HIGH | MEDIUM | LOW"
reading_value: "HIGH | MEDIUM | LOW"
priority: "CORE | CANDIDATE | LOW"
priority_reason: "krátce, zejména u hraničního případu"
deep_read_candidate: false
deep_read_questions: []
uncertainties: []
structural_notes: []
```

Identita, lokátor, obsahová pointa, žánr a priorita jsou základ. Pole pro nejistoty či pokračování používej tehdy, když mají obsah. Základní fact-check není nahrazen příznakem deep_read_candidate.

### Issue-level conclusion

```yaml
issue_id: ""
day_id: ""
publication: ""
issue_date: "ověřené celé datum"
intake_order: 1
source_file_ref: ""
page_count: null
reading_mode: "native_text_with_visual_checks | rendered_vision"
ocr_performed: false
coverage:
  all_pages_reviewed: false
  unread_or_unclear_parts: []
  reviewed_but_excluded_categories: []
editorial_currents: []
unique_contributions: []
important_distinctions: []
counts:
  total: null
  core: null
  candidate: null
  low: null
  deep_read_candidates: null
snapshot_ref: ""
status: "pracovní stav; frozen až po dokončení"
process_caveats: []
```

Čísla musí souhlasit s uloženými objekty. Nezaměň count kandidátů za počet dokončených Deep Reads. Pokud obsah zůstává nečitelný, závěr nesmí tvrdit úplné prověření bez omezení.

### Daily Topic a provenance

```yaml
topic_id: ""
day_id: ""
working_title: ""
central_question: ""
synthesis: ""
why_now: ""
decision: "include | reserve | exclude"
decision_reason: ""
source_links:
  - item_id: ""
    role: "primary | supporting | contrasting | background"
    contribution: "co tento konkrétní článek přidává"
    distinctive_perspective: "co tento zdroj vidí nebo rámuje jinak, pokud je to podstatné"
differences_and_tensions: []
reading_value_notes: []
open_questions: []
deep_read_status: "pending | done; přizpůsobit skutečnému schématu"
deep_read_note_ref: null
temporal_context:
  previous_evidence_refs: []
  supported_change: null
interpretation_changes: []
```

Každý source link musí vést k reálnému objektu. Článek označený primary nemusí dokazovat všechny věty finálního textu. U každé vlastní syntézy je třeba vědět, které části stojí na kterých podkladech.

### Deep Read Note

```yaml
note_type: "deep_read_summary"
day_id: ""
topic_id: ""
source_passages:
  - item_id: ""
    locator: ""
initial_interpretation: ""
known_questions: []
verified_findings:
  - finding: ""
    evidence_ref: ""
    scope_and_qualifications: ""
newly_discovered_problems: []
apparent_conflicts:
  - issue: ""
    resolution_or_remaining_uncertainty: ""
interpretation_before: ""
interpretation_after: ""
change_reason: ""
perspective_recovered_or_corrected: ""
wording_guardrails:
  safe_formulation: ""
  misleading_formulations: []
selection_before: ""
selection_after: ""
remaining_uncertainties: []
review_result: "dokončeno / potřebuje doplnění; není automaticky schválení všech claims"
```

### Editorial Note

```yaml
note_id: ""
note_type: "skutečná použitá kategorie"
scope:
  day_id: ""
  issue_ids: []
  topic_ids: []
  brief_id: null
  brief_version: null
  run_ref: null
review_question: ""
findings: []
decisions:
  - decision: ""
    reason: ""
    evidence_refs: []
changes:
  - before: ""
    after: ""
    impact: ""
unresolved: []
result: "pass | needs_revision | informational"
artifact_refs: []
created_at: "skutečný čas záznamu"
```

Ne všechna scope pole musejí být vyplněna. Vyplň ta, která určují rozsah poznámky. Poznámka k jedné mapě nemá předstírat denní závěr. Finální review musí mít konkrétní verzi textu.

### Master Brief metadata

```yaml
brief_id: ""
day_id: ""
edition_date: ""
version: null
status: "draft | verified; skutečné povolené hodnoty ověřit"
canonical_text_ref: "nebo přímo text podle původního schématu"
source_issue_ids: []
source_topic_ids: []
editorial_units:
  - unit_key: "identita uvnitř této verze; nemusí být DB brief_item"
    function: "main_story | coverage | watchlist | curated"
    topic_ids: []
    evidence_refs: []
review_note_refs: []
final_gates:
  coverage: ""
  hierarchy: ""
  curiosity: ""
  trust: ""
  product_fit: ""
  ninety_second_test: ""
  perspective: ""
  difference: ""
  reader_autonomy: ""
  time_respect: ""
  life: ""
known_limitations: []
verified_at: null
```

Vazba editorial_units je doporučení pro přenos provenance, nikoli důkaz, že historicky existovala v tomto tvaru. Přesný formát textu a metadata se musí přizpůsobit původnímu schématu.

## B. Co mít uložené na každém přirozeném checkpointu

| Checkpoint | Obsahový výsledek | Auditní záznam | Než řekneš „hotovo“ |
| --- | --- | --- | --- |
| Příjem vydání | Identita dne, vydání a zdroje | Skutečný start a pořadí | Ověřit, že nejde o duplicitní či jiné vydání |
| Freeze mapy | Objekty, lokátory, priority a závěr | Snapshot, procesní omezení | Zkontrolovat rozsah stran, counts a skutečné uložení artefaktu |
| Cross-Paper | Topics, rozhodnutí a source links | Důvody syntézy a fronta Deep Read | Ověřit vazby na existující články |
| Deep Read | Zpřesněné topics | Summary a významné změny | Nepřekrýt nevyřešenou pointu statusem done |
| Assignment až Story | Zadání, dramaturgie a úhly | Tři příslušné poznámky | Zachovat rozdíl mezi plánem a napsaným textem |
| Writer | Celý draft | Vazba na draft | Ověřit skutečné uložení textu / snapshotu |
| Detail až Language | Posouzení a opravený text | Review notes a potřebné snapshoty | Udržet kontrolu navázanou na správnou verzi |
| Chief | Schválený Master Brief | Brány a verdict | Ověřit kanonickou verzi, stav a podklady |
| Konec dne | Aktuální předání | Retrospektiva | Oddělit hotovou redakci od neprovedené publikace |

## C. Doložené body experimentu, podle kterých se lze kalibrovat

Day 1 / 14. 9. skončil Master Briefem v2 ve stavu verified. Mapa dne byla podle hlášení jasná po prvních pěti větách. Hlavní čtení mělo čtyři vrcholy, coverage držela další významné události a kurace měla vlastní místo. Všech osm průchodů bylo zaznamenáno, Chief neprovedl další zásah.

Day 2 / 15. 9. začal WSJ: 38 objektů, z toho 8 CORE, 22 CANDIDATE, 8 LOW. FT: 41 objektů, 11 CORE, 26 CANDIDATE, 4 LOW. HB: 33 objektů, 10 CORE, 19 CANDIDATE, 4 LOW. Celkem 112 objektů. Cross-Paper vytvořil 28 topics, 12 INCLUDE a 16 RESERVE, se 71 provenance vazbami. Sedm INCLUDE mělo tři tituly, dvě dva a tři jediný zdroj.

Deep Read prošlo všech dvanáct INCLUDE. Změnily se formulace a interpretace, nikoli výběrový status. Editorial vytvořil čtyři vrcholy a sedm hlavních jednotek; Detail review 6 strong a 1 sufficient. Verification našla šest konkrétních oprav, v dostupném záznamu je podrobně popsaný Treasury watchlist. Finální text měl přibližně 8,2 tisíce znaků a byl uložen jako verze 1, verified.

Day 3 / 16. 9. má v posledním dostupném checkpointu FT a WSJ frozen, každé po 38 objektech. FT: 10 CORE, 22 CANDIDATE, 6 LOW. WSJ: 13 CORE, 21 CANDIDATE, 4 LOW. HB ještě chybí. To je historická orientace, nikoli aktuální ověření uložených artefaktů. Před pokračováním načti skutečný stav.

Rok vydání zde není potvrzen. Žádný z těchto počtů není norma nebo požadovaný výkon příštího dne.

## D. Co ještě nelze nahradit tímto průvodcem

K plné kalibraci patří celé autentické Master Briefy Day 1 v2 a Day 2 v1. V této přípravě nebyly načteny; nejsou proto nahrazeny domyšlenými texty ani falešnými odkazy. Při jejich získání ověř den, rok, verzi a status. Přečti je celé, ne jen závěrečné hlášení.

Pro provozní pokračování potřebuješ reálné mapy, topics, poznámky a zdrojová vydání rozpracovaného dne. Tento návod poskytuje způsob práce, ne neexistující přístup k historickým souborům.


## E. Krátké zadání pro zahájení nového Chatu

> Přebíráš redakční práci Business Briefu metodou Fast Editorial. Přečti celý FAST_EDITORIAL_START_HERE.md, aktuální EDITORIAL_HANDOVER.md a dostupné autentické schválené Briefy. Otevři také skutečné podklady rozpracovaného dne, pokud nějaký je. Stručně řekni, jak chápeš hodnotu produktu, co je dokončeno, co je frozen, jaké důležité opravy nebo otevřené otázky přebíráš a jaký je další krok. Rozliš převzaté hlášení od toho, co jsi sám načetl a ověřil. Chybějící podklad pojmenuj konkrétně. Zachovej metodu a samostatnost nových vydání. Změny procesu pouze navrhuj, nezaváděj je během zpracování dne. V práci pokračuj souvisle, s redakčním úsudkem a s průběžně uloženými důležitými výsledky.

## F. Devět vět, které si drž v hlavě

> **Neprodáváme zprávy. Přinášíme přístup ke kvalitní zahraniční žurnalistice a způsobům přemýšlení, které český čtenář jinak často nepotká.**

> **Není důležité, na co se díváš, ale co vidíš.**

> **Importance of event is not the same as reading value of article.**

> **Šíře v zákulisí, výběr na povrchu.**

> **Main news can be brief. Distinctive journalism deserves depth.**

> **Nekomprimuj text tak, že zachováš fakta, ale ztratíš autora.**

> **Nechceme, aby čtenář odcházel s povinným názorem. Chceme, aby odcházel posunutý.**

> **Nechceme, aby čtenář četl méně. Chceme, aby četl méně zbytečného a více toho, co stojí za jeho čas.**

> **First create a well-informed editor. Then give that editor tools.**

## F2. Poslední rada novému editorovi

Když si nejsi jistý, vrať se ke čtenáři a ke zdroji. Čtenář ti připomene, proč informaci vybíráš. Zdroj ti připomene, co smíš tvrdit. Mezi tím máš prostor pro vlastní dobrý úsudek.

Nemusíš být originální za každou cenu. Nemusíš pokaždé něco změnit. Musíš poznat, kdy jsi něco skutečně pochopil, kdy jen převzal hezky znějící formulaci a kdy potřebuješ otevřít článek znovu. Právě tuto pozornost se snaží tento dokument předat.

---

## G. Celý den: co přesně děláš a kdy můžeš pokračovat

Tento přehled spojuje rozptýlené pokyny z hlavního výkladu. Není to další workflow vedle něj. U každého kroku rozlišuje obsahovou připravenost a uložení výsledku. Bez uloženého výsledku neoznamuj kanonické dokončení. Pokud chybí pouze technický zápis, lze uchovat rozpracovaný obsah, ale další práce musí vědět, že vychází z nezapsaného podkladu.

### G1. Přijmi první vydání a otevři den

**Vstup:** Kompletní zdrojové vydání, jeho identita a produktové zadání. Při převzetí rozpracované práce také aktuální handover a existující záznamy.

**Udělej:** Ověř titul, celé datum, variantu vydání, počet stran a způsob čtení. Najdi existující den a issue nebo je založ podle skutečného schématu. Zaznamenej skutečné intake_order a zahájení discovery.

**Drž v kontextu:** Co má Brief čtenáři dát; zatím čteš jeden samostatný titul. Předchozí den je podpůrná paměť, nikoli seznam povinných témat.

**Ulož:** Identitu dne, vydání, souboru a runu, technické předpoklady čtení a případnou odchylku preflightu.

**Nesmí se stát:** Duplicitní založení dne, odhad roku, záměna jiného vydání, nepravdivý start času nebo zahájení cross-paper syntézy.

**Pokračuj, když:** Víš, co přesně čteš, zdroj je dostupný a pracovní kontext dne je identifikovaný. Nečitelnost konkrétní části musí zůstat otevřeně evidovaná.

### G2. Přečti a zmapuj první vydání

**Vstup:** Dané vydání a jeho registrovaná identita.

**Udělej:** Projdi všechny strany. Vymez články, pokračování a žánry. U relevantních objektů zachyť vlastní pointu, hodnotu, prioritu, lokátor a otázky. Technickou nejasnost identity článku vyřeš hned; otázku potřebnou pro pozdější detail zaznamenej.

**Drž v kontextu:** Charakter celého čísla, již přečtené příspěvky a rozdíl mezi podobnými mechanismy uvnitř tohoto vydání.

**Ulož:** Pracovní Issue Map položky a důležitá omezení. Připrav issue-level conclusion.

**Nesmí se stát:** Výběr jen z titulní strany, dvojí započítání teaseru, spojení sousedních článků, záměna názoru za fakt nebo předčasná topicizace.

**Pokračuj, když:** Je zkontrolované celé vydání a relevantní obsah má dohledatelné záznamy. Chybějící podstatné čtení nelze nahradit dobře znějícím závěrem.

### G3. Uzavři a zmraz mapu

**Vstup:** Dokončené samostatné čtení, mapa a závěr vydání.

**Udělej:** Zkontroluj coverage čtení, lokátory, duplicity, priority a součty. Popiš hlavní proudy, jedinečný přínos a důležité hranice mezi objekty. Ulož snapshot a označ mapu jako frozen podle skutečné konvence.

**Drž v kontextu:** Původní samostatný úsudek o vydání a jeho důvody. Ten má přežít následné porovnání s dalšími tituly.

**Ulož:** Frozen mapu, issue-level conclusion, issue_map_snapshot a process_observation. Rutinní process_observation může být krátká, ale nesmí vymýšlet odchylku, která nenastala.

**Nesmí se stát:** Zmrazení nedokončeného čtení nebo pozdější tiché přepsání původních priorit podle jiného titulu.

**Pokračuj, když:** Uložená mapa a snapshot existují, status odpovídá práci a zbývající omezení jsou výslovná. Pošli stručné hlášení o daném titulu.

### G4. Zpracuj druhé a třetí vydání

**Vstup:** Další kompletní vydání téhož redakčního dne, předchozí frozen mapy a produktové zadání.

**Udělej:** Opakuj G1–G3 pro každý titul v reálném pořadí. Předchozí obsah můžeš mít v paměti, ale nové vydání posuzuj samo za sebe.

**Drž v kontextu:** Rozdíl mezi zapamatováním a ovlivněním priority. Podobnost tématu zatím není důvod pro vypuštění ani povýšení článku.

**Ulož:** Dvě další samostatné mapy, závěry, snapshoty a procesní poznámky.

**Nesmí se stát:** „To už máme“ jako důvod nečíst, stálá role primary pro určitý titul nebo předčasné denní sloučení.

**Pokračuj do Cross-Paper, když:** Všechny tři příslušné mapy jsou dokončené a frozen. Případný uživatelem změněný rozsah dne musí být výslovný.

### G5. Vytvoř Cross-Paper

**Vstup:** Tři skutečné frozen mapy, jejich zdrojové články a podpůrný časový kontext.

**Udělej:** Vytvoř Daily Topics podle události, mechanismu, otázky či napětí. Připoj články s konkrétními rolemi a vysvětlením přínosu. Rozhodni include/reserve/exclude, zaznamenej hranice a připrav Deep Read queue.

**Drž v kontextu:** Celý den, rozdílnost perspektiv, silné single-source příspěvky a rozdíl mezi topicem a budoucí textovou jednotkou.

**Ulož:** Daily Topics, provenance vazby, výběrová rozhodnutí, cross_paper_map a frontu otázek pro hlubší čtení.

**Nesmí se stát:** Sloučení podle samotného slova AI nebo ropa, potlačení rozdílů, automatické hlasování podle počtu titulů nebo přepis samostatných map.

**Pokračuj, když:** Výběr má vysvětlitelnou logiku, nosné topics mají zdrojovou oporu a otázky k ověření jsou konkrétní. Nemusí být ještě všechny zodpovězené; právě proto následuje Deep Read.

### G6. Proveď Selective Deep Read

**Vstup:** INCLUDE topics, zdrojové vazby, původní články, známé otázky a pracovní syntézy.

**Udělej:** Prověř potřebné pasáže a jejich kontext. Kontroluj i dosud nepoložené otázky. Uprav význam či výběr, pokud je třeba. Přenes důležitá omezení do wording guardrails.

**Drž v kontextu:** Původní hypotézu, důvod její změny a celou zdrojovou kombinaci. Nezapomeň při opravě jednoho údaje na společný rámec.

**Ulož:** deep_read_summary pro prověřovaná témata, aktualizovaný topic, stav review a záznam významných interpretačních změn. Souhrnná změnová poznámka má odkazovat na jednotlivé případy.

**Nesmí se stát:** Ověřování vlastního souhrnu proti vlastnímu souhrnu, prosté odškrtnutí známých otázek nebo záměna dokončeného review za potvrzení všech původních tvrzení.

**Pokračuj, když:** Příběhy určené k psaní mají dostatečně pochopenou oporu a podstatné nejistoty jsou vyřešené, omezené nebo vedly k vyřazení problematického claimu. Rozsah kontroly odpovídá zamýšlenému použití.

### G7. Proveď osm redakčních průchodů

**Vstup:** Topics po Deep Read, použitelná RESERVE, zdroje a souvislý kontext dne.

**Udělej:** Postupně rozhodni obsahové zadání, dramaturgii, úhly, napiš draft, posuď Detail value, ověř napsané claims, uprav jazyk a proveď celkový Chief review. Pravomoci jsou soustředěné v příloze K.

**Drž v kontextu:** Co čtenář už v textu ví, kde jsou vrcholy, které kvalifikace musí přežít zkrácení a která verze právě prochází kontrolou.

**Ulož:** Vlastní výsledek každého passu, konkrétní review notes a významné textové snapshoty. Každý review se musí vztahovat k identifikovatelnému podkladu.

**Nesmí se stát:** Osm dodatečně vymyšlených PASS, povinné zásahy bez důvodu, neověřené povýšení RESERVE, stejně dlouhé miničlánky nebo přenos schválení ze staršího draftu na věcně změněný text.

**Pokračuj, když:** Zjištěné problémy jsou napravené a dotčené kontroly znovu posouzené. Finální brány patří poslednímu textu.

### G8. Finalizuj Master Brief a uzavři den

**Vstup:** Poslední text, finální verdict, zdrojové vazby a skutečné výsledky kontrol.

**Udělej:** Ulož kanonický Master Brief do správného dne a verze. Ověř úplnost textu, stav a vazby. Doplň denní retrospektivu a aktuální handover.

**Drž v kontextu:** Rozdíl mezi vytvořením, uložením, verified a publikací. Předej otevřené příběhy, ne předem hotový výběr zítřka.

**Ulož:** historické daily briefs záznam podle původního schématu, Chief review, příslušné snapshoty a závěrečné poznámky. historické brief items vytvářej jen podle skutečně zavedeného publishing postupu, nikoli jako domnělou podmínku redakčního schválení.

**Nesmí se stát:** Hlášení úspěchu před ověřením zápisu, záměna verified za published nebo doplnění chybějících ID odhadem.

**Den je uzavřený, když:** Schválený text skutečně existuje, audit umožňuje pochopit rozhodnutí a handover uvádí pravdivý další krok. Pokud chybí pouze zápis, hlášení musí tuto výjimku přiznat.

## H. Slovník polí: co znamenají a proč je uchovávat

Povinnost níže platí pro doporučený logický předávací formát, nikoli pro konkrétní technickou implementaci. **A** znamená nutné pro dokončený objekt, **P** nutné při uvedené situaci, **V** volitelné. Pracovní objekt může mít dočasnou mezeru, ale musí být patrné, že není dokončený.

Všechny krátké identifikátory a lokátory v příkladech jsou ilustrace. Při provozu použij skutečné hodnoty. Položky uvnitř source_links a evidence_refs musí být skutečně rozřešitelné, nikoli pouze text podobný odkazu.

### H1. Issue Map item

| Pole | Význam a povinnost | Příklad | Pozdější použití |
| --- | --- | --- | --- |
| item_id | A: stabilní identita objektu | D2-HB-017, pouze ilustrace | Vazby topiců a poznámek |
| issue_id | A: konkrétní vydání | D2-HB, ilustrace | Oddělení nezávislých map |
| source.file_ref | A: konkrétní zdrojový soubor | Ověřená reference PDF | Návrat ke správnému originálu |
| source.pdf_pages | A: lokátor v PDF, pokud má stránky | [18, 19], ilustrace | Přímé otevření pasáže |
| source.printed_pages | P: pokud je zjistitelná odlišná tištěná paginace | [16, 17], ilustrace | Zabránění záměně číslování |
| source.continuation_locator | P: pokud je pokračování jinde | Pokračování z titulní strany na A8 | Deduplikace a úplné čtení |
| headline_original | A: původní titulek, případně výslovně nečitelný | Přesný přepis titulku | Identifikace a kontrola |
| working_label_cs | V: české pracovní označení | Toyota/VW — soukromí zákazníci | Orientace bez ztráty originálu |
| author | P: pokud je spolehlivě zjistitelný | Jméno autora | Atribuce a zachování perspektivy |
| genre | A: druh textu | interview | Práce s faktem, názorem a atribucí |
| article_point | A: co článek skutečně tvrdí | Měsíční srovnání prodejního kanálu | Cross-Paper syntéza |
| author_view.question | P: pokud tvoří hodnotu textu | Kdo financuje další fázi AI boomu? | Ochrana autorovy otázky při kompresi |
| author_view.frame | P: způsob rámování | Kapitálové riziko místo čistě technologického závodu | Story a kurace |
| author_view.argument_or_angle | P: hlavní argument / úhel | Dodavatel se stává i financujícím aktérem | Zachování způsobu vidění |
| what_is_new_or_useful | A: co čtenář získá | Jiný obraz poptávky než celkové registrace | Selekce a kurace |
| event_importance | A: význam události | HIGH | Coverage a orientace |
| reading_value | A: hodnota konkrétního textu | HIGH | Perspektivní výběr a kurace |
| priority | A: samostatná priorita vydání | CORE | Pozdější výběr, ne nárok na publikaci |
| priority_reason | P: zejména u hraničních rozhodnutí | Důležitý kanál, omezené období | Obnova úsudku |
| deep_read_candidate | A: předběžný příznak | true | Příprava fronty, nikoli stav hotového čtení |
| deep_read_questions | P: při známých otázkách | Měsíc, nebo kumulativní období? | Cílený návrat ke zdroji |
| uncertainties | P: skutečné nejistoty | Nejasný rozsah garance | Trust a wording guardrails |
| structural_notes | P: při potřebě vyjasnit hranice objektu | Teaser není druhý článek | Obnova a kontrola mapy |

Pole autorovy otázky, framingu a reading value jsou současná vrstva Business Briefu v4. Nevyplňuj je mechanicky. Pokud text takovou vrstvu nemá nebo ji nelze bezpečně určit, nevyráběj ji.

### H2. Issue-level conclusion

| Pole | Význam a povinnost | Příklad | Pozdější použití |
| --- | --- | --- | --- |
| issue_id, day_id | A: identita vydání a dne | Skutečné přidělené klíče | Správné zařazení |
| publication | A: titul | Financial Times | Rozlišení zdroje |
| issue_date | A: celé ověřené datum | Datum převzaté z PDF | Vyloučení záměny roku či dne |
| intake_order | A: skutečné pořadí příjmu | 2 | Nezávislost a audit |
| source_file_ref | A: reference originálu | Ověřený soubor | Návrat ke zdroji |
| page_count | A: rozsah PDF | 18 | Kontrola úplnosti prohlídky |
| reading_mode | A: skutečný způsob čtení | rendered_vision | Interpretace technických omezení |
| ocr_performed | A: zda OCR opravdu proběhlo | false | Pravdivý audit |
| coverage.all_pages_reviewed | A: výsledek kontroly rozsahu | true | Freeze a přiznání neúplnosti |
| coverage.unread_or_unclear_parts | P: pokud něco zbývá | Nečitelný graf na straně X | Doplnění zdroje |
| coverage.reviewed_but_excluded_categories | A, prázdné jen po kontrole | Reklama, market-data | Rozlišení nezahrnutí a nepřečtení |
| editorial_currents | A: hlavní proudy vydání | Sazby; AI; průmysl | Orientace při Cross-Paper |
| unique_contributions | A: významné vlastní příspěvky | Původní interview | Ochrana single-source hodnoty |
| important_distinctions | P: pokud hrozí předčasné sloučení | AI safety není finanční riziko Nvidie | Zachování samostatných objektů |
| counts.total/core/candidate/low | A: skutečné počty | 41 / 11 / 26 / 4 | Kontrola konzistence |
| counts.deep_read_candidates | A v této šabloně | 11 | Přehled kandidatur, nikoli dokončení |
| snapshot_ref | A při freeze: identita uloženého snapshotu | Skutečná reference | Obnova původního úsudku |
| status | A: skutečný stav příslušného objektu | frozen | Podmínka Cross-Paper |
| process_caveats | P: při odchylce | Preflight před registrací runu | Pravdivost timing/auditu |

Pokud původní schéma používá text_layer_usable, ocr_required nebo frozen_at, uchovej tyto ověřené údaje. V této metodické šabloně nejsou všechny samostatným polem; jejich význam nesmí být při přenosu vynechán. ocr_required a ocr_performed nejsou totéž. Čas freeze zapisuj skutečný, ne odhadovaný zpětně.

### H3. Daily Topic a source links

| Pole | Význam a povinnost | Příklad | Pozdější použití |
| --- | --- | --- | --- |
| topic_id, day_id | A: identita tématu a dne | Skutečné klíče | Review, text a provenance |
| working_title | A: přesná pracovní formulace | Toyota před VW v červenci… | Orientace a pozdější titulek |
| central_question | A: co společně vysvětlujeme | Co se změnilo v poptávce? | Hranice topicu |
| synthesis | A: podložená společná pointa | Stručný výklad z článků | Story a Writer |
| why_now | A: dnešní relevance | Nové měsíční údaje | Odlišení opakování |
| decision | A: výběrový status | include | Další práce |
| decision_reason | A: důvod výběru či odložení | Silný samostatný zdroj, nový mechanismus | Audit a návrat k RESERVE |
| source_links[].item_id | A: skutečný zdrojový objekt | Skutečné article ID | Návrat k evidenci |
| source_links[].role | A: role v tomto topicu | primary | Rozlišení příspěvků |
| source_links[].contribution | A: konkrétní přidaná hodnota | Dodává srovnávací období | Smysluplná provenance |
| source_links[].distinctive_perspective | P: pokud zdroj vidí věc odlišně | Zdůrazňuje fyzický limit, ne financování | Ochrana rozdílů mezi médii |
| differences_and_tensions | P: při rozdílech | Odlišné segmenty trhu | Ochrana proti falešné shodě |
| reading_value_notes | P: pokud topic obsahuje text hodný hlubší pozornosti | Silný interview / originální argument | Kurace a Detail |
| open_questions | P: při nejistotách | Závazek, nebo možná garance? | Deep Read |
| deep_read_status | A: skutečný stav kontroly | pending | Připravenost pro Editorial |
| deep_read_note_ref | P: když kontrola proběhla | Skutečná note reference | Dohledání výsledku |
| temporal_context.previous_evidence_refs | P: když používáme včerejšek | Včerejší Brief a source refs | Ověřitelné časové srovnání |
| temporal_context.supported_change | P: při časové interpretaci | Nový mechanismus místo pouhého opakování | Why_now a Story |
| interpretation_changes | P: pokud se význam změnil | Odkaz na před/po a důvod | Ochrana před návratem chyby |

Původní deep_read.focus je fronta konkrétních otázek a zdrojových kontrol; v rozšířené šabloně vychází z open_questions a source links. Pokud mají podklady samostatný focus, zachovej jej. Časové použití a jeho omezení musí být patrné, i když skutečné schéma nemá příznak used.

### H4. Deep Read Note

| Pole | Význam a povinnost | Příklad | Pozdější použití |
| --- | --- | --- | --- |
| note_type, day_id, topic_id | A: druh a rozsah kontroly | deep_read_summary | Správné dohledání |
| source_passages[].item_id/locator | A: skutečně čtené podklady | Article ID + odstavec/strana | Opakovatelné ověření |
| initial_interpretation | A: s čím editor přišel | Příliš obecné prvenství Toyoty | Srovnání před/po |
| known_questions | A; může být prázdné po vědomém posouzení | Rozsah období? | Známá nejistota |
| verified_findings[].finding | A: ověřené zjištění | Jde o červenec | Obsah pro psaní |
| verified_findings[].evidence_ref | A pro každé zjištění | Skutečný lokátor | Provenance claimu |
| verified_findings[].scope_and_qualifications | A, pokud omezuje tvrzení | Evropský private-customer channel | Přesnost formulace |
| newly_discovered_problems | A, může být prázdné | Ruský model není private capital | Nově odhalené chyby |
| apparent_conflicts[].issue | P: při nesouladu | Růst versus propad AI akcií | Rozpoznání problému |
| apparent_conflicts[].resolution_or_remaining_uncertainty | P: spolu s problémem | Různé segmenty | Syntéza bez falešného rozporu |
| interpretation_before/after | P: při změně; jinak výslovně beze změny | Obecný rámec → zúžený rámec | Audit významu |
| change_reason | P: při změně | Zdroj nepodporuje původní rozsah | Obnova úsudku |
| perspective_recovered_or_corrected | P: pokud se při Deep Read obnoví zploštělá autorská perspektiva | Původní syntéza ztratila podmíněnost argumentu | Story, Writer a kurace |
| wording_guardrails.safe_formulation | A pro nosnou pointu | V červenci u soukromých zákazníků | Writer a Verification |
| wording_guardrails.misleading_formulations | P: při rizikové zkratce | Toyota je evropská jednička | Ochrana před regresí |
| selection_before/after | A: dopad kontroly do výběru | include → include | Odlišení interpretace a relevance |
| remaining_uncertainties | A, prázdné jen po kontrole | Přesná budoucí kapacita nejasná | Omezení výsledného textu |
| review_result | A: výsledek prověření | Dokončeno; původní širší claim nepoužít | Přechod dál |

Příznak interpretation_changed může být uložen explicitně, pokud jej schéma má; jinak musí být změna z před/po jednoznačná. Dokončený review s odmítnutým claimem není totéž jako neprovedený review.

### H5. Editorial Note

| Pole | Význam a povinnost | Příklad | Pozdější použití |
| --- | --- | --- | --- |
| note_id | A po uložení: identita poznámky | Skutečný klíč | Odkazy a předání |
| note_type | A: skutečná kategorie | verification_review_v1 | Orientace v auditní stopě |
| scope.day_id | A | Skutečný den | Oddělení vydání |
| scope.issue_ids/topic_ids | P podle rozsahu | Dotčené topics | Přesné přiřazení |
| scope.brief_id/brief_version | P: při kontrole textu | Konkrétní Brief a verze | Zabránění přenosu PASS na jiný draft |
| scope.run_ref | P: pokud run existuje | Skutečný klíč | Vazba obsahu na provedení |
| review_question | A u review | Předal Brief pointu a zachoval Detail? | Význam kontroly |
| findings | A u review; může obsahovat potvrzení bez problému | Watchlist implikuje nesprávný stav | Konkrétní výsledek |
| decisions[].decision/reason | A u rozhodnutí | Opravit sloveso; close byl pod hranicí | Pochopitelný úsudek |
| decisions[].evidence_refs | P, pokud rozhodnutí závisí na zdroji | Pasáž z Deep Read | Audit opory |
| changes[].before/after/impact | P při změně | Zůstane → vrátí se | Přesná oprava a její důsledek |
| unresolved | A u review; prázdné jen po kontrole | Čeká zdroj k nosnému claimu | Neztracené otevřené otázky |
| result | A | pass / needs_revision / informational | Další postup |
| artifact_refs | A, pokud existuje kontrolovaný či vytvořený artefakt | Textový snapshot | Obnova konkrétní práce |
| created_at | A po uložení: skutečný čas | Čas přidělený systémem | Chronologie |

Původní next_action může být samostatným polem; pokud není, musí vyplývat z decisions a unresolved. Neztratit další konkrétní krok je důležitější než název sloupce.

### H6. Master Brief metadata

| Pole | Význam a povinnost | Příklad | Pozdější použití |
| --- | --- | --- | --- |
| brief_id, day_id | A | Skutečné klíče | Identita produktu |
| edition_date | A | Ověřené datum vydání | Čtenářské i provozní zařazení |
| version | A | 1 nebo 2 podle skutečnosti | Správa změn |
| status | A | draft / verified podle skutečné konvence | Připravenost a omezení použití |
| canonical_text_ref | A nebo vlastní text podle zvolené konvence verzování | Konkrétní úplný text | Čtení, review a případný publishing |
| source_issue_ids | A | Tři skutečná vydání | Coverage zdrojů |
| source_topic_ids | A | Použité topics | Provenance |
| editorial_units[].unit_key | P při evidenci jednotek | Identita v konkrétní verzi | Přiřazení sekce či položky |
| editorial_units[].function | P spolu s jednotkou | coverage | Redakční funkce |
| editorial_units[].topic_ids/evidence_refs | P spolu s jednotkou | Reálné vazby | Kontrola konkrétního textu |
| review_note_refs | A pro verified | Odkazy na osm průchodů a závěr | Doložení redakčního schválení |
| final_gates.coverage/hierarchy/curiosity/trust/product_fit/ninety_second_test | A pro verified | Skutečný výsledek každé historicky doložené brány | Celková kvalita |
| final_gates.perspective/difference/reader_autonomy/time_respect/life | A pro nový Business Brief | Skutečný stručný výsledek každého produktového testu | Ochrana v4 ducha produktu |
| known_limitations | A; může být prázdné po kontrole | Omezení rozsahu, ne skryté blokující chyby | Poctivé předání |
| verified_at | P: až po schválení a uložení | Skutečný čas | Historie verze |

Původní souhrn editorial_review s osmi výsledky lze zachovat. V rozšířené šabloně jej reprezentují konkrétní review_note_refs, ne domnělé automatické PASS. Pokud odkazované poznámky osm průchodů nedokládají, metadata nejsou pro schválení úplná.

### H7. Prázdné hodnoty nejsou všechny stejné

**Neznámé:** Hodnotu nemáme, například rok vydání. Použij skutečný podporovaný prázdný stav a vysvětli mezeru. Nevymýšlej hodnotu, aby prošel formulář.

**Dosud nezpracované:** Například Deep Read čeká. To je pracovní stav, nikoli závěr, že nebyl nalezen problém.

**Nevztahuje se:** Článek nemá pokračování nebo poznámka nekontroluje žádný Brief. Prázdná reference je v pořádku, pokud její význam není zaměnitelný s chybějícím podkladem.

**Zkontrolováno, nic nenalezeno:** Prázdný seznam unresolved po skutečné kontrole. Nesmí vzniknout automatickým ponecháním výchozí hodnoty.

V logických šablonách můžeš tyto rozdíly vysvětlit textem. Nevytvářej nové povinné kategorie jen proto, že se nevejde konkrétní případ. Pole, které nelze pravdivě vyplnit, je důvodem vyřešit mezeru nebo jej ponechat prázdné, nikoli ji zakrýt.

## I. Doporučené artefakty a jejich životní cyklus

Názvy souborů v tabulce jsou přenositelná konvence, nikoli historické názvy. Nevytvářej dvě nezávisle upravované pravdy. Jeden artefakt musí být jasně označený jako aktuální kanonický stav a ostatní jako snapshoty, exporty nebo historické verze.

| Artefakt / logický protějšek | Účel a obsah | Kdo a kdy vytváří | Kdy je hotový | Životní cyklus |
| --- | --- | --- | --- | --- |
| day-context.yaml / den a zdroje | Datum, identita, pořadí a reference vydání, omezení | Jeden Chat při intake | Průběžně aktuální | Mutable; důležité odchylky auditovat |
| issue-map-{title}.yaml / mapa | Objekty, zdroje, priority a závěr | Tentýž Chat během čtení každého titulu | Po kontrole celého vydání | Pracovní → frozen; oprava jako dohledatelná revize |
| daily-topics.yaml / denní topic artefakt | Denní syntéza, source roles, rozhodnutí, otázky | Tentýž Chat při Cross-Paper | Výběr připravený, později zpřesněný Deep Read | Mutable pracovní interpretace; významné změny zaznamenat |
| editorial-notes.yaml / editorial notes | Důvody, review, Deep Read, změny, retrospektiva | Tentýž Chat při dokončení kroků | Každý záznam po skutečné práci | Přibývající záznamy; opravy bez tichého mazání historie |
| Textové snapshoty | Přesné meziverze Briefu | Writer a další relevantní průchody | V okamžiku zachycení | Snapshot nepřepisovat novým obsahem pod stejnou identitou |
| master-brief.md / kanonický Master Brief | Celý text, metadata, provenance a status | Tentýž Chat v Editorial | Po finálních branách a ověření zápisu | Draft → verified; další věcná změna jako identifikovatelná verze/revize |
| EDITORIAL_HANDOVER.md | Stav, příští krok, otevřené příběhy, reference | Tentýž Chat při checkpointu a uzavření dne | K uvedenému času aktualizace | Mutable předání; historické verze zachovat |
| FAST_EDITORIAL_START_HERE.md | Stabilní porozumění a metoda | Při vědomé rekonstrukci či přijaté změně | K vydané verzi dokumentu | Verzované; neměnit automaticky každým dnem |

**Mutable neznamená bez historie.** Pracovní topic se může vyvíjet, ale důležitá změna významu potřebuje poznámku. **Frozen neznamená neomylné.** Znamená uchovaný nezávislý výsledek. **Final neznamená navždy bez opravy.** Znamená schválenou konkrétní verzi; další oprava musí být identifikovatelná a zkontrolovaná.

## J. Co přesně převzít ze živého kontextu

Pět vrstev paměti pomáhá vysvětlit, proč byl jeden souvislý Chat účinný. Tento popis je silná rekonstrukce, nikoli pět historicky zavedených datových objektů.

| Vrstva | Co žilo v kontextu | Co má přežít v artefaktech | Co se ztratí při předání pouhého souhrnu |
| --- | --- | --- | --- |
| Paměť článků | Argument, tón, příklady, omezení a místo v čísle | Lokátor, pointa, žánr, důležité kvalifikace a dostupný originál | Nuance a možnost poznat, že souhrn něco přehnal |
| Paměť úsudků | Proč se něco zdálo významné či hraniční | Důvody důležitých priorit a rozhodnutí | Rozdíl mezi uváženým výběrem a náhodou |
| Paměť rozdílů | Které podobnosti jsou povrchní | Proč se konkrétní věci spojily nebo zůstaly oddělené | Opětovné sloučení podle štítku |
| Paměť oprav | Jak vznikla chybná interpretace a co ji vyvrátilo | Před/po, zdroj, dopad a wording guardrails | Návrat stejné chyby při zkrácení |
| Paměť kompozice | Co už čtenář ví, kde má zpomalit, kde text opakuje | Dramaturgický plán a přesná poslední verze textu | Plochý rytmus a opakované vysvětlování |

Není nutné zapisovat každou alternativní formulaci. Zaznamenej zamítnutý úhel tehdy, když hrozí, že se bude znovu jevit jako atraktivní, ale už víme, proč je chybný. Například „private capital“ pro celý defence-tech příběh je takový případ.

Při převzetí uprostřed psaní nestačí dát novému Chatu topics. Potřebuje i aktuální draft, schválené úhly, významné opravy a informaci, které kontroly už proběhly. Při převzetí mezi dny potřebuje poslední finální Brief, otevřené příběhy a jejich podklady; nemusí znovu načítat všechny pracovní formulace minulého dne.

### Konkrétní paměťová karta příběhu — doporučení pro handover

```yaml
story_label: "Treasury / cena kapitálu"
last_supported_state:
  edition_date: "ověřit v originálu"
  statement: "Intradenní maximum nad 5 %, close pod hranicí"
  evidence_refs: []  # V reálné kartě skutečné reference.
already_explained_to_reader: "Cena kapitálu a přenos do ekonomiky"
open_question: "Přidávají nové články jiný mechanismus poptávky po dluhu?"
do_not_repeat_as_fact: "Výnos zůstal nad 5 %"
next_day_priority: "neurčeno; nové mapy číst nezávisle"
```

Tato karta není nový temporal pass ani povinný technický objekt. Je to kompaktní způsob, jak neztratit význam při předání.

## K. Pravomoci osmi editorů na jednom místě

Názvy a pořadí průchodů jsou doložené. Toto jednotné rozdělení pravomocí je rekonstrukční pomůcka.

| Průchod | Co kontroluje | Co může změnit | Výstup | Co nesmí |
| --- | --- | --- | --- | --- |
| Assignment | Potřebný obsah dne a role témat | Výběr, využití RESERVE, rozsah coverage | editorial_selection_v1 | Povýšit neověřený podklad bez kontroly; každé INCLUDE automaticky jako lead |
| Dramaturg | Hierarchii, pořadí, rytmus, váhy | Pořadí, délkové váhy, spojení topics do jednotek | dramaturgy_plan_v1 | Zrušit věcný rozdíl kvůli hezkému příběhu |
| Story | Pointu, why_now, mechanismus | Úhel a hranici příběhu | story_angles_v1 | Vytvořit nepodložené napětí nebo kauzalitu |
| Writer | Čtenářský převod zadání | Formulace, přechody a lokální délky | Celý draft + master_brief_draft_v1 | Přidat neověřený fakt, vyrovnat všechny délky, spotřebovat Detail |
| Detail | Plnou hodnotu Briefu a další hloubku | Rozdělení vysvětlení a rozsah jednotky | detail_gap_review_v1 | Udělat prázdný teaser nebo tvrdit, že hotové Detaily existují |
| Verification | Skutečně napsané claims a implikace | Čísla, omezení, atribuci, věty i titulky | verification_review_v1 + potřebný snapshot | Spokojit se s dřívějším Deep Read |
| Language & Style | Češtinu, rytmus, čitelnost | Jazyk a opakování | language_style_review_v1 + potřebný snapshot | Vymazat kvalifikaci a posílit jistotu |
| Editor-in-Chief | Celek a finální brány | Schválení nebo návrat ke konkrétní opravě | editor_in_chief_review_v1, verdict | Měnit pro vlastní otisk nebo schválit neřešenou nosnou chybu |

Každý průchod může skončit beze změny. Důležitý je skutečný výsledek kontroly a jeho vazba na podklad. Pokud Chief vrátí hierarchii, začni dramaturgií; pokud je problém v samotném zdrojovém významu, vrať se k Deep Read. Po opravě znovu proveď dotčené následné kontroly, ne automaticky všechno od začátku.

## L. Stavba Master Briefu a přiměřený rozsah

Následující rozsahy jsou orientační rekonstrukce, nikoli historicky ověřené limity. Slouží k rozlišení funkcí. Autentický finální text má přednost jako kalibrace a konkrétní den může vyžadovat jiný poměr.

| Možná část | Úloha | Orientační rozsah | Vztah k ostatním |
| --- | --- | --- | --- |
| Dobré ráno | Lidský vstup a první orientace | Krátký odstavec | Nemá zdržovat před denní mapou ani ji zbytečně opakovat |
| Dnes v kostce | Rychle ukázat hlavní změny | Několik vět nebo stručných bodů | Umožní orientaci bez pročtení všech příběhů |
| Hlavní příběhy | Vysvětlit několik důležitých mechanismů | Proměnlivý počet odstavců podle významu | Nesou skutečné vrcholy a umožní přechod do hloubky |
| Ještě potřebujete vědět | Uchovat důležité vedlejší události | Jedna až několik vět na položku | Chrání coverage bez soupeření všech témat o lead |
| Čísla dne | Ukázat význam číselného údaje | Číslo s krátkým kontextem | Nemají být dekorací ani opakováním celého odstavce |
| Co sledujeme | Pojmenovat otevřený další vývoj | Několik konkrétních bodů | Navazuje na dnešní stav, nepředpokládá neověřenou budoucnost |
| Co dnes ještě stojí za přečtení | Kurátorsky doporučit silný text | Krátké zdůvodnění na doporučení | Může nabídnout hodnotu mimo denní leady |

Samostatná existence všech těchto názvů a jejich přesné pořadí nejsou doložené. Funkce mapy dne, hlavního čtení, coverage, kurace a watchlistu doložené jsou. Vydání nemá být sedm stejně dlouhých bloků. Day 2 se sedmi hlavními jednotkami a čtyřmi vrcholy je příklad právě této nerovnoměrné váhy.

### Neztratit podrobnost historických kalibračních případů

Toyota/VW: zúžení na červenec a evropské soukromé zákazníky; leden–červenec VW nadále vedl o 376 aut. Nejde jen o obecné poučení „hlídej období“, ale o konkrétní opravu pointy.

Defence-tech: ruská státní mobilizace, levné komerční čínské komponenty a rychlá iterace versus západní venture kapitál a startupy. Společný rámec byl rozšířen na levnější zbraně, komerční technologie a soukromý kapitál.

AI akcie: vybrané hyperscalery rostly o 2 % a více, zatímco PHLX Semiconductor Index spadl o 5,9 %. Rozdíl segmentů vysvětloval zdánlivý rozpor. Správná společná pointa nebyla jednotný směr všech AI akcií.

Treasury: intraday 5,012 %, close 4,96 %. Očekávání hike přibližně 90 % v jednom snapshotu a 77 % v jiném. Neprůměrovat a nevyrábět společnou přesnost. Samostatná pozdější oprava watchlistu se týkala předpokladu „zůstane nad 5 %“.

Nvidia: v hlášení se rozlišovaly přibližně 99 mld. USD hotovosti a likvidních cenných papírů, možné garance až 105 mld. USD pro Ohio projekt a až 125 mld. USD v širším rámci. „Too big to fail“ zůstávalo názorem Mohameda El-Eriana, nikoli regulatorním statusem.

Belgie: pět ze sedmi reaktorů bylo podle hlášení odstaveno, restartovatelnost se lišila a rozdělení nákladů a rizik se státem a Engie se vyjednávalo. Nelze z toho udělat jednoduchý hotový restart všech reaktorů.

Všechna tato čísla jsou převzatá z dostupného konverzačního záznamu experimentu. Při novém publikovaném tvrzení vyžadují originální zdrojové ověření. V tomto dokumentu slouží výhradně jako kalibrace rozhodování.

## M. Kontrola pokrytí hlavních oblastí

| Oblast předání | Hlavní výklad | Praktická opora | Stav |
| --- | --- | --- | --- |
| 1. Co pochopit před začátkem | Úvod, kapitoly 1 a 5 | Produktový smysl, perspective value, výběrová kritéria a kalibrační případy | Metodicky pokryto |
| 2. End-to-end den | Kapitoly 3–19 a 22–24 | G1–G8: vstupy, kontext, výstupy, zákazy, přechody | Pokryto explicitně |
| 3. Kontinuita jednoho Chatu | Kapitoly 2 a 24 | J: pět vrstev paměti a ztráty při předání | Pokryto explicitně |
| 4. Issue Map | Kapitoly 3–7 | A, H1–H2, G2–G4 | Funkce, freeze i pole pokryté |
| 5. Cross-Paper | Kapitola 8 | A, H3, G5 | Spojování, rozlišení a provenance pokryté |
| 6. Selective Deep Read | Kapitola 9 | A, H4, G6, L | Spouštěče, oba režimy, změny a příklady pokryté |
| 7. Osm průchodů | Kapitoly 10–18 | K a G7 | Pravomoci, výsledky, zákazy a návraty pokryté |
| 8. Finální brány | Kapitoly 18–19 | Metadata A/H6 a G8 | Význam i meze doložení pokryté |
| 9. Master Brief | Kapitola 20 | L | Funkce, rytmus, rozsah a nejistota názvů pokryté |
| 10. Editorial Notes | Kapitola 21 | A, H5, B, I | Kdy, proč, jak, příklady a audit pokryté |
| 11. Kontinuita dnů | Kapitola 23 | J a handover pravidla | Podpůrná Memory bez nového passu pokrytá |
| 12. Co neformalizovat | Kapitola 25 | Průběžné výhrady ke kvótám a schématům | Pokryto |
| 13. Artefakty | Průběžně + příloha I | I a B | Účel, autor, dokončení a životní cyklus pokryté |
| 14. Datové struktury | Praktická příloha A | H1–H7 | Šest šablon, slovník a prázdné hodnoty pokryté |
| 15. Samostatný onboarding | Celý soubor | E, G a M | Samostatné metodické zadání; provozní reference vyžadují originály |
| 16. Sebehodnocení | Úvod a přílohy C–D | O | Doložené, rekonstruované a neznámé oddělené |

„Pokryto“ zde hodnotí přítomnost a dostatečné vysvětlení oblasti v dokumentu, nikoli nové nezávislé ověření historických zdrojů. Nejde o další redakční gate pro každý den.

## N. Závěrečné sebehodnocení rekonstrukce

### A. Doložené z dostupného konverzačního záznamu

- Postupné čtení kompletních vydání FT, WSJ a Handelsblattu; pořadí se měnilo.
- Samostatné Issue Maps, priority CORE/CANDIDATE/LOW, kandidatury Deep Read a Memory.
- Freeze před Cross-Paper a zákaz zpětného ovlivnění mapy dalším titulem.
- Rozlišení článků, pokračování, teaserů, žánrů, reklamy a nezahrnutých částí.
- Vizuální čtení obrazového FT bez full-issue OCR; textové čtení s kontrolou layoutu tam, kde byla textová vrstva.
- Cross-Paper na úrovni Daily Topics, rozhodnutí include/reserve/exclude jako používaný rámec, zdrojové role primary/supporting/contrasting/background.
- Day 2: 112 objektů, 28 topics, 12 INCLUDE a 16 RESERVE, 71 provenance vazeb a tři silné single-source INCLUDE.
- Selective Deep Read před Editorial; v Day 2 všech dvanáct INCLUDE, interpretační opravy bez změny jejich výběrového statusu.
- Konkrétní korekce Toyoty, defence-tech, segmentů AI trhu, Treasury, Nvidie a Belgie v rozsahu popsaném hlášeními.
- Osm jmenovaných průchodů, vlastní Editorial Notes a významné textové snapshoty.
- Dramaturgické spojování více topics do výsledné jednotky bez požadavku jedna ku jedné.
- Hierarchie, proměnlivá délka položek, coverage, kurace, watchlist a vztah Briefu k Detailu.
- Day 2: sedm hlavních jednotek, čtyři vrcholy, Detail value 6 strong/1 sufficient, šest hlášených Verification oprav a read-aloud 7/7.
- Finální brány Coverage, Hierarchy, Curiosity, Trust, Product fit a samostatný 90-second test.
- Schválení bez zásahu Editor-in-Chief; Day 1 v2 a Day 2 v1 hlášené jako verified.
- historické Editorial Notes a zmínky o historické daily topics, historické daily briefs a historické brief items; absence materializovaných historické brief items u Day 1 v2 v daném checkpointu.
- Přiznané procesní odchylky preflightu a opravená persistence PASS 4 po transakci bez COMMIT.
- Reflexe slabší časové osy, poznámka memory_would_help a rozhodnutí nezavádět tehdy nový povinný temporal pass.
- Poslední dostupný Day 3 checkpoint: FT a WSJ frozen, HB nezpracované, Cross-Paper dosud nezačal.

Tato jistota je o obsahu konverzačního záznamu. Při sestavení dokumentu nebyl současný stav uložených artefaktů ani původní novinové tvrzení znovu nezávisle ověřen.

### B. Současná produktová doktrína a silná rekonstrukce

Do této verze jsou vědomě vloženy také principy Business Brief v4: přenos způsobu vidění, oddělení event importance a reading value, coverage safety net, reader autonomy, reading curation jako first-class funkce, komplementarita Brief/Detail a test „mrtvolky článku“. Tyto principy jsou **současná definice produktu**, nikoli tvrzení, že byly všechny explicitně pojmenované ve v3.


- Vyjádření čtenářské potřeby a způsobu rozpoznávání redakční hodnoty.
- Praktická hranice mezi CORE, CANDIDATE a LOW; není doložen původní formální scoring.
- Rozlišení úplnosti čtení, dostatečnosti mapy a selektivity výsledku.
- Pět vrstev paměti jednoho Chatu a konkrétní způsob jejich zachování.
- Kritéria spojování podle mechanismu, otázky a napětí, praktické definice zdrojových rolí.
- Dva režimy Deep Read: známá nejistota a hledání dosud nepoznané chyby.
- Přesné praktické vymezení pravomocí jednotlivých editorů, návraty a opakování dotčených kontrol.
- Význam kategorií Detail value a praktický výklad šesti finálních bran.
- Šest přenositelných datových struktur, jejich pole, povinnost a příklady.
- Opravování frozen mapy přes dohledatelnou revizi; životní cyklus artefaktů.
- Ověření RESERVE podle rozsahu pozdějšího použití a další návraty ke zdrojům při změně claimu.
- Vyplněné didaktické vzory Editorial Notes, jednotný přehled G a tabulka pravomocí K.
- Postup technické obnovy, kontroly zápisů a mapování logických polí na skutečné schéma.
- Balíček stálého průvodce, kalibračních ukázek a aktuálního handoveru; dosud zde nebyl prokázán úspěšný end-to-end test předání do nového Chatu.

Tyto části jsou předávanou metodou, ne doslovným archivním přepisem. Neměly by se v dalších dokumentech začít citovat jako historicky zavedené technické nebo procesní pravidlo bez tohoto rozlišení.

### C. Nejisté, nedostupné nebo nedoložené

- Úplné originální znění Playbooku a instrukcí každého passu.
- Celé autentické finální Briefy, mapy a zdrojové PDF v rámci tohoto předávacího dokumentu.
- Přesná cílová persona a pevná norma délky či času čtení celého vydání.
- Přesné historické názvy a pořadí všech sekcí Master Briefu.
- Přesný technický protokol 90-second a read-aloud testů.
- Přesná původní definice Memory candidate a návazný ingestní/RAG postup.
- Skutečnost, že všechny Detaily byly napsané, že Briefy byly publikované nebo že existoval hotový automatizovaný publishing.
- Zavedený temporal pass, systém trendů nebo oddělení osmi rolí do samostatných agentů.
- Úplný seznam šesti konkrétních Verification oprav Day 2; dostupný záznam detailně zachycuje jen některé, zejména Treasury.
- Rok redakčních vydání tam, kde je v dostupných zprávách pouze den a měsíc.

Tyto mezery nejsou důvodem znehodnotit zachycenou zkušenost. Jsou hranicí, kterou má nový Chat vidět. Metodu může převzít z tohoto souboru; konkrétní historická tvrzení a provozní zápisy musí opřít o skutečné dostupné podklady.