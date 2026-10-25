# Fast Editorial — průvodce pro nového editora

**FAST_EDITORIAL_START_HERE.md · úplné metodické předání 3.0 · 25. 10. 2026**

Toto vydání pokrývá všech šestnáct oblastí rekonstrukčního zadání. Obsahuje lidsky psaný průvodce, praktické šablony, úplný provozní přehled, slovník polí a závěrečné rozlišení jistoty. Úplnost metodického předání neznamená, že byly získány chybějící historické originály nebo ověřeno skutečné SQL schéma. Přesný seznam těchto omezení a postup jejich doplnění je v přílohách D, M a O.

## Než otevřeš první noviny

Přebíráš práci, která už v experimentu vedla k dobrým Business Briefům. Nejdůležitější není naučit se názvy kroků. Potřebuješ pochopit, proč jsme noviny četli právě tak, proč jsme některé příběhy spojovali a jiné drželi od sebe, proč jsme se vraceli ke zdrojům a proč jsme hotový text ještě několikrát promýšleli.

Představ si čtenáře, který ráno otevře Brief. Nechce se prohrabat naší výrobou. Nechce sledovat, kolik jsme zpracovali článků a kolik kontrol jsme odškrtli. Chce po několika větách vědět, co se ve světě podstatného děje. U nejdůležitějších věcí chce rozumět tomu, co změnu způsobuje a co může znamenat. A někdy chce narazit na text, který by sám nenašel a který mu otevře novou otázku.

Tvoje práce je tento zážitek vytvořit. Za ním musí stát poctivé čtení a dohledatelná evidence, ale čtenář má dostat přirozené, přesné a živé vydání.

Tento průvodce proto začíná u úsudku. Technické struktury najdeš dále. Čti jej jako vysvětlení od kolegy, který ti předává svůj stůl: co na něm leží, proč to tam je, kde se už jednou spletl a na co si máš dát pozor.

### Co tento dokument skutečně ví

Podkladem je dostupná historie experimentu Fast Editorial v3, následná rekonstrukce a diskuse o předání. Nejsou použity pozdější procesní verze. Nemáme zde úplné původní PDF, SQL schéma, celé mapy ani celé finální Briefy. Máme konkrétní zprávy o průběhu a rozhodnutích, včetně oprav a výsledků.

Aby tě text nezahltil výhradou v každém odstavci, platí toto rozlišení pro celý dokument:

- **Doložená zkušenost** jsou popsané události experimentu, názvy použitých průchodů a poznámek, zaznamenané výsledky a příklady oprav.
- **Předávaná redakční praxe** je srozumitelná rekonstrukce toho, jak tento způsob práce zopakovat. Výklad rozhodovacích situací a vyplněné vzory nejsou doslovným historickým Playbookem.
- **Technická implementace** musí odpovídat skutečně načtenému původnímu schématu. Logické struktury v tomto dokumentu nejsou SQL migrací ani důkazem existence stejně pojmenovaných sloupců.

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
9. Jak spolu souvisejí data a kam patří výsledky v Supabase.
10. Jak řešit obtížné situace a obnovit práci.
11. Praktické šablony, historie experimentu a předání.

Praktické přílohy: **A** šest struktur; **B** ukládání na checkpointech; **C** doložené výsledky; **D** potřebné originální podklady; **E** startovací zadání; **F** rada editorovi; **G** celý den krok za krokem; **H** úplný slovník polí; **I** životní cyklus artefaktů; **J** přenos živého kontextu; **K** pravomoci osmi editorů; **L** stavba a rozsah Briefu; **M** konkrétní provozní napojení a jeho meze; **N** kontrola všech šestnácti oblastí; **O** závěrečné sebehodnocení A/B/C.

Aktuální stav rozpracované práce patří do EDITORIAL_HANDOVER.md. Tento dokument vysvětluje metodu a mění se při vědomé změně metody, nikoli po každém novém vydání.

---

## 1. Jaký Brief se snažíme vytvořit

### Čtenář má získat orientaci a porozumění

Umět vyjmenovat události není totéž jako rozumět dni. Představ si pět zpráv o výnosech dluhopisů, sazbách, zadlužení firem, rozpočtech a hypotékách. Můžeš z nich udělat pět korektních výtahů. Čtenář se dozví pět věcí, ale nemusí uvidět, že růst ceny kapitálu prochází různými částmi ekonomiky.

Na druhou stranu je nemůžeš bez rozmyslu slepit do obecného tvrzení „všechno zdražuje“. Tím bys zahodil rozdílné mechanismy, časové horizonty a důkazy. Dobrý Brief hledá míru: společnou souvislost vysvětlí a důležité rozdíly zachová.

Právě mezi těmito dvěma chybami pracuje redakční úsudek. Příliš roztříštěné vydání nechá syntézu na čtenáři. Příliš uhlazené vydání mu nabídne přesvědčivý, ale zjednodušený příběh.

### Důležitost není jen velikost titulku

Velký titulek je informace o tom, co zdůrazňuje daná redakce. Ber ho vážně. Ale i krátký text uvnitř čísla může popisovat podstatnou změnu. A dlouhá analýza nemusí být dnešním hlavním příběhem, přestože může být výborná pro kuraci.

Hledej, co se změnilo, komu na tom záleží, jak to funguje a zda článek přináší něco, co stojí za čtenářův čas. „Je to o velké firmě“ není úplná odpověď. „Je to originální“ také nestačí, pokud originalita nemá pro produkt význam.

Přesná cílová persona není v dostupných záznamech určena. Nevymýšlej jí příjem, profesi nebo investiční profil. Drž se doloženého slibu: orientace v byznysu, ekonomice, technologiích a relevantním politickém dění.

### Brief má být velkorysý k času čtenáře

Nenuť čtenáře odhadovat, proč mu nějakou informaci dáváš. Nestačí napsat, že se něco stalo a „má to zásadní důsledky“. Vysvětli jeden konkrétní důsledek nebo přesný mechanismus, pokud jej zdroje podporují.

Přitom nevysvětluj každému tématu celý svět od začátku. Krátká věta může stačit tam, kde jde o coverage. Hlavní příběh si zaslouží více prostoru, protože bez něj by čtenář nepochopil změnu.

Přirozený jazyk není povrchnost. Přesnost nemusí znít akademicky. Když se ti pointa nedaří říct srozumitelně, vrať se k otázce, zda jí skutečně rozumíš.

### Curiosity má vycházet z obsahu

Čtenářskou zvědavost nevyvoláváme zadržováním odpovědi. Pokud text ví, proč je problém důležitý, řekne to. Další čtení má nabídnout hloubku, nikoli teprve základní vysvětlení slibu z titulku.

Například finanční role Nvidie může otevřít otázku, jak se v AI ekonomice propojuje zákazník, dodavatel a financování. Nemusíme předstírat tajemství. Stačí přesně ukázat zajímavý mechanismus a jeho omezení.

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

### Co může dát článku vysokou hodnotu

**Nová skutečnost s významným dopadem.** Událost mění situaci pro trh, odvětví, stát nebo důležitou skupinu lidí. Potřebuješ vědět, co je skutečně nové a co je již známé pozadí.

**Mechanismus, který dosud nebyl vidět.** Text vysvětluje, proč se něco děje. Day 3 WSJ o skladbě kupujících Treasuries byl zajímavý právě tím, že mohl přidat mechanismus za známý pohyb výnosů.

**Přenos z jedné oblasti do druhé.** Cena ropy se může proměnit v náklad domácností, pricing firem nebo inflační tlak. Přenos ale musí být podložený; nesmíš jej odvodit pouze z toho, že dvě věci nastaly zároveň.

**Konkrétní případ širší změny.** Malý případ může být výmluvný, pokud zdroj vysvětluje jeho reprezentativnost. Jedna zajímavá firma sama nedokládá trend celého odvětví.

**Silná strategická otázka.** Interview, analýza nebo dlouhý text mohou ukázat rozhodování s dlouhodobými důsledky. Nemusejí být leadem; mohou být výbornou kurací.

**Důležitá protiváha.** Text může komplikovat příběh, který ostatní zdroje líčí příliš hladce. Jeho hodnota může spočívat právě v omezení naší vlastní teze.

### CORE, CANDIDATE a LOW

CORE používej pro objekty, bez kterých by samostatný obraz vydání ztratil významnou část své businessové hodnoty. Může to být velká událost, silný mechanismus nebo mimořádný původní příspěvek. CORE není synonymum titulní strany.

CANDIDATE je relevantní článek, jehož konečné využití záleží na denním obrazu, přínosu vůči jiným zdrojům a prostoru. Není to slabší známka kvality psaní novin. Může se později stát důležitou částí hlavního topicu.

LOW je relevantní objekt s nižší předběžnou prioritou pro tento produkt a toto vydání. Nemá být zásobníkem všeho, co zůstalo na stránce. Reklama či irelevantní obsah nemusí být v mapě vůbec.

U hraničního případu napiš krátce důvod: „relevantní, ale zatím především firemní událost bez doloženého širšího dopadu“ je užitečnější než neurčité „středně důležité“.

### Co dělat, když si nejsi jistý

Jestli nevíš, co článek říká, ještě jsi jej dostatečně nepochopil: dočti potřebnou pasáž. Jestli víš, co říká, ale nevíš, jak důležitý bude v dnešním celku, může zůstat CANDIDATE. Jestli je nejasná konkrétní metrika či rozsah, zapiš otázku pro Deep Read; rozhodnutí o prioritě nepředstírej jako ověření všech detailů.

Nedávej CORE jen proto, že by ti bylo líto článek ztratit. Od toho máš mapu, CANDIDATE a později RESERVE. Záznam zachovává možnost návratu bez povinnosti publikovat.

### Paměťový potenciál je jiná otázka

Memory candidate se v experimentu evidoval, jeho přesná historická definice však není dostupná. Při rekonstrukci jej chápej jako označení možné dlouhodobější užitečnosti. Není totožný s dnešní prioritou. Silný strukturální text může být paměťově hodnotný a přitom dnes nepatřit mezi leady.

Nepřidávej automaticky takto označený článek do jiné databáze či RAG, pokud pro to nemáš skutečný zavedený postup. Příznak není důkaz dokončené ingestce.

## 6. Issue Map: co musí uchovat a co nemá předstírat

Mapa má umožnit pozdější srovnání a návrat ke zdroji. Nemá být prvním návrhem celého Briefu. Dobrá položka zachytí identitu článku, jeho vlastní pointu, redakční hodnotu a důležité otázky.

Když napíšeš jen „AI / významné / CORE“, další editor z toho nic nezíská. Když napíšeš dlouhý obecný esej o AI, ztratíš konkrétní článek. Hledej přiměřenou prostřední úroveň: několik přesných vět a spolehlivý lokátor.

Lokátor musí člověka nebo další Chat dovést na stejné místo. Pokud se liší fyzická strana PDF a tištěné číslo stránky, uchovej obě, když je znáš. Záznam „strana 8“ bez určení souboru není dostatečný. Původní titulek nepočešťuj tak, že jej potom nepůjde identifikovat; pracovní český název může být vedle něj.

Závěr vydání má říct, jaké bylo jeho redakční těžiště, čím přispělo, co zůstává nejisté a které objekty musí zůstat odlišitelné. Počty jsou kontrola konzistence, ne hlavní obsah závěru.

Freeze znamená: samostatné čtení tohoto vydání je uzavřeno a jeho původní úsudek uchován. Další noviny nesmějí přepsat to, co jsme viděli nezávisle. Oprava objektivní chyby je možná, ale zřetelně a s uchováním původního snapshotu. Tento opravný mechanismus je naše praktické doporučení pro přenos, nikoli doložená původní databázová funkce.

Po freeze pošli uživateli stručný stav: titul je hotový, co jej charakterizuje, případné podstatné omezení a co následuje. Nepředstírej již hotové denní závěry.

## 7. Druhé a třetí vydání: nezávislost při zachované paměti

Předchozí titul nelze z živého kontextu vymazat a není to potřeba. Důležitá je disciplína rozhodnutí. Při čtení nového čísla nevynechávej článek proto, že podobný už znáš. Právě rozdíly v podání mohou být později cenné.

Naopak nehledej za každou cenu potvrzení oblíbeného tématu z prvního titulu. Pokud druhé noviny přinášejí jiný silný příběh, dovol jim jej ukázat. Počet zmínek není jediným měřítkem důležitosti.

V tomto kroku ještě nerozhoduj „FT je primary a WSJ supporting“. To jsou role v konkrétním Daily Topic, který vznikne až při Cross-Paper. Značka novin nemá stálou roli pro všechny příběhy.

Po každém titulu proveď stejné uzavření a freeze. Třetí vydání není jen doplněk ke dvěma předchozím. Má dostat stejnou možnost přinést vlastní hodnotu.

## 8. Cross-Paper: hledání příběhu pod články

Teď poprvé smíš z trojice vydání vytvářet společný obraz dne. Máš již dostatek podkladů, abys rozhodoval, které podobnosti něco znamenají a které jsou jen slovní.

### Začni otázkou, nikoli složkou

Topic „AI“ je příliš široký. Topic „jak bezpečnostní rizika mění kapitálový závod AI“ už pojmenovává napětí. Ještě musíš ověřit, že jej zdroje skutečně nesou.

Stejná událost je přirozený důvod ke spojení, ale není jediný. Články mohou společně vysvětlovat mechanismus, například přenos vyšší ceny kapitálu. Nemusíš však spojit všechny dopady do jednoho topicu už zde. Můžeš zachovat samostatné topics a propojit je až dramaturgicky.

### Rozliš tři druhy vztahu

**Popisují totéž.** Vyber hlavní nosný zdroj, ostatní přidají doplnění či nezávislé potvrzení, pokud skutečně jsou nezávislé.

**Doplňují se.** Jeden text přináší událost, druhý mechanismus nebo důsledek. Pojmenuj, co přidává každý, a nevydávej nově vytvořenou souvislost za citát některého z nich.

**Jsou příbuzné, ale samostatné.** Bezpečnost AI, financování Nvidií a dostupnost datacenter se mohou objevit v jedné dramaturgické oblasti, aniž tvoří jeden Daily Topic.

Slučování musí čtenáři něco vysvětlit. Pokud jen šetří počet řádků v databázi, nemá redakční důvod.

### Role zdrojů jsou konkrétní

Primary nese jádro konkrétního příběhu. Supporting přidává důkaz nebo aspekt. Contrasting upozorňuje na relevantní odlišný výklad či protitlak. Background poskytuje kontext. Ke každé vazbě přidej krátké vysvětlení příspěvku; samotná role je příliš chudá pro pozdější obnovení úsudku.

Tři články citující stejný podklad nejsou automaticky tři nezávislá potvrzení. Je-li jejich společný původ patrný, zachovej jej v poznámce. Toto je doporučení pro práci s evidencí, nikoli tvrzení o konkrétním incidentu experimentu.

### Rozpor nejprve rozlož

Ptáš se na stejný čas, stejné období, stejný segment, stejnou metriku a stejnou míru jistoty? Porovnáváš stav při uzávěrce s intradenní hodnotou? Celý trh s vybranými firmami? Schválený závazek s uvažovaným maximem?

Teprve když tyto rozdíly nevysvětlují nesoulad, máš skutečný rozpor. Pak jej vyřeš návratem ke zdrojům, nebo jej transparentně ponech jako nejistotu. Nevybírej pohodlnější údaj jen proto, že lépe sedí do titulku.

### INCLUDE, RESERVE, EXCLUDE

INCLUDE je rozhodnutí, že topic patří do další hlavní redakční práce. Neurčuje ještě jeho konečnou délku ani sekci. RESERVE je relevantní materiál, který nyní není hlavní volbou, ale může posloužit coverage, kuraci či změně výběru. EXCLUDE znamená vědomě nepoužít v tomto dni; důvod může být nízká relevance, duplicita či nedostatečný podklad.

Nepotřebuješ vytvořit topic pro každý článek jen proto, aby se všechny položky mapy „spotřebovaly“. Mapa je širší než denní výběr. Pokud však vypadne významný CORE příspěvek, měl bys umět říct proč.

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

Vycházej z topics po Deep Read a z rezervy. Znovu neprovádíš nezávislé mapování novin; rozhoduješ o využití již pochopeného materiálu. Pokud se objeví mezera, vrať se k mapám a zdrojům.

Výsledek má být srozumitelný i bez databáze: „dnes vysvětlíme cenu kapitálu a její přenos, fyzické limity ropy, napětí v AI a novou ekonomiku obrany; ostatní významné události pokryjeme kratší vrstvou“. To je obsahové zadání, nikoli ještě hotový text.

V poznámce zachyť hlavní výběr, funkci důležitých vedlejších témat, případně co zůstalo v rezervě a proč. Pokud využiješ reserve nad dosavadní úroveň ověření, doplň zdrojovou práci. Automatické INCLUDE pro každý CORE neexistuje.

## 12. Dramaturg: dej vydání tvar

Představ si průchod čtenáře celým textem. Co uvidí nejdřív? Kde musí zpomalit? Kde potřebuje zrychlit? Nevyčerpá první dlouhá položka všechnu pozornost? Nenásledují za sebou tři podobné příběhy, které si čtenář začne plést?

Hierarchie se vytváří pořadím, délkou, přesností úvodu a množstvím vysvětlení. Nestačí dát všem stejný blok a prvnímu přidat označení „hlavní“.

V Day 2 vznikly čtyři vrcholy a sedm hlavních jednotek. Dramaturg spojil sazby s dopady do bilancí a rozpočtů a západní AI safety s čínským paradoxem. Nvidia a fyzická infrastruktura zůstaly odlišitelné. To je konkrétní zkušenost, nikoli příkaz vyrábět každý den stejnou kompozici.

Pokud dvě témata propojíš, uchovej jejich původní identity a zdrojové vazby. Nemusíš kvůli tomu zpětně přepsat Cross-Paper ani frozen mapy. V textu však nesmí vzniknout kauzalita, kterou zdroje nepodporují.

V dramaturgické poznámce popiš pořadí, vrcholy, spojení a účel kratších vrstev. Není třeba plánovat každou větu.

## 13. Story Editor: najdi přesnou pointu

U každé hlavní jednotky si polož otázku: co by měl čtenář umět po přečtení říct vlastními slovy? Pokud odpověď zní jen „je to důležité téma“, příběh ještě nemáš.

Úhel není ozdobný titulek. Je to vybraná cesta materiálem. U Treasury může být úhlem překročení hranice, změna kupujících nebo přenos do financování. Nevybírej je podle atraktivity slov, ale podle toho, co dnes přibylo a co nesou zdroje.

Příběh nemusí obsahovat konflikt dvou osob. Může jít o napětí mezi ambicí a fyzickou kapacitou, mezi investicemi a rizikem nebo mezi krátkodobým pohybem a dlouhodobou strukturou. Nenutíš každému textu stejné dramatické schéma.

Zapiš pointu, why_now, hlavní mechanismus a hranici tvrzení. Pokud nedokážeš formulovat úhel bez přesahu přes zdroje, zúž jej nebo se vrať k Deep Read.

## 14. Brief Writer: napiš čtenáři text, který lze číst

Teď už nepíšeš poznámky pro sebe. Píšeš člověku, který neviděl tvoje tabulky. V úvodu mu dej orientaci. V hlavních příbězích vysvětli změnu a význam. V kratších položkách nezdržuj. Kuraci zdůvodni konkrétní hodnotou textu.

Nezačínej každou položku stejným obecným úvodem. Neopakuj u každé „co to znamená pro byznys“, pokud můžeš význam přirozeně vysvětlit v jedné větě. Různé příběhy potřebují různou stavbu.

Termín použij, když pomáhá přesnosti, a vysvětli jej tam, kde je to potřeba. „Hyperscaler“ není zakázané slovo, ale nesmí být náhradou za pochopení toho, o kterých firmách a obchodních modelech mluvíš.

Pozor na drobná slova: „už“, „stále“, „poprvé“, „zůstává“, „všichni“, „musí“. Často do textu propašují historické, kvantitativní nebo kauzální tvrzení, které žádná tabulka čísel nekontrolovala.

Nevkládej do čtenářského textu provozní značky CORE, INCLUDE nebo PASS. Podkladová struktura je pro redakci. Čtenářská struktura je pro porozumění.

Draft ulož jako jednu konkrétní verzi. Nestačí napsat do poznámky, že „draft vznikl“. Musí existovat text, ke kterému se další kontrola vztahuje.

## 15. Detail Editor: dej Briefu plnou hodnotu a zachovej hloubku

Ptej se, zda čtenář po Briefu chápe pointu a zda případné další čtení nabízí něco skutečného navíc. Pokud musí otevřít Detail, aby se dozvěděl, co se vlastně stalo, Brief neposkytl slíbenou hodnotu. Pokud už Brief vyčerpal všechny argumenty, důkazy a výjimky, pravděpodobně je příliš dlouhý nebo vztah k Detailu není dobře promyšlený.

Strong Detail value znamená, že téma má další podstatnou hloubku. Sufficient znamená, že rozvinutí má smysl, i když není dominantní. Weak je signál k přehodnocení rozsahu či umístění. Toto je výklad zaznamenaných kategorií, nikoli doložený přesný historický scoring.

Nevyráběj cliffhanger jen proto, aby přechod do Detailu vypadal lákavě. Napiš, co může hlubší čtení vysvětlit: finanční strukturu, rozdílné scénáře, technické limity, rozdělení rizik.

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

## 20. Jak může výsledné vydání působit

Přesné názvy sekcí musíme ověřit z autentických finálních Briefů. Následující vysvětlení jejich možných funkcí není tvrzením, že existoval závazný sedmisekční template.

„Dobré ráno“ může čtenáře uvést do dne. Nemá to být dlouhá obecná úvaha před zprávami. „Dnes v kostce“ může rychle zpřístupnit denní mapu. Pokud obě části říkají totéž, stačí funkci spojit nebo zkrátit.

„Hlavní příběhy“ nesou vysvětlení. Ne každý musí mít stejný počet odstavců. „Ještě potřebujete vědět“ chrání coverage a dává důležitým vedlejším věcem přiměřený prostor.

„Čísla dne“ mají smysl jen tehdy, když číslo něco osvětluje. Bez jednotky, období a kontextu je dekorací. Není nutné opakovat číslo z hlavního příběhu jen kvůli naplnění sekce.

„Co sledujeme“ má pojmenovat otevřenou otázku či další rozhodující vývoj. Nepředstírej budoucí datum nebo očekávanou událost, kterou zdroje nedávají. „Budeme sledovat situaci“ nic konkrétního nepřidává.

„Co dnes ještě stojí za přečtení“ vysvětluje hodnotu doporučeného textu. Kurace není zbytková hromádka. Rooftop solar a private equity v Day 1 měly vlastní místo, aniž byly násilně povýšeny na leady.

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

## 22. Supabase: jak si představit skutečné vazby

V experimentu sloužila Supabase jako místo kanonických výsledků a auditní stopy. Chat držel živý kontext a prováděl úsudek. Tyto funkce se doplňovaly. Databázový záznam sám nenahradil čtení a konverzační hlášení nenahradilo uložený výsledek.

Máme doložené zmínky o daily_topics, daily_briefs, brief_items a bbv3.editorial_notes. Máme zprávy o workflow runech, zdrojových článcích a jejich vazbách. Nemáme zde úplné názvy tabulek pro den, vydání, mapu ani vazební tabulku. Nepředpokládej proto, že následující logické entity jsou přesné SQL názvy.

### Logický model, který musíš zachovat

| Entita | Co představuje | Jak se váže dál |
| --- | --- | --- |
| Den | Jedno redakční datum | Má zdrojová vydání, topics, poznámky a Briefy |
| Vydání | Konkrétní FT, WSJ či HB | Patří ke dni a zdrojovému souboru; má samostatnou mapu |
| Editorial object | Konkrétní článek nebo relevantní objekt | Patří k vydání, má lokátor a úsudek |
| Daily Topic | Denní příběh | Spojuje zdrojové objekty přes vysvětlené role |
| Provenance vazba | Příspěvek článku k topicu | Uchovává identitu obou stran, roli a přínos |
| Editorial Note | Rozhodnutí, kontrola či snapshot | Patří k určitému dni a relevantnímu vydání/topicu/verzi |
| Master Brief | Kanonický čtenářský text | Má den, verzi, stav a vazbu na podklady |
| Brief item | Materializovaná jednotka produktu, pokud existuje | Musí vycházet ze schváleného textu a zachovat provenance |
| Workflow run | Záznam provedení kroku | Popisuje skutečný běh, ne obsahový úsudek |

Jedno vydání má mnoho objektů. Topic může čerpat z více objektů a jeden objekt může přispívat k více topics, pokud pro každý přínos existuje konkrétní důvod. Poslední možnost je doporučený logický model, nikoli ověření cardinality původní vazební tabulky. Finální textová jednotka může spojit více topics. Tyto vztahy nesmí zaniknout pouhým přejmenováním titulku.

### Kam ukládat jednotlivé výsledky

Day a issue metadata ukládej do skutečných existujících objektů dne a vydání. Issue Map položky do původního úložiště editorial objects; snapshot a závěr vydání zachovej také příslušnou Editorial Note podle skutečného formátu. Nevytvářej paralelní tabulku jen podle názvu šablony v tomto dokumentu.

Cross-Paper zapisuje daily_topics a zdrojové vazby; souhrnný důvod výběru patří do cross_paper_map. Deep Read doplňuje topic a jeho stav a ukládá deep_read_summary. Změna interpretace musí zůstat dohledatelná.

Editorial vytváří poznámky k passům a textové snapshoty. Finální kanonický text patří do daily_briefs v konkrétní verzi. Chief review musí odkazovat na tento text, ne na neurčité „aktuální vydání“.

U Day 1 v2 existoval verified Master Brief a topic provenance bez materializovaných brief_items. Proto jejich absence sama o sobě nedokazuje nehotovou redakční práci. Je to samostatná otázka přípravy pro publishing, kterou tento proces automaticky neřeší.

### Co musí nový Chat zjistit před prvním zápisem

Tato část je provozní doporučení pro bezpečné navázání, nikoli dodatečně vymyšlené historické schéma.

1. Identifikuj přesný autorizovaný projekt a původní v3 datový prostor. Pokud je více kandidátů, nevybírej podle podobného názvu bez opory.
2. Přečti příslušné existující tabulky a jejich schéma: primární klíče, cizí klíče, povinné hodnoty, JSON pole, unikátní omezení a povolené stavy.
3. Načti několik autentických relevantních záznamů z experimentu: dokončené vydání, topic s vazbami, Deep Read note, pass note a verified Brief. To ukáže skutečnou konvenci, nikoli jen názvy sloupců.
4. Přiřaď logické struktury tohoto průvodce ke skutečným polím. Rozdíl řeš mapováním, ne okamžitou migrací schématu.
5. Ověř aktuální den a existující verze. Nezakládej druhý stejný den nebo duplicitní issue, pokud už existuje.
6. Zapiš přesné reference a ověřené konvence do předávací poznámky. Nevkládej tajné klíče.

Takto získané informace jsou technické zjištění. Neznamenají povolení načítat novější redakční architekturu a zpětně jí měnit v3. Když skutečné historické objekty nelze oddělit od novějších, pojmenuj tento problém a nepředstírej čistou rekonstrukci.

### Co musí být jasné u každého zápisu

Víš, zda vytváříš nový objekt, opravuješ pracovní objekt, přidáváš poznámku, nebo ukládáš novou verzi. Znáš jeho den a přesné identity vazeb. Nepoužíváš shodu titulku jako jediný způsob přiřazení. Nepřepisuješ frozen výsledek jen proto, že finální text používá jiný název.

Po zápisu ověř skutečně uložený obsah a důležité vazby. Výsledek nástroje „dotaz proběhl“ nemusí znamenat, že se změnil požadovaný řádek. U finálního textu zkontroluj, že je celý, má správný den a verzi a že status odpovídá review.

Neber historická slova frozen, DONE, done, briefing a verified jako jednu univerzální stavovou posloupnost. V hlášeních patřila různým objektům. Platné hodnoty ověř v jejich skutečné struktuře.

### Když zápis selže

Nedělej z technického problému nový redakční výběr. Uchovej připravený výsledek, zjisti, zda se zápis částečně provedl, a oprav jen chybějící část. Před opakováním hledej už vytvořený záznam, abys nevytvořil duplicitu.

Konkrétní zkušenost: PASS 4 byl v explicitní transakci bez COMMIT a neuložil se. Oprava persistence podle hlášení nezměnila obsah. Poučení není „vždy používej určitý SQL obal“, ale „rozuměj transakčnímu chování použitého rozhraní a ověř uložení“.

Když není databáze dostupná, můžeš připravit lokální pracovní výstup, ale označ jej jako nezapsaný. Nepovažuj jej za nový kanonický stav. Přechod do náhradního trvalého úložiště musí být vědomý, ne skrytá změna architektury.

## 23. Rozhodování v obtížných situacích

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

## 24. Časová kontinuita bez předurčení nového dne

V experimentu jsme si uvědomili, že horizontální spojení tří novin funguje lépe než formalizovaná osa přes čas. Uživatel upozornil na Treasury a vznikla poznámka memory_would_help. Nový povinný temporal pass ale zaveden nebyl.

Nes si z předchozího dne poslední ověřený stav, to, co jsme čtenáři už vysvětlili, a otevřené otázky. Při samostatném čtení dnešních vydání nepoužívej tento seznam jako objednávku leadů. Nový den může mít jiné těžiště.

Po freeze map zvaž, zda jde o pokračování, zesílení, obrat, nový mechanismus nebo pouhé opakování. Nepiš „pokračuje trend“ jen proto, že se téma objevilo dvakrát. Pokud souvislost znáš pouze z konverzační paměti, ověř ji před konkrétním publikovaným srovnáním.

Zkušenost s Treasury ukazuje možnou návaznost: cena kapitálu a blízkost hranice; intradenní překročení; další otázka struktury kupujících a přenosu do hypoték. Smyslem není znovu každý den vysvětlovat všechno, ale přesně říct, co dnešní zdroje přidaly.

## 25. Jak zacházet s koncem Chatu

Nespoléhej na to, že bude čas napsat dokonalé poslední předání. Ukládej dokončené artefakty průběžně a při denní retrospektivě obnov stručnou předávací poznámku. Nejlepší přechod je mezi dny nebo po uzavřeném kroku.

Novému Chatu předej tři druhy informace: tento způsob práce, autentické výsledky jako měřítko a aktuální stav s otevřenými příběhy. Přesný vnitřní kontext předchozího Chatu přenést nelze, ale lze obnovit pracovní porozumění.

Nepředávej pouze stále kratší souhrn souhrnu. Udržuj odkazy na skutečné mapy, texty, poznámky a zdroje. Při rozpracovaném dni musí být zřejmé, které části už byly ověřeny a které ne.

Po načtení má nový Chat stručně vyjádřit, co přebírá a co udělá dál. Nejde o nový gate ani povinné čekání na potvrzení, pokud má dost podkladů a zadání. Je to kontrola, že nezaměnil například dvě frozen mapy za dokončený Cross-Paper.

## 26. Co nepřidávat jen pro pocit úplnosti

Tento dlouhý průvodce má být bohatý vysvětlením, nikoli počtem povinností. Nepřeváděj každý jeho odstavec na pole, check-box nebo samostatný workflow run.

Nepotřebujeme skóre každého článku, kvótu témat, povinný konflikt v každém příběhu, stejné délky poznámek ani povinný zásah posledního editora. Nepotřebujeme samostatného agenta pro každou roli. Nepotřebujeme trendový objekt jen proto, že se něco objevilo dvakrát.

Potřebujeme spolehlivou identitu zdrojů, nezávislé mapy, poctivou syntézu, návrat ke zdrojům, čitelný text, skutečné kontroly a důvody zásadních rozhodnutí. Když přibývající administrativa začne bránit čtení a úsudku, vrať se k tomu, čemu má sloužit.

---

# Praktická příloha: struktury a provozní orientace

Následující část soustředí šablony na jedno místo. Jsou to logické kontrakty pro přenos práce. Před zápisem do Supabase je mapuj na skutečné ověřené schéma. Žádná ukázková hodnota není existujícím ID.

## A. Šest základních struktur

### Issue Map item

```yaml
item_id: "skutečné přidělené ID"
issue_id: "skutečné ID vydání"
source:
  file_ref: "dohledatelný zdroj"
  pdf_pages: []
  printed_pages: []
  continuation_locator: null
headline_original: ""
working_label_cs: ""
genre: "news | analysis | interview | opinion | editorial | lex | other"
article_point: "co tvrdí tento článek, nikoli celý sektor"
editorial_value: "proč může být důležitý pro čtenáře"
priority: "CORE | CANDIDATE | LOW"
priority_reason: "krátce, zejména u hraničního případu"
deep_read_candidate: false
deep_read_questions: []
memory_candidate: false
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
  memory_candidates: null
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
differences_and_tensions: []
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
  workflow_run_id: null
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
known_limitations: []
verified_at: null
```

Vazba editorial_units je doporučení pro přenos provenance, nikoli důkaz, že historicky existovala v tomto tvaru. Přesný formát textu a metadata se musí přizpůsobit původnímu schématu.

## B. Co mít uložené na každém přirozeném checkpointu

| Checkpoint | Obsahový výsledek | Auditní záznam | Než řekneš „hotovo“ |
| --- | --- | --- | --- |
| Příjem vydání | Identita dne, vydání a zdroje | Skutečný start a pořadí | Ověřit, že nejde o duplicitní či jiné vydání |
| Freeze mapy | Objekty, lokátory, priority a závěr | Snapshot, procesní omezení | Zkontrolovat rozsah stran, counts a persistence |
| Cross-Paper | Topics, rozhodnutí a source links | Důvody syntézy a fronta Deep Read | Ověřit vazby na existující články |
| Deep Read | Zpřesněné topics | Summary a významné změny | Nepřekrýt nevyřešenou pointu statusem done |
| Assignment až Story | Zadání, dramaturgie a úhly | Tři příslušné poznámky | Zachovat rozdíl mezi plánem a napsaným textem |
| Writer | Celý draft | Vazba na draft | Ověřit skutečné uložení textu |
| Detail až Language | Posouzení a opravený text | Review notes a potřebné snapshoty | Udržet kontrolu navázanou na správnou verzi |
| Chief | Schválený Master Brief | Brány a verdict | Ověřit kanonickou verzi, stav a podklady |
| Konec dne | Aktuální předání | Retrospektiva | Oddělit hotovou redakci od neprovedené publikace |

## C. Doložené body experimentu, podle kterých se lze kalibrovat

Day 1 / 14. 9. skončil Master Briefem v2 ve stavu verified. Mapa dne byla podle hlášení jasná po prvních pěti větách. Hlavní čtení mělo čtyři vrcholy, coverage držela další významné události a kurace měla vlastní místo. Všech osm průchodů bylo zaznamenáno, Chief neprovedl další zásah.

Day 2 / 15. 9. začal WSJ: 38 objektů, z toho 8 CORE, 22 CANDIDATE, 8 LOW. FT: 41 objektů, 11 CORE, 26 CANDIDATE, 4 LOW. HB: 33 objektů, 10 CORE, 19 CANDIDATE, 4 LOW. Celkem 112 objektů. Cross-Paper vytvořil 28 topics, 12 INCLUDE a 16 RESERVE, se 71 provenance vazbami. Sedm INCLUDE mělo tři tituly, dvě dva a tři jediný zdroj.

Deep Read prošlo všech dvanáct INCLUDE. Změnily se formulace a interpretace, nikoli výběrový status. Editorial vytvořil čtyři vrcholy a sedm hlavních jednotek; Detail review 6 strong a 1 sufficient. Verification našla šest konkrétních oprav, v dostupném záznamu je podrobně popsaný Treasury watchlist. Finální text měl přibližně 8,2 tisíce znaků a byl uložen jako verze 1, verified.

Day 3 / 16. 9. má v posledním dostupném checkpointu FT a WSJ frozen, každé po 38 objektech. FT: 10 CORE, 22 CANDIDATE, 6 LOW. WSJ: 13 CORE, 21 CANDIDATE, 4 LOW. HB ještě chybí. To je historická orientace, nikoli aktuální ověření databáze. Před pokračováním načti skutečný stav.

Rok vydání zde není potvrzen. Žádný z těchto počtů není norma nebo požadovaný výkon příštího dne.

## D. Co ještě nelze nahradit tímto průvodcem

K plné kalibraci patří celé autentické Master Briefy Day 1 v2 a Day 2 v1. V této přípravě nebyly načteny; nejsou proto nahrazeny domyšlenými texty ani falešnými odkazy. Při jejich získání ověř den, rok, verzi a status. Přečti je celé, ne jen závěrečné hlášení.

Pro provozní pokračování potřebuješ reálné mapy, topics, poznámky a zdrojová vydání rozpracovaného dne. Tento návod poskytuje způsob práce, ne neexistující přístup k historickým souborům.

Pro přesné zápisy potřebuješ identitu projektu a ověřené původní schéma. Známé názvy daily_briefs, daily_topics, brief_items a bbv3.editorial_notes jsou vodítka, nikoli kompletní připojovací konfigurace. Nevytvářej databázi podle tohoto dokumentu jen proto, že schéma ještě nemáš.

## E. Krátké zadání pro zahájení nového Chatu

> Přebíráš redakční práci Business Briefu metodou Fast Editorial v3. Přečti celý FAST_EDITORIAL_START_HERE.md, aktuální EDITORIAL_HANDOVER.md a dostupné autentické schválené Briefy. Obnov skutečné podklady rozpracovaného dne. Stručně řekni, jak chápeš produkt, co je dokončeno, co je frozen a jaký je další krok. Rozliš převzaté hlášení od vlastního ověření. Chybějící potřebný podklad pojmenuj konkrétně. Zachovej metodu a samostatnost nových vydání. Před prvním zápisem ověř správný původní projekt a schéma; nevymýšlej identifikátory ani nové tabulky. V práci pokračuj souvisle, s redakčním úsudkem a s průběžně uloženými důležitými výsledky.

## F. Poslední rada novému editorovi

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

**Ulož:** daily_briefs záznam podle původního schématu, Chief review, příslušné snapshoty a závěrečné poznámky. brief_items vytvářej jen podle skutečně zavedeného publishing postupu, nikoli jako domnělou podmínku redakčního schválení.

**Nesmí se stát:** Hlášení úspěchu před ověřením zápisu, záměna verified za published nebo doplnění chybějících ID odhadem.

**Den je uzavřený, když:** Schválený text skutečně existuje, audit umožňuje pochopit rozhodnutí a handover uvádí pravdivý další krok. Pokud chybí pouze zápis, hlášení musí tuto výjimku přiznat.

## H. Slovník polí: co znamenají a proč je uchovávat

Povinnost níže platí pro doporučený logický předávací formát, nikoli pro neověřené SQL schéma. **A** znamená nutné pro dokončený objekt, **P** nutné při uvedené situaci, **V** volitelné. Pracovní objekt může mít dočasnou mezeru, ale musí být patrné, že není dokončený.

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
| genre | A: druh textu | interview | Atribuce a práce s názory |
| article_point | A: vlastní obsah článku | Měsíční srovnání prodejního kanálu | Cross-Paper syntéza |
| editorial_value | A: proč stojí za pozornost | Jiný obraz poptávky než celkové registrace | Selekce |
| priority | A: samostatná priorita vydání | CORE | Pozdější výběr, ne nárok na publikaci |
| priority_reason | P: zejména u hraničních či překvapivých rozhodnutí | Důležitý kanál, omezené období | Obnova úsudku |
| deep_read_candidate | A: předběžný příznak | true | Příprava fronty, nikoli stav hotového čtení |
| deep_read_questions | P: při známých otázkách | Měsíc, nebo kumulativní období? | Cílený návrat ke zdroji |
| memory_candidate | A v této šabloně: pracovní úsudek o paměťové hodnotě | true | Pozdější kontext; není potvrzení ingestce |
| structural_notes | P: při potřebě vyjasnit hranice objektu | Teaser není druhý článek | Obnova a kontrola mapy |

Původní rekonstrukce používala headline, source_locator, open_questions a deep_read_reason. V rozšířené šabloně jejich význam nesou headline_original/working_label_cs, source a deep_read_questions. Výslovný důvod kandidatury připoj k otázkám nebo do skutečného existujícího pole; při mapování nesmí zmizet. Nejde o požadavek přejmenovat databázové sloupce.

### H2. Issue-level conclusion

| Pole | Význam a povinnost | Příklad | Pozdější použití |
| --- | --- | --- | --- |
| issue_id, day_id | A: identita vydání a dne | Skutečné přidělené klíče | Správné zařazení |
| publication | A: titul | Financial Times | Rozlišení zdroje |
| issue_date | A: celé ověřené datum | Datum převzaté z PDF | Vyloučení záměny roku či dne |
| intake_order | A: skutečné pořadí příjmu | 2 | Nezávislost a audit |
| source_file_ref | A: reference originálu | Ověřený soubor | Návrat ke zdroji |
| page_count | A: rozsah PDF | 18 | Kontrola úplnosti prohlídky |