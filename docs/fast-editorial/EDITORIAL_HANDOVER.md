# Fast Editorial — EDITORIAL_HANDOVER contract

Tento soubor je **kontrakt a lidsky čitelná šablona**, nikoli provozní source of truth.

Aktuální handover konkrétního dne žije v Supabase:

- project: `business-brief-v4`
- schema: `fast_editorial`
- table: `handover_state`

Nový Chat nesmí z tohoto souboru odvozovat aktuální stav dne. Musí načíst skutečný stav z Supabase.

## Kdy handover aktualizovat

Aktualizuj `fast_editorial.handover_state` na přirozených hranicích:

1. po každém frozen Issue Map;
2. po dokončení Cross-Paper;
3. po dokončení podstatného Deep Read bloku;
4. při přerušení práce uprostřed Editorial fáze;
5. po vytvoření VERIFIED Master Briefu;
6. při uzavření dne.

Není nutné aktualizovat handover po každé drobné stylistické změně.

## Co musí handover zachovat

- `day_id`
- poslední dokončený den, pokud existuje;
- `last_verified_brief_id`, pokud existuje;
- aktuální redakční stav;
- dokončené kroky;
- frozen issue identities;
- stav Cross-Paper;
- stav Deep Read;
- stav Editorial review;
- přesný další krok;
- blocking inputs;
- otevřené story threads;
- zděděné guardrails a corrections;
- source refs;
- artifact refs.

## Mutable versus history

`handover_state` je mutable current-state objekt.

Historie významných změn se nepřepisuje do handoveru. Patří do append-only `editorial_notes`, frozen artefaktů a konkrétních Brief versions.

Handover odpovídá na otázku:

> Kde práce stojí právě teď a co má další editor udělat jako první?

Editorial Notes odpovídají na otázku:

> Co významného se během práce rozhodlo, změnilo nebo opravilo?

## Startup nového Chatu

Nový Chat:

1. načte poslední relevantní `fast_editorial.days`;
2. načte odpovídající `handover_state`;
3. zkontroluje skutečné frozen issues;
4. načte topics + provenance;
5. načte Deep Read Notes a Editorial Notes;
6. načte poslední Brief version + gates;
7. načte relevantní active story_threads;
8. vlastními slovy shrne:
   - hodnotu Business Briefu,
   - aktuální stav,
   - co je frozen/closed,
   - převzaté corrections/guardrails,
   - otevřené otázky,
   - další konkrétní krok.

Pokud v Supabase není žádný aktivní den, nový Chat to řekne explicitně a zahájí nový den až po skutečném intake Reference Edition.

## Uzavření dne

Den lze označit `CLOSED` až když:

- existuje VERIFIED Master Brief;
- existuje aktuální `handover_state`;
- `verified_at` a `closed_at` odpovídají skutečnosti;
- další krok je pravdivý;
- otevřené story threads nejsou zaměněny za předem vybranou agendu dalšího dne.

## Story threads boundary

`fast_editorial.story_threads` jsou pouze lehká kontinuita Fast Editorialu.

Nejsou:
- Editorial Memory;
- Signal;
- Trend;
- RAG knowledge object;
- náhrada Deep/Memory větve.

Slouží jen k přenosu posledního doloženého stavu, toho, co už čtenář ví, důležitých kvalifikací, známých chyb a otázky, jaká další změna by byla materiální.
