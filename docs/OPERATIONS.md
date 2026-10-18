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

Kontrakt v1 je implementovaný v samostatné Railway službě; v3 i v4 writer mají zaznamenaný rollout a jednotlivé receipt-backed acceptance stránky. Verze a acceptance jsou v CURRENT_STATE a INGESTOR.md §20–21. Normativní API, HTTP/BLOCKED chyby a acceptance gate jsou v [INGESTOR.md §19](INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1). Legacy Ingestor worker není součástí tohoto workflow.

Před aktivací ověřit explicitní source/output bucket konfiguraci (oba privátní), server-only Supabase secret, dedikovaný revokovatelný bridge token se scopes/publication allowlist, 300s signed read URLs, durable idempotency binding a koordinaci source-state změn s canonical zápisem. Runtime musí používat aktuální TLS podporované Supabase; [oznámené odstranění CBC cipher suites](https://supabase.com/changelog/cbc-tls-ciphers-deprecated) se týká i Storage HTTP API.

Audit log obsahuje request ID, principal ID, endpoint, source UUID/SHA, manifest SHA, page number, canonical bucket/key, artifact SHA, outcome/error code a readback výsledek; ne credentials, signed URLs ani source text. Omezit velikost/rate podle §19 a ověřit log redaction. Idempotency metadata není editorial artefakt ani náhrada Storage JSONu. Žádná nová tabulka tímto dokumentem nevzniká.

Při timeoutu/upload/readback nejistotě hlásit BLOCKED a persistence UNKNOWN. Opakovat stejný payload/idempotency key po obnově služby, znovu ověřit zdroj i uložené bytes; žádný automatický overwrite, delete nebo přechod na další stránku. 409 vyžaduje rozlišení příčiny podle kontraktu, nikoli slepý retry. STORED po ověřeném downloadu nenahrazuje editorial verification; NEEDS_REVIEW není dokončený verified pass. Provozní acceptance musí prokázat skutečný přístup z cílového Chatu a jednu canonical stránku, pak STOP.

## Ingest acceptance and rollout
Ordinary Chat image + inline OCR read path and first v2 persist passed. The persisted content is superseded acceptance evidence (HISTORY); do not overwrite/delete it or accept it for assembly merely because technical readback reports VERIFIED. Daily ingest runs in ordinary Chat; Codex is for system development/debugging.

Bridge v3 validation/generation mapping is deployed; Site v4 already supports unchanged body transport and required no redeploy. User-authorized page-1 acceptance passed once through the connected plugin, with exact readback SHA/identity; no further page or assembly. Select generation explicitly downstream; preserve existing idempotency bindings and retry original requests only for transport recovery. Further content acceptance requires explicit user instruction. See INGESTOR.md §19–20 and bridge/README.md. The bridge remains pinned; review main-linked service auto-deploy effects before merging the open #4 → #5 → #6 → #7 → #8 chain.

## Article assets / v4 (D022)
The writer reuses private page-ingest and source/generation-derived immutable keys. See INGESTOR §21.5 and bridge/README for deterministic PNG encoding, limits, durable reserved set binding and recovery. Preserve v2/v3 objects and bindings. A partial set remains fenced and must be retried with the original submission/key; never automatically delete crops, expire claims, or substitute enriched output for a null-artifact submission. 409 ASSET_SET_CONFLICT / ASSET_CONFLICT requires explicit reconciliation. Source eligibility stays fenced through all crops and Page JSON readback; STORED verifies the full set.

Deploy only the reviewed/tested pinned bridge commit. Main-linked services still include an unrelated historical cron; do not merge to deploy. Existing Site v4 uses generic JSON transport and requires no change for server-side crops. Actual runtime revision, deployment ID and single-page acceptance are recorded in CURRENT_STATE/HISTORY; do not infer them from local test success.

Verified v4 rollout: runtime `b6d465c49dbf546f0ea31876d218121428d495c8`, deployment `4489131f-d578-4062-b88f-40adc3716932` SUCCESS. Additive private bucket JSON/PNG configuration was read back; original-request reconciliation closed the initial MIME failure. Exactly page 2 WSJ 2026-10-14 stored with all three chart crops and both bindings VERIFIED, SHA/size/identity matched, usable_for_assembly=true. Existing v2/v3 metadata remained unchanged. Site v4 was not redeployed. 226 tests pass; STOP/no assembly. See CURRENT_STATE/HISTORY for precise artifact identities.

## Ordinary-Chat corpus verification and visual defect gate
The subsequent WSJ 2026-10-14 page-3–10 pass is reported in the original Chat; HISTORY distinguishes archived receipts from conversational result reports. No stored-page read/list endpoint is exposed by the connected bridge. Do not use source-page evidence GET as proof that a canonical Page JSON exists, or replay a POST to discover storage in a read-only task.

Apply INGESTOR §21.7 before every asset visual_checked:true/persist: render from the authoritative PNG using exact writer-equivalent floor/ceil bbox bounds and independently preview every crop as its own image, including all visual edges/labels. Full-page bbox inspection alone is insufficient. No available preview means no verified visual acceptance. Writer SHA/readback remains a separate required gate.

Page 6 has a known immutable visually-invalid About Face crop (F011), despite reported usable_for_assembly=true. Hold page-6/corpus visual acceptance; resolve Q014 with an authorized revision/correction protocol, independent preview, production writer/readback and explicit downstream selection. Never overwrite/delete or persist the manually estimated replacement bbox during documentation consolidation. Reconcile receipts and page generations (Q015); page 1 has no evidenced v4 artifact. The PR chain remains #4 → #5 → #6 → #7 → #8, with documentation consolidation stacked on #8. No merge, deploy, assembly or production correction is part of this task.

## Revision and manifest rollout gate
INGESTOR §22 / D024 introduces source-scoped readback, full-snapshot revisions and explicit edition-selection. Deploy the tested pinned bridge and private Site transport before production correction. Independently inspect all exact source-derived revision crops, then write a new revision with its own request identity. Reconcile selected pages through readback; accept the manifest only after every JSON/PNG identity passes and known defective/superseded artifacts are excluded. Stop after manifest persistence, before assembly. Preserve #4 → #5 → #6 → #7 → #8 → #9 and stack the new PR on #9; no merge to main.

D024 acceptance is complete for WSJ 2026-10-14: bridge pin 388f2c879ae5d30b9544a08d95b7283a2f4c6fe6 / Railway fdaf8dfa-5ec9-4706-a5ef-7e15a209610a SUCCESS; private Site v6 / appgdep_6ad5259db29c8191aee9f97bc8c8896f succeeded. Page-6 r1 and all selected Page JSON/PNG readbacks passed before the single ACCEPTED_FOR_ASSEMBLY manifest was stored. CURRENT_STATE/HISTORY supersede historical #9 evidence-limit statements above. STOP after manifest; no assembly/merge.
