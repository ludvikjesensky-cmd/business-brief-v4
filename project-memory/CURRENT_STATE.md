# Current State — Business Brief v4

**Last consolidated:** 2026-10-15  
**Runtime must be re-verified in Supabase/Railway before operational claims.**

## Current phase
v4 opouští automatizovanou rekonstrukci článků přes Physical Map / Visual Page Map jako produkční cestu.

Nový přijatý směr je:

closed source edition → Technician → validated Source Bundle → Ingestor v2.0 (live Chat) → one verified JSON per page → Assembler → canonical Article Records → Composer → Translator → Editorial Workflow.

Ingestor v1.1 (ingestor-v4-physical-map-v1.1) a navazující Physical Map / semantic-layout experimenty jsou neaktivní legacy. Jejich kód a historie zůstávají jako evidence a failure knowledge, ale nejsou current production architecture.

## Established foundation
- Technician zůstává technický gateway bez editorial interpretation.
- Source Bundle v4 zůstává upstream kontrakt pro Ingestor.
- Supabase je operational memory/archive; Railway je workshop.
- Provenance, immutable source a page-level evidence zůstávají first-class.
- Watcher byl odstraněn; acquisition je stále explicitní upstream problém.
- Reálný full-edition API editorial processing se neosvědčil ekonomicky ani jako spolehlivý jednorázový interpretační mechanismus.

## Ingestor v2.0
Ingestor v2.0 je pracovní role živého Chatu, ne autonomous API worker.

Pracuje:
- nad Technician Source Bundle;
- jednu stránku po druhé;
- iterativně nad page image + prepared text/evidence;
- s explicitním ověřováním textu a metadat;
- s Business Brief relevance v kontextu projektu;
- s jedním Page JSON jako jediným výstupem každé dokončené stránky.

Po každé stránce se zastaví. Další stránku zpracuje až na pokyn uživatele.

Machine contract Page JSON je definován v `src/business_brief/contracts.py` jako `page-ingest-v2`, včetně page-level `PerspectiveEvidence`.

Canonical Page JSON se po validaci ukládá do Supabase Storage pod logickým klíčem `page-ingest/<publication_id>/<edition_date>/<source_sha256>/ingestor-v2.0/page-<NNNN>.json`. Konkrétní bucket je operational konfigurace. Page pass není dokončen, dokud durable write není ověřen.

## Ingestor Access Bridge — contract accepted, implementation pending

K 2026-10-15 je přijat D018 a normativní [HTTP kontrakt v docs/INGESTOR.md §19](../docs/INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1). Tři endpointy řeší current source, evidence access a validaci/persistence jedné stránky. Bridge nedělá editorial interpretaci; preferovaným budoucím runtime je malá samostatná Railway HTTP služba.

Tato změna je pouze dokumentace: služba, Chat connector, auth konfigurace, durable idempotency mechanismus a source-state fencing nejsou implementované ani provozně ověřené. Referencovaný první page-1 acceptance pokus hlásil BLOCKED kvůli chybějícímu přístupu k obsahu privátního Storage a zápisu canonical JSONu; nejde o nově ověřený live stav. Úspěšná persistence ani dokončení strany 1 se tímto kontraktem neprokazují.

## Technician
Produkční runtime je stále na Technician v4.2. PR #3 připravuje novější technickou přípravu s lepším page evidence/OCR validation, ale není mergnutý a práce na něm je dočasně pozastavena kvůli Usage.

Desetistránkový WSJ 2026-10-14 prošel Technicianem v4.2 a skončil ve stavu READY_FOR_INGESTOR.

## Inactive legacy
Následující nejsou current production path:
- Ingestor v1.1 / Physical Map worker;
- reconstruction článků pouze z Physical Map;
- Visual Page Mapper + BODY_FLOW + bbox/overlap assembly;
- controller-directed block-ID experiment;
- paid Fast Editorial full-edition flow.

Neodstraňovat jejich historii z FAILURES/HISTORY; nevracet je do current architecture bez nové ověřené skutečnosti.

## Next steps
1. Implementovat a ověřit Ingestor Access Bridge podle docs/INGESTOR.md §19 včetně skutečného přístupu z Chatu, autorizace, fencing, idempotency a readback recovery. Potom zopakovat pouze stranu 1 WSJ 2026-10-14 s revalidací live source a durable persistence; po stránce STOP.
2. Ověřit Ingestor v2.0 ručně na několika různých stránkách a publikacích.
3. Rozhodnout a implementovat dedicated operational index/table pro Page JSONy pouze pokud acceptance test ukáže, že je potřeba.
4. Teprve poté implementovat Assembler nad Page JSONy a uložit canonical Article Records do Supabase Storage + Postgres.
5. Později navázat Composerem, Translator API workflow a stávajícím Editorial Workflow.

## Operational authority
Jobs, deployments, live status, runtime artifacts a health ověřuj v Supabase/Railway. Tento dokument je kanonický snapshot směru projektu, nikoli live monitoring.
