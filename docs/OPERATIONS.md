# Operations — Business Brief v4

Cílem je ranní provoz, který je nakonec autonomní, ale ne slepý.

## Operating rules
- Runtime truth ověřuj v Supabase/Railway, ne ve starém Markdown snapshotu.
- Každý job musí být auditovatelný, idempotentní kde to dává smysl a mít viditelný failure.
- Paid/model steps mají explicitní model/version identity a usage/cost telemetry.
- Automatický schedule placeného editorial discovery není povolen, dokud acceptance test nepotvrdí cenu, čas a kvalitu.
- Watcher pro WSJ byl odstraněn; acquisition není automaticky vyřešená.
- Dashboard je primární healthy-state surface. Alerty pouze pro skutečné problémy.
- Publication gate musí umět zastavit nezdravé vydání.

## Cost discipline
Reálný Fast Editorial WSJ run ukázal přibližně USD 7.95 za jeden průchod a kolem 49 requests. Toto je failure baseline. Každý nový návrh musí před full runem ukázat očekávaný cost model a malý test.

## Debugging order
1. PROJECT.md + CURRENT_STATE.
2. Supabase jobs/events/artifacts.
3. Railway deployment/logs.
4. Relevantní component contract/docs.
5. DECISIONS + FAILURES před změnou architektury.

## Documentation
Denní runtime eventy se nepřepisují do Markdownu. Do Project Memory patří pouze změna stavu, decision, failure nebo lesson s dlouhodobou hodnotou.


## Ingestor Access Bridge — operational gate

Kontrakt v1 je implementovaný v samostatné Railway službě; v3 extension je nasazená a ověřená na jedné stránce. Verze a acceptance jsou v CURRENT_STATE a INGESTOR.md §20. Normativní API, HTTP/BLOCKED chyby a acceptance gate jsou v [INGESTOR.md §19](INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1). Legacy Ingestor worker není součástí tohoto workflow.

Před aktivací ověřit explicitní source/output bucket konfiguraci (oba privátní), server-only Supabase secret, dedikovaný revokovatelný bridge token se scopes/publication allowlist, 300s signed read URLs, durable idempotency binding a koordinaci source-state změn s canonical zápisem. Runtime musí používat aktuální TLS podporované Supabase; [oznámené odstranění CBC cipher suites](https://supabase.com/changelog/cbc-tls-ciphers-deprecated) se týká i Storage HTTP API.

Audit log obsahuje request ID, principal ID, endpoint, source UUID/SHA, manifest SHA, page number, canonical bucket/key, artifact SHA, outcome/error code a readback výsledek; ne credentials, signed URLs ani source text. Omezit velikost/rate podle §19 a ověřit log redaction. Idempotency metadata není editorial artefakt ani náhrada Storage JSONu. Žádná nová tabulka tímto dokumentem nevzniká.

Při timeoutu/upload/readback nejistotě hlásit BLOCKED a persistence UNKNOWN. Opakovat stejný payload/idempotency key po obnově služby, znovu ověřit zdroj i uložené bytes; žádný automatický overwrite, delete nebo přechod na další stránku. 409 vyžaduje rozlišení příčiny podle kontraktu, nikoli slepý retry. STORED po ověřeném downloadu nenahrazuje editorial verification; NEEDS_REVIEW není dokončený verified pass. Provozní acceptance musí prokázat skutečný přístup z cílového Chatu a jednu canonical stránku, pak STOP.

## Ingest acceptance and rollout
Ordinary Chat image + inline OCR read path and first v2 persist passed. The persisted content is superseded acceptance evidence (HISTORY); do not overwrite/delete it or accept it for assembly merely because technical readback reports VERIFIED. Daily ingest runs in ordinary Chat; Codex is for system development/debugging.

Bridge v3 validation/generation mapping is deployed; Site v4 already supports unchanged body transport and required no redeploy. User-authorized page-1 acceptance passed once through the connected plugin, with exact readback SHA/identity; no further page or assembly. Select generation explicitly downstream; preserve existing idempotency bindings and retry original requests only for transport recovery. Further content acceptance requires explicit user instruction. See INGESTOR.md §19–20 and bridge/README.md. The bridge remains pinned; review main-linked service auto-deploy effects before merging the open #4 → #5 → #6 chain.

## Article assets / v4 gate (D022)
The accepted v4 layout reuses private `page-ingest`; no bucket provisioning, deployment, production ingest/persist, deletion or overwrite is part of this consolidation. See INGESTOR.md §21 for exact keys and write guarantees. Retain immutable v2/v3 artifacts (including existing v3 pages 1 and 2) and bindings. Page-2 existence is user-reported here, not a new live check.

Local v4 schema/path validation and empty-assets Page JSON use the existing persistence fence. Nonempty-assets writes return CONFIGURATION_MISSING/NOT_WRITTEN before claims or mutation: binary crop writer and adapter are not implemented. Before activation require controlled proof of server-derived source-bound PNG crops, private bucket, create-if-absent, SHA/exact readback, durable idempotency, source fencing through all assets and JSON, timeout/concurrency/conflict recovery and Chat visual/anchor acceptance. Partial crop writes must remain immutable for original-request reconciliation, never cleanup/overwrite. Artifact retention cannot expire a referenced crop before its Page JSON. Production remains pinned v3; review main-linked auto-deploy effects before any merge. New work is stacked after #6.
