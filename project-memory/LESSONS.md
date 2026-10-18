# Lessons — Business Brief v4

## L001
Úplnost a redakční výběr nejsou protiklady, pokud žijí v různých vrstvách.

## L002
Article/event importance není totéž co reading value. Text může být cenný způsobem vidění i bez dominantní headline události.

## L003
Perspektiva autora je informace. Summary, které zachová fakta a ztratí argument, může být fakticky správné a produktově mrtvé.

## L004
Provenance, nejistota a možnost auditu nejsou interní technické luxusy; jsou součást důvěry produktu.

## L005
Modelová inteligence patří tam, kde přidává úsudek. Mechanickou práci má dělat kód/SQL/parser, pokud stačí.

## L006
Nejprve ověř capability, input, failure modes a cenu nejmenším reverzibilním testem. Až potom investuj do automatizace.

## L007
Nová generace musí zdědit znalost předchozí generace, ne nutně její architekturu.

## L008
Operational truth patří do databáze/logů. Markdown má držet význam, rozhodnutí, stav a poučení.

## L009
Zdrojové acquisition a downstream processing jsou oddělené problémy. Nespolehlivý upstream nelze zamaskovat lepším workerem.

## L010
Jedna redakční pravda umožňuje konzistentní web, e-mail a audio bez paralelních obsahových realit.

## L011 — HISTORICAL / SUPERSEDED experiment — Sémantický úsudek a geometrické vykonání mají odlišný vstup
**Origin:** WSJ 2026-10-12, strany 5 a 2. Člověku podobné čtení layoutu může určit vision model z low-res obrázku; textovou věrnost a provedení mapy zajišťuje Physical Map + Python. Explicitní BODY_FLOW/reading order odstraňuje potřebu znovu odhadovat tok v kódu. Nezaměňovat tento princip za ověřenou generalizaci na celé vydání.

## L012 — Hranice objektu je součást kontraktu
**Origin:** strana 2. Graf zahrnuje i osy, legendu a poznámky; fotografie vyžaduje skutečný bbox overlap, jinak mohou mizet sousední řádky. Správná identifikace článku nezaručuje úplné a čisté tělo. Tento bbox experiment je historical/superseded (F008); nejde o současný production threshold.

## L013 — Ověřuj jednotlivé stupně a nevoď cenu z velikosti JPEG
**Origin:** low-res a full-issue experiment. Layout lze zkoušet bez OCR body textu a bez placeného API; rendering, semantic mapping, assembly a editorial quality jsou samostatné úrovně ověření. Malý obraz může pomoci ekonomice, skutečnou cenu však určí zvolený model a měření. Velké binární/base64 výstupy nepatří do logového transportu a paralelní deploye znejasňují experiment.

## L014 — Transport acceptance and content acceptance are separate
Valid schema, stored bytes and identity readback prove persistence, not faithful prose or useful selection. Ordinary Chat integration must be tested in ordinary Chat; Codex HTTPS alone was insufficient. The ordinary Chat read gate is now closed, while full-corpus acceptance remains open (Q010, F011).

## L015 — Minimal extraction preserves editorial value
Carry source-faithful, visually checked text forward and interpret the full article downstream. Mandatory interpretation and rejected-item inventories can obscure the useful handoff. An immutable contract correction needs a new generation, not a silent rewrite.

## L016 — Visual acceptance requires inspection of the actual crop
F011 shows that SHA/readback proves byte identity, not completeness of the intended visual. Render every crop from the authoritative PNG using writer-equivalent floor/ceil bounds, inspect each image independently for all edges, labels, legend and ownership, then assert visual_checked:true before persistence. A bbox on the full-page image is insufficient. Immutable defects require explicit correction provenance and downstream selection, not overwrite.

## L017 — Preserve semantic structure without duplicating layout
Reconstruct text; preserve visuals as crops. Pull quotes are presentation/layout, not new semantic content: do not duplicate them into prose, items or assets. A distinct boxed prose sidebar remains an editorial item. A visually verified ad-only page can canonically persist items:[] with explanatory notes and no article assets. Preserve source-visible internal article subheads in faithful prose when semantically part of the article. Reported coverage across generations and technical usable_for_assembly flags do not establish a homogeneous or fully visually accepted corpus.
