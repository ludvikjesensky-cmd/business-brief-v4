# Fast Editorial

**Status:** CANDIDATE READY FOR ACCEPTANCE  
**Canonical status:** NOT YET CANONICAL

This directory contains the new Fast Editorial rebuilt from:
- the successful v3 Chat experiment;
- the original Chat's reconstruction of its own working method;
- the Business Brief v4 product and editorial doctrine.

The previous Fast Editorial design remains suspended under:

`docs/suspended/fast-editorial-pre-greenfield/`

Do not use those suspended briefings as operating instructions.

---

## Main handoff

### `FAST_EDITORIAL_START_HERE.md`

This is now the **primary complete handoff for a new Fast Editorial editor**.

It is intentionally comprehensive. It transfers:
- why Business Brief exists;
- how the editor should think;
- the reconstructed v3 working method;
- the v4 perspective / reading-value doctrine;
- Issue Map, freeze and Cross-Paper;
- Selective Deep Read;
- eight Editorial Review passes;
- final quality gates;
- Editorial Notes;
- difficult decision cases;
- cross-day continuity;
- practical structures and field semantics;
- calibration cases;
- handoff principles;
- evidence boundaries.

It now includes the current Fast Editorial persistence, input, Master Editorial Truth, handover and channel-boundary contracts. Deep/Memory infrastructure remains outside the Fast Editorial handoff.

The untouched source produced by the original v3 experiment Chat is preserved at:

`reference/FAST_EDITORIAL_START_HERE_V3_CHAT_SOURCE.md`

---

## Normal startup for a new Chat

A new editor should receive:

1. `FAST_EDITORIAL_START_HERE.md`
2. `EDITORIAL_HANDOVER.md` as the handover contract plus the actual `fast_editorial.handover_state` from Supabase
3. the authentic approved V3 calibration Briefs in `reference/V3_APPROVED_MASTER_BRIEFS.md`
4. relevant source editions and saved editorial artifacts for the active day

After loading them, the Chat should briefly state:
- what value Business Brief is meant to create;
- where the work stands;
- what is already frozen / closed;
- what important corrections or open questions it inherits;
- what exact next step it will perform.

This is a comprehension check, not an approval gate.

---

## Supporting reference documents

The files `00_...` through `09_...` are **development and reconstruction references**, not the normal startup surface.

They preserve:
- reconstruction evidence;
- workflow decomposition;
- working data structures;
- v3-only mechanism control;
- anti-overformalization guardrails;
- Business Brief spirit;
- earlier synthesis drafts;
- continuity design;
- calibration notes;
- a provisional editorial-memory structure.

Use them when:
- auditing why a rule exists;
- comparing the integrated handoff with the original reconstruction;
- changing the method;
- running regression analysis.

Do not require a normal daily editor to read them all.

---

## Reconstructed operating chain

```
Complete edition A
→ independent Issue Map
→ freeze

Complete edition B
→ independent Issue Map
→ freeze

Complete edition C
→ independent Issue Map
→ freeze

Three frozen Issue Maps
→ Cross-Paper
→ Selective Deep Read
→ eight Editorial Review passes
→ final quality gates
→ verified Master Brief
```

Default model: **one continuously working Chat for the editorial day and, where practical, several consecutive days.**

---

## Current open work

The Closure Pass is complete: authentic Day 1 v2 / Day 2 v1 calibration, handover contract, Supabase persistence invariants, durable input contract, Master Editorial Truth schema and Publishing boundary are implemented.

Before declaring Fast Editorial canonical, one acceptance step remains:

1. regression-test the complete handoff in a genuinely clean Chat against a real Reference Edition;
2. compare the result with the historical experiment and approved V3 examples;
3. adjust only if that clean-room test reveals a real editorial gap or unnecessary formalism.

Do not add new architecture merely for completeness.
