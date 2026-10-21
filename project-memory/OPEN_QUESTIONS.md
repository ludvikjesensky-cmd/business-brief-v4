# Open Questions — Business Brief v4

## Q001 — OPEN — Ekonomicky udržitelný editorial processing
Které downstream editorial kroky mohou bezpečně běžet automatizovaně/API po vzniku spolehlivých Article Records a které mají zůstat v live Chat/human-supervised režimu?

## Q002 — OPEN — Source acquisition
Jak spolehlivě a legálně dostávat denní FT/WSJ/HB a později časopisy do systému bez odstraněného watcher mechanismu?

## Q003 — OPEN — Production editorial workflow
Které části osmi editorial passes mají být kód, model, silný model, lidský review nebo vůbec nemají být samostatným krokem?

## Q004 — OPEN — Publication gate
Jaké minimum evidence/kvality musí být splněno před autonomním publikováním?

## Q005 — OPEN — Rights/licensing
Jaký konkrétní právní/licenční režim bude použit pro jednotlivé zdroje a pro Brief/Detail před komerčním spuštěním?

## Q006 — OPEN — Business model
Finální pricing, free/paid hranice, B2B balíčky a role Detailu nejsou definitivně rozhodnuté.

## Q007 — OPEN — Editorial Memory implementation
D026/D027/D028 now define hybrid search, daily continuity and first-class article/topic enrichment, Story Threads, Signals and Trends. docs/ENRICHMENT.md fixes the conceptual and normalized relational model; broader knowledge semantics are no longer undecided. Operational implementation/acceptance remains open under Q017/Q018/Q019, including recency and editorial use beyond daily Composer.

## Q008 — OPEN — Audio
Kdy a jak zavést stabilní hlasovou identitu a audio adaptaci, aniž by předběhla ověřený textový produkt?

## Q009 — RESOLVED — Minimal Page Ingest contract
D019/D020 define page-ingest-v3 in the existing contracts.py and a new canonical generation. Required perspective expansion and irrelevant inventory are removed. Deployment and corpus acceptance remain Q010, not an undecided schema question.

## Q010 — OPEN — Ingestor v2 acceptance
Jaké minimum reálných stránek a publikací musí Chat Ingestor v2.0 úspěšně zpracovat, než bude Page JSON contract frozen a Assembler implementován?

Acceptance musí zahrnout komplexní novinovou stránku, continuation, grafiku/reklamu a alespoň jednu odlišnou publikaci; později i časopis.

## Q011 — RESOLVED — Assembler review policy
D025 resolves the review boundary. Assembler consumes exactly one accepted manifest ID + SHA, independently verifies selected bytes and joins parts automatically only when continuation evidence yields exactly one valid chain. Similarity/title/byline may corroborate but never create a join. Zero/multiple candidates or ambiguous evidence become NEEDS_REVIEW; broken provenance/input becomes BLOCKED. Assets re-anchor only on one unique authoritative anchor_text match; otherwise they remain unplaced with placement_needs_review.

## Q012 — RESOLVED — Article asset representation and physical storage
D022 decides authoritative page-PNG crops, dual page/text anchors and existing private page-ingest bucket in a new v4/ingestor-v2.2 namespace. OCR inside visuals is optional noncanonical support. Missing/ambiguous placement is review/unplaced, never a guess. This is no longer an undecided bucket/schema question; the implementation gate is INGESTOR.md §21.5.

## Q013 — RESOLVED — Article asset writer and one-page acceptance
D022 / INGESTOR §21.5 writer is implemented, pinned/deployed and accepted on WSJ 2026-10-14 page 2 with three chart crops, exact set-wide readback and VERIFIED durable bindings (CURRENT_STATE/HISTORY). Site v4's generic JSON transport required no redeploy. This closes the writer/transport/single-page gate; it does not establish corpus acceptance or assembly. Q010 remains open; Q011 is resolved by D025, asset placement review follows SYSTEM; any unresolved shared-anchor ordering must remain explicit rather than guessed.

## Q014 — RESOLVED — Immutable editorial correction and page-6 remediation
D024 / INGESTOR §22 implements page-revision-v1 full snapshots with explicit canonical supersedes key/SHA, author/time/reason, standalone crop preview hashes, source fencing and immutable set readback. Production r1 corrected the About Face infographic and the independently discovered clipped photo; all other page-6 text/non-crop metadata is unchanged. Original canonical JSON/PNGs remain intact and blocked from accepted selection. Exact deployed/verified revision identities are in CURRENT_STATE/HISTORY.

## Q015 — RESOLVED — Corpus readback and explicit generation selection
Fresh source-scoped readback verified canonical pages 1–10 and every selected asset, reconciled pages 3–10 with #9 HISTORY without discrepancies and confirmed no v4 page 1. The immutable ACCEPTED_FOR_ASSEMBLY manifest selects v3 page 1, v4 canonical pages 2–5/7–10, and v4 revision r1 page 6. CURRENT_STATE records exact manifest ID/key/SHA and deployment provenance. This resolves this source's receipt/generation-selection gate; Q010 broader quality/publication acceptance remains open; D025 now resolves Q011. No assembly has run.

## Q016 — RESOLVED — Indexer search-layer architecture
D026 / docs/INDEXER.md chooses derived article/chunk embeddings and full-text projections over immutable Article Records, BB-CHUNKING-V1, first-class Cohere BB-EMBEDDING-V1 and Supabase pgvector vector(1024). Eligibility, version/SHA binding, logical tables, states, post-check and multilingual hybrid retrieval are decided. Implementation/acceptance are not implied.

## Q017 — OPEN — Indexer implementation details and retrieval calibration
Before runtime implementation, fix tokenizer/version, paragraph segmentation and whitespace rules, long-paragraph splitting/overlap edge cases, deterministic ID encoding and article embedding serialization/oversized-input policy. Verify provider model availability/limits and 1024D profile support without silent truncation. Specify physical schema/constraints, full-text language configuration, atomic index publication, concurrency, retries and profile-aware retrieval. Evaluate Czech→English/German recall, latency and cost on a small acceptance set. Hybrid score fusion, weighting and thresholds remain deliberately unfrozen pending evidence.

## Q018 — OPEN — Composer implementation and acceptance
D027 / docs/COMPOSER.md fixes architecture, daily-topic-v1 logical handoff, daily-first memory boundary, role separation and review gates. Before runtime implementation, freeze editorial-day timezone/cutoffs and edition-selection closure policy, deterministic topic/corpus hash serialization and output revision identity, physical relational constraints, transactional run/output publication and supersession. Define exact candidate retrieval/fusion/threshold configuration (with Q017), entity annotation provenance, semantic method/model/prompt version and confidence scale, passage evidence encoding, bounded continuity retrieval and review correction protocol. Decide prior-topic indexing/storage details without treating today's article indexes as an implemented topic index. Measure multilingual grouping quality, false merges/splits, singleton and individual reading-value preservation, provenance, review load, latency and cost on a small real acceptance set under D007/D011. No model/provider call, migration or production run is authorized by this question.

## Q019 — OPEN — Enrichment persistence, review and knowledge acceptance
D028 / docs/ENRICHMENT.md defines editorial-enrichment-v1 and normalized derived knowledge tables; offline binding/evidence/coverage/promotion validators and exact metadata/profile candidate helpers are implemented. No deployed system or real-source semantic acceptance is claimed.

The candidate-staging migration is implemented and locally tested, with accepted state unavailable. Exact accepted-knowledge migration/adapter gate: implement accepted Assembler physical articles(article_id, artifact_sha256) unique key and immutable readback; Q017 article/index/chunk IDs and source ranges; Q018 exact Composer output/member identities. Then freeze enrichment JSON wire/storage envelopes, immutable output/retry/selection protocol, catalog/taxonomy snapshot/version and entity alias/disambiguation policy. Extend the FK-bound private staging tables with real upstream FKs, immutable review/evidence/catalog/topic records, transactional selected publication/promotion and authorized review. Local staging integrity/privilege tests pass; real adapter/concurrency/promotion tests remain required. No independent article catalog, invented index schema or canonical prose copies.

Real acceptance must assess source entailment, signal observation dates/independence, counterevidence, reviewed lifecycle changes, multilingual metadata/full-text/vector recall, false entity/cluster merges, latency/cost and review burden. Structural two-article/two-date minimum never replaces editorial trend judgment. Future Q017/Q018 adapters must compare typed snapshots to independently persisted identities; helpers do not approve model-supplied catalogs.
