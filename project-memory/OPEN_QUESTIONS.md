# Open Questions — Business Brief v4

## Q001 — OPEN — Ekonomicky udržitelný editorial processing
Které downstream editorial kroky mohou bezpečně běžet automatizovaně/API po vzniku spolehlivých Article Records a které mají zůstat v live Chat/human-supervised režimu?

## Q002 — OPEN — Source acquisition
Jak spolehlivě a legálně dostávat denní FT/WSJ/HB a později časopisy do systému bez odstraněného watcher mechanismu?

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

## Q009 — RESOLVED — Minimal Page Ingest contract
D019/D020 define page-ingest-v3 in the existing contracts.py and a new canonical generation. Required perspective expansion and irrelevant inventory are removed. Deployment and corpus acceptance remain Q010, not an undecided schema question.

## Q010 — OPEN — Ingestor v2 acceptance
Jaké minimum reálných stránek a publikací musí Chat Ingestor v2.0 úspěšně zpracovat, než bude Page JSON contract frozen a Assembler implementován?

Acceptance musí zahrnout komplexní novinovou stránku, continuation, grafiku/reklamu a alespoň jednu odlišnou publikaci; později i časopis.

## Q011 — OPEN — Assembler review policy
Kdy může Assembler spojit části článku deterministicky a kdy musí výsledek označit NEEDS_REVIEW místo pokusu o chytré domýšlení?
