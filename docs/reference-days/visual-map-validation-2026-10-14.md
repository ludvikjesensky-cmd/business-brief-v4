# Visual Page Map v1.1 — oprava pravidel a opakování vzorku

Datum: 2026-10-14. Šest volání GPT-6 Luna, všechna dokončena bez timeoutu či oprav JSON. Odhad ceny $0.012351 podle uloženého usage, nikoli účetní vyúčtování.

Stejný model, medium reasoning, 600px JPEG75, image detail high, limit6000. Jediný prompt pro oba deníky, bez newspaper-specific pravidel. Nové instrukce jsou přímo ve zdrojovém PROMPT; hash zachycuje skutečné instrukce. Reasoning je součástí mapper config/resume. Předchozí baselines měly experimentální transportové doplňky; toto není randomizovaný experiment ani potvrzení stabilní kvality. Label lookup se v novém per-page vzorku vztahuje jen k vybrané stránce; continuations nejsou předmětem porovnání.

## Pokrytí — před → po

| Stránka / náhled | Assigned | Unmatched | Ambiguous |
|---|---:|---:|---:|
| WSJ 5 | 263 → 227 | 5 → 33 | 0 → 0 |
| WSJ 10 | 569 → 533 | 11 → 12 | 1 → 0 |
| WSJ 12 | 549 → 561 | 64 → 72 | 0 → 6 |
| HB 1 | 136 → 154 | 49 → 31 | 0 → 0 |
| HB 6 | 46 → 46 | 0 → 0 | 0 → 0 |
| HB 30 | 258 → 279 | 0 → 0 | 0 → 0 |

## Kontrola kvality

- WSJ 5: druhý titulek je kompletní a byline oddělené; body zóny ale vynechávají úvodní řádky a část hran. Pokrytí se zhoršilo, stránka neprošla kvalitativně.
- WSJ 10: infografika už neodtrhla článek do samostatné položky. Její titulek a některé popisky ale stále pronikají do headline/body; nevyřešeno.
- WSJ 12: kontrolovaný Scaries body už neobsahuje křížovkové útržky a titulek obsahuje poslední řádek Scarier. Titulek druhého článku ale stále obsahuje cizí slova a zvýšily se nejednoznačnosti.
- HB 1: druhý článek má nyní samostatně mapovaný standfirst; nepřiřazené bloky klesly. Hranové omissions nejsou všechny vyřešeny.
- HB 6: kicker, obě řádky titulku a standfirst jsou ve správném pořadí před hlavním body. Toto je konkrétní zlepšení při stejném blokovém pokrytí.
- HB 30: fotografie má footprint jako union dvou obdélníků. Nový konzervativní source audit odhalil 15 párů duplicitního textu ve stejném místě. Text není mazán; potřebuje oddělené řešení kvality zdrojové vrstvy.

Přidána diagnostika shodného source textu (>=8 znaků) s bbox souřadnicemi do 0,25 bodu; toto není automatický dedup ani sémantická inference. Změny textu/Physical Map nebyly provedeny.

125 unit/integration testů prošlo. Jeden původní dashboard HTTP startup test zůstává vynechán pro známý sandboxový zákaz socketu. Produkční worker, queue, DB a deployment beze změn. Žádný Fast Editorial, editorial selection/deep read ani full-issue paid rerun.

**Závěr:** pravidla zlepšují konkrétní role a oddělení obsahu, ale výsledky jsou smíšené. Kvalitativní acceptance neprošla. Další experiment musí izolovat geometrickou přesnost (stejné stránky, prompt a model; vyšší rozlišení vs600px), místo dalšího rozšiřování promptu naslepo. To zatím nebylo spuštěno.

## Dřívější benchmarky

WSJ 2026-10-12: technicky dokončeno26/26, 27calls včetně jednoho explicitního retry neplatné geometrie na straně17, cena odhadem$0.056861; assigned12998/excluded968/unmatched1110/ambiguous9 z15085. Jeden duplicitní region ID na straně10 byl laboratorně přejmenován s logem, nikoli opravením geometrie. Quality acceptance neprošla (split článků, crossword contamination, hranice titulků/fotografií). Cross-page links nebyly reviewed.

HB 2026-10-06, 50stran: vzorek1,4,5,6,12,30; validní mapy1,6,30, timeouty4/5/12 s neznámým billing bez automatického retry. Známé usage$0.004781 nezahrnuje timeouty. Native PDF duplicity potvrzené na straně30. Archivní cesta nese2026-10-05, skutečné vydání6.října ověřeno na titulní stránce. Celých50stran testováno nebylo.

Původní manuální Visual Page Map experimenty byly bez placených API. Navazující lokální benchmarky již autorizovaná placená OpenAI volání provedly, nikdy Fast Editorial. Pokus o Railway render zůstává historický failure F007; lokální full WSJ technický průchod jej později nahradil. Měřená levná cena samotného mapování neprokazuje úsporu celé editorial pipeline při stejné kvalitě.
