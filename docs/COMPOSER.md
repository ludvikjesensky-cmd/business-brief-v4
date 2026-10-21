# Composer — Business Brief v4

## Authority and boundary
This is the canonical Composer design contract (D027), analogous to [INDEXER.md](INDEXER.md) and [INGESTOR.md](INGESTOR.md). [SYSTEM.md](SYSTEM.md) owns the Assembler / immutable Article Record boundary. Project Memory owns decisions, current evidence and unresolved implementation questions. This is documentation acceptance only; no Composer runtime, model API call, migration, deployment or production write is implied.

Composer is the v4 successor to v3 Cross-Paper Editor: it produces cross-source daily topics, not a final dossier, editorial selection, Brief or final angle.

```text
verified persisted Article Records
→ Indexer → index post-check
→ Composer → topic post-check
→ Selective Deep Read (where recommended and accepted)
→ Editorial Workflow: Assignment Editor → … → Editor-in-Chief
```

Translator remains a downstream transformation of known source material when required; it is not a prerequisite for multilingual clustering.

## Input: a closed current-day corpus
Freeze an explicit editorial_day and the complete intended current-day corpus before candidate retrieval. Record its publication/edition/source/selection scope, exact article identities, index identities, exclusions and closure time in the run. Current-day means membership in that explicitly selected editorial-day corpus, not a model-inferred date or an unrestricted latest-record query. Day/timezone and edition-cutoff rules must be fixed before implementation (Q018).

Each member must have:
- assembly.status = VERIFIED or VERIFIED_WITH_NOTES;
- post_check.status = PASS and verified durable Article Record persistence;
- a successfully INDEXED set with a passing index post-check for the exact article_record_sha256 and compatible Indexer profiles.

Resolve article_id, publication_id, source_id, Storage bucket/key and article_record_sha256 (persisted artifact SHA, not full-text SHA), plus exact index_run_id and profile identities. Missing or failed indexes remain explicit exclusions/incomplete coverage; never silently call a partial intended corpus complete. An empty corpus produces an explicit empty report, never memory-generated topics.

Canonical Article Records, source text and assets remain immutable. Any correction to source truth follows the existing source review, immutable revision/selection, Assembler and Indexer gates.

## Candidate relationships and semantic grouping
1. Build candidate edges within today's closed eligible corpus using Indexer article embeddings, chunk embeddings, PostgreSQL full-text and metadata/entities. Use only compatible profiles. Entity annotations, if derived, carry producer/version and article provenance; they do not rewrite canonical metadata.
2. Record each candidate relationship's endpoint article/version/index identities, retrieval channels, scores, matched passages/chunks and configuration. Retrieval proposes candidates; embeddings alone never create a topic. Connected components or transitive similarity are not accepted topics by themselves.
3. A semantic/model layer evaluates whether articles describe the same current-day event, story or concrete problem. It may merge, split, retain a single-source topic or mark ambiguity for review. Shared companies, sectors or broad subjects are insufficient. Two unrelated Volkswagen events stay separate even if vector similarity is high.
4. Preserve explainable membership and the distinct contribution of each article. Candidate edges rejected by semantic evaluation remain auditable in the run. Low similarity does not justify silently dropping an eligible article: account for every input as a topic member, explicit singleton or unresolved review item.
5. Only after today's groups exist may prior indexed topics/articles be retrieved for continuity. This retrieval cannot create today's coverage or convert an old article into a current member.

A primary member is a technical identity anchor, not an editorial lead. Adjacent material must demonstrably illuminate the same concrete story/problem; broad topical adjacency stays a separate topic. An uncertain boundary is NEEDS_REVIEW, not an excuse to merge.

## daily-topic-v1 logical output
This freezes the logical handoff, not a machine JSON Schema or SQL migration.

```text
daily-topic-v1
  topic_id
  editorial_day
  working_title
  topic_identity
    description
    evidence_refs[]
  articles[]
    article_id
    publication
      publication_id
      canonical_name
    source_id
    article_record_sha256
    role_in_topic: primary | same_event | follow_up | background_today | adjacent
    membership_reason
    membership_confidence?       # method/scale recorded, not calibrated probability
    evidence_refs[]
    index_refs[]
      index_run_id
      embedding_profile
      chunking_profile
      chunk_ids[]               # when chunk evidence was used
  coverage
    source_count
    publication_count
    cross_source
    single_source
  continuity
    status: new_story | continuing_story | follow_up | unclear
    prior_topic_refs[]
    evidence_refs[]
    notes[]
  daily_delta?                  # today's change, never unsupported synthesis
    description
    evidence_refs[]
  deep_read
    recommendation: recommended | not_recommended | review_required
    reasons[]
    evidence_refs[]
  composer
    status: VERIFIED | VERIFIED_WITH_NOTES | NEEDS_REVIEW | BLOCKED
    confidence
    confidence_method
    method
    notes[]
  provenance
    composer_run_id
    contract_version = daily-topic-v1
    corpus_snapshot_sha256
    candidate_config_version
    semantic_method_version
    model_producer_version?     # if used
    article_refs[]              # exact bucket/key/article_id/artifact SHA
    index_refs[]                # exact run, profiles and used chunk identities
    claim_evidence[]            # field/claim -> article evidence refs
  post_check
    status: PASS | FAIL
    checks[]
```

working_title is a machine/editorial identifier, not the final Brief headline. topic_identity describes the bounded shared story/problem, with article evidence; it is not a final angle. Every evidence reference resolves an exact article_id + article_record_sha256 and a source passage/range or exact chunk_id/text_sha256. Index references resolve back to that same canonical version. Prior topic references additionally identify editorial_day, topic_id, composer_run_id and exact topic output SHA/version.

topic_id is deterministic from editorial_day plus the sorted unique set of current member (article_id, article_record_sha256) pairs, under a versioned hash encoding. Titles, model wording, ranking order and memory matches do not define identity. Identical day/member versions retain the ID; merge, split or changed member bytes produce new IDs. This is a daily group identity, not a permanent story-thread ID. Different evaluations of the same membership are retained as separate run/output versions; never overwrite accepted history. Exact hash serialization and output revision encoding are Q018 implementation gates.

membership_reason and evidence_refs are mandatory even if confidence is supplied. role_in_topic is technical: primary anchors the group; same_event covers the same event; follow_up adds a today's development; background_today is a today's article explaining that story; adjacent is an explicitly justified closely related contribution. None means lead, coverage, curated, INCLUDE, RESERVE or EXCLUDE.

coverage counts distinct source_id and publication_id among today's members only. cross_source is true only when both counts exceed one; single_source is true when publication_count = 1, including multiple articles/editions from one publication. Repeated articles from one publication never manufacture cross-paper coverage. Source count is not independent corroboration or importance.

## Daily = delta. Memory = context.
First form today's topics from today's eligible records. Then retrieve compatible prior indexed articles/topics, verify their exact identities and attach continuity/prior_topic_refs. Historical articles belong in memory references, never articles[]. Memory cannot substitute for missing current-day coverage or inflate coverage counts.

new_story requires an explicit bounded continuity search with no supported prior match; an unavailable or inconclusive search is unclear, not proof of novelty. continuing_story and follow_up require cited prior evidence plus today's relationship. daily_delta is optional: omit it or retain uncertainty when today's difference cannot be supported. Claims about change cite today's evidence and prior evidence where comparison requires it. Memory absence must not block honest today's coverage; report the continuity limitation.

## Selective Deep Read and editorial separation
Composer recommends Deep Read and states why; it does not perform it. Triggers include conflicting sources, a high-value long analysis, evidence spread across sources, uncertain cluster identity, or one source carrying decisive details. Uncertain identity first enters Composer review; a Deep Read recommendation does not bypass that gate.

| Role | Responsibility |
| --- | --- |
| Composer / Cross-Paper Editor | Which current articles describe the same story/problem? |
| Selective Deep Read | Read and verify selected source evidence in depth; resolve detailed evidentiary questions. |
| Assignment Editor | Choose final inclusion, hierarchy, space/form and editorial roles. |
| Story Editor | Establish final angle, tension and story framing. |
| Brief Writer | Write within the approved selection, hierarchy and framing. |

Preserve v3's importance of event ≠ reading value of article (v4 L002). A major event may benefit from cross-paper synthesis; a smaller singleton or one distinctive article inside a group may deserve reading curation. Keep article identity, author/publication metadata and exact original text/assets accessible so author argument and perspective survive grouping. Composer does not score final importance or allocate editorial roles. Assignment Editor receives all accepted topics and their individual articles, not only a preselected subset.

## Minimal relational operational structures
These are intended logical structures only. Reuse existing article/index identity rather than duplicating authoritative prose.

| Structure | Minimal logical contents |
| --- | --- |
| editorial_days | editorial_day identity, timezone/cutoff policy, selected edition/source/manifest scope, closure state/time, corpus snapshot identity/SHA and exact eligible/excluded member identities with reasons |
| composer_runs | run_id, day FK, corpus SHA, contract/config/method/model versions, candidate graph/evidence and rejected-edge trace, review correction refs, input/output counts, unresolved articles, status/post-check, timestamps/error and versioned output identities/SHA |
| daily_topics | topic_id, day FK, run_id FK, output version/SHA, working_title, topic_identity/evidence, coverage, continuity, optional delta/evidence, deep_read recommendation/reasons, composer confidence/method/notes, status/post-check |
| daily_topic_articles | topic output FK, ordered article/version FK, publication/source identity, technical role, reason/confidence, membership evidence, exact index/profile/chunk refs |
| daily_topic_memory_refs | topic output FK, prior topic output or prior article/version FK, relationship/reason and exact evidence/index provenance |

Unique topic outputs are keyed by run_id + topic_id; memberships are unique by topic output + article_id + article_record_sha256. An article may serve multiple concrete problems only with separate explicit reasons; report this overlap, never duplicate it within one topic. Prior-reference targets must exist and be earlier than today's editorial day. Preserve accepted run/output versions and explicit supersession/selection on rerun. Physical constraints, transactional publication and artifact serialization/storage details remain Q018. These structures hold operational relationships and derived judgments; canonical Article Records remain unchanged.

## Topic post-check, statuses and review gate
The deterministic structural check independently verifies:
- every current article ID, artifact SHA, Storage identity and index/profile/chunk reference exists, matches and passed eligibility;
- current memberships are confined to the frozen corpus; every input is accounted for and unresolved/overlapping membership is explicit;
- topic IDs reproduce from exact day/member inputs; no duplicate membership;
- coverage counts recompute from today's members; cross-source really spans more than one publication/source and single-source is explicit;
- every membership has an explainable reason and resolvable evidence; every memory reference exists at its exact prior identity;
- generated factual claims in identity/title/delta/continuity/reasons/notes carry article provenance; no unsupported model assertion is accepted.

A structural PASS proves integrity and presence of evidence, not semantic truth or entailment. Semantic grouping and claim support still require model/Chat judgment and review when uncertain. Similarity/confidence or source count never substitutes for that judgment.

| Status | Meaning and handoff |
| --- | --- |
| VERIFIED | Structural PASS, supported identity/membership and no unresolved semantic issue; eligible downstream. |
| VERIFIED_WITH_NOTES | Structural PASS and supported membership, with explicit nonblocking limitations; eligible downstream with notes. |
| NEEDS_REVIEW | Semantic ambiguity, contested membership or unresolved claim support; stop downstream use of that output. |
| BLOCKED | Broken/missing identities, SHA/integrity or eligibility failure, failed structural gate; repair before retry. |

A run cannot claim complete acceptance while intended inputs/topics remain NEEDS_REVIEW or BLOCKED; report counts and partial coverage explicitly. Optional unavailable memory can be a nonblocking note with continuity unclear; a claimed but dangling memory reference is BLOCKED.

```text
Indexer → index post-check → Composer → topic post-check
  NEEDS_REVIEW → Chat review against exact article evidence
               → explicit recorded membership/identity correction
               → rerun Composer + topic post-check
  BLOCKED → repair underlying input/index/integrity failure → rerun gates
  VERIFIED / VERIFIED_WITH_NOTES → Selective Deep Read → Editorial Workflow
```

Chat corrections record author/reason, exact evidence and superseded output/run; they do not patch canonical articles or bypass rerun. If source truth is wrong, use upstream immutable correction and reassembly/reindexing first. A future pipeline runner may orchestrate deterministic steps, retries and reports, but must stop at semantic review gates.

## v3 inheritance and implementation boundary
Historical sources: business-brief-v3 at commit 933b5c47fb96c97333ff24dda4e7e019486ebbfd, [EDITORIAL_PIPELINE §9](https://github.com/ludvikjesensky-cmd/business-brief-v3/blob/933b5c47fb96c97333ff24dda4e7e019486ebbfd/docs/EDITORIAL_PIPELINE.md#9-daily-editorial-layer), [EDITORIAL_WORKFLOW §§4–7](https://github.com/ludvikjesensky-cmd/business-brief-v3/blob/933b5c47fb96c97333ff24dda4e7e019486ebbfd/docs/EDITORIAL_WORKFLOW.md#4-kanonický-redakční-řetězec), and EDITORIAL_PLAYBOOK §6 in that same tree. Reuse Cross-Paper Editor, daily_topics, daily_delta, single-source vs cross-paper, Selective Deep Read, and the separation of importance and reading value. The old Fast Editorial INCLUDE/RESERVE/EXCLUDE stage is not a Composer selection power.

v4 starts from verified assembled/indexed Article Records. Do not reintroduce Provisional Issue Maps, provisional discovery or a Memory-ready prerequisite as a required v4 layer. v3 is historical design evidence, not a code dependency.

Before implementation, resolve Q018 alongside Q017 and measure a small real multilingual acceptance set: same-event cross-paper matches, same-entity different events, transitive false merges, singletons, distinctive analyses, ambiguous identity, memory-only temptations and conflicting evidence. Fix review behavior and cost/quality under D007/D011 before automation. This consolidation makes no runtime changes, model calls, database migrations, deployments or production data writes.
