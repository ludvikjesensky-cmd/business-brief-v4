# Fast Editorial — Current Editorial Memory

**Status:** LIVE HANDOFF ARTIFACT  
**Purpose:** current work state and useful cross-day editorial context  
**Update cadence:** after each completed editorial day and when a handoff becomes necessary  
**Canonical:** operational continuity artifact, not product doctrine

---

## 1. Current work state

```yaml
editorial_state:
  last_completed_day: ""
  last_verified_brief_ref: ""

  active_day:
    date: ""
    status: not_started

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

At present, this file is intentionally initialized without an active production day.

Do not import historical experiment Day 3 as current operational state.

---

## 2. Open story threads

Add only threads that are useful for future editorial work.

```yaml
story_threads: []
```

For each active thread use:

```yaml
- thread_id: ""
  label: ""

  last_known_state:
    date: ""
    summary: ""

  what_reader_already_knows: []

  important_qualifications: []

  interpretation_to_avoid: ""

  next_material_change: []

  source_refs: []
  note_refs: []
```

---

## 3. Important inherited corrections

Record durable editorial guardrails discovered during recent work.

Do not duplicate the full calibration pack here.

Only include corrections that remain operationally relevant to active story threads.

```yaml
active_corrections: []
```

---

## 4. Handoff note

When a Chat hands work to another Chat, append:

```yaml
handoff:
  from_day: ""
  created_at: ""

  closed_artifacts: []
  immutable_or_frozen: []

  inherited_open_questions: []
  inherited_guardrails: []

  exact_next_step: ""

  source_refs: []
  artifact_refs: []
```

---

## 5. Update rule

After each completed day:

- point to the verified Master Brief;
- clear completed active-day workflow state;
- retain only editorially useful open story threads;
- update what the reader has already been told;
- preserve important qualifications;
- record what future evidence would represent a real change.

Do not turn this into a full history of Business Brief.

History belongs in source artifacts and project history.

This file is a working memory for the next editorial Chat.

---

## 6. Independence rule

This memory must not determine the independent Issue Maps of the next day.

Use it after today's maps are frozen to recognize:

- continuity;
- change;
- contradiction;
- repetition;
- reinterpretation.

Memory is context.

It is not tomorrow's assignment editor.
