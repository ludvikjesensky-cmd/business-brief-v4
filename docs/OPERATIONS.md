# Operations — Business Brief v4

Cílem je ranní provoz, který je nakonec autonomní, ale ne slepý.

## Operating rules
- Runtime truth ověřuj v Supabase/Railway, ne ve starém Markdown snapshotu.
- Každý job musí být auditovatelný, idempotentní kde to dává smysl a mít viditelný failure.
- Paid/model steps mají explicitní model/version identity a usage/cost telemetry.
- Automatický schedule placeného editorial discovery není povolen, dokud acceptance test nepotvrdí cenu, čas a kvalitu.
- Watcher pro WSJ byl odstraněn; acquisition není automaticky vyřešená.
- Dashboard je primární healthy-state surface. Alerty pouze pro skutečné problémy.
- Publication gate musí umět zastavit nezdravé vydání.

## Cost discipline
Reálný Fast Editorial WSJ run ukázal přibližně USD 7.95 za jeden průchod a kolem 49 requests. Toto je failure baseline. Každý nový návrh musí před full runem ukázat očekávaný cost model a malý test.

## Debugging order
1. PROJECT.md + CURRENT_STATE.
2. Supabase jobs/events/artifacts.
3. Railway deployment/logs.
4. Relevantní component contract/docs.
5. DECISIONS + FAILURES před změnou architektury.

## Documentation
Denní runtime eventy se nepřepisují do Markdownu. Do Project Memory patří pouze změna stavu, decision, failure nebo lesson s dlouhodobou hodnotou.

## Visual Page Map local lab
Příkazy a artefakty jsou v [SYSTEM](SYSTEM.md#visual-page-map-v1--implementace-a-spuštění). Lokální prepare/offline map/assemble nespouštějí placenou službu. Live mapper vyžaduje `--live --allow-paid --model`, default nejvýše jeden request na spuštění a výstupový limit; jde o limit calls/tokens, nikoli zaručenou cenu v USD. Modelový usage se uchovává po stránkách. Bez předem spočítaného cost modelu a acceptance se neplánuje automatický full-edition běh.

Doporučený vstup je `bb-ingestor` (Source Bundle → obě mapy + handoff) a následně `bb-assembler` (ověřený handoff → text/coverage). Částečný Ingestor run vrací kód 2 a `PARTIAL`; nejde o hotové vydání. Existující durable worker v produkční queue je zatím Physical Map-only, nový kontrakt na něj nebyl nasazen a nezapíná modelová volání automaticky.

API timeout s neznámým billing stavem nemá automatický retry. Durable attempt je nutné prozkoumat před novým pokusem; uloženou odpověď lze znovu validovat bez placení. OS lock brání paralelním writerům v jednom lokálním issue adresáři. Žádné Railway deploye nebo obrázky v base64 logách nejsou součástí tohoto CLI workflow. Produkční runtime a gates zůstávají beze změny.
