# Indexer — Business Brief v4

## Authority and boundary
This is the canonical Indexer design contract (D026), analogous in role to [INGESTOR.md](INGESTOR.md). [SYSTEM.md](SYSTEM.md) owns the Assembler / Article Record contract; Project Memory owns decisions, current status and open questions. This document defines intended behavior, not a deployed runtime or an accepted retrieval benchmark.

The Article Record is canonical, immutable JSON in private Supabase Storage. Indexer creates only derived, rebuildable search data. It must never mutate Article Records, their full_text, source Page JSONs or PNG assets. PostgreSQL search text is a disposable projection, never a second canonical article body.

## Input and eligibility
Select explicit Article Record identities from a particular assembly run or edition selection. Resolve and verify article_id, Storage bucket/key and exact article_record_sha256 before indexing. This SHA is the SHA-256 of the persisted Article Record bytes (articles.artifact_sha256), distinct from the full-text SHA.

Both gates are required:
- assembly.status = VERIFIED or VERIFIED_WITH_NOTES;
- post_check.status = PASS, plus verified durable Article Record persistence.

NEEDS_REVIEW and BLOCKED are excluded and reported with reasons; never silently promote them. An index for one article_record_sha256 is not valid for another revision.

## BB-CHUNKING-V1
Input is canonical full_text in its original language. Preserve Unicode, paragraph order and source wording. No summary, translation, paraphrase or rewrite before embedding. Any technical whitespace normalization must be deterministic, versioned and traceable to the original paragraphs; it cannot modify canonical bytes.

Build chunks from whole paragraphs, targeting roughly 450–700 tokens. Close a chunk before the next paragraph would exceed the target upper bound. Short articles and the final remainder may be shorter. Use exactly one paragraph of overlap between adjacent ordinary chunks. Ensure forward progress: overlap must not produce duplicate-only chunks. An exceptionally long paragraph may be technically split; retain source paragraph identity and fragment offsets. Never split on physical page boundaries.

Every chunk carries zero-based chunk_index, paragraph_from / paragraph_to, exact derived text and text_sha256 over its UTF-8 bytes. chunk_id is deterministic from article_id, article_record_sha256, chunking_profile, chunk_index, source range (including fragment offsets when present) and text_sha256; the same versioned inputs must produce the same IDs and ordered chunks. Hash encoding and tokenizer/split details must be frozen before runtime implementation (OPEN_QUESTIONS Q017), not improvised per run.

## BB-EMBEDDING-V1
Treat this profile as first-class versioned configuration, resolved and recorded by both indexing and retrieval:

| Setting | Value |
| --- | --- |
| Provider | Cohere |
| Model | embed-v5.0-pro |
| Dimensions | 1024 |
| Indexed document input_type | search_document |
| Query input_type | search_query |
| Similarity | cosine |
| Chunking profile | BB-CHUNKING-V1 |
| Language space | shared multilingual vector space |

Cohere produces vectors; Supabase/Postgres pgvector stores and compares vector(1024). Produce one article-level embedding for thematic article similarity and one embedding per chunk for passage retrieval. Article representation uses source title, optional subtitle/byline and full_text, without generated prose. Exact field serialization and oversized-input handling remain implementation gates; silent truncation is forbidden.

A material model, dimension, input representation or chunking change requires a new profile version and rebuild. Never mix incompatible profiles in one similarity search or relabel old vectors. This records the chosen project profile; provider capability, limits, cost and multilingual quality still require implementation-time validation.

## Derived logical tables
These are logical contracts, not SQL migrations. Each row binds to the exact canonical version and profile.

```text
article_embeddings
  article_id
  article_record_sha256
  embedding_profile
  embedding_model
  input_type = search_document
  embedding vector(1024)
  created_at

article_chunks
  chunk_id
  article_id
  article_record_sha256
  chunking_profile
  chunk_index
  paragraph_from
  paragraph_to
  fragment_offsets?          # for exceptionally long split paragraphs
  text
  text_sha256
  embedding_profile
  embedding_model
  input_type = search_document
  embedding vector(1024)
  created_at

article_index_runs
  index_run_id
  article_id
  article_record_sha256
  chunking_profile
  embedding_profile
  status
  chunk_count
  started_at
  completed_at
  error?
```

Article embedding identity includes article_id + article_record_sha256 + embedding_profile. Chunk order is unique within article/version/chunking profile; vector identity also includes embedding_profile so a later embedding rebuild need not collide with stable chunk identity. Physical keys/constraints remain to be designed. Store derived PostgreSQL full-text search data alongside these projections; exact tsvector placement and language configuration remain open.

## Execution and index post-check
1. Resolve explicit inputs; verify persistence, identities, SHA and eligibility. Report excluded records.
2. Resolve the exact chunking and embedding profiles; create a PENDING run.
3. Move to INDEXING; derive article representation and ordered chunks, compute hashes, obtain article/chunk embeddings and persist derived full-text/vector data.
4. Independently post-check the persisted set against the expected deterministic output:
   - expected chunk_count equals actual count, with complete contiguous chunk_index coverage;
   - chunk IDs and per-version/profile order are unique;
   - source ranges, exact chunk text and recomputed text_sha256 match;
   - article-level embedding and every expected chunk embedding exist and contain exactly 1024 finite dimensions;
   - all rows have the same intended article_id, article_record_sha256 and compatible model/profiles/input_type;
   - derived full-text projection is present and bound to the same canonical version.
5. Set INDEXED only after the complete set passes. Missing/partial data, API errors or failed post-check yield FAILED with an actionable error. Incomplete sets must not be served as a completed index.

States are PENDING → INDEXING → INDEXED or FAILED. Retry failed work against the same exact canonical identity and profiles; a retry must not duplicate a successful set or expose partial results. Atomic publication/concurrency and recovery mechanics must be fixed before implementation. Failure leaves canonical content intact; rebuilding replaces only derived data.

Report eligible, skipped (with reasons), INDEXED and FAILED article counts, article embedding count, expected/actual chunk and chunk embedding counts, full-text coverage and post-check result. Done means every intended eligible article passed; partial completion remains explicit.

## Retrieval
Hybrid retrieval combines metadata filters (publication, edition/date, source and article identity), PostgreSQL full-text relevance and vector cosine similarity. Both article-level similarity and chunk-level evidence are available. Ranking weights, score fusion and thresholds are deliberately not frozen; evaluate them on real editorial queries.

Embed queries with BB-EMBEDDING-V1 / search_query and compare only with compatible search_document vectors. Multilingual retrieval must allow a Czech query to retrieve English or German source passages in the shared space. Return original source text with article/version/chunk provenance; no translation is required to index or retrieve it. Translation or synthesis belongs downstream. PostgreSQL lexical matching alone is not a promise of cross-language recall.

## Manual workflow and future runner
ordinary Chat Ingestor → accepted Edition Selection Manifest → Assembler → assembly post-check → immutable Article Record persistence → Indexer → index post-check → done.

If assembly is NEEDS_REVIEW, ordinary Chat reviews against source evidence, corrects through the immutable revision/explicit selection discipline, then reruns Assembler and its post-check. No direct patch to an existing canonical Article Record and no bypass of eligibility. BLOCKED integrity failures require repair of the underlying input/implementation before rerun.

A future pipeline runner may orchestrate these explicit handoffs, retries, reports and review pauses. It must preserve ordinary Chat supervision and all acceptance gates; this decision does not authorize autonomous semantic ingest.

## Implementation boundary
No Indexer runtime, database migration, bucket creation, Cohere call or runner deployment is included in this design consolidation. Before implementation resolve Q017, validate the chosen provider profile and measure a small multilingual acceptance set under D007/D011. Operational proof belongs in CURRENT_STATE, not inferred from this specification.

## Enrichment metadata and hybrid Memory (D028)
[ENRICHMENT.md](ENRICHMENT.md) owns derived article/topic annotations and reviewed Story Thread / Signal / Trend relations. Join selected enrichment to exact article_id + article_record_sha256 and producer/profile/version; never enrich canonical prose or replace the original source representation with generated tags. Source-only enrichment may run after Article Record persistence; it does not require embeddings and does not alter Indexer eligibility. Missing metadata remains explicit rather than silently dropping indexed articles.

SQL metadata filters include accepted entity, topic, industry, geography, tag, Story Thread and Trend IDs, plus date/source and review/lifecycle constraints. Candidates require an explicit review query mode. Return evidence, relation direction, exact accepted revision and index/profile/chunk provenance; a contradiction to a trend is not support. Metadata matches complement full-text and vectors. Broad shared trend/topic alone cannot force daily-topic membership. Article/chunk vectors remain derived Cohere BB-EMBEDDING-V1 in its shared multilingual space; PostgreSQL supplies storage/comparison and configured lexical search, not a promise of cross-language lexical recall.

Offline knowledge_retrieval.py now provides exact accepted metadata matching, metadata candidate pairs and profile-compatible hit assembly. It makes no Cohere/full-text/SQL calls and does not fuse scores or form topics. Q017/Q018/Q019 still gate physical schema, live retrieval adapters, bounded prior knowledge retrieval and real Czech→EN/DE acceptance. These additions do not claim an implemented Indexer.
