# Day 1 replay manifest — 2026-09-14

Status: **baseline identified; source artifacts pending extraction from v3 Supabase**

This replay intentionally preserves the v3 Fast Editorial process. It is not a redesign.

## Verified v3 identity

- editorial date: `2026-09-14`
- v3 editorial day id: `70cb878b-5bf5-4913-90c7-4b440f6cbb69`
- run mode: experiment
- final v3 state: completed

## Frozen source maps

Expected provisional items:

| Publication | Items |
|---|---:|
| Handelsblatt | 32 |
| Financial Times | 33 |
| Wall Street Journal | 37 |
| **Total** | **102** |

The three maps must be treated as independently frozen. No replay step may retrospectively modify one map after viewing another publication.

## Cross-paper baseline

- expected daily topics: **24**

## Brief baselines

### Brief v1
- id: `e63566b5-b0e6-45e8-8664-1f839408d0b9`
- status: verified
- structured `brief_items`: 13
- role: original Day 1 experiment baseline

### Master Brief v2
- id: `30d0e38c-38fb-4db4-9c19-e11209a853f8`
- status: verified
- structured `brief_items`: 0
- full text is expected in `daily_briefs.content_md`
- role: same information base, recomposed through Editorial Workflow v1

## Acceptance target

The replay is successful when the v4 Chat-driven process, using the same source editions and v3 editorial rules:

1. independently maps all three editions;
2. freezes each Issue Map before cross-paper synthesis;
3. produces materially similar editorial coverage and priority decisions;
4. produces a comparable set of cross-paper topics;
5. runs the same eight editorial passes;
6. preserves the secondary-coverage guardrail exemplified by the German crypto-tax item;
7. does not use OpenAI API orchestration;
8. does not depend on v4 Deep Read / Assembler / Article Records / Memory.

Exact textual identity is **not** the acceptance criterion. Editorial-process fidelity and materially similar decisions are.

## Artifact slots

The following files must be populated from the original v3 records, not reconstructed from memory:

```
source/
  handelsblatt-issue-map.md
  financial-times-issue-map.md
  wall-street-journal-issue-map.md
  cross-paper-topics.md
  brief-v1.md
  master-brief-v2.md
  editorial-notes.md
```

Until the original v3 records are exported, these artifacts remain intentionally absent.
