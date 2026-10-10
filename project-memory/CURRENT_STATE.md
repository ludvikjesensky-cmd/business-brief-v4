# Current State — Business Brief v4

**Last verified from project documentation:** 2026-10-10  
**Runtime must be re-verified in Supabase/Railway before operational claims.**

## Current phase
v4 je ve fázi ověřování technického ingestion základu a levnějšího, spolehlivějšího editorial workflow. Produktová filozofie v4 je ustálená, ale plně autonomní ranní výroba není hotová.

## Known working / established
- Repository v4 a základní Railway/Supabase infrastruktura existují.
- Technician a Ingestor mají definované oddělené odpovědnosti a durable queue/storage model.
- Technician watcher byl odstraněn; automatické získávání WSJ se nesmí předpokládat.
- Dashboard/observability vrstva existuje a byla uvedena do provozu.
- WSJ 9 Oct 2026 prošel reálným Fast Editorial experimentem.

## Critical current constraints
- Fast Editorial reálný běh vytvořil nepřijatelný API náklad, přibližně USD 7.95 / 49 requests podle tehdejšího měření. Placené automatické spouštění je pozastaveno do cost redesign/auditu.
- v3 prokázala, že spolehlivá rekonstrukce článků pouze z technické/Physical Map je pro ranní produkt problematická; tento přístup se nesmí znovu navrhovat bez nové evidence.
- Source acquisition, zejména WSJ, není spolehlivě automatizovaný.
- Editorial workflow musí být ověřováno na skutečných vydáních, nikoli jen kontrakty/testy.

## Near-term direction
1. Udržet Technician/Ingestor jako levnou a auditovatelnou technickou vrstvu.
2. Změřit a redesignovat editorial processing tak, aby cena a čas byly přijatelné.
3. Zachovat úplnost zdrojové evidence, ale nepřevádět ji automaticky na drahou úplnou LLM rekonstrukci.
4. Ověřit workflow na malých reverzibilních testech před schedulerem/autonomií.
5. Runtime stav před dalším debuggingem ověřit přímo v Supabase/Railway.

## Not authoritative here
Konkrétní počty jobs, queue stav, poslední deployment a aktuální runtime health patří do provozního Source of Truth, nikoli do tohoto snapshotu.
