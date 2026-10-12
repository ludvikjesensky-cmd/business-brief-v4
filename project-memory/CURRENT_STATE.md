# Current State — Business Brief v4

**Last consolidated:** 2026-10-12  
**Evidence:** projektová dokumentace + uživatelovo zadání a dostupný záznam konverzace „Stav zpracování WSJ“; následná lokální implementace a syntetické testy. Původní WSJ experimenty nebyly znovu spuštěny.
**Runtime must be re-verified in Supabase/Railway before operational claims.**

## Current phase
v4 ověřuje levnější editorial discovery. Lokální Ingestor vytváří Physical Map i Visual Page Map; samostatný Assembler sestavuje články (D015). Semantic layout má původní dílčí pozitivní výsledky na stranách 5 a 2 WSJ 2026-10-12. Plně autonomní ranní výroba ani reálná WSJ full-issue validation nejsou hotové. Detail experimentu i implementace má jediný domov v [docs/SYSTEM.md](../docs/SYSTEM.md#visual-page-map--semantic-layout--experiment-wsj-2026-10-12).

## Established foundation
- Technician připravuje Source Bundle; Ingestor drží neutrální Physical Map a sémantický layout v oddělené Visual Page Map. Assembler vykonává mapy, editorial výběr je následná vrstva.
- Repository, Railway/Supabase infrastruktura a dashboard existují podle dosavadní dokumentace; současný health není tímto potvrzen.
- WSJ watcher byl odstraněn; acquisition není vyřešená.
- Platná architektura je v ARCHITECTURE; Visual Page Mapper je interní fáze lokálního Ingestoru. Existující produkční durable worker zatím vytváří pouze Physical Map; nový kontrakt není nasazen do queue.

## Implementation validation
- `bb-ingestor` / `extract_maps` vytváří obě mapy a handoff `ingestor-output.json`, neprovádí assembly. `bb-assembler` ověřuje handoff a sestavuje text; CLI prepare/map/assemble zůstává kompatibilní laboratorní cesta. Kontrakt v1, lokální render, offline/API adaptér, review/coverage, durable provenance/resume a explicitní reviewed continuations jsou implementovány. Rozhodnutí D014/D015; použití v docs/SYSTEM.md.
- 74 nových testů ověřuje lokální mechaniku včetně řádků pod fotkou, footprintů, reading order, nejednoznačnosti, hashů, limitů calls, chyb API, cross-page linků a dvoumapového handoffu Ingestor → Assembler. Se stávající sadou prošlo 123 testů; jeden původní HTTP startup test dashboardu byl po zjištění sandboxového zákazu lokálního socketu vynechán. Tento limit není chyba nového mapperu ani důkaz runtime health.
- Syntetické dvoustránkové PDF prošlo skutečným Ingestorem, renderem a offline mapováním/sestavením: 11 bloků, 9 assigned, 2 excluded, žádné unmatched/ambiguous. Toto neověřuje schopnost vision modelu na reálném WSJ.

## Experimental results and blockers
- Strany 5 a 2 podporují vision mapování článků a explicitního reading order; Python sestavuje text z Physical Map. 600px JPEG stačil pro layout.
- Otevřené geometrické problémy: hranové chyby Physical Map, neúplný footprint grafů a vyloučení řádků těsně pod fotografií. Navržený photo overlap threshold ještě není validovaný.
- Test celého 26stránkového WSJ není dokončen. Strany 1–4 byly vyrenderovány do low-res kontaktního listu a vizuálně prošly; to není ověření sestavení článků. Render stran 5–26 po skupinách se zadrhl při překrývajících se deployích téže dočasné Railway funkce a problémech s návratem/base64 logy. Následovalo čekání/polling a uživatelské přerušení. Pozdější pokyn pokračovat není důkazem dokončení; dostupný záznam dokončení nepotvrzuje.
- Během těchto experimentů nebyl spuštěn žádný placený Fast Editorial/OpenAI API a produkční pipeline se neměnila.
- Paid Fast Editorial automation zůstává pozastavena (D011/F003). Ekonomická výhoda Visual Page Map je hypotéza, nikoli naměřená úspora.

## Next steps
1. Ověřit implementovaný kontrakt a geometrické defaults na skutečných mapách/artefaktech stran 5 a 2; zachovat provenance a porovnat chyby s původním experimentem.
2. Dokončit render/map/assembly přes lokální sekvenční CLI po malých dávkách; bez překrývajících se Railway deployů a bez přenosu obrázků přes logy. Live API má default limit jeden call na spuštění a vyžaduje explicitní opt-in/model.
3. Dokončit mapování, sestavení a audit všech 26 stran včetně continuations; změřit omissions, kontaminaci, reading order a chybovost.
4. Před placeným benchmarkem spočítat cost model; cenu, čas a kvalitu ověřit malým acceptance testem před automatizací.

## Operational authority
Jobs, deployments, logs, artefakty a živý health ověřuj v Supabase/Railway. Tento snapshot zachycuje konsolidovaný experimentální stav, nikoli live monitoring.
