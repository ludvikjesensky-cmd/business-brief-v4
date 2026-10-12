# Architecture — Business Brief v4

Architektura odděluje fyzickou evidenci, interpretaci, editorial judgment a publikaci.

Conceptual flow: closed source edition → Technician → validated Source Bundle → Ingestor → neutral Physical Map/evidence → editorial discovery/reading → cross-source editorial workflow → Master editorial truth → Brief/Detail/channel adaptations.

Technician je technický gateway: identity, immutable original, SHA/provenance, OCR, page evidence, mechanický split, validace a atomic handoff. Nedělá editorial interpretation.

Ingestor vytváří neutrální fyzickou/geometrickou/textovou reprezentaci. Physical Map je evidence layer, nikoli article truth.

Editorial vrstva odděluje úplnou znalost vydání od redakčního výběru. Fast Editorial byl experiment pro discovery, ne automaticky finální architektura; jeho současný cost profile je constraint.

Supabase PostgreSQL drží identity, relationships, jobs, state, provenance a events. Supabase Storage drží immutable sources a validované artefakty. Railway je worker/runtime a temporary workspace.

Dnešní vydání nese completeness. Brief je kurátorský. Detail rozvíjí hloubku. Editorial Memory přidává kontinuitu. Kanály adaptují jednu redakční pravdu.

Acquisition je upstream problém. Technician není downloader/crawler a odstraněný watcher není current komponenta.

## Experimental local tooling
Visual Page Map v1 má samostatný CLI pro ověřený PDF/Physical Map → JPEG → dodanou nebo opt-in vision mapu → geometrické sestavení → coverage/provenance/editorial handoff. Produkční tok výše ani workery se tím nemění; nejde o nasazenou náhradu Fast Editorial. Kontrakt, moduly a provozní použití mají jediný detailní domov v [docs/SYSTEM.md](../docs/SYSTEM.md#visual-page-map-v1--implementace-a-spuštění). Stav acceptance je v CURRENT_STATE, pravidla D013/D014 a gate D007/D011.
