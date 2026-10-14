# Current State — Business Brief v4

**Last consolidated:** 2026-10-14
**Evidence:** lokální implementace, unit/integration testy, uložené placené Responses API odpovědi a vizuální/výběrový textový audit WSJ/HB. Runtime health ověřuj zvlášť.

## Current phase
Ingestor vytváří Physical Map a Visual Page Map; samostatný Assembler vykonává geometrii (D015). Produkční durable worker zůstává Physical Map-only. Lokální WSJ full-issue technický test je dokončený26/26; kvalita rekonstrukce článků acceptance neprošla. HB má jen částečný šestistránkový vzorek, ne full issue.

## Implementation validation
Mapper v1.1 má obecná pravidla pro titulky/standfirst, byline, sloupce, fotografie/grafy, infographic ownership a utility. Schéma v1 zůstává. Explicitní reasoning effort je opt-in a součást provenance/resume. Assembler hlásí source duplicity bez mazání textu. 125 testů prošlo; jeden původní dashboard HTTP/socket test je vynechán kvůli sandboxu. Syntetický fixture ani unit testy neprokazují vision quality.

## Experimental results and blockers
Kanonický protokol metrik, nákladů a konkrétních chyb je [visual-map-validation-2026-10-14](../docs/reference-days/visual-map-validation-2026-10-14.md). V1.1 re-test dokončil šest ze šesti volání; některé role/oddělení obsahu se zlepšily, geometrie a omissions nikoli konzistentně. Quality acceptance neprošla. HB native PDF má potvrzené duplicitní texty; jejich odstranění není implementováno. Starší HB timeouty mají neznámý billing a nebyly automaticky opakovány.

Původní manuální WSJ experimenty byly bez paid API. Navazující benchmarky byly uživatelem autorizované placené OpenAI calls; Fast Editorial se nespouštěl. F007 Railway render failure je historický a zůstává zachován; lokální WSJ test již dokončil technický průchod celého vydání. Úspora celé editorial pipeline při stejné kvalitě dosud prokázaná není. Paid Fast Editorial automation zůstává pozastavena (D011/F003).

## Next steps
1. Izolovat geometrickou přesnost na stejném kontrolním vzorku: neměnit model/prompt zároveň s rozlišením; nezvyšovat pokrytí broad boxes.
2. Odděleně vyřešit text-layer duplicity/decoding a ověřit přesný text; nepřenášet body OCR do Visual Mapperu.
3. Vyřešit transport/latency a uložit request/response důkazy bez automatických neznámých paid retries.
4. Před škálováním ověřit skutečné články, omissions, contamination, reading order a reviewed continuations; coverage/full completion není acceptance.

## Operational authority
Jobs, deployments, logs a live health ověřuj v Supabase/Railway. Lokální nástroje a PR nejsou potvrzením produkčního rollout ani editorial acceptance.
