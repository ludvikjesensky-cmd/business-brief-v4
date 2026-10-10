# Memory — role ve v4

**Status:** PRODUCT PRINCIPLE; TECHNICAL DESIGN DEFERRED

## 1. Úloha

Memory je dlouhodobá paměť Business Briefu. Uchovává vztahy mezi články, tématy, argumenty, firmami, lidmi, událostmi, čísly, postoji a změnami v čase.

Je důležitá, ale nesmí se stát motorem, který ranní Brief odtrhne od dnešních vydání.

## 2. Ranní pravidlo

> **Dnešní texty jsou primární. Memory je podpůrná.**

Ranní Brief začíná četbou dnešních Reference Editions. Memory vstupuje až poté, když pomáhá vysvětlit kontext, poznat opakování, zachytit posun argumentu, připomenout starší text nebo porovnat dnešní perspektivu s předchozí.

Nikdy nemá obrátit proces na „Memory nám říká, jaká témata máme dnes v novinách hledat“.

## 3. Detail

V Detailu může Memory přidat vrstvu: co jsme o tématu četli dříve, jak se změnil pohled stejného média, zda se naplnily předchozí předpoklady, které argumenty se opakují a jak se vyvíjí firma nebo sektor.

Tato vrstva musí být jasně oddělena od rekonstrukce původního článku.

## 4. Budoucí produkty

Pro Trendy a Analýzy může být Memory později primárním zdrojem, protože jejich účelem je syntéza přes čas.

To však není důvod, aby v4 předčasně optimalizovala ranní Brief pro dlouhodobou analytickou pipeline.

## 5. Technický princip

Předpokládaný směr z v3 zůstává rozumný: relační metadata, full text, vektorové vyhledávání, provenance, vazby článek ↔ vydání ↔ téma ↔ entita ↔ argument a časová kontinuita.

Konkrétní schéma se nepřenáší automaticky. Bude navrženo až podle ověřeného v4 produktu.

## 6. Interní vs. zákaznická Memory

Interní Article Memory může být bohatší než to, co je zpřístupněno uživateli. Její účel je redakční práce, provenance, kontinuita a pozdější syntéza.

Zákaznická Memory nemá fungovat jako cesta k reprodukci plných zdrojových článků. Má pracovat především s vlastními redakčními objekty Business Briefu: Briefy, Detaily, tématy, entitami, vztahy, trendy a časovými liniemi.

Toto oddělení je produktové i právně-rizikové pravidlo. Viz [RIGHTS_AND_TRANSFORMATION.md](RIGHTS_AND_TRANSFORMATION.md).

## 7. Memory jako spojovací tkáň portálu

Dlouhodobě má Memory umožnit, aby čtenář při vstupu do tématu nedostal stovky izolovaných článků, ale smysluplnou cestu přes vybrané Detaily, klíčové obraty, rozdílné perspektivy a vývoj v čase.

> **Brief je časový produkt. Detail je znalostní produkt. Memory je spojovací tkáň.**
