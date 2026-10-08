# Autonomous Morning & Operations Dashboard — Business Brief v4

**Status:** CANONICAL OPERATIONAL DIRECTION  
**Purpose:** bezpečná ranní výroba bez přítomnosti člověka

## 1. Provozní realita

Ranní vydání musí vznikat v době, kdy šéfredaktor nemusí být dostupný. Produkční systém proto nesmí být pouze automatizovaný nástroj pro člověka. Cílem je **autonomní ranní redakce s lidskou kontrolou nad pravidly, auditem a výjimkami**.

Pracovní cíl:
- **TARGET publication: 08:35 Europe/Prague**
- **SLA: 08:45 Europe/Prague**

Časy jsou produktový cíl, ne zatím garantovaná veřejná SLA.

## 2. Zdrojový rytmus

FT a Handelsblatt se mají zpracovávat co nejdříve po dostupnosti Reference Edition.

WSJ je poslední kritický vstup, nikoli start celé pipeline. Pracovní pozorování je, že oficiální ranní elektronické vydání bývá dostupné několik minut po 08:00 českého času. Tento čas je nutné dále měřit a nesmí být natvrdo zakódován jako neověřitelný předpoklad.

Po příchodu WSJ se doplní společná mapa dne, cross-paper reconciliation a finální redakční práce.

## 3. Zásada autonomie

> **Automatizovat publikaci neznamená publikovat za každou cenu.**

Systém musí umět:
- dokončit zdravé vydání bez člověka;
- rozpoznat neúplný nebo podezřelý vstup;
- retry / self-heal;
- degradovat pouze tam, kde je to předem povoleno;
- zastavit publication gate při kritické nejistotě;
- vysvětlit člověku, co se stalo.

## 4. Publication Gate

Před publikací musí být explicitní stav READY / BLOCKED.

Minimální gate dimensions:
- Sources / Reference Editions;
- Coverage;
- Provenance;
- Editorial artifacts;
- Verification;
- unresolved critical issues;
- channel-specific QA.

Výsledek musí být auditovatelný. Žádný kritický gate nesmí být skrytý v promptu jednoho modelu.

## 5. Dashboard

Dashboard je provozní součást produktu.

Horní pohled má během několika sekund odpovědět:
- běží dnešní vydání?
- jsme ON TRACK / AT RISK / BLOCKED?
- kde přesně pipeline je?
- co čeká na vstup?
- co selhalo?
- co systém právě dělá pro nápravu?
- jaký je odhad vůči TARGET / SLA?

Preferovaná jednoduchá stavová řeč:
- ⚪ not started / waiting;
- 🟡 running;
- 🟢 completed + passed;
- 🔴 blocked / human attention required.

## 6. Zdroje na dashboardu

Každý hlavní zdroj samostatně:
- detected / acquired time;
- Reference Edition identity;
- page/article counts;
- extraction / mapping coverage;
- QA result;
- retries;
- link na Issue Map / Article Records.

## 7. Redakční pipeline na dashboardu

Dashboard má ukázat tok například:

**FT → HB → WSJ → Issue Map → Selection → Deep Read → Master Brief → Verify → Channel Adaptation → Publish**

Konkrétní kroky se musí řídit kanonickým EDITORIAL_WORKFLOW, nikoli tímto ilustrativním seznamem.

U každého kroku:
- start/end;
- duration;
- status;
- artifact;
- model/runtime pokud relevantní;
- cost pokud relevantní;
- failure / retry;
- human override.

## 8. Alert policy

**Green stays on dashboard. Phone is for exceptions.**

Běžný úspěch nemá vytvářet push hluk.

Úrovně:
1. INFO — pouze event log;
2. WARNING — dashboard, systém se pokouší opravit sám;
3. CRITICAL — tvrdý alert na telefon, pokud je ohrožen deadline, integrita nebo publikace.

Critical alert má obsahovat:
- co selhalo;
- dopad;
- co systém zkusil;
- aktuální recovery action;
- zda je publication blocked;
- čas do SLA.

## 9. Emergency actions

Budoucí mobilní rozhraní může nabídnout rychlé explicitní zásahy, např.:
- DELAY;
- ABORT;
- povolený degraded publish.

Publikace bez některého ze základních zdrojů nesmí vzniknout tichým automatickým fallbackem. Musí být buď předem schválenou politikou, nebo explicitním lidským rozhodnutím.

## 10. Event Log & observability

Každý významný krok má zapisovat událost. Dlouhodobě chceme měřit:
- arrival time zdrojů;
- processing durations;
- retry rates;
- failure modes;
- model/API costs;
- coverage;
- počet lidských zásahů;
- publication time;
- podíl autonomně dokončených vydání.

Cílem je po týdnech znát skutečný provoz, ne ho odhadovat pocitem.

## 11. Role člověka

Šéfredaktor nemá být každodenní operátor pipeline. Jeho role:
- definovat redakční a bezpečnostní pravidla;
- vyhodnocovat vydání;
- měnit workflow na základě chyb;
- řešit skutečné výjimky;
- držet konečnou odpovědnost.

Autonomie se získává prokázanou spolehlivostí, nikoli deklarací.
