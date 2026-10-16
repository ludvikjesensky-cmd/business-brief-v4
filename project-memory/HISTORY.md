# History — Business Brief family

## v1 — Completeness, provenance, production foundation
První generace definovala základní produkt: český přehled hodnoty FT, WSJ a Handelsblattu, důraz na úplnost, provenance, důvěru, Brief/Detail/Memory a robustní technickou pipeline. Silná stránka byla disciplína coverage; slabina byla rostoucí technická složitost a ambice rekonstruovat vydání velmi detailně.

## v2 — Understand the issue first
v2 posunula důraz k pochopení celého vydání před publikací a k tomu, aby se inteligence používala na editorial judgment. Posílila oddělení operational state v Supabase od dlouhodobých decisions v Markdownu a princip manuálního ověření před API automatizací.

## v3 — Evidence, contracts, semantic experiments
v3 formalizovala Technician, Ingestor/Physical Map, Semantic Mapper, Comparator a silné kontrakty/provenance. Přinesla důležité lekce o hranici mezi fyzickou evidencí a semantic interpretation. Praktické experimenty ukázaly, že spolehlivě skládat články z technické mapy je obtížné, drahé a křehké. Dokumentace se zároveň rozrostla do mnoha handoffů a specializovaných souborů.

## v4 — Editorial value first
v4 vědomě převzala důvěru, provenance, completeness a Memory, ale změnila definici hodnoty. Hlavní otázka už není jen „co musí čtenář vědět“, ale „co stojí za přenos do jeho přemýšlení“. Completeness se přesouvá do Dnešních vydání; Brief je skutečný redakční výběr. Důraz je na perspektivu, argument, otázku a čtenářskou hodnotu.

Technicky v4 znovu oddělila Technician a Ingestor od editorial interpretation, odstranila nefunkční watcher a otestovala Fast Editorial na reálném WSJ. Reálný API náklad ukázal, že full-edition placený modelový průchod v této podobě není ekonomicky přijatelný.

## Documentation reset — 2026-10-10
Dosavadní v4 docs byly archivovány a nahrazeny Project Memory standardem: PROJECT.md, project-memory/ a malou sadou tematických docs. Cílem je zachovat historii bez soupeřících zdrojů pravdy.

## Semantic layout research — 2026-10-12 až 2026-10-14
Physical Map byla doplněna experimenty s vision layoutem, BODY_FLOW, geometry matching a později block-ID assembly. Některé jednotlivé stránky byly částečně úspěšné, ale obecná spolehlivost article ownership, reading order a čistého textu zůstala nedostatečná a vyžadovala opakované ruční zásahy. Tyto experimenty jsou zachovány ve FAILURES, nikoli v current architecture.

## Ingestor v2 pivot — 2026-10-14
Projekt přijal nový generační řez: Ingestor v1.1 / Physical Map production path je superseded. Ingestor v2.0 je živá Chat role nad Technician Source Bundle, pracuje jednu stránku po druhé a vytváří jeden ověřený Page JSON na stránku.

Tím se page semantics přesouvá tam, kde lze opakovaně kontrolovat source image, textovou evidence a vlastní předchozí hypotézy. Automatizace se vrací až za stabilní Page JSON contract: Assembler skládá články, Composer seskupuje témata napříč zdroji, Translator je kandidát pro API transformaci a Editorial Workflow zůstává vrstvou redakčního judgmentu.

## Ordinary Chat read and first write acceptance — consolidated 2026-10-16
Site v3 added verified PNG MCP image delivery; private Site v4 added bounded page-isolated inline OCR extraction. Ordinary Chat then returned image + OCR successfully, closing the earlier separate-connector read gate (details in docs/INGESTOR.md §20).

Acceptance source: UUID `603e8242-ffe8-4e1d-a5de-9adb3da4d188`, source SHA `2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f`, source bundle SHA `e14e274810bbde45f738d94ca4a93f3eacefffb32bbb2221b259e2777a84e74d`, publication `the-wall-street-journal`, edition `2026-10-14`, variant `default`, 10 pages.

First production page 1 persisted as VERIFIED / CREATED at `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.0/page-0001.json`, artifact SHA `f135489008902816526cd4d2b73710e18e4833931f8adcae47af5ab793741e97`, 42424 B, readback identity verified, usable_for_assembly=true.

The object remains immutable technical acceptance evidence, product-superseded because it inventories irrelevant items, represents What's News digests separately and expands perspective metadata unnecessarily (F009). D019/D020 introduce relevant source-faithful extraction and a separate v3 generation; no v2 rewrite or new production pass occurred during consolidation. Acceptance facts were supplied by the user; raw runtime events stay in operational storage.

## Minimal v3 rollout and page-1 acceptance — 2026-10-16
Bridge commit 1442da050a0b3dcb4a5de9a11611a2b5ec9084c9 was pinned and deployed on Railway (7d1fa8aa-401d-4a2c-8fe0-5a4804eeb029, SUCCESS). The existing owner-private Site v4 needed no transport change. The PR chain remained open to avoid unrelated main-linked service deploys.

Post-deploy resolve → page-1 image + OCR → visual comparison → local v3 validation → one production persist ran through the connected plugin in Codex, using the ordinary-Chat-compatible transport. Six relevant article starts, no PerspectiveEvidence or rejected-item inventory, were stored at `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.1/page-0001.json`, SHA `bc287714ea5a290833976b7dfec6caf56f09a668e2c0d401c9e317ac246055e6`, 14,568 B. Receipt: STORED/CREATED, VERIFIED_WITH_NOTES, identity_matches=true, usable_for_assembly=true; downloaded SHA matched locally computed RFC8785 bytes. Notes preserve page-boundary fragments. Existing v2 bytes were never targeted; no next page or assembly ran. This establishes one-page acceptance, not corpus quality or a new separate ordinary-Chat session.
