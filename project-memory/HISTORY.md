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
