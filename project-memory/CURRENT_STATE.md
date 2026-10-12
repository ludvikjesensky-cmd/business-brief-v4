# Current State — Business Brief v4

**Last consolidated:** 2026-10-12  
**Evidence:** projektová dokumentace + uživatelovo zadání a dostupný záznam konverzace „Stav zpracování WSJ“. Experimenty nebyly při konsolidaci znovu spuštěny.  
**Runtime must be re-verified in Supabase/Railway before operational claims.**

## Current phase
v4 ověřuje levnější editorial discovery. Visual Page Map / semantic layout má dílčí pozitivní výsledky na stranách 5 a 2 WSJ 2026-10-12; plně autonomní ranní výroba ani full-issue validation nejsou hotové. Detail experimentu má jediný domov v [docs/SYSTEM.md](../docs/SYSTEM.md#visual-page-map--semantic-layout--experiment-wsj-2026-10-12).

## Established foundation
- Technician/Ingestor oddělují technickou přípravu a Physical Map od sémantické interpretace.
- Repository, Railway/Supabase infrastruktura a dashboard existují podle dosavadní dokumentace; současný health není tímto potvrzen.
- WSJ watcher byl odstraněn; acquisition není vyřešená.
- Platná architektura je v ARCHITECTURE; Visual Page Mapper je laboratorní návrh.

## Experimental results and blockers
- Strany 5 a 2 podporují vision mapování článků a explicitního reading order; Python sestavuje text z Physical Map. 600px JPEG stačil pro layout.
- Otevřené geometrické problémy: hranové chyby Physical Map, neúplný footprint grafů a vyloučení řádků těsně pod fotografií. Navržený photo overlap threshold ještě není validovaný.
- Test celého 26stránkového WSJ není dokončen. Strany 1–4 byly vyrenderovány do low-res kontaktního listu a vizuálně prošly; to není ověření sestavení článků. Render stran 5–26 po skupinách se zadrhl při překrývajících se deployích téže dočasné Railway funkce a problémech s návratem/base64 logy. Následovalo čekání/polling a uživatelské přerušení. Pozdější pokyn pokračovat není důkazem dokončení; dostupný záznam dokončení nepotvrzuje.
- Během těchto experimentů nebyl spuštěn žádný placený Fast Editorial/OpenAI API a produkční pipeline se neměnila.
- Paid Fast Editorial automation zůstává pozastavena (D011/F003). Ekonomická výhoda Visual Page Map je hypotéza, nikoli naměřená úspora.

## Next steps
1. Přesně definovat page-map kontrakt, footprint objektů a overlap metriku; ověřit hranice na stranách 5 a 2.
2. Navázat od strany 5 malými sekvenčními dávkami (např. 4 strany), po ověření runtime stavu; zabránit překrývajícím se deployům a přenosu velkých obrázků přes logy.
3. Dokončit mapování, sestavení a audit všech 26 stran včetně continuations; změřit omissions, kontaminaci, reading order a chybovost.
4. Před placeným benchmarkem spočítat cost model; cenu, čas a kvalitu ověřit malým acceptance testem před automatizací.

## Operational authority
Jobs, deployments, logs, artefakty a živý health ověřuj v Supabase/Railway. Tento snapshot zachycuje konsolidovaný experimentální stav, nikoli live monitoring.
