# V3 Reconstruction Baseline

**Status:** SOURCE-BASED WORKING BASELINE  
**Purpose:** capture the proven mechanism of the original Fast Editorial experiment before adding later editorial philosophy  
**Source:** reconstruction produced by the original v3 experiment Chat from its own conversation history  
**Canonical:** no

This document is intentionally about **how the successful process worked**. It is not yet the final Business Brief constitution or onboarding prompt.

Where the old Chat distinguished between documented history and reconstruction, this document preserves that caution. Concrete field names below are working structures, not claims about an exact historical database schema.

---

## 1. Proven end-to-end chain

The reconstructed working sequence was:

```
Independent Issue Maps
→ Cross-Paper
→ Selective Deep Read
→ eight Editorial Review passes
→ verified Master Brief
```

Temporal / Memory context was useful, but was not a mandatory standalone pass.

One continuously working Chat carried the process. It read the newspaper issues, created independent frozen maps, compared them, returned to source articles, performed the editorial review and produced the Master Brief.

The important separation was between **editorial modes and artifacts**, not necessarily between separate Chats.

---

## 2. Reading principle

Three different kinds of completeness must remain distinct:

1. **Complete issue review**  
   The editor must inspect the whole edition, not only the front page or obvious business stories.

2. **Sufficient Issue Map**  
   Relevant editorial objects must be captured well enough to support later selection and return to source.

3. **Selective final Brief**  
   The final product must not reproduce the whole map.

Working rule:

> Read broadly, record proportionately, select boldly, explain precisely.

An Issue Map is not proof that every article has been understood deeply enough for final writing. It is a map for editorial judgment and for later return to source.

---

## 3. Continuity of one Chat

The original workflow benefited from live context that was richer than the saved artifacts.

The Chat carried:
- memory of article arguments, tone, examples and qualifications;
- memory of why it had made earlier editorial judgments;
- memory of differences between apparently similar stories;
- memory of corrections discovered during Deep Read;
- awareness of what the reader had already been told in the evolving Brief;
- rhythm and composition of the whole edition.

Persist:
- source identity and article location;
- frozen Issue Maps;
- priority and important decisions;
- Daily Topics and provenance;
- important uncertainties;
- interpretation changes;
- results of editorial review;
- final text;
- reasons for major changes;
- knowledge that must survive the conversation.

Do **not** try to persist every act of thinking. Working comparison, hesitation, candidate angles and rhythm can remain live editorial context.

Core rule:

> Persist state and consequential reasons. Do not turn every mental operation into an administrative object.

---

## 4. Independent Issue Maps

Each newspaper issue is first read as its own editorial world.

The map is frozen before another newspaper is allowed to alter its interpretation.

After freeze, later newspapers may change the **daily relevance** of an item, but they must not rewrite the original independent reading of that issue.

An Issue Map must not become:
- the final Brief;
- a few broad topics that dissolve individual articles;
- a front-page-only list;
- an automatic inventory of every text block;
- a map retrofitted to agree with other newspapers.

### Working Issue Map item

```yaml
item_id: ""
issue_id: ""

source_locator:
  pages: []
  continuation_pages: []
  source_ref: ""

headline: ""
headline_is_working_label: false
genre: news  # analysis | interview | opinion | editorial | lex | other

article_point: ""
editorial_value: ""

priority: CORE  # CANDIDATE | LOW

deep_read_candidate: false
deep_read_reason: ""

open_questions: []
structural_notes: []
```

The historical experiment did use CORE / CANDIDATE / LOW and Deep Read candidates. Other fields here are reconstruction structures for faithful reuse.

### Issue-level conclusion

Capture at minimum:
- issue identity and intake order;
- page count and reading mode;
- whether the whole issue was reviewed;
- important source limitations;
- counts by priority;
- main editorial currents;
- distinctive articles that should remain visible as individual objects;
- preliminary Deep Read candidates;
- frozen status.

The map freezes the independent judgment of that issue. It does not freeze the later daily synthesis.

---

## 5. Cross-Paper

After all Issue Maps are frozen, the unit of work changes:

```
article inside one newspaper
→ daily story supported by one or more articles
```

Cross-Paper is not only deduplication.

Articles may belong together when they jointly explain a sufficiently concrete:
- event;
- mechanism;
- problem;
- tension;
- strategic question.

They should remain separate when the commonality is merely a sector label, company name or broad keyword.

Strong single-source stories must remain eligible. Number of publications is not a quality score.

### Apparent disagreement check

Before declaring that publications disagree, check:
1. time / market snapshot;
2. metric;
3. market or population segment;
4. geography;
5. period;
6. fact vs forecast vs opinion.

Different results may be compatible descriptions of different slices of reality.

### Source contribution roles

Useful reconstructed roles:
- primary;
- supporting;
- contrasting;
- background.

These roles describe contribution, not prestige.

### Working Daily Topic

```yaml
topic_id: ""
day_id: ""

working_title: ""
central_question: ""
synthesis: ""
why_now: ""

decision: include  # reserve | exclude
decision_reason: ""

source_links:
  - item_id: ""
    role: primary  # supporting | contrasting | background
    contribution: ""

differences_and_tensions: []
open_questions: []

deep_read:
  status: pending
  focus: []
  note_ref: ""

interpretation_changes: []
```

Daily Topics are not necessarily the final editorial units of the Brief. Dramaturgy may later combine more than one Daily Topic into a single reader-facing unit without rewriting the underlying maps.

---

## 6. Selective Deep Read

Selective Deep Read was a real step between Cross-Paper and Editorial Review.

In the documented Day 2 workflow, all 12 INCLUDE topics were revisited before editorial writing.

"Selective" meant:
- do not reread all three newspapers at equal depth;
- return deeply to the source articles required for the selected daily stories.

Deep Read must do two jobs:

### A. Resolve known uncertainty
Example questions:
- Is the comparison monthly or year-to-date?
- Is a number intraday or closing?
- Is this a decision, negotiation or scenario?

### B. Discover unknown problems
Even a plausible synthesis must be tested against the source.

The purpose is not only fact checking. It is to verify whether the **meaning of the story** is correct.

Deep Read may:
- narrow a claim;
- split a mechanism;
- explain an apparent contradiction;
- change a topic title or synthesis;
- change include / reserve status if required;
- create wording guardrails for later writing.

### Working Deep Read Note

```yaml
note_type: deep_read_summary
topic_id: ""

source_passages:
  - item_id: ""
    locator: ""

initial_interpretation: ""
questions_before_reading: []

verified_findings: []
newly_discovered_problems: []
apparent_conflicts: []

interpretation_changed: false
interpretation_before: ""
interpretation_after: ""
change_reason: ""

wording_guardrails:
  safe_formulation: ""
  misleading_formulations: []

selection:
  before: include
  after: include
  change_reason: ""

remaining_uncertainties: []
status: done
```

Deep Read is distinct from later Verification:
- Deep Read verifies **understanding of the source story**.
- Verification checks **the claims actually written in the Brief**.

---

## 7. Eight Editorial Review passes

The documented experiment used eight passes:

1. Assignment Editor
2. Dramaturg
3. Story Editor
4. Brief Writer
5. Detail Editor
6. Verification Editor
7. Language & Style Editor
8. Editor-in-Chief

These are eight editorial perspectives. They do not require eight separate agents.

A pass must perform its judgment. It does **not** have to force a change.

"Pass with no change" is valid.

### Assignment Editor
Determines what belongs in the edition and the editorial role of topics. RESERVE can return when useful.

### Dramaturg
Builds hierarchy, order, grouping, pace and reader load. May combine multiple Daily Topics into one final editorial unit.

### Story Editor
Defines the actual point, tension and reader understanding of the main stories without inventing drama.

### Brief Writer
Writes the reader-facing edition from the approved selection and dramaturgy. Item lengths must follow editorial function, not uniform templates.

### Detail Editor
Checks that the Brief communicates a real point while preserving legitimate value for deeper Detail. The Brief must not become either a hollow teaser or a complete substitute.

### Verification Editor
Checks the claims as actually written: figures, scope, attribution, certainty, titles and implications. Passing Deep Read earlier does not remove this responsibility.

### Language & Style Editor
Improves natural Czech, rhythm, transitions, jargon and read-aloud quality without altering meaning or certainty.

### Editor-in-Chief
Judges the edition as a whole and may approve it unchanged or return a problem to the appropriate earlier stage.

---

## 8. Final quality gates

The reconstructed historical gates were:

### Coverage
Has something important disappeared from the day's picture?

Coverage is a safety net, not a requirement to include every mapped object.

### Hierarchy
Is it obvious what matters most and what is secondary?

Hierarchy appears in position, length and intensity of explanation.

### Curiosity
Does the edition create a legitimate desire to understand further without withholding the basic point?

### Trust
Are claims precise, proportionate and correctly attributed?

### Product fit
Does the result function as a Business Brief rather than a pile of summaries, an analyst report or a teaser?

### 90-second test
Can a fast reader obtain a real map of the day quickly?

This does not mean that the whole Brief must be readable in 90 seconds.

---

## 9. Minimal working artifacts

The reconstruction suggests a deliberately small artifact set:

```
day-context.yaml
issue-map-{publication}.yaml   # one per issue, frozen
daily-topics.yaml              # mutable through Deep Read
editorial-notes.yaml           # append-only reasoning and review record
master-brief.md                # versioned, final after review
```

Do not create a separate artifact merely because a mental role exists.

The original experiment also used technical run state and persistence controls, but those protected reliability rather than creating editorial quality.

---

## 10. What not to formalize

Keep these primarily editorial:
- recognition of importance;
- story angle;
- joining articles by mechanism;
- item length;
- number of lead stories;
- curiosity;
- return to sources;
- internal comparison and hesitation;
- whether a review pass changes the text.

Do not turn observed Day 1 / Day 2 counts into quotas.

Do not create eight independent agents merely because there are eight review perspectives.

Do not let workflow state begin to determine content.

Formalize mainly:
- independent Issue Map boundaries;
- freeze;
- provenance;
- return to source;
- significant interpretation changes;
- final quality review.

---

## 11. Continuity across days

The experiment benefited from knowledge of previous days, but did not establish a mandatory Temporal / Memory pass.

Previous-day context must not influence the independent Issue Maps of the new day.

After freeze, prior context can help distinguish:
- what is new;
- what continues;
- what changes previous interpretation;
- what is repetition;
- why today's development matters now.

A lightweight continuity input can include:
- previous final Brief;
- open story threads;
- last known state;
- important qualifications;
- source references.

Do not mistake recurrence for a trend automatically.

---

## 12. Current reconstruction boundary

This baseline deliberately does **not yet** define:
- the final Business Brief editorial constitution;
- the final onboarding prompt;
- the exact final Master Brief section template;
- database schemas;
- automation;
- multi-agent orchestration;
- integration with Deep / Memory infrastructure.

Those decisions come only after the proven mechanism above is combined with the product spirit and editorial constitution.
