# Fast Editorial — Working Data Structures

**Status:** GREENFIELD WORKING SPEC  
**Source basis:** v3 Chat reconstruction  
**Canonical:** not yet  
**Important:** field names are reconstruction structures unless explicitly noted as historically documented.

---

## 1. Design rule

Data structures exist to support editorial judgment and return to source.

They must not become the product.

Core principle:

> Persist state, provenance and consequential reasons. Do not persist every act of thinking.

Avoid mandatory filler fields. Empty fields are better than administrative prose.

---

## 2. Minimal artifact set

Recommended minimum for one editorial day:

```
day-context.yaml
issue-map-{publication}.yaml   # one per publication; frozen
daily-topics.yaml              # mutable through Selective Deep Read
editorial-notes.yaml           # append-only reasoning / review log
master-brief.md                # versioned final product
```

Do not create one file per mental role merely because a role exists.

---

## 3. day-context.yaml

Purpose:
- identify the editorial day;
- identify source editions;
- preserve intake order and source limitations;
- support continuity without becoming a workflow engine.

```yaml
day_id: ""
editorial_date: "YYYY-MM-DD"

editions:
  - issue_id: ""
    publication: FT
    issue_date: "YYYY-MM-DD"
    intake_order: 1

    source:
      source_ref: ""
      page_count: null
      text_layer_usable: null
      reading_mode: ""
      ocr_performed: false

    limitations: []

previous_day:
  available: false
  master_brief_ref: ""
  open_story_threads: []
  important_qualifications: []
```

Previous-day context is supportive only and must not influence independent Issue Maps before freeze.

---

## 4. Issue Map

### 4.1 Issue Map item

Historically documented concepts:
- independent issue objects;
- CORE / CANDIDATE / LOW;
- Deep Read candidate;
- source location;
- issue-level freezing.

Working structure:

```yaml
item_id: ""
issue_id: ""

source_locator:
  pages: []
  continuation_pages: []
  source_ref: ""

headline: ""
headline_is_working_label: false

genre: news
# analysis | interview | opinion | editorial | lex | other

article_point: ""
editorial_value: ""

priority: CORE
# CANDIDATE | LOW

deep_read_candidate: false
deep_read_reason: ""

open_questions: []
structural_notes: []
```

### 4.2 Issue-level conclusion

```yaml
issue_id: ""
day_id: ""
publication: ""
issue_date: "YYYY-MM-DD"
intake_order: null

source:
  source_ref: ""
  page_count: null
  reading_mode: ""
  text_layer_usable: null
  ocr_performed: false

coverage:
  all_pages_reviewed: false
  omitted_content_categories: []
  limitations: []

counts:
  total: null
  core: null
  candidate: null
  low: null
  deep_read_candidates: null

editorial_currents: []
distinct_articles_to_preserve: []
issue_contribution: ""

status: frozen
frozen_at: ""
process_caveats: []
```

### Freeze semantics

Frozen means:
- original independent interpretation is preserved;
- downstream relevance may change;
- later newspapers do not rewrite the map.

If an objective correction is required later:
- preserve the original snapshot;
- record the correction and reason downstream.

---

## 5. Daily Topic

Cross-Paper changes the unit from article to daily story.

```yaml
topic_id: ""
day_id: ""

working_title: ""
central_question: ""
synthesis: ""
why_now: ""

decision: include
# reserve | exclude

decision_reason: ""

source_links:
  - item_id: ""
    role: primary
    # supporting | contrasting | background
    contribution: ""

differences_and_tensions: []
open_questions: []

deep_read:
  status: pending
  # done
  focus: []
  note_ref: ""

temporal_context:
  used: false
  previous_day_refs: []
  relevant_change: ""
  limitations: ""

interpretation_changes: []
```

### Source role semantics

- **primary**: carries the core story;
- **supporting**: adds evidence or another useful dimension;
- **contrasting**: supplies genuine counter-pressure or different interpretation;
- **background**: provides context.

Do not label something “contrasting” until time, metric, segment, geography, period and fact/opinion differences have been checked.

---

## 6. Selective Deep Read Note

```yaml
note_type: deep_read_summary
topic_id: ""

source_passages:
  - item_id: ""
    locator: ""

initial_interpretation: ""
questions_before_reading: []

verified_findings:
  - claim: ""
    evidence_ref: ""
    scope_or_qualification: ""

newly_discovered_problems: []

apparent_conflicts:
  - issue: ""
    explanation: ""

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

Deep Read Notes should preserve:
- what was originally believed;
- what source reading established;
- what changed;
- what wording is now safe;
- what remains uncertain.

---

## 7. Editorial Note

Use one append-only note stream for meaningful editorial decisions and review results.

```yaml
note_id: ""
note_type: ""
day_id: ""

scope:
  issue_ids: []
  topic_ids: []
  brief_version: null

review_question: ""

findings: []

decisions:
  - decision: ""
    reason: ""
    evidence_refs: []

changes: []
unresolved: []

result: pass
# needs_revision | informational

next_action: ""
artifact_refs: []
```

Useful note types may include:
- issue_map_snapshot;
- process_observation;
- cross_paper_map;
- deep_read_summary;
- deep_read_changed_interpretation;
- editorial_selection;
- dramaturgy_plan;
- story_angles;
- master_brief_draft;
- detail_gap_review;
- verification_review;
- language_style_review;
- editor_in_chief_review;
- day_retrospective.

Do not treat the historical names as mandatory storage schema.

---

## 8. Master Brief metadata

```yaml
day_id: ""
edition_date: "YYYY-MM-DD"
version: 1

status: verified
# draft | verified

canonical_text_ref: ""

source_issue_ids: []
source_topic_ids: []

editorial_review:
  assignment: pass
  dramaturgy: pass
  story: pass
  writer: completed
  detail: pass
  verification: pass
  language_style: pass
  editor_in_chief: pass

final_gates:
  coverage: pass
  hierarchy: pass
  curiosity: pass
  trust: pass
  product_fit: pass
  ninety_second_test: pass

editorial_units:
  - unit_id: ""
    function: main_story
    # coverage | watchlist | curated
    topic_ids: []
    source_refs: []

known_limitations: []
review_note_refs: []
verified_at: ""
```

`editorial_units` is a working provenance structure, not a claim about exact historical materialization.

---

## 9. State model

Use only the states that protect editorial integrity.

### Issue Map
- working
- frozen

### Daily Topics
- working
- deep_read_pending
- deep_read_complete

### Master Brief
- draft
- verified

Avoid building a large state machine before the process proves it needs one.

---

## 10. What not to encode

Do not create mandatory machine fields for:
- “importance score”;
- exact number of lead stories;
- fixed item lengths;
- curiosity score;
- number of source publications;
- number of edits per review pass;
- a mandatory taxonomy of every story.

Do not use observed Day 1 / Day 2 counts as quotas.

---

## 11. Provenance requirement

Every downstream claim should be traceable through:

```
Master Brief unit
→ Daily Topic
→ Issue Map item
→ source locator
```

The purpose is to make source return easy.

The purpose is not to replace the source with increasingly elaborate metadata.
