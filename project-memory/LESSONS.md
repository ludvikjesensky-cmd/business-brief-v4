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

## L011 — Sémantický úsudek a geometrické vykonání mají odlišný vstup
**Origin:** WSJ 2026-10-12, strany 5 a 2. Člověku podobné čtení layoutu může určit vision model z low-res obrázku; textovou věrnost a provedení mapy zajišťuje Physical Map + Python. Explicitní BODY_FLOW/reading order odstraňuje potřebu znovu odhadovat tok v kódu. Nezaměňovat tento princip za ověřenou generalizaci na celé vydání.

## L012 — Hranice objektu je součást kontraktu
**Origin:** strana 2. Graf zahrnuje i osy, legendu a poznámky; fotografie vyžaduje skutečný bbox overlap, jinak mohou mizet sousední řádky. Správná identifikace článku nezaručuje úplné a čisté tělo. Detail a navržený, zatím neověřený threshold jsou v docs/SYSTEM.md.

## L013 — Ověřuj jednotlivé stupně a nevoď cenu z velikosti JPEG
**Origin:** low-res a full-issue experiment. Layout lze zkoušet bez OCR body textu a bez placeného API; rendering, semantic mapping, assembly a editorial quality jsou samostatné úrovně ověření. Malý obraz může pomoci ekonomice, skutečnou cenu však určí zvolený model a měření. Velké binární/base64 výstupy nepatří do logového transportu a paralelní deploye znejasňují experiment.
