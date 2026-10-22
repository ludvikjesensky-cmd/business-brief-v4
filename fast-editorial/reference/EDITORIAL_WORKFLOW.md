# Business Brief — Editorial Workflow v1

**Datum:** 29. 9. 2026  
**Stav:** kanonický redakční workflow pro tvorbu ranního Briefu během 10denního experimentu  
**Nadřazený dokument:** PRODUCT_MODEL.md  
**Účel:** převést kvalitní issue-level a cross-paper analýzu do živého, hierarchického a čtivého Business Briefu bez ztráty přesnosti.

---

## 1. Proč tento workflow vzniká

Day 1 experimentu ukázal, že Fast Editorial velmi dobře zvládá:

- rychle pochopit jednotlivá vydání;
- vytvořit použitelné provisional Issue Maps;
- spojit články do cross-paper témat;
- provést selektivní Deep Read;
- ověřit fakta a nejistoty.

Slabší částí Day 1 nebyla analýza vstupů, ale **konečná editorská kompozice**.

První Brief byl informačně správný a důvěryhodný, ale:

- jednotlivé položky měly téměř stejnou váhu a délku;
- výsledek působil jako série miničlánků;
- rytmus byl monotónní a málo vhodný pro audio;
- text často uzavíral příběh místo toho, aby probudil zájem;
- některé kvalitní RESERVE položky úplně zmizely místo krátkého coverage zmínění;
- vznikla sekce „Analýzy“, která neodpovídala významu Analýz v PRODUCT_MODEL.md.

Z toho plynou dva principy:

> **Brief musí být informačně úplný, ale obsahově nevyčerpávající.**

> **Brief má odhalit pointu článku nebo tématu a otevřít jeho hloubku, ne ji celou spotřebovat.**

---

## 2. Role nejsou agenti

Níže definované role jsou **redakční průchody**.

Neznamená to, že každá role musí být samostatný agent, API call, služba nebo model.

V experimentu je důležité oddělit **odpovědnosti a rozhodnutí**, ne maximalizovat počet technických komponent.

Pozdější automatizace může některé průchody spojit, pokud desetidenní experiment prokáže, že tím neutrpí kvalita, auditovatelnost ani redakční kontrola.

---

## 3. Redakční kontrakt Briefu

Struktura Briefu se nevymýšlí každý den znovu. Vychází z PRODUCT_MODEL.md:

1. **Dnes v kostce**
2. **Co stojí za přečtení**
3. **Další důležité změny**
4. **Ještě stojí za pozornost**
5. **Signály**
6. **Co sledovat dál**

Ne každá sekce musí být každý den naplněná.

Nová sekce se ale nemá vytvářet pouze proto, že zbyly texty, které se jinam nevešly.

Zvlášť platí:

- sekce **Analýzy** je vyhrazena vlastní analytické větvi Business Briefu;
- shrnutí nebo syntéza kvalitního článku FT, WSJ nebo Handelsblattu není automaticky vlastní Analýza Business Briefu;
- současné **Co stojí za přečtení** funguje během experimentu hlavně jako syntetická vrstva hlavních příběhů dne;
- **Ještě stojí za pozornost** je primární reading-curation vrstva: texty, které stojí za skutečný čas čtenáře;
- importance of event a reading value of article se posuzují odděleně.

---

## 4. Kanonický redakční řetězec

Fast Editorial předává po cross-paper vrstvě sadu daily_topics, Deep Read poznámky a provenance.

Od tohoto bodu probíhá osm redakčních průchodů:

~~~text
daily_topics + Deep Read + provenance
        ↓
1. Assignment Editor
        ↓
2. Dramaturg
        ↓
3. Story Editor
        ↓
4. Brief Writer
        ↓
5. Detail Editor
        ↓
6. Verification Editor
        ↓
7. Language & Style Editor
        ↓
8. Editor-in-Chief
        ↓
verified Daily Brief
~~~

Každý průchod má vlastní otázku, pravomoci a zákaz.

---

## 5. Role 1 — Assignment Editor

### Hlavní otázka

> **Co dnes opravdu patří do vydání a jak velký prostor si to zaslouží?**

### Vstup

- všechny daily_topics, nejen INCLUDE;
- rozhodnutí INCLUDE / RESERVE / EXCLUDE;
- Deep Read poznámky;
- daily_delta;
- importance_reason;
- source provenance;
- PRODUCT_MODEL.md.

### Úkol

Assignment Editor vytváří hierarchii.

Každé relevantní téma zařadí do jedné z rolí:

- topline — kandidát do Dnes v kostce;
- lead — velký blok Co stojí za přečtení;
- secondary — kratší, ale stále významná položka;
- coverage — jedna až dvě věty v Dalších důležitých změnách;
- curated — Ještě stojí za pozornost;
- signal — dnešní nový důkaz dlouhodobějšího vývoje;
- watch — Co sledovat dál;
- drop — dnes do Briefu nepatří.

### Povinné zásady

- INCLUDE v databázi **neznamená automaticky velký blok**.
- RESERVE **neznamená automaticky zmizení z Briefu**.
- Coverage je součást „minimum pro informovanost“.
- Velký prostor dostává jen to, co si ho zaslouží.
- Duplicitní témata se mohou spojovat.

### Nesmí

- psát hotový Brief;
- přikrášlovat fakta;
- zvětšovat téma jen proto, že ho pokrývají všechny tři zdroje;
- vytvářet novou produktovou strukturu mimo PRODUCT_MODEL.md.

### Výstup

editorial_selection_v1

Minimálně:
- topic id;
- editorial role;
- cílová sekce;
- doporučená délka nebo form factor;
- stručný důvod;
- případné spojení s jiným tématem.

---

## 6. Role 2 — Dramaturg

### Hlavní otázka

> **Jak má celé vydání téct, aby čtenář pochopil hierarchii a chtěl pokračovat?**

### Úkol

Dramaturg pracuje s vydáním jako celkem.

Určuje:
- pořadí;
- velikost jednotlivých bloků;
- střídání témat;
- rytmus;
- gradaci;
- kde má být krátké tempo a kde delší zastavení;
- které tematicky blízké bloky je lepší spojit.

### Povinné zásady

- Různá důležitost musí být vidět i v prostoru.
- Sedm témat nesmí vypadat jako sedm stejně velkých hlavních zpráv.
- Po sobě nemají chodit témata stejného typu a stejného rytmu bez důvodu.
- Dramaturgie musí fungovat i při poslechu.
- Brief má mít jasný začátek, střed a zakončení.

### Typický zásah

Day 1:
- americké dluhopisy + ECB lze dramaturgicky spojit pod širší příběh **ceny kapitálu**, pokud tím nezmizí podstatná informace.

### Nesmí

- měnit fakta;
- doplňovat nové source claims;
- přepisovat rozhodnutí jen podle osobního tematického vkusu bez redakčního důvodu.

### Výstup

dramaturgy_plan_v1

Minimálně:
- pořadí sekcí;
- pořadí témat;
- formát každé položky;
- plán spojení nebo rozdělení;
- rytmické poznámky.

---

## 7. Role 3 — Story Editor

### Hlavní otázka

> **Jaký je skutečný úhel této položky a proč by měl čtenář chtít vědět víc?**

Story Editor ještě nepíše finální text.

Pro každou významnější položku vytvoří redakční kartu:

### A. Fact

Co se skutečně stalo? Jedna jasná věta.

### B. Angle

Proč je to zajímavější nebo důležitější, než napovídá samotný titulek?

Může jít o:
- konflikt;
- paradox;
- překvapivé číslo;
- druhý řád dopadu;
- spojení dvou zdrojů;
- širší otázku;
- změnu proti předchozímu stavu.

### C. Tension

Co je na příběhu stále neuzavřené, sporné nebo překvapivé?

### D. Detail Promise

Co konkrétně získá čtenář, pokud otevře Detail?

Například:
- rozpad čísel;
- scénáře;
- argumentaci autora;
- konkrétní firemní opatření;
- srovnání zdrojů;
- historický kontext;
- důkazní řetězec.

### Klíčový princip

> **Ne clickbait. Curiosity gap nesmí vzniknout zatajením základního faktu.**

Čtenář musí po Briefu znát hlavní informaci.

Důvod otevřít Detail vzniká z toho, že příběh má **další skutečnou hloubku**, ne z toho, že jsme hlavní fakt schovali.

### Nesmí

- vymýšlet drama;
- přehánět;
- měnit míru jistoty;
- nahrazovat fakt otázkou jen proto, aby text působil zajímavěji.

### Výstup

story_angles_v1

Pole:
- fact;
- angle;
- tension;
- detail_promise;
- opening_candidate;
- forbidden_overstatement nebo uncertainty note.

---

## 8. Role 4 — Brief Writer

### Hlavní otázka

> **Jak to napsat jasně, živě a úsporně podle schválené hierarchie?**

Writer dostává:
- selection;
- dramaturgy plan;
- story angles;
- ověřené Deep Read poznámky.

Nemá znovu rozhodovat o celé hierarchii.

### Povinné zásady

- Držet se PRODUCT_MODEL struktury.
- Různé formáty mají různou délku.
- Hlavní položka může být přibližně 350–600 znaků.
- Coverage může být 1–2 věty.
- Curated recommendation může být krátké doporučení s důvodem, proč stojí za čas.
- Dnes v kostce musí dávat hodnotu i čtenáři, který už dál nepokračuje.
- Text nesmí systematicky opakovat vzorec „stalo se X → pro firmy je důležité Y“.

### Variabilita vstupu do příběhu

Podle charakteru tématu lze začít:
- číslem;
- konfliktem;
- důsledkem;
- obrazem;
- paradoxem;
- otázkou;
- samotnou událostí.

Variabilita nesmí být samoúčelná.

### Nesmí

- vyčerpávat všechny detaily článku;
- přidávat informace, které nejsou ve schválených podkladech;
- nafukovat položku, kterou Assignment Editor označil jako coverage;
- psát clickbait.

### Výstup

brief_draft_vN

---

## 9. Role 5 — Detail Editor

### Hlavní otázka

> **Po přečtení hlavní položky zůstává legitimní důvod otevřít Detail?**

Toto je samostatný quality gate.

### Kontroluje

- zda Brief předal pointu;
- zda ale nevyčerpal článek nebo téma;
- zda zůstala skutečná další hloubka;
- zda Detail nabízí něco víc než jen delší shrnutí stejného textu;
- zda hlavní položka přirozeně otevírá otázku, scénář, argumentaci nebo čísla vhodná pro Detail.

### Pokud důvod otevřít Detail chybí

Editor může doporučit:
- odebrat vedlejší čísla;
- přesunout detailní mechanismus až do Detailu;
- zkrátit argumentaci;
- zvýraznit otevřenou otázku;
- přesněji formulovat detail_promise.

### Tvrdá hranice

> **Nikdy se nesmí odstranit klíčový fakt jen proto, aby vznikl klik.**

### Výstup

detail_gap_review_v1

Pro každou hlavní položku:
- detail_value = strong | sufficient | weak;
- proč;
- co případně přesunout do Detailu;
- zda Brief stále splňuje minimum pro informovanost.

---

## 10. Role 6 — Verification Editor

### Hlavní otázka

> **Je každý důležitý claim přesný, doložený a formulovaný se správnou mírou jistoty?**

Verification Editor kontroluje finální význam textu proti:
- Deep Read;
- source provenance;
- případným externím fact-checkům;
- známým uncertainty notes.

### Hlídá zejména

- interní scénář ≠ veřejná prognóza;
- tržní očekávání ≠ rozhodnutí centrální banky;
- diskutovaná možnost ≠ přijaté rozhodnutí;
- komentář zdroje ≠ ověřený fakt;
- syntéza Business Briefu ≠ tvrzení zdroje;
- korelace ≠ příčina;
- čísla, data, jména, jednotky a časové ukotvení.

### Nesmí

- dělat stylistickou přestavbu celého vydání;
- vracet do textu všechny detaily, které Detail Editor správně odstranil;
- nahrazovat redakční úsudek mechanickým „více zdrojů = pravda“.

### Výstup

verification_review_v1

Stav každé položky:
- checked;
- needs_revision;
- blocked.

---

## 11. Role 7 — Language & Style Editor

### Hlavní otázka

> **Zní to jako Business Brief a chtěl bych pokračovat ve čtení nebo poslechu?**

Tato role už neřeší výběr témat ani source truth.

Řeší:
- rytmus;
- přirozenou češtinu;
- délku vět;
- opakování;
- monotónnost;
- nadbytečný korporátní jazyk;
- titulky;
- přechody;
- vhodnost pro audio.

### Povinné zásady

Text má působit jako:
- inteligentní editor provázející novinami;
- nikoli databáze;
- nikoli školní referát;
- nikoli marketingový copywriting;
- nikoli syntetický seznam shrnutí.

### Anti-patterns

Opakované formule typu:
- „Pro management je důležité...“
- „Pro firmy je podstatné...“
- „Jde tedy o...“
- „Z toho vyplývá...“

mohou být jednotlivě správné, ale při opakování ničí hlas a rytmus.

### Audio test

Významnější blok se má dát přirozeně přečíst nahlas.

Pokud třetí nebo čtvrtá položka zní rytmicky stejně jako první, je potřeba úprava.

### Výstup

language_voice_review_v1

---

## 12. Role 8 — Editor-in-Chief

### Hlavní otázka

> **Je to dnes skutečně vydání Business Briefu?**

Editor-in-Chief čte výsledný Brief jako celek.

Ideálně nepracuje detailně s historií všech předchozích průchodů, aby dokázal simulovat skutečného čtenáře.

### Tři finální gate

#### A. Coverage

Dostane čtenář věrný obraz toho, co bylo dnes ve sledovaných novinách podstatné?

#### B. Hierarchy

Je do 30–90 sekund jasné, které tři až pět věcí opravdu definují den?

#### C. Curiosity

Vyvolává alespoň několik hlavních položek přirozenou chuť otevřít Detail nebo originální zdroj?

### Další kontroly

- není Brief zbytečně dlouhý;
- není příliš krátký na to, aby ztratil coverage;
- hlavní témata mají skutečně větší prostor;
- RESERVE položky nezmizely automaticky;
- Dnes v kostce funguje samostatně;
- Co sledovat dál obsahuje skutečné triggery, ne obecný kalendář;
- nevznikla produktově chybná sekce.

### Pravomoc

Editor-in-Chief může:
- škrtat;
- zkracovat;
- přesouvat;
- spojovat;
- vrátit jednotlivou položku o jeden konkrétní průchod zpět.

Nemá bezdůvodně restartovat celý proces.

### Výstup

daily_brief verified

---

## 13. Povinné artefakty a audit

Během experimentu chceme zachovat stopu rozhodnutí.

Doporučený řetězec:

~~~text
daily_topics
→ editorial_selection_v1
→ dramaturgy_plan_v1
→ story_angles_v1
→ brief_draft_vN
→ detail_gap_review_v1
→ verification_review_v1
→ language_voice_review_v1
→ daily_brief verified
~~~

Tyto názvy jsou **logické artefakty workflow**, nikoli automatický požadavek na nové databázové tabulky.

Během 10denního experimentu lze výstupy ukládat jako:
- strukturovaná data tam, kde už schéma stačí;
- Markdown derived artifacts;
- Editorial Notes;
- workflow artifacts.

Nové DB tabulky nebo schema se mají přidat až tehdy, když experiment ukáže, že jsou dlouhodobě potřebné.

---

## 14. Content budget a redakční hierarchie

Nezavádíme pevnou kvótu článků.

Ale zavádíme zásadu:

> **Ne všechna témata mají mít stejnou délku.**

Orientační form factors:

- topline: 1 věta;
- lead: 350–600 znaků;
- secondary: 200–400 znaků;
- coverage: 1–2 věty;
- curated: krátké doporučení + proč stojí za pozornost;
- signal: velmi krátká informace + vztah k trendu;
- watch: známý stav + neznámá + trigger.

Celková délka není cíl sama o sobě.

Cíl je:
- vysoká informační hustota;
- jasná hierarchie;
- dostatečná coverage;
- čitelnost a poslouchatelnost.

---

## 15. Vztah Brief → Detail

Produktová dvojice:

> **Brief = Tohle byste měli vědět a tady je důvod, proč je to zajímavé.**

> **Detail = Tady je celý příběh, argumentace, evidence a souvislosti, které jsme v Briefu jen otevřeli.**

Detail nesmí být pouze delší verzí stejného shrnutí.

Měl by přidat například:
- plnou argumentaci;
- scénáře;
- další čísla;
- časovou osu;
- rozdíly mezi zdroji;
- důkazní oporu;
- Memory kontext;
- souvislosti a implikace.

---

## 16. Vztah k audio formátu

Audio je odvozeno ze stejného schváleného redakčního jádra, ale není mechanickým TTS newsletteru.

Language & Style Editor a pozdější audio adaptace musí respektovat:
- kratší věty;
- slyšitelnou hierarchii;
- přechody;
- změny tempa;
- omezení dlouhých výčtů;
- přirozený mluvený rytmus.

Audio má působit jako **editor, který posluchače provádí dnešním tiskem**.

---

## 17. Day 1 jako baseline

Day 1 / 14. 9. 2026 zůstává zachován jako baseline.

Jeho první Brief se nemá zpětně přepsat.

Další test:

> **Vytvořit Day 1 Brief v2 ze stejných 24 daily_topics a stejných Deep Read podkladů, bez nového research, pouze pomocí Editorial Workflow v1.**

Cíl:
- izolovat přínos samotné editorské práce;
- porovnat v1 vs. v2 nad identickým informačním základem;
- zjistit, zda workflow zlepšuje hierarchii, rytmus, coverage a curiosity bez ztráty přesnosti.

Teprve potom pokračovat k dalším automatizačním rozhodnutím.

---

## 18. Co budeme během experimentu sledovat

K existujícím metrikám přidat kvalitativní pozorování:

- kolik INCLUDE témat skončilo jako lead vs. short form;
- kolik RESERVE témat se vrátilo do coverage;
- kolik položek Dramaturg spojil;
- kolik Story Editor úhlů bylo použito;
- kolik hlavních položek mělo po Detail Review slabý detail_value;
- kolik claimů Verification Editor vrátil;
- kolik textu Language Editor zkrátil nebo přepsal kvůli monotónnosti;
- zda Editor-in-Chief vrátil vydání zpět;
- zda se Brief dá pochopit jen z Dnes v kostce;
- zda hlavní položky přirozeně otevírají Detail.

Experiment nemá používat umělý numerický quality score jako náhradu redakčního úsudku.

---

## 19. Shrnutí rolí

| Role | Hlavní otázka | Smí měnit | Nesmí měnit |
| --- | --- | --- | --- |
| Assignment Editor | Co a jak velké? | výběr, hierarchii, form factor | fakta |
| Dramaturg | Jak to má téct? | pořadí, rytmus, spojení | source truth |
| Story Editor | Proč je to zajímavé? | úhel, tension, Detail promise | jistotu faktů |
| Brief Writer | Jak to napsat? | formulaci v daném rámci | hierarchii bez důvodu |
| Detail Editor | Zůstává důvod jít hlouběji? | rozsah a hloubku Briefu | hlavní fakt |
| Verification Editor | Je to přesné? | problematické formulace | dramaturgii bez potřeby |
| Language & Style Editor | Chci poslouchat dál? | jazyk, rytmus, titulky | význam |
| Editor-in-Chief | Je to skutečně vydání? | finální škrty a návraty | source truth |

---

## 20. Nejkratší interní pravidlo

> **Vyber. Seřaď. Najdi úhel. Napiš. Nevyčerpej. Ověř. Oživ. Vydávej až potom.**

---

## 21. Publishing layer — Web / Email / Audio

Osm redakčních průchodů vytváří jeden schválený **Master Brief**.

Master Brief je kanonický redakční obraz dne. Není přímo newsletter ani voice script.

Po Editor-in-Chief gate následuje samostatná Publishing vrstva:

~~~text
MASTER BRIEF
├→ Web Editor   → Web Brief
├→ Email Editor → Email Brief
└→ Audio Editor → Voice Script
                   ↓
               Channel QA
~~~

Pravidla:
- všechny kanály sdílejí stejnou redakční hierarchii, factual truth a míru jistoty;
- web může být nejúplnější podobou vydání;
- e-mail je rychlejší ranní vstup a nemusí reprodukovat celý web;
- audio je samostatná mluvená adaptace, nikoli mechanický TTS newsletteru;
- kanálová adaptace smí měnit délku, syntax a přechody, ale nesmí vytvářet novou redakční pravdu.

Detailní pracovní instrukce jsou v `docs/EDITORIAL_PLAYBOOK.md`.
