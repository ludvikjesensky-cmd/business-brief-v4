# Fast Editorial v3 replica in v4

## Purpose

This directory preserves the **Fast Editorial** process proven in Business Brief v3 during the 10-day experiment.

The first goal in v4 is **reproduction, not redesign**.

We intentionally do **not** connect this work to the v4 Deep Read / Assembler / Article Records / Memory pipeline yet.

We also do **not** use the OpenAI API in this phase. The workflow remains **Chat-driven and provisional**, exactly as in the v3 experiment.

## Canonical process to reproduce

Reference Editions: FT / WSJ / Handelsblatt

→ independent Editorial Discovery for each edition

→ Provisional Issue Map

→ freeze each map before another title can influence it

→ Cross-Paper Topics

→ Selective Deep Read only where needed for the Brief

→ Editorial Workflow v1

→ Master Brief

→ Editorial Notes / Day Dossier

The eight editorial passes remain:

1. Assignment Editor
2. Dramaturg
3. Story Editor
4. Brief Writer
5. Detail Editor
6. Verification Editor
7. Language & Style Editor
8. Editor-in-Chief

These are editorial passes, not technical agents.

## What is copied from v3

The files under `reference/` are copied **verbatim** from `business-brief-v3/docs`:

- EDITORIAL_EXPERIMENT.md
- EDITORIAL_PIPELINE.md
- EDITORIAL_WORKFLOW.md
- EDITORIAL_PLAYBOOK.md
- PRODUCT_MODEL.md

They are the source of truth for the replication phase.

## What is deliberately out of scope

For the first replication phase:

- no OpenAI API orchestration;
- no GitHub Actions;
- no automatic agents;
- no integration with v4 Assembler;
- no integration with v4 Article Records;
- no Memory integration;
- no redesign of schemas;
- no new editorial rules unless a direct v3 source requires them.

## Acceptance test

Use **Day 1, 14 September 2026** as the first replay baseline.

Known v3 baseline:

- 3 frozen Reference Editions;
- 102 provisional editorial items;
- 24 cross-paper topics;
- verified Brief v1;
- verified Master Brief v2.

The first acceptance question is not whether v4 produces a “better” Brief.

It is whether the Chat-driven v4 replica can reproduce the **same editorial process and materially similar decisions** from the same inputs.

Only after that passes should we consider automation or integration with other v4 pipelines.
