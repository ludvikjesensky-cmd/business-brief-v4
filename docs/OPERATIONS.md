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


## Ingestor Access Bridge — future operational gate

Kontrakt v1 je přijatý design, nikoli běžící služba. Normativní API, HTTP/BLOCKED chyby a acceptance gate jsou v [INGESTOR.md §19](INGESTOR.md#19-ingestor-access-bridge--normative-http-contract-v1). Implementace nesmí oživovat legacy Ingestor worker. Preferované umístění je samostatná malá Railway HTTP služba.

Před aktivací ověřit explicitní source/output bucket konfiguraci (oba privátní), server-only Supabase secret, dedikovaný revokovatelný bridge token se scopes/publication allowlist, 300s signed read URLs, durable idempotency binding a koordinaci source-state změn s canonical zápisem. Runtime musí používat aktuální TLS podporované Supabase; [oznámené odstranění CBC cipher suites](https://supabase.com/changelog/cbc-tls-ciphers-deprecated) se týká i Storage HTTP API.

Audit log obsahuje request ID, principal ID, endpoint, source UUID/SHA, manifest SHA, page number, canonical bucket/key, artifact SHA, outcome/error code a readback výsledek; ne credentials, signed URLs ani source text. Omezit velikost/rate podle §19 a ověřit log redaction. Idempotency metadata není editorial artefakt ani náhrada Storage JSONu. Žádná nová tabulka tímto dokumentem nevzniká.

Při timeoutu/upload/readback nejistotě hlásit BLOCKED a persistence UNKNOWN. Opakovat stejný payload/idempotency key po obnově služby, znovu ověřit zdroj i uložené bytes; žádný automatický overwrite, delete nebo přechod na další stránku. 409 vyžaduje rozlišení příčiny podle kontraktu, nikoli slepý retry. STORED po ověřeném downloadu nenahrazuje editorial verification; NEEDS_REVIEW není dokončený verified pass. Provozní acceptance musí prokázat skutečný přístup z cílového Chatu a jednu canonical stránku, pak STOP.
