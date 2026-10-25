# Fast Editorial — Continuity, Handoff & Editorial Memory

**Status:** GREENFIELD WORKING SPEC  
**Purpose:** preserve editorial understanding when work continues in a new Chat  
**Canonical:** not yet  
**Role:** continuity layer only; not a new editorial pass

---

## 1. Core principle

A process manual is not enough.

A new Chat needs three things:

1. **Stable working method** — how Fast Editorial works and why.
2. **Calibration examples** — what good editorial work actually looks like.
3. **Current editorial memory** — where the work stands and what matters now.

The goal is not to reproduce every token of the previous Chat.

The goal is to restore sufficiently similar editorial understanding that the next Chat can continue with the same standards and context.

---

## 2. Preserve continuity, do not fragment the newsroom

Default operating model remains:

> **One Chat handles one full editorial day and, where practical, several consecutive days.**

Handoff exists to recover continuity when a new Chat is necessary.

It is not a reason to split Issue Reading, Cross-Paper, Deep Read and Editorial Review into separate Chats.

---

## 3. The handoff package

### A. Stable Fast Editorial briefing

Use the current approved onboarding for:
- product purpose;
- editorial doctrine;
- issue independence;
- freeze;
- Cross-Paper;
- Selective Deep Read;
- Editorial Review;
- final gates;
- key boundaries and anti-patterns.

This foundation changes only when the editorial method itself changes.

Do not rewrite it after every day.

The reconstruction history should continue to distinguish:
- documented experiment behavior;
- strong reconstruction;
- uncertain / unproven details.

### B. Calibration examples

A new Chat should receive **one or two complete approved Master Briefs**, not only summaries.

The purpose is to teach:
- rhythm;
- hierarchy;
- varying item length;
- natural Czech;
- amount of explanation;
- balance between coverage and distinctive journalism;
- what a strong recommendation looks like;
- how much uncertainty is acceptable;
- what “alive, not AI-digest” means in practice.

Also provide a small set of decision examples using:

```
initial judgment
→ what the sources actually showed
→ correction
→ lesson
```

Calibration is not a style template to imitate mechanically.

It is evidence of editorial standards in action.

### C. Current editorial memory

This is the living handoff layer.

It should answer:

- where the work currently stands;
- what is already closed / frozen;
- what the next concrete step is;
- which stories remain open;
- what has already been explained to the reader;
- which interpretation errors must not recur;
- what new evidence would materially change the current story;
- where the underlying source artifacts live.

Editorial memory is not a chronological transcript.

It is **what the next editor needs in order to work well**.

---

## 4. Current work state

Keep a concise status block.

Recommended structure:

```yaml
editorial_state:
  last_completed_day: ""
  last_verified_brief_ref: ""

  active_day:
    date: ""
    status: ""

  completed_steps: []
  frozen_issue_maps: []

  cross_paper_status: not_started
  deep_read_status: not_started
  editorial_review_status: not_started

  next_step: ""

  source_refs: []
  artifact_refs: []

  blocking_inputs: []
```

Example of the level of specificity:

> Day 3: FT and WSJ are frozen. Handelsblatt is still missing. Cross-Paper has not started. Next step: independently read Handelsblatt. Existing FT/WSJ maps must not be adjusted to anticipated synthesis.

---

## 5. Editorial memory

Track only open or useful editorial context.

Recommended structure:

```yaml
story_threads:
  - thread_id: ""
    label: ""

    last_known_state:
      date: ""
      summary: ""

    what_reader_already_knows: []

    important_qualifications: []

    interpretation_to_avoid: ""

    next_material_change:
      - ""

    source_refs: []
    note_refs: []
```

Example logic:

A Treasury thread should not say only:

> rates are being watched

It should preserve the changing story, for example:

- price of capital;
- intraday crossing of a threshold;
- later composition of buyers;
- transmission into mortgages;

with dates and source references.

---

## 6. Memory must not determine tomorrow's importance

Editorial memory is supportive.

It must not decide in advance what today's newspapers are about.

Rule:

> **Read today's editions independently first. Use prior memory after freeze to recognize change, continuity, repetition or reinterpretation.**

Do not promote a recurring story merely because it existed yesterday.

Do not infer a trend merely from recurrence.

---

## 7. When to hand off

### Best time

Between two completed editorial days.

A new Chat begins the next day with:
- stable method;
- calibration examples;
- latest editorial memory.

### Acceptable time during a day

At a completed boundary such as:
- after a frozen Issue Map;
- after all three maps are frozen;
- after Cross-Paper;
- after Selective Deep Read;
- after a completed Editorial Review stage.

Avoid handing off in the middle of an unresolved editorial judgment if possible.

---

## 8. Do not wait for failure

Do not wait until a Chat is no longer usable.

After each completed editorial day, update:

- work state;
- open story threads;
- important corrections;
- what the reader has already been told;
- relevant source / note references.

This can be incorporated into the existing day retrospective.

It is **not a new editorial pass**.

During the day, frozen maps, Cross-Paper output, Deep Read notes and draft snapshots already provide natural recovery points.

---

## 9. Handoff comprehension check

After loading the handoff package, the new Chat should briefly restate:

1. How it understands the value of Business Brief.
2. Where the work currently stands.
3. What is already closed / frozen and must not be silently rewritten.
4. Which important corrections and open questions it inherits.
5. What exact next step it will perform.

This is a comprehension check, not another approval gate.

If the restatement is correct and the assignment is clear, the Chat may proceed.

---

## 10. Do not hand off summaries of summaries

The handoff memory must point back to original artifacts.

A new Chat should not receive only:
- previous Chat summary;
- summary of that summary;
- hand-edited digest of prior reasoning.

That creates progressive loss of:
- qualifications;
- provenance;
- uncertainty;
- source scope;
- original decisions.

Use memory as an index into:
- frozen Issue Maps;
- Daily Topics;
- Deep Read Notes;
- Editorial Notes;
- previous verified Briefs;
- source editions.

---

## 11. What cannot be transferred perfectly

The live context of the previous Chat cannot be reproduced exactly.

That includes:
- subtle article impressions;
- temporary comparisons;
- abandoned alternative angles;
- sense of rhythm;
- accumulated editorial intuition.

Do not try to encode all of it.

Instead restore similar working understanding through:

```
clear method
+ real approved outputs
+ consequential decision examples
+ current editorial memory
+ source access
```

This is sufficient to preserve much of the useful continuity without building a memory bureaucracy.

---

## 12. Minimal handoff package

A new Chat should normally receive:

### 1. Stable briefing
`06_INTEGRATED_ONBOARDING.md` or its later canonical successor.

### 2. Calibration pack
- 1–2 approved Master Briefs;
- several compact decision examples.

### 3. Current editorial memory
- current work state;
- open story threads;
- important corrections and guardrails;
- source / artifact references.

That is the default transfer bundle.

---

## 13. Anti-patterns

Do not create:

- a handoff after every editorial substep;
- a giant transcript summary;
- a new agent whose only job is memory;
- a mandatory temporal pass;
- memory-driven issue selection;
- dozens of story-thread objects with no editorial use;
- duplicated facts without source references.

The continuity layer should remain small, explicit and useful.

---

## 14. Core handoff rule

> **The next Chat must inherit not only what to do, but enough evidence of why previous good work was good.**

The purpose is not to teach the phrase “perform eight passes.”

The purpose is to teach the judgments that made those passes valuable.
