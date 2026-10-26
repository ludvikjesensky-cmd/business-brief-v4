# Deep/Memory Runner v1

**Status:** IMPLEMENTED CANDIDATE, not yet production-deployed  
**Branch:** `runner-v1`

## Purpose

Runner v1 is the narrow server-side execution boundary that lets an ordinary
Chat orchestrate deterministic Deep/Memory runtime components without SSH and
without receiving Supabase, Cohere, database or host credentials.

It does not replace the Ingestor Access Bridge. The Bridge remains the evidence
and Page JSON boundary. Runner calls existing Assembler/Indexer code and keeps
their exact gates and idempotency semantics.

## Why it is a separate service

The Bridge deliberately imports no workers, models or editorial processing.
Runner therefore lives beside it rather than adding execution endpoints to the
Bridge. Both services use the same principles: bearer authentication, no secret
echoing, no request logging, HTTPS-only public access through Caddy and explicit
least-privilege scopes.

## Capabilities

Remote-capable in v1:

- Assembler plan, read-only;
- Assembler persist;
- Indexer plan, read-only and no Cohere call;
- Indexer persist;
- exact selection status;
- vector + lexical search.

Not remote-capable in v1:

- Technician.

Technician currently accepts a local PDF filesystem path and writes a local
workspace. There is no accepted immutable remote upload/intake contract yet.
Runner reports `technician_remote: false` rather than inventing one. A future
intake decision must define source upload, immutable identity, limits,
publication/date trust evidence and Technician-to-Supabase handoff.

## Exact selection contract

Assembler, Indexer and status accept exactly:

```json
{
  "source_id": "<uuid>",
  "manifest_id": "<explicit manifest id>",
  "manifest_sha256": "<64 lowercase hex>"
}
```

No "latest" discovery is allowed.

## HTTP tools

- `GET /ready`
- `POST /v1/status`
- `POST /v1/assembler/plan`
- `POST /v1/assembler/persist`
- `POST /v1/indexer/plan`
- `POST /v1/indexer/persist`
- `POST /v1/search`

The Chat-facing OpenAPI definition is `runner/openapi.yaml`.

## Authentication

Configure `RUNNER_PRINCIPALS` server-side as JSON:

```json
[
  {
    "id": "ordinary-chat",
    "token": "<at least 43 characters of cryptographic randomness>",
    "scopes": ["runner:read", "runner:write"]
  }
]
```

Use a dedicated runner token. Do not reuse the SSH key, Supabase secret,
Cohere key, database password or Bridge token as the client credential.

Scopes:

- `runner:read`: ready, status, plan and search;
- `runner:write`: Assembler/Indexer persistence.

The runner itself receives the existing server-side environment needed by
Assembler/Indexer:

- `SUPABASE_URL`
- `SUPABASE_SECRET_KEY`
- `INGESTOR_BRIDGE_URL`
- `INGESTOR_BRIDGE_TOKEN`
- `COHERE_API_KEY`
- `RUNNER_PRINCIPALS`

Secrets remain in `/opt/business-brief-v4/.env`, mode 600.

## Replay cost safety

Runner v1 also changes Indexer replay behavior: if the exact run is already
`INDEXED`, the stored rows are post-checked and returned as `REPLAYED`
before Cohere is called. This preserves idempotency economically as well as
structurally.

## Intended ordinary-Chat sequence

After an accepted Edition Selection Manifest exists:

1. call `assembler_plan`;
2. stop if BLOCKED/NEEDS_REVIEW;
3. call `assembler_persist`;
4. call `indexer_plan`;
5. stop if any article is skipped;
6. call `indexer_persist`;
7. call `pipeline_status`;
8. use `search_index` for retrieval/calibration.

Ordinary Chat never needs SSH.

## Hetzner deployment candidate

Build from repository root:

```sh
docker build -f runner/Dockerfile -t business-brief-runner:local .
```

Run only on loopback:

```sh
docker run -d \
  --name business-brief-runner \
  --restart unless-stopped \
  --env-file /opt/business-brief-v4/.env \
  -p 127.0.0.1:8090:8090 \
  business-brief-runner:local
```

Caddy candidate:

```caddy
runner.businessbrief.cz {
    reverse_proxy 127.0.0.1:8090 {
        header_up X-Forwarded-Proto https
    }
}
```

Before public deployment:

- create `runner.businessbrief.cz A 46.225.32.16`;
- generate a dedicated high-entropy runner bearer token;
- add `RUNNER_PRINCIPALS` to the server `.env`;
- build/run the container on loopback;
- validate and reload Caddy;
- test `/ready` with the bearer credential;
- run WSJ plan/status/search first;
- run write endpoints only after plan acceptance;
- verify Supabase row counts remain unchanged on exact replay.

Do not expose port 8090 directly.
