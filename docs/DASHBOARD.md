# Deep/Memory Control Tower

Updates the existing `bb-dashboard`, rather than introducing a second frontend.
Read-only operator overview: PDF preparation, page write receipts, exact selections,
persisted articles, indexed article versions/chunks, runner history and next step.
Fast Editorial is separate. No runner mutations, paid calls or automatic chaining.

## Evidence and limitations

- Up to 100 most recently received active edition sources, including historical dates.
- Page progress is distinct page numbers with VERIFIED Bridge bindings for the current
  page-ingest-v4 generation (`ingestor-v2.2`), including immutable revisions. Bindings
  are evidence of writes, not fresh Storage readback, full semantic acceptance or a
  heartbeat of ordinary Chat. Missing bindings do not prove missing page files.
- Selections come from verified manifest bindings, Article Records and runner ledger.
  Discovery is observational only; it does not select `latest` or authorize execution.
  A stored manifest binding alone is not acceptance/revalidation of its contents.
- Article/index/chunk counts join exact source + manifest ID + SHA and article SHA.
  INDEXED counts persisted article versions, not final retrieval quality. Counts can
  include multiple index profiles; they are not a new current-profile post-check.
- At most 50 newest receipts per selection. The latest result per operation controls
  guidance; RUNNING/UNKNOWN is uncertain, COMPLETE without PASS is not success.
- Plans and requested persistence are distinct. Persist requested does not prove
  all writes succeeded; persisted counts come independently from canonical tables.
- Search PASS only establishes technical execution. Human relevance review and Q017
  benchmark remain separate. Historical CLI executions need not have runner receipts.
- Legacy Technician-only 30-day health totals, global queue and legacy Ingestor worker
  counters no longer stand in for Deep/Memory completion. Pending inbox objects with
  no active identified edition are outside this first edition-oriented overview.
- Timestamp is last successful database observation, displayed in Europe/Prague.
  Refresh is every 30 seconds; failures retain previous data with a visible warning.

## Server boundary

`BRIDGE_DATABASE_URL` is server-only; the dashboard uses a repeatable-read READ ONLY
transaction and 15-second statement timeout. SQL creates no tables, views or grants;
`bridge_private` stays outside the Data API. No raw runner result text, provider
errors, source paths, bearer credentials or principal IDs are sent to the browser.

Set dedicated `DASHBOARD_USER` and `DASHBOARD_PASSWORD` server-side. Both HTML and JSON
require Basic authentication when configured. With missing configuration JSON fails
closed with 503 (the static shell remains available). Use HTTPS at Caddy; never send
Basic credentials over a public unencrypted connection. This is an owner/operator
view of all active sources, not a publication-scoped multi-user portal. Do not reuse
a broad Bridge principal token as the dashboard password.

## Hetzner deployment

Implementation is prepared; deployment has not been performed by this change.
Use the reviewed commit, existing configuration backup procedure and a separate
mode-600 dashboard env file outside Git. It needs only the DB URL and dedicated
login above; no Cohere key or Bridge principal token is needed. Prefer a dedicated
read-only database role with SELECT on the tables referenced in dashboard.sql;
configure it through the established privileged operator workflow.

Build:

```sh
docker build -f dashboard/Dockerfile -t business-brief-dashboard:<commit> .
```

Run in a separate container, leaving Bridge on port 8080:

```sh
docker run -d --name business-brief-dashboard --restart unless-stopped \
  --env-file /opt/business-brief-v4/.env.dashboard \
  -p 127.0.0.1:8081:8080 business-brief-dashboard:<commit>
```

Choose and confirm the private dashboard hostname before editing DNS/Caddy; do not
assume an existing dashboard deployment URL or replace public businessbrief.cz.
Back up Caddy, add HTTPS reverse proxy to 127.0.0.1:8081, validate then reload.
No new public container port. Check unauthenticated 401, authenticated HTML/JSON,
no-store headers, WSJ exact counts and refresh/error behavior. Retain prior image
for rollback. Do not apply migrations, enable runner persistence or publish the
ordinary Chat adapter as a side effect of dashboard rollout.

## Validation

```sh
PYTHONPATH=src pytest tests/test_dashboard.py tests/test_dashboard_process.py -q
node tests/dashboard_ui.mjs
```

The SQL was executed read-only against the production schema on 2026-10-26:
WSJ 2026-10-14 exact selection returned 21 articles, 21 INDEXED versions, 39 chunks,
three completed plan/search receipts, and nine distinct v4 page write receipts.
The latter is intentionally not presented as missing-page or completeness proof.

HTTP/state tests and inline JavaScript execution checks passed locally. A real
browser screenshot check was attempted but the Chromium download was unavailable
in the execution environment; desktop/mobile visual review remains a rollout check.
