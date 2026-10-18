# Failures — Business Brief v4

## F001 — Rekonstrukce článků z technické/Physical Map
**Origin:** zejména v3–v4.  
**Goal:** z fyzické mapy vydání spolehlivě rekonstruovat články a jejich continuations.  
**Result:** cesta byla křehká, publication/layout dependent a náročná na ověřování; pro ranní produkt nebyla spolehlivým univerzálním základem.  
**Lesson:** technická/geometrická evidence sama neurčuje article truth.  
**Status 2026-10-14:** production path opuštěna; Ingestor v1.1 je superseded D014.  
**Retry only if:** nová skutečnost prokáže zásadně lepší univerzální mechanismus, ne jen další heuristickou vrstvu.

## F002 — Předčasná složitost pipeline
**Origin:** v1–v3.  
**Result:** technická architektura a množství rolí/dokumentů rostly rychleji než ověřená čtenářská hodnota.  
**Lesson:** architecture follows verified product; role ≠ agent ≠ API call.

## F003 — Fast Editorial full-edition API economics
**Origin:** v4, WSJ 9 Oct 2026.  
**Approach:** page-level model calls + issue synthesis pro celé vydání.  
**Observed:** přibližně USD 7.95 za jediný reálný průchod, kolem 49 requests podle zaznamenaného experimentu.  
**Impact:** nepřijatelné pro rutinní ranní provoz v této podobě.  
**Retry only if:** cost model je předem spočítán a malý acceptance test prokáže přijatelnou cenu při zachování kvality.

## F004 — WSJ automatic watcher/acquisition
**Origin:** v4.  
**Result:** watcher nebyl dostatečně spolehlivý a byl odstraněn z Railway i experimentální větve.  
**Lesson:** acquisition nesmí být skrytý předpoklad downstream pipeline.  
**Retry only if:** existuje nová spolehlivá acquisition capability a je ověřena odděleně.

## F005 — Handoff/status proliferation
**Origin:** v1–v4 documentation.  
**Result:** STATUS, HANDOFF, NEW_CONVERSATION_HANDOFF, V4_HANDOFF, dated PROGRESS a další dokumenty soutěžily o autoritu.  
**Lesson:** jeden PROJECT.md + jeden CURRENT_STATE; history/decisions/failures mají vlastní domovy.

## F006 — Automatizovat před ověřením editorial workflow
**Origin:** zkušenost v2–v4.  
**Result:** technicky funkční automatizace neprokazuje editorial value.  
**Lesson:** nejdřív skutečný referenční den a lidské acceptance, potom škálování.

## F007 — Překrývající se Railway deploye/logy při full-issue render testu
**Date / origin:** 2026-10-12, WSJ 26 stran.  
**Goal:** rozšířit Visual Page Map ověření na celé vydání.  
**Observed:** orchestrace deployů/logů zablokovala čisté dokončení full-issue validation.  
**Lesson:** laboratorní orchestrace nesmí být zaměněna za ověřenou produkční schopnost.  
**Status:** experimentální větev byla později opuštěna z širších důvodů F008.

## F008 — Jednorázový semantic/API pass nenahradil iterativní lidsky vedenou interpretaci
**Date / origin:** 2026-10-12 až 2026-10-14.  
**Goal:** automatizovaně nebo jedním modelovým průchodem určit article ownership, reading order a věrohodně sestavit text z komplexních novinových stran.  
**Tried:** Visual Page Map, BODY_FLOW, geometry/overlap execution, full-page model calls, controller-directed block-ID assembly a další varianty mezi Physical Map a final article textem.  
**Observed:** jednotlivé stránky mohly vypadat slibně, ale kvalita nebyla stabilní napříč layouty; chyby v hranicích, ownership, omissions a contamination vyžadovaly opakované lidsky vedené kontroly. API průchod navíc není vhodné místo pro dlouhou konverzační iteraci.  
**Cost/risk:** vysoký vývojový čas; u Fast Editorial navíc nepřijatelný API cost.  
**Lesson:** page semantics je potřeba řešit v live conversation nad source evidence. Previous model output nesmí být evidence; každá oprava se musí vracet k source page.  
**Decision:** D014.  
**Retry only if:** nový přístup prokáže na reálném corpus srovnatelnou iterativní spolehlivost, auditovatelnost a výrazně lepší ekonomiku.

## F009 — Valid persistence with an overgrown content contract
**Date:** consolidated 2026-10-16.
**Goal:** faithful relevant article extraction on WSJ page 1.
**Tried/result:** v2 production persistence technically passed, but mandatory irrelevant inventory, separate What's News digests and large perspective objects overgrew the intended page handoff.
**Risk:** a VERIFIED readback/usable_for_assembly flag could be mistaken for product acceptance.
**Resolution:** retain the object as superseded acceptance evidence; D019/D020 simplify content in a new namespace.
**Retry only if:** an explicit downstream use requires richer metadata and separately validates its value; never overwrite the existing object.

## F010 — JSON-only output bucket blocked first PNG acceptance
**Date:** 2026-10-18. **Goal:** first v4 page-2 asset persistence. **Observed:** local writer tests passed, but the retained production bucket allowed only application/json (5 MiB), so first PNG create returned PERSISTENCE_UNVERIFIED/UNKNOWN. Both durable claims stayed PENDING; live inspection found zero v4 objects. **Resolution:** tested additive deployment hook allows image/png and a 32 MiB limit, preserves private access and existing MIME types/objects, verifies configuration readback. Original request/key retry completed STORED/CREATED with the full set verified. **Lesson:** include retained bucket capability/configuration in rollout tests, not just binary writer correctness; no overwrite/delete/claim expiry is a recovery strategy. **Status:** resolved.
