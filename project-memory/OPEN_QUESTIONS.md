# Open Questions — Business Brief v4

## Q001 — OPEN — Ekonomicky udržitelný editorial processing
Jak získat dostatečně úplnou a kvalitní editorial map/reading bez full-edition API nákladu typu zaznamenaného Fast Editorial runu? Visual Page Map (D013; detail v docs/SYSTEM.md) je kandidát, ne vyřešení otázky. Potřebujeme cost model a malý placený benchmark ceny/latence/kvality; experiment 2026-10-12 placené API nepoužil.

## Q002 — OPEN — Source acquisition
Jak spolehlivě a legálně dostávat denní FT/WSJ/HB do systému, zejména WSJ, bez odstraněného watcher mechanismu?

## Q003 — OPEN — Production editorial workflow
Které části osmi editorial passes mají být kód, model, silný model, lidský review nebo vůbec nemají být samostatným krokem?

## Q004 — OPEN — Publication gate
Jaké minimum evidence/kvality musí být splněno před autonomním publikováním?

## Q005 — OPEN — Rights/licensing
Jaký konkrétní právní/licenční režim bude použit pro jednotlivé zdroje a pro Brief/Detail před komerčním spuštěním?

## Q006 — OPEN — Business model
Finální pricing, free/paid hranice, B2B balíčky a role Detailu nejsou definitivně rozhodnuté.

## Q007 — OPEN — Editorial Memory implementation
Jaký minimální schema/retrieval model poskytne kontinuitu bez toho, aby starší obsah přebil dnešní vydání?

## Q008 — OPEN — Audio
Kdy a jak zavést stabilní hlasovou identitu a audio adaptaci, aniž by předběhla ověřený textový produkt?

## Q009 — OPEN — Visual Page Map contract and boundary matching
Jak přesně serializovat souřadnice, BODY_FLOW/reading order, embedded objects a exclusions do page-map.json? Jak definovat plný footprint grafu a overlap metriku/toleranci fotografie bez ztráty řádků? Navržených >60 % je testovací varianta, ne přijatý univerzální práh. Rozhodnutí vyžaduje regresní kontrolu stran 2 a 5 a širší corpus.

## Q010 — OPEN — Full-issue completeness and generalization
Funguje nový přístup na všech 26 stranách WSJ 2026-10-12, přes continuations a dále na jiných publikacích? Nejprve dokončit přerušený test (CURRENT_STATE/F007), auditovat chybějící a přimíchaný text, pořadí a vazby mezi stranami. Zatím nelze uvést full-issue error rate ani claim o produkční připravenosti.
