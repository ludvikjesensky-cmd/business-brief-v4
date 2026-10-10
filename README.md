# Business Brief v4

> **Není hlavní, na co se díváš. Hlavní je, co vidíš.**

Business Brief v4 je česká redakční brána do kvalitního světového ekonomického a business tisku. Denní páteř tvoří Financial Times, The Wall Street Journal a Handelsblatt.

V4 nechce být další news briefing ani stroj na kompresi článků. Přenáší hodnotné myšlenky, otázky, argumenty, perspektivy a pozorování z dnešních textů.

## Dokumentace

**Jediný kanonický vstup do projektu je [PROJECT.md](PROJECT.md).**

PROJECT.md určuje, co číst podle typu práce a kde ověřovat provozní skutečnost.

Kanonická dlouhodobá paměť projektu je v `project-memory/`:
- SCOPE — co projekt je a není;
- CURRENT_STATE — současný konsolidovaný stav;
- ARCHITECTURE — platná architektura;
- DECISIONS — přijatá rozhodnutí a důvody;
- FAILURES — slepé cesty, které se nemají opakovat bez nové evidence;
- LESSONS — přenositelné poznatky;
- HISTORY — vývoj v1 → v4;
- OPEN_QUESTIONS — skutečně nerozhodnuté otázky;
- GLOSSARY — projektový jazyk.

Detailní současná dokumentace je záměrně malá:
- `docs/PRODUCT.md`
- `docs/EDITORIAL.md`
- `docs/SYSTEM.md`
- `docs/OPERATIONS.md`
- `docs/SOURCES_RIGHTS.md`
- `docs/EDITORIAL_MEMORY.md`

Předchozí v4 dokumentace byla při resetu 10. 10. 2026 přesunuta do `docs.archive/`. Archiv je historický zdroj a evidence, nikoli současná autorita.

## Základní produktová věta

**Dnešní vydání orientuje. Brief otevírá. Detail rozvíjí.**

Dnešní vydání nese systematickou coverage. Brief je redakční výběr. Detail přidává hloubku. Editorial Memory přidává kontinuitu. Úsudek zůstává čtenáři.

## Pro AI / novou konverzaci

Nezačínej čtením celého repository ani archivu. Začni `PROJECT.md`.

Před architektonickou změnou vždy zkontroluj DECISIONS a FAILURES. Před provozním tvrzením ověř live stav v operational Source of Truth. Starší Business Brief v1, v2 a v3 jsou historické Projects ve stejné family a slouží jako provenance a zdroj lessons, nikoli jako current code dependencies.
