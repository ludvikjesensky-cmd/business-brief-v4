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

## Q012 — RESOLVED — Article asset representation and physical storage
D022 decides authoritative page-PNG crops, dual page/text anchors and existing private page-ingest bucket in a new v4/ingestor-v2.2 namespace. OCR inside visuals is optional noncanonical support. Missing/ambiguous placement is review/unplaced, never a guess. This is no longer an undecided bucket/schema question; the implementation gate is INGESTOR.md §21.5.

## Q013 — OPEN — Article asset writer and acceptance
Implement the fenced binary crop writer and adapter transport; prove source-PNG/crop identity, pixel rounding/bounds, immutable create/replay/conflict/concurrency/timeout recovery and set-wide Page JSON readback before any separately authorized rollout. The current code deliberately blocks nonempty-assets persistence. Define explicit ordering or review for multiple assets at the same text anchor; assembly must not invent it. Real visual/anchor acceptance remains distinct from schema tests. Q011 still covers broader cross-page assembly identity/review policy; D022 already resolves anchor ambiguity to review.
