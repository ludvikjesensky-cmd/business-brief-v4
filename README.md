# Business Brief v4

> **Není hlavní, na co se díváš. Hlavní je, co vidíš.**

Business Brief v4 je redakčně vedená brána do způsobu, jakým kvalitní světový ekonomický tisk přemýšlí. Výchozími zdroji jsou především aktuální vydání **Financial Times, The Wall Street Journal a Handelsblatt**.

V4 nevzniká jako další news briefing ani jako stroj na kompresi článků. Jejím cílem je přenášet do češtiny hodnotné **myšlenky, otázky, argumenty, perspektivy a pozorování**, které vznikají v dnešních textech těchto novin.

## Základní produktová věta

**Dnešní vydání orientuje. Brief otevírá. Detail rozvíjí.**

- **Dnešní vydání**: úplná mapa aktuálních vydání FT / WSJ / HB. Dává čtenáři šíři a možnost jít mimo náš výběr.
- **Business Brief**: redakční četba dnešních vydání. Vybírá to, co stojí za přenesení do přemýšlení čtenáře.
- **Detail**: důkladná česká redakční rekonstrukce konkrétního článku, jeho myšlenkové konstrukce, argumentů, faktů a perspektivy, doplněná kontextem a jasně odděleným komentářem.
- **Memory**: dlouhodobá paměť textů, témat, argumentů, lidí, firem a vývoje.

## Co v4 není

Business Brief není český Reuters, Bloomberg ani obecný ekonomický newswire; není AI summary tří novin; není seznam headline + tři odrážky; není nástroj, který má čtenáře zbavit potřeby číst; a není názorový produkt, který čtenáři říká, co si má myslet.

## Co chceme vyvolat

Ideální reakce po Briefu není „tak, teď už vím“. Může být:

- „Takhle jsem o tom nepřemýšlel.“
- „Tohle je zajímavá otázka.“
- „S tím nesouhlasím, ale chci pochopit argument.“
- „Tenhle Detail si chci přečíst.“
- „Tohle mi zůstalo v hlavě.“

Brief má šetřit pozornost, nikoli uzavírat četbu. **Brief otevírá; Detail rozvíjí; úsudek zůstává čtenáři.**

## Dokumentace

Doporučené pořadí:

1. [VISION.md](docs/VISION.md) — proč projekt existuje.
2. [PRODUCT_MODEL.md](docs/PRODUCT_MODEL.md) — kanonický produktový model v4.
3. [GOALS_AND_VALUES.md](docs/GOALS_AND_VALUES.md) — stabilní cíle, hodnoty a zásady zděděné i z v1–v3.
4. [SCOPE_AND_AUDIENCE.md](docs/SCOPE_AND_AUDIENCE.md) — cílový čtenář, tematický a zdrojový rozsah, B2C/B2B.
5. [EDITORIAL_PHILOSOPHY.md](docs/EDITORIAL_PHILOSOPHY.md) — redakční DNA a kritéria výběru.
6. [BRIEF.md](docs/BRIEF.md) — dramaturgie ranního vydání.
7. [DETAIL.md](docs/DETAIL.md) — definice prémiového Detailu.
8. [TODAYS_EDITIONS.md](docs/TODAYS_EDITIONS.md) — úplná mapa FT / WSJ / HB.
9. [MEMORY.md](docs/MEMORY.md) — role dlouhodobé paměti.
10. [SOURCE_AND_PORTAL_STRATEGY.md](docs/SOURCE_AND_PORTAL_STRATEGY.md) — kurátorství zdrojů, portál a knihovna Detailů.
11. [RIGHTS_AND_TRANSFORMATION.md](docs/RIGHTS_AND_TRANSFORMATION.md) — hranice zdrojové a publikační vrstvy.
12. [AUTONOMOUS_MORNING.md](docs/AUTONOMOUS_MORNING.md) — autonomní ranní provoz, dashboard, gate a alerty.
13. [AUDIO.md](docs/AUDIO.md) — audio produkt, hlas a TTS principy.
14. [TECHNICIAN.md](docs/TECHNICIAN.md) — kanonická definice univerzální technické vstupní brány, identity vydání, deduplikace a Source Bundle v4.
15. [V4_HANDOFF.md](docs/V4_HANDOFF.md) — autoritativní handoff pro nové konverzace.

## Ověřený implementační stav — 9. 10. 2026

WSJ prošel **Technician → Ingestor → Fast Editorial**: 44 stran, 137 fragmentů,
99 předběžných redakčních položek, stav `FROZEN`. Finální Brief zatím není hotový;
úplnost textu pod vodoznakem není nezávisle ověřena. Poslední testy: 50 passed.

Podrobný stav, artefakty, limity ověření a další kroky:
[PROGRESS_2026-10-09.md](docs/PROGRESS_2026-10-09.md).

## Výchozí produktová fáze (historický kontext)

**Fáze: Product & Editorial Foundation → Autonomous Production Design.**

Nejdříve fixujeme produkt a redakční principy. Architektura, datový model a automatizace mají následovat až poté, co ručně ověříme, že umíme vytvořit vydání, které odpovídá této filozofii.

V3 zůstává technologickou a experimentální referencí. V4 se nemá mechanicky naplnit starými dokumenty a pipeline. Každý převzatý prvek musí znovu projít otázkou:

> **Slouží produktu v4?**

### Historická kontinuita

[PRODUCT_HERITAGE.md](docs/PRODUCT_HERITAGE.md) vysvětluje, co v4 vědomě přebírá z v1, v2 a v3, co mění a proč. Je to ochrana proti tomu, aby se v dalších konverzacích ztrácely starší dobré principy nebo se vracely překonané předpoklady.


## Aktuální provozní směr — 8. 10. 2026

Ranní produkt má být schopen bezpečně vzniknout bez přítomnosti člověka. Pracovní target je 08:35, provozní hranice 08:45 Europe/Prague. Autonomie je podmíněna Publication Gate, observability, dashboardem a exception-only alerty.

Audio je plnohodnotný kanál s vlastním Audio Adapterem a cílově originálním hlasem značky. Konkrétní TTS vendor zůstává v ověřování.
