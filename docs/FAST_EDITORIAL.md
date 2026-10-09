# Fast Editorial v4 — first edition discovery worker

Version: `fast-editorial-v4.1`. Output: `editorial-issue-map-v1`.
Based on v3 `EDITORIAL_EXPERIMENT.md` and the v4 editorial philosophy.

## Scope

This stage creates a provisional Issue Map of one complete edition. It precedes
cross-paper selection, Selective Deep Read and the eight editorial passes.
FROZEN means an immutable, structurally validated provisional map, not a verified
Brief or canonical Article/Memory reconstruction. No publication happens here.

Every page is inspected with its verified image and full neutral Physical Map
blocks. No text truncation, source order or physical relations are passed as
semantic hints. Four page calls may run concurrently. All discovered fragments,
including LOW items, must appear exactly once in the issue synthesis. Continuation
grouping is provisional; same-topic articles must retain their distinct identity.
Ads/listings/navigation are noted in per-page observations rather than editorial items.

Coverage means all pages inspected. It does not establish complete character
accounting, perfect article recall, or the canonical Coverage Gate. A page marked
unreadable/needs_review blocks freezing and needs correction/review.

Each item preserves source page/block references, exact evidence quotes, author's
angle, new information, event importance, reading value, priority, uncertainties
and Selective Deep Read needs. Event importance and reading value are separate.
No article is automatically approved for a Brief.

## Storage and operations

Apply `docs/fast-editorial.sql`. Jobs have source/version/model identity, leases,
heartbeat and immutable FROZEN state. Page checkpoints store response IDs, actual
model and token usage, and are reused only when input hashes match. Completed
jobs cannot be reclaimed. Failed jobs resume existing valid checkpoints on an
explicit retry. A network failure after an API response but before checkpoint
persistence can still require another paid call; exactly-once billing is not claimed.

Verified JSON and Markdown artifacts are uploaded to `source-archive` before the
single transaction freezes the job and inserts provisional `editorial_map_items`.
Neither source evidence nor canonical article data is changed. RLS is enabled and
client-role access revoked. Events use component `FAST_EDITORIAL`.

Required server environment:

- `SUPABASE_URL` and `SUPABASE_SECRET_KEY`;
- `OPENAI_API_KEY`, entered directly in Railway Variables;
- `FAST_EDITORIAL_MODEL`, explicit model selection.

```sh
PYTHONPATH=src python -m business_brief.fast_editorial_worker --source-id <source UUID> --concurrency 4
```

First acceptance is scoped to WSJ 9 October 2026, 44 pages. With no retries/cache:
44 page requests plus one issue synthesis. The provider bounds each response to
16,000 output tokens and retries only selected transient HTTP failures, at most
three attempts. Refused, incomplete or unsupported evidence is not accepted.
Use of Responses API image inputs and strict JSON schema follows:
https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses

No automatic schedule is enabled for paid discovery until the first real run is
reviewed for recall, continuation handling, editorial quality, time and token usage.
Prioritize WSJ; FT/HB discovery should start as soon as their editions are ready,
so WSJ is the last critical morning input rather than the start of all work.

## Acceptance

Unit/DB smoke tests establish evidence checks, missing-page rejection, exactly-once
fragment accounting, lease fencing and incomplete-edition freeze rejection.
They do not establish that a real WSJ Issue Map has been generated or editorially
reviewed. Record the real run separately, with page count, item funnel, timing,
token usage, important uncertainties and the human acceptance result.


## Watermarks and review gaps
Watermarks are expected input artifacts. Page review is nonfatal for provisional
Issue Maps; exact source-block quotes remain mandatory and invalid evidence still
rejects the page. Unreadable pages retain explicit observations and review flags,
with no invented items. `coverage_status=needs_review` and `review_page_refs`
identify incomplete coverage. Affected items retain source uncertainties and
`requires_review` independently of the synthesis model. FROZEN means immutable,
not verified or complete coverage. Markdown exposes these flags.
Previously validated v4.1 checkpoints are reused only when physical-map/image SHA,
model, schema and the exact legacy prompt fingerprint match; remaining pages use
the watermark guidance. No source or stored page checkpoint is overwritten.

Issue-level synthesis has a separate 64,000-token output ceiling; page calls retain
the 16,000-token ceiling. Incomplete API responses are rejected with a sanitized
reason. Resuming synthesis reuses all persisted page results.

Full-edition synthesis permits up to 600 seconds for its larger response; page
requests keep the 180-second timeout. Heartbeats renew the DB lease while waiting.
