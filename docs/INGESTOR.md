# Ingestor v4

Ported from business-brief-v3 commit `933b5c47fb96c97333ff24dda4e7e019486ebbfd`.
The extraction algorithm and `physical-map-v1` semantics remain unchanged.
Worker version: `ingestor-v4-physical-map-v1.1`.

## Evidence boundary

Extract exact PDF line text, geometry, fonts, source order and stable block IDs.
Generate neutral local relations (`below`, `right_of`, `same_physical_lane`,
`probable_physical_successor`). Relations are physical hypotheses, never semantic
article boundaries or reading order. Semantic Mapper must receive neutral blocks
without relations or source order, following the v3 boundary.

## v4 adapter

Accept only `source-bundle-v4` from a DB source in `READY_FOR_INGESTOR`.
The durable queue admits only active edition sources, excluding collisions.
Read the manifest and prepared PDF from `source-archive`, validate source identity,
prepared PDF SHA-256 and full page sequence/count. Remote storage keys never become
local filesystem paths. Physical Map `source_id` is the database source UUID;
`source_sha256` retains original-byte identity. The archived manifest is immutable.

## Worker

Apply `docs/ingestor-queue.sql` before starting:

```sh
PYTHONPATH=src python -m business_brief.ingestor_worker
```

Required environment: `SUPABASE_URL`, `SUPABASE_SECRET_KEY` (server only).
For a scoped acceptance run, add `--source-id <database UUID> --verify-repeat`.
This downloads and extracts the same prepared PDF twice and requires identical
canonical Physical Map bytes before upload/finalization. The job metrics record
`repeatability_verified: true` only when that check succeeds.
The CLI drains eligible DB jobs and exits; it does not install a scheduler or HTTP
wake endpoint. Repeated invocations reconcile missing jobs without duplicating DONE
work. Job identity is `(source_id, ingestor_version)`.

Claims use `FOR UPDATE SKIP LOCKED`, a lease token and a heartbeat. Expired leases
are reclaimable. Upload and hash verification precede atomic DB finalization.
Finalization rejects a stale lease or a source that is no longer active/ready.
Transient failures retry; evidence invariant failures become BLOCKED. Immutable
content-addressed output paths permit safe retries after upload/finalization failure.
The worker does not delete source artifacts or change Technician READY status.

Output: `source-archive/ingestor/<source UUID>/<worker version>/sha256-<map hash>/physical-map.json`.
Job rows retain output path/hash, page/block/character metrics and failure evidence.
Pipeline events use component `INGESTOR`; event logging is best effort.

## Verification

Unit tests cover repeatability, neutral physical relations, DB UUID provenance,
corrupted PDF rejection, unsupported contracts, readiness, page-count mismatch,
unsafe keys and archive-prefix confinement. A real-source production acceptance
is a separate check; unit tests alone do not establish WSJ ingestion success.
