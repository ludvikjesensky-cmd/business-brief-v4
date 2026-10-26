# Operations — Business Brief v4

Cílem je ranní provoz, který je nakonec autonomní, ale ne slepý.

## Operating rules
- Runtime truth ověřuj na Hetzneru (Caddy, Docker, veřejné endpointy) a v Supabase; viz [INFRASTRUCTURE.md](INFRASTRUCTURE.md). Railway je pouze historická provenance.
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
3. Hetzner Caddy/Docker stav a logy, poté veřejné HTTPS endpointy; Railway logy pouze při historickém šetření.
4. Relevantní component contract/docs.
5. DECISIONS + FAILURES před změnou architektury.

## Documentation
Denní runtime eventy se nepřepisují do Markdownu. Do Project Memory patří pouze změna stavu, decision, failure nebo lesson s dlouhodobou hodnotou.


## Ingestor Access Bridge — operational gate

Kontrakt v1 je implementovaný v samostatné Docker HTTP službě na Hetzneru za Caddy; v3 i v4 writer mají zaznamenaný rollout a jednotlivé receipt-backed acceptance stránky. Verze a acceptance jsou v CURRENT_STATE a INGESTOR.md §20–21. Normativní API, HTTP/BLOCKED chyby a acceptance gate jsou v [INGESTOR.md §19](INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1). Legacy Ingestor worker není součástí tohoto workflow.

Před aktivací ověřit explicitní source/output bucket konfiguraci (oba privátní), server-only Supabase secret, dedikovaný revokovatelný bridge token se scopes/publication allowlist, 300s signed read URLs, durable idempotency binding a koordinaci source-state změn s canonical zápisem. Runtime musí používat aktuální TLS podporované Supabase; [oznámené odstranění CBC cipher suites](https://supabase.com/changelog/cbc-tls-ciphers-deprecated) se týká i Storage HTTP API.

Audit log obsahuje request ID, principal ID, endpoint, source UUID/SHA, manifest SHA, page number, canonical bucket/key, artifact SHA, outcome/error code a readback výsledek; ne credentials, signed URLs ani source text. Omezit velikost/rate podle §19 a ověřit log redaction. Idempotency metadata není editorial artefakt ani náhrada Storage JSONu. Žádná nová tabulka tímto dokumentem nevzniká.

Při timeoutu/upload/readback nejistotě hlásit BLOCKED a persistence UNKNOWN. Opakovat stejný payload/idempotency key po obnově služby, znovu ověřit zdroj i uložené bytes; žádný automatický overwrite, delete nebo přechod na další stránku. 409 vyžaduje rozlišení příčiny podle kontraktu, nikoli slepý retry. STORED po ověřeném downloadu nenahrazuje editorial verification; NEEDS_REVIEW není dokončený verified pass. Provozní acceptance musí prokázat skutečný přístup z cílového Chatu a jednu canonical stránku, pak STOP.

## Ingest acceptance and rollout
Ordinary Chat image + inline OCR read path and first v2 persist passed. The persisted content is superseded acceptance evidence (HISTORY); do not overwrite/delete it or accept it for assembly merely because technical readback reports VERIFIED. Daily ingest runs in ordinary Chat; Codex is for system development/debugging.

Bridge v3 validation/generation mapping is deployed; Site v4 already supports unchanged body transport and required no redeploy. User-authorized page-1 acceptance passed once through the connected plugin, with exact readback SHA/identity; that historical run stopped after page 1. Subsequent selected-corpus and Q020 acceptance are recorded below. Select generation explicitly downstream; preserve existing idempotency bindings and retry original requests only for transport recovery. Further content acceptance requires explicit user instruction. See INGESTOR.md §19–20 and bridge/README.md. PRs #4–#10 are now merged/closed; historical Railway pins are retained only as provenance. See CURRENT_STATE for verified post-merge runtime identities.

## Article assets / v4 (D022)
The writer reuses private page-ingest and source/generation-derived immutable keys. See INGESTOR §21.5 and bridge/README for deterministic PNG encoding, limits, durable reserved set binding and recovery. Preserve v2/v3 objects and bindings. A partial set remains fenced and must be retried with the original submission/key; never automatically delete crops, expire claims, or substitute enriched output for a null-artifact submission. 409 ASSET_SET_CONFLICT / ASSET_CONFLICT requires explicit reconciliation. Source eligibility stays fenced through all crops and Page JSON readback; STORED verifies the full set.

Deploy only a reviewed/tested Bridge revision using the manual Hetzner runbook in INFRASTRUCTURE.md. Historical pre-migration isolation: the unrelated legacy `ingestor` cron was pinned to `a8d6c26e8002c8a4dcad42fce7fa6c5763e65580`; its pre-merge redeploy `2e44c090-63b8-4b95-b5c6-8e263b14850e` was SUCCESS. These Railway IDs do not establish current runtime health; a main merge is not a Hetzner deployment mechanism. Existing Site v4 uses generic JSON transport and requires no change for server-side crops. Actual runtime revision, deployment ID and single-page acceptance are recorded in CURRENT_STATE/HISTORY; do not infer them from local test success.

Historical 2026-10-18 Railway v4 rollout: runtime `b6d465c49dbf546f0ea31876d218121428d495c8`, deployment `4489131f-d578-4062-b88f-40adc3716932` SUCCESS. Additive private bucket JSON/PNG configuration was read back; original-request reconciliation closed the initial MIME failure. Exactly page 2 WSJ 2026-10-14 stored with all three chart crops and both bindings VERIFIED, SHA/size/identity matched, usable_for_assembly=true. Existing v2/v3 metadata remained unchanged. Site v4 was not redeployed. 226 tests pass; STOP/no assembly. See CURRENT_STATE/HISTORY for precise artifact identities.

## Ordinary-Chat corpus verification and visual defect gate
The subsequent WSJ 2026-10-14 page-3–10 pass is reported in the original Chat; HISTORY distinguishes archived receipts from conversational result reports. At that historical stage no stored-page read/list endpoint was exposed; D024 now provides verified readback (see below). Do not use source-page evidence GET as proof that a canonical Page JSON exists, or replay a POST to discover storage in a read-only task.

Apply INGESTOR §21.7 before every asset visual_checked:true/persist: render from the authoritative PNG using exact writer-equivalent floor/ceil bbox bounds and independently preview every crop as its own image, including all visual edges/labels. Full-page bbox inspection alone is insufficient. No available preview means no verified visual acceptance. Writer SHA/readback remains a separate required gate.

The original canonical page-6 About Face crop remains immutable and blocked from accepted selection (F011). Q014/Q015 are resolved: independently previewed revision r1 is selected by the accepted manifest, and receipt/generation reconciliation is complete for this source. Page 1 is explicitly selected from v3; no v4 page-1 artifact is claimed. Preserve originals and use exact revision/manifest identities in CURRENT_STATE/HISTORY.

## Revision and manifest rollout gate
INGESTOR §22 / D024 introduces source-scoped readback, full-snapshot revisions and explicit edition-selection. Deploy the tested pinned bridge and private Site transport before production correction. Independently inspect all exact source-derived revision crops, then write a new revision with its own request identity. Reconcile selected pages through readback; accept the manifest only after every JSON/PNG identity passes and known defective/superseded artifacts are excluded. Stop after manifest persistence, before assembly. The implementation and ingest handoff are merged into main through PR #10; the former #4–#10 stack is closed.

Historical D024 ingest acceptance is complete for WSJ 2026-10-14: bridge pin 388f2c879ae5d30b9544a08d95b7283a2f4c6fe6 / Railway fdaf8dfa-5ec9-4706-a5ef-7e15a209610a SUCCESS; private Site v6 / appgdep_6ad5259db29c8191aee9f97bc8c8896f succeeded. Page-6 r1 and all selected Page JSON/PNG readbacks passed before the single ACCEPTED_FOR_ASSEMBLY manifest was stored. CURRENT_STATE/HISTORY supersede historical #9 evidence-limit statements above. That historical acceptance stopped after manifest persistence. On 2026-10-22, Q020 subsequently passed on Hetzner: read-only assembly, CREATED persistence receipts and REPLAYED receipts on the identical rerun. Q011 is resolved by D025; current evidence is in CURRENT_STATE and INFRASTRUCTURE.md. See CURRENT_STATE for the verified main SHA and separate open/Draft PR #3.

## Current production checks and security — 2026-10-22
Hetzner `tannenberg-prod-01` (`46.225.32.16`, Ubuntu 26.04.1 LTS) runs Caddy as HTTPS gateway and the Docker Bridge bound to `127.0.0.1:8080`. The public Bridge is `https://bridge.businessbrief.cz`; authenticated `/ready` returned 200 READY. `https://businessbrief.cz/` returned 200 and serves static `business-brief-web-v2/public/` files from `/var/www/businessbrief.cz`. Supabase remains operational DB/Storage. These are migration acceptance observations, not a continuous health guarantee.

Use [INFRASTRUCTURE.md](INFRASTRUCTURE.md) for manual deployment, Caddy validation/reload, recovery and endpoint checks. Verify both public hosts after changes. Run Assembler read-only first against explicit source UUID + manifest ID + SHA; use `--persist` deliberately and repeat the identical command to verify replay. Q020 is complete for the exact WSJ selection recorded in CURRENT_STATE. Indexer v1 has now passed first live WSJ plan/persist/replay acceptance and initial Czech→English retrieval spot checks; Q017 remains open for Czech→German and final calibration. Composer acceptance remains separate.

The operator-reported Railway Variables security warning triggered treatment of stored credentials as potentially exposed. The Supabase secret was rotated for Hetzner; production values belong only in `/opt/business-brief-v4/.env` (mode 600), outside Git. Review the affected credential inventory and rotate/revoke any remaining exposed credentials; do not infer complete revocation from a successful endpoint check. Use dedicated revocable Bridge credentials, SSH public-key authentication and read-only GitHub deploy keys. Record credential purpose and rotation/revocation status without values, tokens, signed URLs or passwords. The warning is not evidence of confirmed application-data compromise.


## Indexer runtime acceptance

Current Indexer runtime is deployed through the Hetzner checkout/image and uses server-side `COHERE_API_KEY` from `/opt/business-brief-v4/.env`; the key value must never be committed or printed.

Safe acceptance sequence:

1. run `bb-indexer` without `--persist` against an explicit source UUID + manifest ID + manifest SHA;
2. verify eligible/skipped counts and deterministic planned chunk count;
3. run the same command with `--persist`;
4. verify CREATED receipts and direct Supabase readback;
5. repeat the identical `--persist` command and require REPLAYED with unchanged row counts;
6. run multilingual retrieval calibration with `bb-search`.

Accepted WSJ baseline on 2026-10-26:
- 21 article rows;
- 21 eligible, 0 skipped;
- 39 planned/persisted chunks;
- first persist: 21 CREATED;
- identical replay: 21 REPLAYED;
- direct Supabase readback: 21 INDEXED runs, 21 article embeddings, 39 chunks covering all 21 articles.

Initial Czech→English semantic spot checks passed for bank rates/profits, U.S. defense startups in Taiwan and Chinese stagnation/Gen Z. Lexical results may be empty for Czech queries against English source prose; vector retrieval is the primary cross-language signal. Do not freeze hybrid weights from these spot checks. Q017 remains open until Czech→German and the predeclared latency/cost/quality acceptance set are complete.

## Deep/Memory runner implementation — 2026-10-26

See [DEEP_RUNNER.md](DEEP_RUNNER.md) for the Bridge-authenticated runner contract, safe defaults, Technician boundary and Hetzner rollout. Repository implementation does not establish deployment or ordinary Chat acceptance. Fast Editorial is unchanged.
