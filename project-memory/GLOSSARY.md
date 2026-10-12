# Glossary — Business Brief v4

**Dnešní vydání / Today's Editions** — úplná orientační vrstva nad sledovanými vydáními; nese completeness.

**Brief** — kurátorský ranní produkt; vybírá to, co stojí za pozornost/přenos do přemýšlení.

**Detail** — hlubší transformační redakční zpracování vybraného textu nebo tématu.

**Project Memory** — dokumenty v `project-memory/` o projektu samotném: stav, decisions, failures, lessons, history.

**Editorial Memory** — znalostní infrastruktura produktu nad zdroji, články, tématy, tvrzeními a historií. Není Project Memory.

**Technician** — technický gateway od source edition k validovanému Source Bundle.

**Source Bundle** — immutable original + připravené deriváty + page evidence + manifest/provenance.

**Ingestor** — převádí připravený zdroj na neutrální fyzickou/textovou evidenci.

**Physical Map** — geometrická/textová evidence dokumentu bez editorial interpretace.

**Fast Editorial** — v4 experimentální first-edition discovery worker; není automaticky finální produkční architektura.

**Extraction miss** — obsah ve vydání existoval, ale technická/evidence vrstva jej nezachytila.

**Editorial omission** — obsah byl známý, ale redakce jej vědomě nezařadila.

**Master editorial truth** — schválené společné redakční jádro, z něhož vznikají kanálové adaptace.

**Reference day/edition** — reálné vydání používané k lidskému acceptance a porovnávání workflow.

**Visual Page Map / semantic layout** — experimentální sémantická mapa článků, jejich oblastí, reading order a vložených/vyloučených objektů odvozená z obrazu stránky. Je oddělená od Physical Map.

**Visual Page Mapper** — vision role vytvářející Visual Page Map; v1 má lokální opt-in API adaptér, neprovádí OCR těla ani editorial deep read.

**BODY_FLOW** — uspořádaný seznam explicitních oblastí těla článku, podle kterého Python skládá zdrojový text.

**Visual footprint** — celá plocha objektu včetně přidružených popisků; u grafu zahrnuje osy, legendu a poznámky.

**Page-map envelope** — v1 serializovaný layout spolu s binding k original/prepared PDF, Physical Map a renderu, layout hash a mapper proveniencí; v CLI artefaktech `maps/pNNNN.json`. Strojový layout kontrakt je `visual_page_map.py` / CLI `schema`.

**Block accounting** — rozdělení Physical Map bloků na assigned/excluded/unmatched/ambiguous. Neprokazuje sémantickou úplnost vydání ani správnost exclusions.
