# Architecture — Business Brief v4

Architektura odděluje fyzickou evidenci, interpretaci, editorial judgment a publikaci.

Conceptual flow: closed source edition → Technician → validated Source Bundle → Ingestor [Physical Map + Visual Page Map] → Assembler → editorial discovery/reading → cross-source editorial workflow → Master editorial truth → Brief/Detail/channel adaptations.

Technician je technický gateway: identity, immutable original, SHA/provenance, OCR, page evidence, mechanický split, validace a atomic handoff. Nedělá editorial interpretation.

Ingestor vytváří **obě mapy**: neutrální fyzickou/geometrickou/textovou Physical Map a samostatnou Visual Page Map určující layout a reading order. Vision mapper je jeho interní fáze; sémantiku nezapisuje do Physical Map. Physical Map zůstává evidence layer, nikoli article truth.

Assembler je samostatná deterministická role. Konzumuje obě mapy, geometricky sestavuje text, zachovává provenance, provádí schválená propojení pokračování a označuje mezery/nejednoznačnosti. Nevytváří mapy ani neprovádí editorial selection nebo vlastní modelový úsudek.

Editorial vrstva odděluje úplnou znalost vydání od redakčního výběru. Fast Editorial byl experiment pro discovery, ne automaticky finální architektura; jeho současný cost profile je constraint.

Supabase PostgreSQL drží identity, relationships, jobs, state, provenance a events. Supabase Storage drží immutable sources a validované artefakty. Railway je worker/runtime a temporary workspace.

Dnešní vydání nese completeness. Brief je kurátorský. Detail rozvíjí hloubku. Editorial Memory přidává kontinuitu. Kanály adaptují jednu redakční pravdu.

Acquisition je upstream problém. Technician není downloader/crawler a odstraněný watcher není current komponenta.

## Experimental local tooling
`bb-ingestor` / `extract_maps` implementuje dvoumapový kontrakt a `ingestor-output.json` handoff; `bb-assembler` jej ověřuje a sestavuje články. Původní `bb-visual-page-map` zůstává laboratorní rozhraní. Produkční durable Ingestor worker nadále vytváří pouze Physical Map; přechod queue na nový kontrakt zatím není nasazen. Nejde o nasazenou náhradu Fast Editorial. Kontrakt, moduly a provozní použití mají jediný detailní domov v [docs/SYSTEM.md](../docs/SYSTEM.md#visual-page-map-v1--implementace-a-spuštění). Stav acceptance je v CURRENT_STATE, pravidla D013–D015 a gate D007/D011.
