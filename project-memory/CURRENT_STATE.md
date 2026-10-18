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

## Ingestor Access Bridge — implemented; technical page-1 access verified

K 2026-10-15 je implementovaná samostatná Railway HTTP služba `ingestor-access-bridge` podle [INGESTOR.md §19](../docs/INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1), viz [PR #5](https://github.com/ludvikjesensky-cmd/business-brief-v4/pull/5), navazující na kontrakt PR #4. Direct PostgreSQL session funguje po zapnutí IPv6 egress a s oficiální Supabase CA (`verify-full`). Migrace `20261015184146_ingestor_bridge_bindings` poskytuje durable idempotency binding a pending-write guards; přímé row/session locks drží kritickou sekci přes Storage create a readback. Buckety `source-archive` a `page-ingest` jsou privátní.

Autentizovaný technický acceptance z Codex HTTPS klienta ověřil health/readiness, WSJ 2026-10-14 `default`, source UUID `603e8242-ffe8-4e1d-a5de-9adb3da4d188`, manifest SHA a skutečné stažení/hash evidence pouze strany 1 včetně required PDF fallbacku. Samostatný ChatGPT connector nebyl vytvořen ani ověřen. Replay/concurrency/timeout recovery jsou pokryté kontrolovanými testy; live DB diagnostika ověřila row locks a pending guards s rollbackem. Nejde o real production write acceptance.

Semantic ingestion, Page JSON persistence, editorial processing ani Assembler nebyly spuštěny. První ruční page pass a §19.8 gate pro konkrétní ChatGPT integraci zůstávají otevřené. Pro runtime proměnné, credential scopes a recovery viz [bridge/README.md](../bridge/README.md).

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
1. Provést uživatelem výslovně zahájený ruční pass pouze strany 1 WSJ 2026-10-14 s revalidací live source a verified persistence; po stránce STOP. Pro samostatný ChatGPT nejprve nakonfigurovat a ověřit jeho connector/auth. Technický read-only acceptance bridge z Codexu již prošel.
2. Ověřit Ingestor v2.0 ručně na několika různých stránkách a publikacích.
3. Rozhodnout a implementovat dedicated operational index/table pro Page JSONy pouze pokud acceptance test ukáže, že je potřeba.
4. Teprve poté implementovat Assembler nad Page JSONy a uložit canonical Article Records do Supabase Storage + Postgres.
5. Později navázat Composerem, Translator API workflow a stávajícím Editorial Workflow.

## Operational authority
Jobs, deployments, live status, runtime artifacts a health ověřuj v Supabase/Railway. Tento dokument je kanonický snapshot směru projektu, nikoli live monitoring.
