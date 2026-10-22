# Business Brief — Editorial Playbook v1

**Datum:** 29. 9. 2026  
**Stav:** první pracovní koncept pro Day 1 → Brief v2  
**Nadřazené dokumenty:** `PRODUCT_MODEL.md`, `EDITORIAL_WORKFLOW.md`  
**Účel:** převést kanonický workflow do konkrétních pracovních instrukcí, rozhodovacích pravidel, výstupních kontraktů a quality gates.

---

## 1. Co tento dokument je

`PRODUCT_MODEL.md` říká **co je Business Brief**.

`EDITORIAL_WORKFLOW.md` říká **jaké redakční průchody existují a kde končí jejich odpovědnost**.

Tento Playbook říká:

> **Jak se každý průchod skutečně provádí.**

Je záměrně označen jako **v1 / pracovní koncept**.

Není to sbírka definitivních pravidel pro všechny budoucí situace. Má být dostatečně přesný, aby šel konzistentně použít na Day 1 Brief v2, a současně dostatečně lehký, aby se po praktickém testu dal opravit podle skutečných selhání.

Zásada proti over-engineeringu:

> **Nové pravidlo nevzniká proto, že si umíme představit výjimku. Vzniká až tehdy, když konkrétní průchod bez něj opakovaně selhává.**

---

# PART A — GLOBÁLNÍ REDAKČNÍ KONTRAKT

## 2. Produktová severka

Denní Brief musí současně splnit šest věcí:

1. **Coverage** — nic podstatného z hlavních vydání nezmizí jen proto, že nedostalo dlouhý blok.
2. **Hierarchy** — během desítek sekund je jasné, co dnes opravdu dominuje.
3. **Curiosity** — nejlepší položky přirozeně otevírají chuť jít do Detailu.
4. **Reading value** — Brief aktivně ukazuje texty, které stojí za skutečný čas čtenáře, i když nejsou největšími zprávami dne.
5. **Trust** — míra jistoty odpovídá zdrojům.
6. **Economy** — čtenářův čas je vzácnější než prostor, který máme k dispozici.

Dvě závazné věty:

> **Brief musí být informačně úplný, ale obsahově nevyčerpávající.**

> **Brief má odhalit pointu a otevřít hloubku, ne ji celou spotřebovat.**

---

## 3. Kanonická struktura Briefu

Struktura je redakční kontrakt, nikoli volná inspirace:

1. **Dnes v kostce**
2. **Co stojí za přečtení**
3. **Další důležité změny**
4. **Ještě stojí za pozornost**
5. **Signály**
6. **Co sledovat dál**

Ne každá sekce musí být každý den naplněná.

Nová sekce se nevytváří jen proto, že některé texty nezapadají do zbytku.

Zvlášť:
- „Analýzy“ nejsou odkladiště delších textů ze zdrojů;
- vlastní Analýza Business Briefu je samostatný produkt nad Memory.

---

## 4. Master Brief a distribuční kanály

Editorial Workflow nevyrábí přímo newsletter ani audio skript.

Nejprve vzniká jeden **Master Brief**.

Master Brief je kanonický redakční obraz dne:
- co je důležité;
- jaká je hierarchie;
- jaké jsou pointy;
- co je coverage;
- co je curated;
- jaké jsou signály;
- co sledujeme dál;
- jaké jsou ověřené claims;
- kde je legitimní cesta do Detailu.

Teprve po schválení Master Briefu vznikají kanálové adaptace:

~~~text
NEWSROOM
Issue Maps → Cross-Paper Topics → Selective Deep Read

EDITORIAL
Assignment
→ Dramaturgy
→ Story
→ Writing
→ Detail Gap
→ Verification
→ Language & Style
→ Editor-in-Chief
→ MASTER BRIEF

PUBLISHING
MASTER BRIEF
├→ Web Editor   → Web Brief
├→ Email Editor → Email Brief
└→ Audio Editor → Voice Script
                   ↓
               Channel QA
                   ↓
                 Publish
~~~

Zásada:

> **Web, e-mail a audio mají jednu redakční pravdu, ale tři různé způsoby podání.**

Kanál nesmí vytvořit jinou hierarchii dne, jinou míru jistoty ani nový faktický obsah bez návratu do redakční vrstvy.

---

## 5. Co jednotlivé role nesmějí dělat

### Source truth invariant

Fakt se může:
- zkrátit;
- přesunout;
- stylisticky přeformulovat.

Nesmí:
- změnit význam;
- změnit míru jistoty;
- proměnit možnost v rozhodnutí;
- proměnit scénář v prognózu;
- proměnit komentář ve fakt.

### Responsibility invariant

Každý průchod řeší jen svou vrstvu.

Například:
- Language & Style Editor znovu nevybírá témata;
- Verification Editor nepřestavuje celé pořadí;
- Brief Writer svévolně nemění form factor;
- Audio Editor nevytváří nový redakční závěr.

### Curiosity invariant

Zájem může vzniknout z:
- konfliktu;
- překvapivého čísla;
- paradoxu;
- širšího dopadu;
- neuzavřeného rozhodnutí;
- vztahu mezi několika články;
- další vrstvy důkazů.

Nesmí vzniknout zatajením hlavního faktu.

---

# PART B — MASTER EDITORIAL WORKFLOW

## 6. PASS 1 — Assignment Editor

### Purpose

Rozhodnout:

> **Co dnes patří do vydání a kolik prostoru si to zaslouží?**

Assignment Editor je první role, která přestává uvažovat v logice „INCLUDE / RESERVE“ a začíná uvažovat v logice skutečného produktu.

### Input

Vidí:
- všechny `daily_topics`, nejen INCLUDE;
- INCLUDE / RESERVE / EXCLUDE;
- `daily_delta`;
- `importance_reason`;
- source coverage;
- Deep Read summary, pokud existuje;
- uncertainties;
- informaci, zda je téma single-source nebo cross-paper.

Nevidí hotový Brief v1 při prvním čistém průchodu Day 1 v2, pokud to není nutné. Cílem je snížit anchoring na starou kompozici.

### Povinný postup

Pro každé téma položit postupně:

#### Q1 — Bez tohoto tématu bude obraz dne zkreslený?

Pokud ano:
- kandidát na `lead`, `secondary` nebo alespoň `coverage`.

#### Q2 — Potřebuje čtenář vysvětlení, nebo stačí vědět, že se to stalo?

Pokud potřebuje mechanismus, konflikt nebo význam:
- `lead` / `secondary`.

Pokud stačí 1–2 věty:
- `coverage`.

#### Q3 — Je to skvělý text, ale ne událost definující den?

Pokud ano:
- `curated`.

`curated` není odkladiště méně důležitých zpráv. Je to explicitní doporučení k četbě.

Reading value může vznikat například z:
- originálního argumentu;
- nečekaného úhlu;
- reportérské práce;
- objevnosti;
- kvalitního vysvětlení;
- silné interpretace;
- mimořádně užitečného profesního nebo sektorového pohledu.

Důležitost události a hodnota textu k přečtení se posuzují odděleně.

#### Q4 — Je to dnešní důkaz širší změny?

Pokud ano:
- může být zároveň `signal`.

#### Q5 — Má příběh konkrétní neznámou nebo trigger?

Pokud ano:
- může být zároveň `watch`.

#### Q6 — Ztratí čtenář něco podstatného, pokud téma úplně zmizí?

Pokud ne:
- `drop`.

### Povolené editorial roles

- `topline`
- `lead`
- `secondary`
- `coverage`
- `curated`
- `signal`
- `watch`
- `drop`

Jedno téma může mít jednu hlavní roli a případně jednu doplňkovou, například `lead + watch`.

### Tvrdá pravidla

- INCLUDE ≠ lead.
- RESERVE ≠ drop.
- Počet zdrojů není automatická míra důležitosti.
- Výjimečný single-source článek může být lead.
- Shoda všech tří titulů může zvyšovat confidence, ale sama nevytváří význam.
- Coverage je legitimní finální forma, ne „prohra“ tématu.
- „Je to zajímavé“ samo o sobě nestačí.

### Výstupní kontrakt

Pro každý topic:

~~~text
topic_id:
working_title:
editorial_role:
secondary_role:
target_section:
target_form:
target_length:
why_now:
why_this_size:
merge_candidate:
detail_candidate:
notes:
~~~

`target_form` typicky:
- one_sentence
- two_sentence
- short_block
- lead_block
- curated_note
- signal
- watch_item

### PASS gate

PASS pokud:
- všechny relevantní topics mají explicitní roli;
- žádné INCLUDE není automaticky lead bez důvodu;
- žádné RESERVE nezmizelo bez vědomého rozhodnutí;
- existuje jasně rozlišitelná horní hierarchie;
- coverage chrání „minimum pro informovanost“.

REVISION pokud:
- více než přibližně 5–6 témat působí jako stejně velké leady;
- role byly přiděleny podle zdrojového prestiže místo významu;
- velká část RESERVE byla mechanicky dropnuta;
- není jasné, co má být čtenářova mapa dne.

### Day 1 v2 focus

Zvlášť znovu posoudit:
- zda dluhopisy + ECB mají zůstat dvě témata;
- které z 11 RESERVE mají dostat coverage;
- zda Le Pen / CDU potřebují plné bloky;
- které „analytické“ texty jsou spíš `curated`.

---

## 7. PASS 2 — Dramaturg

### Purpose

Rozhodnout:

> **Jak má vydání téct jako celek?**

Dramaturg neřeší znovu „je téma důležité?“. Řeší:
- pořadí;
- kontrast;
- rytmus;
- spojování;
- gradaci;
- čitelnost;
- poslouchatelnost.

### Input

Vidí:
- `editorial_selection_v1`;
- názvy a krátké charakteristiky témat;
- případné merge candidates;
- základní source provenance.

Nemá důvod vracet se do všech raw článků.

### Povinný postup

#### Krok A — Urči 3–5 vrcholů dne

Ty musí být rozeznatelné i bez čtení celého Briefu.

#### Krok B — Odstraň falešné dvojice

Pokud dvě položky vysvětlují tentýž ekonomický mechanismus, zvaž:
- merge;
- lead + inset;
- lead + coverage;
- lead + watch.

#### Krok C — Navrhni rytmus

Střídej podle potřeby:
- makro / firma / geopolitika / technologie;
- dlouhé / krátké;
- těžké / lehčí;
- faktické / kurátorské.

Ne mechanicky. Cílem je zabránit monotónnímu bloku stejných typů textu.

#### Krok D — Ověř začátek

První třetina musí nést nejsilnější hodnotu vydání.

Nesmí být potřeba čekat do poloviny textu, než přijde skutečný vrchol.

#### Krok E — Ověř konec

Konec nemá „dojet“. Má uzavřít den:
- signály;
- watchlist;
- konkrétní trigger;
- pocit, že čtenář ví, co sledovat.

### Tvrdá pravidla

- Délka je nositelem hierarchie.
- Pořadí je nositelem hierarchie.
- Stejná délka 13 položek je implicitní tvrzení, že všech 13 je stejně důležitých.
- Merge nesmí vymazat odlišný význam.
- Audio test začíná už zde: vydání musí mít slyšitelný rytmus.

### Výstupní kontrakt

~~~text
master_order:
  1:
  2:
  ...

section_plan:
  dnes_v_kostce:
  co_stoji_za_precteni:
  dalsi_dulezite_zmeny:
  jeste_stoji_za_pozornost:
  signaly:
  co_sledovat_dal:

merge_plan:
rhythm_notes:
opening_logic:
closing_logic:
audio_risk_notes:
~~~

### PASS gate

PASS pokud:
- 3–5 vrcholů je zřetelných;
- Brief není řada rovnocenných bloků;
- sekce mají rozdílnou funkci;
- opakující se témata byla vědomě spojena nebo ponechána odděleně z důvodu;
- pořadí lze obhájit jednou větou.

REVISION pokud:
- „Co stojí za přečtení“ je jen seznam všeho důležitého;
- první polovina je rytmicky monotónní;
- stejné téma se vrací bez nové funkce;
- konec nemá žádný watch / signal rozměr.

---

## 8. PASS 3 — Story Editor

### Purpose

Najít pro každou hlavní položku:

> **Pointu, napětí a legitimní důvod jít do Detailu.**

Toto je klíčový anti-boredom pass.

### Input

Vidí:
- schválenou hierarchii;
- daily topic;
- Deep Read;
- source contributions;
- uncertainty notes.

### Povinná Story Card

Pro každý `lead` a `secondary`:

#### FACT

Jedna věta bez ozdob:

> Co se stalo?

#### ANGLE

Jedna věta:

> Proč je to zajímavější nebo důležitější, než napovídá samotný fakt?

#### TENSION

Jedna věta:

> Co je neuzavřené, překvapivé, konfliktní nebo paradoxní?

Pokud příběh žádné skutečné napětí nemá, nevymýšlet ho.

#### DETAIL VALUE

Jedna věta:

> Co konkrétně zůstane pro Detail?

Musí jít o reálnou hodnotu, například:
- čísla;
- argumentaci;
- scénáře;
- konkrétní opatření;
- jednotlivé source differences;
- časovou osu;
- mechanismus;
- evidence;
- Memory context.

#### OPENING CANDIDATE

Jedna navržená vstupní věta.

Může začít:
- číslem;
- konfliktem;
- důsledkem;
- obrazem;
- paradoxem;
- otázkou;
- samotným faktem.

#### DON'T OVERSTATE

Explicitní brzda.

Například:
- „8 milionů je interní scénář, ne forecast.“
- „Další hike ECB není rozhodnutý.“
- „Návrh není schválená regulace.“

### Curiosity test

Po Story Card položit:

> Kdybych čtenáři sdělil pouze FACT + ANGLE, ví dost na orientaci, ale zůstává mu smysluplný důvod otevřít Detail?

Pokud ne:
- buď téma nemá Detail value;
- nebo jsme už do Briefu nacpali příliš mnoho.

### Tvrdá pravidla

- Tension se nevyrábí uměle.
- Otazník není náhrada za úhel.
- „Co to znamená pro firmy?“ není automatický angle.
- Detail promise nesmí být „více informací“.
- Pokud neumíme pojmenovat konkrétní přidanou hodnotu Detailu, Detail není produktově připravený.

### Výstupní kontrakt

~~~text
topic_id:
fact:
angle:
tension:
detail_value:
opening_candidate:
dont_overstate:
source_specific_value:
~~~

### PASS gate

PASS pokud:
- každý lead má jasně jinou pointu než pouhé summary;
- Detail value je konkrétní;
- curiosity nevzniká zatajením faktu;
- uncertainty je explicitně zachována.

REVISION pokud:
- angle pouze parafrázuje fact;
- tension je marketingová;
- Detail promise je vágní;
- Story Card obsahuje tvrzení, které Deep Read nepodporuje.

---

## 9. PASS 4 — Brief Writer

### Purpose

Napsat první **Master Brief draft**, nikoli newsletter a nikoli voice script.

### Input

Vidí:
- editorial selection;
- dramaturgy plan;
- Story Cards;
- ověřené Deep Read podklady;
- PRODUCT_MODEL structure.

Nemá volnost znovu přidělit hierarchii.

### Writing principles

#### Dnes v kostce

- 3–5 konkrétních posunů;
- každý bod musí být informace;
- bez obecných štítků typu „AI zůstává tématem dne“;
- čtenář, který skončí zde, musí stále dostat hodnotu.

#### Co stojí za přečtení

V současném experimentu jde funkčně o **hlavní syntetickou vrstvu dne**, nikoli automaticky o seznam originálních článků, které má čtenář otevřít.

- jen skutečné leady;
- přibližně 350–600 znaků jako orientační rámec, ne mechanický limit;
- pointa před úplností;
- použít rozdílné vstupy do příběhu;
- cross-paper syntéza má ukázat, co zdroje přinášejí navíc, ne pouze sečíst fakta;
- hlavní zprávu má Brief pokud možno vysvětlit tak dobře, aby kvůli základní orientaci nebylo nutné číst několik paralelních originálů.

#### Další důležité změny

- 1–2 věty;
- jedna změna + případně jedna věta významu;
- žádný mini-esej.

#### Ještě stojí za pozornost

Toto je **vrstva doporučeného čtení**.

- doporučit konkrétní text a říct, proč stojí za skutečný čas čtenáře;
- může být méně „news“, více „worth your time“;
- nevybírat pouze podle důležitosti události;
- preferovat texty s originálním argumentem, nečekaným úhlem, silnou reportérskou prací, objevností nebo mimořádně užitečnou interpretací;
- položka má čtenáře inspirovat k otevření originálu nebo Detailu, nikoli pouze doplnit coverage;
- sekce nesmí působit jako druhý news feed ani jako koš na zbylé RESERVE.

#### Signály

- dnešní nový důkaz;
- vztah k širšímu směru;
- neprohlašovat jeden signál za trend.

#### Co sledovat dál

Každá položka ideálně:
- known;
- unknown;
- trigger.

### Voice of the Master Brief

Má působit jako:
- inteligentní editor;
- ekonomicky gramotný;
- stručný;
- konkrétní;
- zvědavý;
- střízlivý.

Nemá působit jako:
- školní referát;
- consulting memo;
- marketing;
- databázový export;
- sada třinácti stejných summaries.

### Anti-patterns

Hlídá zejména opakování:
- „Pro management je důležité...“
- „Pro firmy je podstatné...“
- „Jde tedy o...“
- „Z toho vyplývá...“

Tyto formulace nejsou zakázané jednotlivě. Zakázaný je monotónní vzorec.

### Výstupní kontrakt

`master_brief_draft_v1.md`

Musí používat přesně kanonické sekce.

U každé lead položky interně zachovat vazbu na:
- topic_id;
- Detail candidate;
- source provenance.

### PASS gate

PASS pokud:
- text lze přečíst od začátku jako jeden celek;
- je vidět hierarchie;
- leady nepůsobí jako miničlánky se stejnou kadencí;
- coverage je skutečně krátké;
- úvodní sekce funguje i samostatně;
- žádná sekce nevznikla mimo PRODUCT_MODEL jen kvůli zbytkům.

REVISION pokud:
- Writer nafoukl coverage;
- leady mají všechny stejný rytmus;
- text uzavírá všechny otázky a Detail nemá co nabídnout;
- Writer přidal nové, neověřené claims.

---

## 10. PASS 5 — Detail Editor

### Purpose

Ověřit:

> **Je Brief plnohodnotný, ale zároveň nesežral Detail?**

### Input

Vidí:
- Master Brief draft;
- Story Cards;
- Deep Read;
- plánovanou hodnotu Detailu.

### Povinný test pro každý lead

#### Test 1 — Orientace

Po přečtení Briefu:
- vím co se stalo?
- vím proč je to důležité?

Pokud ne:
- FAIL, Brief je teaser.

#### Test 2 — Další hodnota

Zůstává po přečtení alespoň jedna konkrétní vrstva:
- evidence;
- scénář;
- rozpad čísel;
- celý mechanismus;
- argumentace;
- source differences;
- timeline;
- context?

Pokud ne:
- Detail value = weak.

#### Test 3 — Neoprávněné zatajování

Byl odstraněn klíčový fakt jen kvůli kliknutí?

Pokud ano:
- FAIL.

### Povolené zásahy

Může doporučit:
- odstranit vedlejší čísla;
- odstranit druhý nebo třetí příklad;
- zkrátit mechanismus;
- ponechat v Briefu pointu a přesunout důkazní hloubku do Detailu;
- zpřesnit poslední větu tak, aby otevřela skutečnou otázku.

### Výstupní kontrakt

Pro každý lead:

~~~text
topic_id:
orientation_complete: yes/no
detail_value: strong/sufficient/weak
what_remains_for_detail:
what_to_remove_from_brief:
what_must_stay_in_brief:
revision_required: yes/no
~~~

### PASS gate

Celý Brief PASS pokud:
- žádný lead není clickbaitový teaser;
- většina leadů má strong nebo sufficient Detail value;
- weak Detail value je vědomý stav, ne přehlédnutí;
- zkrácením se neztratila orientace.

---

## 11. PASS 6 — Verification Editor

### Purpose

Ověřit celý text **po zkrácení a přepsání**, protože právě editace může nenápadně změnit význam.

### Input

Vidí:
- Master Brief po Detail Review;
- Deep Read;
- provenance;
- uncertainty notes;
- případný dated external verification použitý během Deep Read.

### Claim-level checklist

U každého významného tvrzení:

1. Je podloženo?
2. Je správně přiřazeno zdroji?
3. Je časově ukotveno?
4. Nezměnila formulace míru jistoty?
5. Nezaměnili jsme návrh, scénář, očekávání, rozhodnutí a fakt?
6. Neudělali jsme z komentáře zdroje vlastní tvrzení?
7. Pokud jde o syntézu, je zřetelné, že je to naše redakční syntéza?

### High-risk categories

Zvýšená pozornost:
- čísla;
- procenta;
- měnová politika;
- interní firemní scénáře;
- politika a volby;
- konflikty a bezpečnost;
- právní/regulatorní návrhy;
- kauzalita;
- predikce.

### Výstupní kontrakt

Pro každou položku:
- checked
- needs_revision
- blocked

A stručně:
- claim;
- issue;
- required correction.

### PASS gate

PASS pouze pokud:
- žádný významný claim není blocked;
- needs_revision bylo opraveno;
- source note / provenance lze dohledat.

Verification Editor nesmí vrátit do textu zbytečné detaily jen proto, že byly ověřené.

---

## 12. PASS 7 — Language & Style Editor

### Naming note

V `EDITORIAL_WORKFLOW.md` je tato role zatím označena jako **Language & Voice Editor**.

V Playbooku používáme pracovní označení **Language & Style Editor**, protože skutečná audio adaptace patří až do Publishing vrstvy.

Po experimentu se může kanonický název sjednotit.

### Purpose

Ověřit:

> **Zní Master Brief živě, přirozeně a konzistentně, aniž by stylistická úprava změnila význam?**

### Input

Vidí:
- verified Master Brief;
- nemusí znovu číst raw source;
- uncertainty flags pouze pro ochranu významu.

### Kontroluje

- opakované konstrukce;
- příliš dlouhé věty;
- přetížené odstavce;
- abstraktní substantiva;
- korporátní vatu;
- titulky;
- přechody;
- rytmus;
- čitelnost nahlas.

### Voice guide v1

Preferovat:
- konkrétní podstatná jména a slovesa;
- aktivní věty;
- přirozenou češtinu;
- přesná čísla jen tam, kde nesou pointu;
- kontrast;
- krátkou větu po dlouhé;
- občasný obraz, pokud vychází z faktů;
- přímé pojmenování nejistoty.

Omezovat:
- „v kontextu“;
- „z hlediska“;
- „v rámci“;
- „pro management“;
- „pro firmy“;
- „lze očekávat“ bez zdroje;
- mechanický závěr každého odstavce typu „to je důležité, protože...“.

### Read-aloud test

Každý lead se jednou posoudí jako mluvený text:
- nezakopává jazyk?
- nejsou za sebou tři čísla?
- neopakuje stejnou melodii jako předchozí blok?
- je pointa slyšitelná?

Nejde ještě o voice script. Jde o kontrolu, zda master copy není mrtvé na papíře.

### Výstup

`master_brief_language_edited_v1.md`

A stručné poznámky:
- major rewrites;
- repeated patterns removed;
- unresolved style risks.

### PASS gate

PASS pokud:
- text nemá dominantní opakující se šablonu;
- titulky nejsou všechny stejného typu;
- význam se nezměnil;
- text jde přirozeně číst nahlas;
- styl nepřekročil hranici do clickbaitu.

---

## 13. PASS 8 — Editor-in-Chief

### Purpose

Rozhodnout:

> **Je toto skutečně dnešní Business Brief?**

### Input

Dostane pouze téměř finální Master Brief + velmi stručné metadata o coverage.

Ideálně nevidí celou historii všech mikroúprav, aby mohl simulovat čtenáře.

### Finální gate A — Coverage

- chybí nějaká důležitá oblast dne?
- nezmizela důležitá RESERVE položka jen proto, že nebyla lead?
- funguje coverage safety net?

### Finální gate B — Hierarchy

Do 30–90 sekund:
- je jasné, co je dnes opravdu hlavní?
- jsou 3–5 vrcholů rozeznatelné?

### Finální gate C — Curiosity

U hlavních textů:
- mám přirozenou chuť otevřít některý Detail?
- je tato chuť založena na skutečné další hodnotě?

### Finální gate D — Trust

- nepůsobí text jistěji než evidence?
- jsou nejistoty tam, kde jsou důležité?

### Finální gate E — Product fit

- odpovídá struktura PRODUCT_MODEL?
- neproměnil se Brief v obecný news digest?
- necpe se vlastní Analýza tam, kde máme jen shrnutí cizího textu?
- funguje „světový tisk na vašem stole“?

### Povolené zásahy

Editor-in-Chief může:
- škrtat;
- přesunout;
- zkrátit;
- spojit;
- vrátit konkrétní položku na konkrétní pass.

Nemá bez důvodu restartovat celé vydání.

### Výstup

`MASTER_BRIEF_VERIFIED`

Teprve tento stav otevírá Publishing Workflow.

---

# PART C — CHANNEL PRODUCTION WORKFLOW

## 14. Zásada channel adaptation

Publishing není copy-paste.

Každý kanál smí:
- měnit délku;
- měnit syntax;
- měnit přechody;
- měnit prezentaci.

Nesmí:
- změnit hierarchy truth;
- změnit factual truth;
- vytvořit nové claims;
- posunout míru jistoty;
- vytvořit nový „hlavní příběh dne“ bez návratu k Editor-in-Chief.

---

## 15. Web Editor

### Role webu

Web je nejúplnější veřejná podoba ranního vydání.

Je to **titulní strana dne**, ne dashboard.

### Input

- MASTER_BRIEF_VERIFIED;
- topic ids;
- Detail availability;
- source links/provenance;
- případné vizuální assety.

### Web může přidat

- typografickou hierarchii;
- velikostní rozdíly;
- Detail CTA;
- source link;
- vizuál;
- graf;
- related thread;
- Memory context box, pokud je redakčně schválený.

### Web nesmí

- prodlužovat každý text jen proto, že má prostor;
- proměnit homepage v feed karet;
- skrýt základní coverage pouze do kliků;
- přidávat neověřený kontext.

### Výstup

`web_brief_v1`

---

## 16. Email Editor

### Role e-mailu

E-mail je **rychlejší ranní vstup do vydání**.

Není to zmenšený web ani dump Master Briefu.

### Input

- MASTER_BRIEF_VERIFIED;
- web hierarchy;
- Detail links.

### E-mail typicky

- zachová Dnes v kostce;
- zachová 3–5 nejsilnějších příběhů;
- zkrátí coverage;
- z curated udělá krátká doporučení;
- může část méně zásadního coverage přesunout na web;
- používá odkazy do Detailu nebo webového vydání.

### Zásada

Čtenář e-mailu musí dostat základní orientaci i bez kliknutí.

Ale nemusí dostat každý odstavec webové verze.

### Email Editor nesmí

- změnit redakční pořadí bez důvodu;
- nafukovat teaser language;
- zamlčet hlavní fakt kvůli CTR;
- vytvářet jiný tón než Business Brief.

### Výstup

`email_brief_v1`

---

## 17. Audio Editor

### Role audio

Audio není TTS newsletteru.

Je to **mluvená redakční adaptace stejného vydání**.

Má působit jako editor, který posluchače provádí dnešním tiskem.

### Input

- MASTER_BRIEF_VERIFIED;
- hierarchy;
- Story Cards;
- pronunciation notes / names;
- Detail priorities.

### Audio Editor smí

- spojovat krátké bloky;
- přidávat přechody;
- převádět titulky do přirozených vět;
- zjednodušit číselné pasáže;
- zopakovat klíčový kontext, pokud je to při poslechu nutné;
- mírně změnit lokální pořadí uvnitř schválené dramaturgie kvůli přirozenému toku;
- přidat orientační věty typu „Začněme ropou“ nebo „Teď jedna věc, která s tím na první pohled nesouvisí“.

### Audio Editor nesmí

- změnit význam;
- přidat nový fact;
- přehnat dramatizaci;
- vytvořit „moderátorský názor“;
- mechanicky číst source ids nebo webové UX prvky.

### Voice script principles v1

- kratší věty;
- méně čísel v jedné větě;
- slyšitelné přechody;
- rytmická variabilita;
- každých několik minut znovu ukotvit posluchače;
- názvy a zkratky připravit pro správnou výslovnost;
- odkazy do Detailu formulovat přirozeně, ne jako webová CTA.

### Výstup

`audio_script_v1`

---

## 18. Channel QA

Každý kanál musí projít lehkým QA.

### Factual parity

- stejná factual truth jako Master Brief;
- žádný nový claim;
- stejná míra jistoty.

### Hierarchy parity

- nejdůležitější příběhy zůstávají nejdůležitější;
- zkrácení kanálu nesmí převrátit význam dne.

### Product parity

- Brief zůstává hodnotný i bez kliknutí;
- Detail zůstává skutečná hloubka;
- žádný kanál nepoužívá clickbait.

### Channel fit

- web: scan + depth;
- e-mail: rychlost + návrat na web;
- audio: flow + poslouchatelnost.

---

# PART D — DAY 1 → BRIEF V2 PROTOKOL

## 19. Cíl prvního Playbook testu

Day 1 v1 je baseline.

Day 1 v2 se vytvoří:
- ze stejných 24 daily_topics;
- ze stejných Deep Read podkladů;
- ze stejné source provenance;
- bez nového research;
- bez přidání nových externích zdrojů;
- bez změny issue maps.

Testujeme jedinou proměnnou:

> **Co udělá lepší editorství se stejným informačním materiálem?**

---

## 20. Povinné stop points pro první test

Při prvním průchodu Playbookem nepoběží osm rolí skrytě jako jedna operace.

Po každém z prvních klíčových průchodů se uloží artifact.

Pro Day 1 v2:

1. `editorial_selection_v1`
2. `dramaturgy_plan_v1`
3. `story_angles_v1`
4. `master_brief_draft_v1`
5. `detail_gap_review_v1`
6. `verification_review_v1`
7. `master_brief_language_edited_v1`
8. `MASTER_BRIEF_VERIFIED`

Teprve potom:
9. `web_brief_v1`
10. `email_brief_v1`
11. `audio_script_v1`

Pro první test je vhodné po Assignment, Dramaturgy a Story passu výstup lidsky zkontrolovat, protože právě zde se rodí největší redakční rozhodnutí.

---

## 21. Co se v Day 1 v2 nesmí měnit

- žádné nové téma mimo existujících 24 daily_topics;
- žádný nový Deep Read;
- žádný nový web research;
- žádná změna source map;
- žádné zpětné přepsání Day 1 v1;
- žádná změna databázových contracts kvůli stylistickému experimentu.

---

## 22. Co budeme po v2 porovnávat s v1

Ne jeden syntetický score.

Budeme se ptát:

### Hierarchy
- Je okamžitě jasnější, co je hlavní?

### Coverage
- Ví čtenář o více důležitých změnách, i když je Brief kratší?

### Rhythm
- Má text různé tempo a formy?

### Curiosity
- Chci otevřít alespoň některé Detaily?

### Reading inspiration
- Ukázal mi Brief alespoň několik textů, které bych chtěl skutečně číst, i když nepatří k největším zprávám dne?
- Je zřejmé, proč jsou tyto texty hodnotné jako texty, ne jen jako nosiče další informace?

### Trust
- Zůstala přesnost a správná míra jistoty?

### Economy
- Ubylo textu, který nepřidává orientaci ani zvědavost?

### Channel readiness
- Dá se Master Brief přirozeně převést na web, email i audio bez toho, aby se musel redakčně stavět znovu?

---

# PART E — UČENÍ A VERZOVÁNÍ PLAYBOOKU

## 23. Jak Playbook měnit

Po každém dni lze zapisovat:
- rule worked;
- rule unclear;
- rule caused over-editing;
- missing rule;
- role overlap;
- unnecessary pass;
- channel conflict.

Pravidlo se stává pevnější součástí Playbooku až tehdy, když:
- řeší opakující se problém;
- nebo chrání kritickou produktovou hranici, například fakta vs. teaser.

---

## 24. Co zatím neautomatizujeme

Playbook v1 **neříká**, že:
- každá role dostane vlastního agenta;
- každý pass bude samostatný API call;
- vznikne nová tabulka pro každý artifact;
- všechny kanálové varianty budou generovány automaticky.

Nejdřív ověřujeme redakční logiku.

Teprve pak řešíme orchestration.

---

## 25. Nejkratší pracovní mantra

### Master Editorial

> **Vyber. Seřaď. Najdi pointu. Napiš. Nevyčerpej. Ověř. Oživ. Schval.**

### Publishing

> **Jedna redakční pravda. Tři různé způsoby vyprávění.**
