# System — Business Brief v4

## Boundary
Technická vrstva připravuje evidence. Editorial vrstva interpretuje. Publishing distribuuje schválenou redakční pravdu.

## Technician
Input: uzavřené source edition. Output: validovaný Source Bundle. Odpovědnosti: identity, immutable original, SHA/provenance, container validation, OCR decision/derivative, page renders, mechanical split, manifest, atomic handoff. Žádná editorial interpretace.

## Ingestor
Input: Source Bundle. Output: neutral Physical Map / evidence representation. Odpovědnost je geometrie, text a fyzická struktura, nikoli article/editorial truth.

## Editorial
Fast Editorial prokázal možnost page-level discovery, ale jeho současný full-edition cost profile není přijatelný jako default production architecture. Budoucí editorial design musí respektovat tuto zkušenost.

## Persistence
Supabase PostgreSQL: publications, editions, physical sources/arrivals, jobs, state, provenance, events a další operational entities. Supabase Storage: source inbox/archive a artefakty. Railway: workers a temporary workspace.

## State integrity
Immutable source a provenance jsou first-class. Ready state se nastavuje až po durable uploadu a validaci. Destruktivní cleanup inboxu je poslední krok.

## Observability
Dashboard má číst strukturovaný operational state. Zelený provoz patří na dashboard; alert je pro skutečnou integritu/deadline threat.

## Acquisition
Acquisition je oddělené upstream workflow. Technician není crawler/downloader. Odstraněný watcher není součást current architecture.
