# Audio — Business Brief v4

**Status:** PRODUCT DECISION; IMPLEMENTATION UNDER EXPLORATION  
**Purpose:** definice audio kanálu bez předčasného uzamčení konkrétní TTS technologie

## 1. Role audia

Audio je plnohodnotná ranní forma Business Briefu, ne mechanicky přečtený web nebo e-mail.

Kanonická redakční pravda vzniká v Master Briefu. Audio Adapter ji převádí do přirozené mluvené češtiny bez změny faktů, hierarchie dne, perspektivy ani míry jistoty.

**Master Brief → Audio Adapter → Audio Script → TTS / Voice Engine → Audio QA → Publication**

## 2. Audio Adapter

Smí upravit:
- syntaxi pro poslech;
- délku vět a přechody;
- interpunkci a pauzy;
- čtení čísel, měn, procent a zkratek;
- výslovnost jmen, firem a cizojazyčných pojmů;
- jemné orientační věty pro posluchače.

Nesmí:
- přidávat nové informace;
- měnit argument;
- měnit pořadí a významovou hierarchii bez redakčního důvodu;
- zesilovat jistotu;
- vytvářet jinou redakční verzi dne.

## 3. Hlas jako součást značky

Cílem není používat generický katalogový hlas. Business Brief má mít dlouhodobě **originální, rozpoznatelný hlas**, který se stane součástí značky.

Pracovní charakter:
- český, přirozený, kultivovaný;
- klidný a inteligentní, ne autoritativní;
- lehce hlubší, ale ne „hlas večerních zpráv“;
- mluví jednomu člověku, ne davu;
- zvládá jemnou zvědavost, otázku a lehký humor;
- neunavuje při 8–15 minutách poslechu;
- jistě zvládá anglická a německá jména v české větě.

Preferovaný model značky je jeden konzistentní hlas, nikoli umělé „AI rádio“ s více moderátory.

## 4. Voice identity test

Kandidátní hlasy se mají porovnávat na stejném testovacím textu a hodnotit minimálně podle:
- přirozenosti češtiny;
- důvěryhodnosti;
- únavy po 10 minutách;
- práce s otázkou a změnou rytmu;
- čtení čísel;
- anglických a německých jmen;
- schopnosti jemného humoru;
- konzistence;
- pocitu člověka vs. syntetického hlasu.

Nejdůležitější není první dojem, ale dlouhodobá poslouchatelnost.

## 5. Pronunciation layer

Business Brief potřebuje vlastní pronunciation dictionary / lexikon výslovnosti pro:
- osoby;
- firmy;
- instituce;
- německé a anglické názvy;
- zkratky;
- finanční a technologické termíny.

Audio preprocessing má převádět zápis do mluvené podoby tam, kde by TTS četlo nepřirozeně.

## 6. Segmentace

Preferovaný směr je generovat audio po logických redakčních segmentech a teprve potom skládat finální soubor.

Důvody:
- levnější a rychlejší opravy;
- retry pouze vadné části;
- cache;
- kapitoly / seek points;
- snazší QA;
- lepší observability.

Segmentace nesmí způsobit slyšitelné změny hlasu, hlasitosti nebo rytmu mezi částmi.

## 7. Technologie

ElevenLabs API je silný kandidát pro první produkční cestu, ale **není zatím kanonicky zvoleným vendor lockem**. Paralelně se ověřuje řešení přes Codex.

Rozhodnutí se má řídit kvalitou češtiny, originalitou hlasu, stabilitou API, latencí, cenou, licencí hlasu, možností pronunciation control a provozní spolehlivostí.

## 8. Produkční cíl

Audio má být součástí stejného autonomního ranního cyklu jako web/e-mail. Nemá vyžadovat každodenní ruční namlouvání ani manuální Publish.

Audio QA musí umět zastavit pouze audio kanál, aniž by nutně blokovalo již ověřený textový Brief, pokud chyba není ve společném Master Briefu.
