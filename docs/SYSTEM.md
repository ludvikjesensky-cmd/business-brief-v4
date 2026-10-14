# System — Business Brief v4

## Boundary
Technická vrstva připravuje evidence. Ingestor interpretuje konkrétní source page v live conversation. Assembler skládá články. Editorial vrstva rozhoduje o významu a publikaci.

## Technician
Input: uzavřené source edition.

Output: validovaný source-bundle-v4.

Odpovědnosti: identity, immutable original, SHA/provenance, container validation, OCR decision/derivative, page evidence, mechanical split, manifest, atomic handoff. Žádná editorial interpretace.

## Ingestor v2.0
Input: Technician Source Bundle.

Execution model: live Chat, human-supervised, page-by-page.

Output: přesně jeden verified Page JSON pro každou dokončenou source page.

Ingestor v2.0 používá:
- page image jako primární vizuální autoritu;
- prepared text/OCR jako evidence;
- metadata Source Bundle;
- Scope a Editorial purpose pro relevance judgment;
- opakované conversational iterations při nejasnosti.

Nevytváří final multi-page Article Record. Nespojuje více publikací. Neprovádí batch semantic processing přes API.

Po dokončení každé stránky se zastaví.

Detail role je v docs/INGESTOR.md.

## Page JSON
Page JSON je nový handoff artefakt mezi Ingestorem a Assemblerem.

Má reprezentovat:
- source/publication/page identity;
- editorial items na stránce;
- title/subtitle/byline/metadata;
- text přítomný na dané stránce;
- starts/continues/continuation evidence;
- relevance;
- verification a explicitní uncertainty;
- provenance k Technician source.

Přesné machine schema ještě není frozen. Má být definováno v existujícím contract systemu v src/business_brief/contracts.py.

## Assembler
Input: Page JSONy jednoho edition/source.

Output: canonical Article Records.

Assembler spojuje části článků napříč stránkami, ale nemá znovu interpretovat page layout. Nejasné případy musí být reviewable.

Article artefakty patří do Supabase Storage; identity, vztahy, provenance a stav do PostgreSQL.

## Composer
Composer pracuje nad Article Records více zdrojů a vytváří topic groupings/dossiers pro články o společném tématu.

Composer není Assignment Editor a nerozhoduje sám o finálním Brief selection.

## Translator
Translator navazuje na sestavené spolehlivé články/topic material. Je vhodným kandidátem pro API automatizaci, protože pracuje s již známým textem.

## Editorial
Editorial Workflow pracuje až nad spolehlivým obsahovým základem. Rozlišuje fakta, perspektivy autorů, cross-source synthesis, kontext a Business Brief commentary.

## Persistence
Supabase PostgreSQL: publications, editions, physical sources/arrivals, jobs, state, provenance, relations a další operational entities.

Supabase Storage: source inbox/archive, Technician artifacts, Page JSONs, assembled article artifacts a další validované artefakty.

Railway: workers a temporary workspace.

## State integrity
Immutable source a provenance jsou first-class. Ready state se nastavuje až po durable uploadu a validaci. Destruktivní cleanup inboxu je poslední krok.

## Observability
Dashboard má číst strukturovaný operational state. Zelený provoz patří na dashboard; alert je pro skutečnou integritu/deadline threat.

## Acquisition
Acquisition je oddělené upstream workflow. Technician není crawler/downloader. Odstraněný watcher není součást current architecture.

## Legacy: Ingestor v1.1 / Physical Map
ingestor-v4-physical-map-v1.1, physical-map.json jako povinný production handoff, Visual Page Map, BODY_FLOW, bbox/overlap matching a block-ID article assembly jsou superseded.

Jejich kód může dočasně zůstat v repository kvůli historii, testům nebo diagnostice, ale nesmí být považován za current production architecture.

Historické důvody a podmínky případného návratu jsou v project-memory/FAILURES.md a DECISIONS.md.
