# Enrichment and Editorial Knowledge — Business Brief v4

## Authority and purpose
This document defines the v4 derived enrichment and long-term editorial knowledge contract. It carries forward the useful v3 editorial-enrichment-v0.2 / Memory semantics while adapting them to immutable v4 Article Records.

Canonical source truth remains the immutable article-record-v1 artifact. Enrichment never rewrites canonical prose, title, byline, assets or provenance. Every enrichment row is rebuildable, versioned and bound to the exact article_id + article_record_sha256.

Knowledge chain:

    Article / current-day event
    → Story Thread
    → Signal
    → Trend
    → Analysis / Business Intelligence

A Trend is not a synonym for a topic. A Story Thread is not a broad trend. A single article may create a Signal or candidate relationship, but it must not automatically create an accepted long-term Trend.

## BB-ENRICHMENT-V1
Article-level enrichment uses profile BB-ENRICHMENT-V1.

Required article metadata:
- exactly one broad category;
- topics[]: concrete subjects directly discussed;
- tags[]: useful retrieval/filter terms;
- entities[]: important people, companies, institutions or organizations;
- geographies[]: materially relevant locations;
- industries[]: materially relevant sectors;
- story_thread_candidates[]: candidate links to concrete continuing stories;
- trend_candidates[]: candidate links to broader long-running developments;
- signals[]: evidence-bearing observations that may support, weaken, contradict or neutrally relate to a thread/trend.

The broad category controlled list is carried forward from v3 unless a future profile supersedes it: Politika, Geopolitika, Ekonomika, Energie, Firmy a průmysl, Technologie, Finance a trhy, Osobní finance, Právo a regulace, Média, Ostatní.

Every run records profile, producer, producer/model version where applicable, article_record_sha256, status and evidence/provenance. Model output is derived editorial metadata, never source evidence.

## Article enrichment contract
Logical payload:

    editorial-enrichment-v1
      profile = BB-ENRICHMENT-V1
      producer
      articles[]
        article_id
        article_record_sha256
        category
        topics[]
        tags[]
        entities[]
        geographies[]
        industries[]
        story_thread_candidates[]
          label
          relation
          evidence_refs[]
          confidence?
        trend_candidates[]
          label
          relation
          evidence_refs[]
          confidence?
        signals[]
          signal_id
          description
          polarity: supports | weakens | contradicts | neutral
          target_kind?: story_thread | trend
          target_ref_or_label?
          evidence_refs[]

Validation requires exact coverage of the intended input set, no duplicate article_id, exact SHA binding, non-empty normalized labels, unique values inside list fields, and evidence refs for every candidate/Signal claim. An enrichment for one Article Record SHA is invalid for another revision.

## Story Threads
A Story Thread is a concrete continuing story, company action, policy, transaction, conflict, regulatory process or event lineage that can be followed through time. Lifecycle: candidate → accepted → retired, with rejected retained as an auditable review result.

A candidate may come from article enrichment or Composer. Accepted status requires explicit review/promotion and durable provenance. Shared broad topic/industry/entity is not enough to establish a Story Thread relationship.

## Signals
A Signal is a dated evidence unit derived from a specific Article Record or accepted daily topic. It says that something may be changing. Signal polarity is supports, weakens, contradicts or neutral. Every Signal must have exact evidence refs and exact canonical article/version provenance. A Brief may report today's Signal/delta without asserting that a Trend is established.

## Trends
A Trend is a broad long-term phenomenon evidenced by repeated Signals, events and/or Story Threads across time and sources. Lifecycle: candidate → accepted → retired, with rejected retained for audit.

Promotion to accepted is a separate knowledge decision. It requires more than one Signal and must not be automated from a single article, one daily topic, shared entity, vector similarity or model confidence alone. Promotion records supporting Signal IDs, provenance, reviewer/method and version. Later evidence may strengthen, weaken or reverse the interpretation without deleting prior history.

## Daily topics and Composer
Composer may attach knowledge_links to daily-topic-v1: topics/tags/entities/geographies/industries aggregated from exact member enrichments; Story Thread candidates or accepted links; today's Signals; Trend candidates or accepted links.

These links help continuity and Memory. They do not determine daily-topic membership. Broad shared Trend/Topic/Industry/Geography alone must never merge otherwise unrelated current-day articles. Composer may propose new candidates, but it cannot silently promote long-term knowledge.

## Hybrid Editorial Memory
Business Brief Memory is not only vector RAG. It combines SQL metadata and exact relationships, PostgreSQL full-text retrieval, multilingual vector retrieval through the versioned embedding profile, time and provenance, entities, Story Threads, Signals, Trends, editorial history and published outputs.

For the morning Brief: Daily = delta. Memory = context.
For Trend and Analysis products, Memory is primary knowledge material.

Indexer may use enrichment as metadata filters only when it is bound to the exact Article Record SHA and accepted profile/status. Cohere creates multilingual embeddings; PostgreSQL/pgvector stores and searches vectors and is itself language-agnostic.

## Persistence model
The v4 relational knowledge layer is additive and derived: article_enrichment_runs, article_enrichments, story_threads, story_thread_articles, signals, trends and trend_signals. Canonical prose remains only in Article Record Storage.

Until the Assembler article index tables are implemented, enrichment rows bind by article_id + article_record_sha256 without pretending that a missing FK already exists. A later additive migration may attach FKs to the operational article index.

## Review and gates
Derived enrichment statuses: PENDING, VERIFIED, VERIFIED_WITH_NOTES, NEEDS_REVIEW, BLOCKED. Durable Story Thread/Trend lifecycle: candidate, accepted, rejected, retired.

Rules:
- unsupported semantic claims → NEEDS_REVIEW;
- broken identity/SHA/evidence refs → BLOCKED;
- no one-article automatic Trend promotion;
- candidate knowledge never masquerades as accepted knowledge;
- accepted history is append/audit oriented, not silently overwritten.

## v3 migration
Retained: category/topics/tags/entities/geographies/industries, Story Thread vs Trend distinction, Story Threads for continuity, Signals as evidence over time, Trends from repeated evidence, hybrid Memory, exact enrichment coverage validation, and the principle that today's Brief uses Signals while long-term Memory supports Trend/Analysis work.

Adapted: enrichment is a sidecar bound to immutable Article Records; multilingual vector search uses BB-EMBEDDING-V1; Composer works from verified assembled/indexed records; long-term knowledge promotion is explicit and versioned.

Not carried forward: v3 Provisional Issue Map as a required layer, v3 Czech translation/summary prerequisite for Memory readiness, or any assumption that a model label alone is accepted durable knowledge.