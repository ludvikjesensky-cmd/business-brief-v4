# Architecture — Business Brief v4

Architektura odděluje technickou přípravu zdroje, page-level interpretaci, skládání článků, cross-source kompozici, překlad, editorial judgment a publikaci.

## Canonical flow

closed source edition  
→ Technician  
→ validated Source Bundle  
→ Ingestor Access Bridge (authorized evidence access; contract only)
→ **Ingestor v2.0 (live Chat)**  
→ Ingestor Access Bridge (validation + verified canonical persistence; contract only)
→ one verified Page JSON per source page  
→ Assembler  
→ canonical Article Records  
→ Composer  
→ Topic Dossiers / cross-source groupings  
→ Translator  
→ Editorial Workflow  
→ Master editorial truth  
→ Brief / Detail / channel adaptations

## Technician
Technician je technický gateway: identity, immutable original, SHA/provenance, OCR, page evidence, mechanický split, validace a atomic handoff. Nedělá editorial interpretation.

Jeho output je validovaný source-bundle-v4.

## Ingestor v2.0
Ingestor v2.0 je živá Chat role.

Jeho vstupem je Technician Source Bundle. Zpracovává vždy jednu stránku. Používá obraz stránky a připravenou textovou/evidence vrstvu iterativně a vytváří jeden ověřený Page JSON.

Jeho odpovědností je:
- pochopit obsah a layout konkrétní stránky;
- identifikovat relevantní editorial objects;
- určit titulky, metadata, byline a pokračování;
- rekonstruovat věrohodný source-faithful text přítomný na dané stránce;
- explicitně evidovat nejistoty;
- posoudit relevance v kontextu Scope/Editorial purpose;
- zastavit se po dokončení stránky.

Nevytváří final multi-page Article Record a nespojuje zdroje.

## Ingestor Access Bridge

D018 přijímá úzký HTTP kontrakt v1, zatím bez implementace nebo deploymentu. Jediná normativní wire specifikace je [docs/INGESTOR.md §19](../docs/INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1). Bridge bezpečně rozliší current active source, poskytne autorizovaný přístup k privátní evidenci a uloží právě jeden validovaný Page JSON. Preferovaný runtime je samostatná malá Railway HTTP služba, ne legacy Ingestor worker.

Nedělá editorial interpretaci, OCR ani assembly. Source UUID v DB/API a SHA identita manifestu mají explicitní ověřenou vazbu. Zápis používá serverem odvozený D017 klíč, RFC8785 JCS/SHA-256, create-if-absent, durable idempotency binding a download verification. Rozdílný canonical obsah vrací 409 bez přepisu; nejistá persistence BLOCKED. Scopes/publication allowlist chrání každý endpoint, credentials zůstávají server-side a signed URLs mají 300 sekund. Kontrakt vyžaduje fencing vůči změnám source identity/readiness při zápisu; neurčuje novou DB tabulku.

## Assembler
Assembler spotřebovává Page JSONy jednoho vydání.

Spojuje části článků přes stránky, řeší continuations a vytváří canonical Article Records. Výsledné články ukládá do Supabase Storage a jejich identity, vztahy, stav a provenance do PostgreSQL.

Assembler nemá znovu interpretovat původní layout stránky. Pokud Page JSON neposkytuje dostatečnou jistotu, výsledek musí jít do review místo hádání.

## Composer
Composer pracuje nad canonical Article Records více publikací. Seskupuje články, které se týkají společného tématu nebo příběhu, a vytváří topic dossier. Není to ještě finální editorial selection.

## Translator
Translator pracuje až nad spolehlivě sestaveným textem. Je vhodným kandidátem pro API automatizaci, protože jde o řízenou transformaci známého textu, nikoli page-layout interpretation.

## Editorial
Editorial Workflow rozhoduje, co stojí za přenos, jak spojit perspektivy, co číst do hloubky a co publikovat. Completeness a curation zůstávají oddělené.

## Persistence
Supabase PostgreSQL drží identity, relationships, jobs, state, provenance a events.

Supabase Storage drží immutable sources, Technician artefakty, Page JSONy, assembled article artefakty a další validované výstupy.

Railway je worker/runtime a temporary workspace.

## Legacy boundary
Ingestor v1.1 (ingestor-v4-physical-map-v1.1) a Physical Map production path jsou superseded a neaktivní.

Physical Map může zůstat historický/debug artefakt nebo diagnostická evidence, ale není required input Ingestoru v2.0 ani canonical krok pipeline.

Visual Page Map, BODY_FLOW, bbox/overlap matching a block-ID assembly nejsou current architecture.

Acquisition je upstream problém. Technician není downloader/crawler a odstraněný watcher není current komponenta.
