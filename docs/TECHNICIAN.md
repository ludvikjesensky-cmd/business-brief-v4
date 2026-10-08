# Technician v4

**Status:** CANONICAL COMPONENT DEFINITION  
**Owner:** Technician  
**Phase:** Autonomous Production Design  
**Upstream:** Source Inbox / future Source Acquirer  
**Downstream:** Ingestor  
**Primary output:** `source-bundle-v4`

## 1. Purpose

Technician is the universal technical intake gateway for Business Brief v4.

It accepts a closed physical representation of an edition, establishes its technical and logical identity, preserves the immutable source, prepares reliable physical evidence for downstream processing, and hands a validated Source Bundle to the Ingestor.

Technician is not specific to Financial Times, The Wall Street Journal or Handelsblatt. The same component must be able to accept any publication that the platform may process in the future.

> **Technician may determine what document it has received. It must not determine what the document is about.**

Its responsibility ends at technical evidence preparation. Editorial and article semantics belong downstream.

## 2. Boundary

Canonical flow:

```
Source Acquirer / manual upload
          ↓
      SOURCE INBOX
          ↓
      TECHNICIAN
          ↓
   source-bundle-v4
          ↓
       INGESTOR
```

Source acquisition is explicitly outside Technician.

A future FT, WSJ, Handelsblatt or other Source Acquirer may detect and download an edition and place it into the Source Inbox. A human may do the same manually. Technician must behave identically regardless of how the source arrived.

The Source Inbox is an intake location, not the durable processing queue.

> **Inbox is not the queue. The database is the queue.**

## 3. Runtime model

Technician is intended to run on Railway as an **on-demand worker**, not as a permanently polling service.

A source arrival creates a durable Technician job. An event/webhook may wake the worker, but the event is not the source of truth.

> **Webhook is a wake-up signal, not a processing guarantee.**

When Technician starts, it drains all available claimable jobs, one by one, and exits when no work remains.

A periodic reconciliation/safety sweep may wake Technician if pending jobs exist and no worker is processing them. This protects the pipeline against lost webhooks or failed wake-ups.

The exact Supabase → Railway wake-up implementation remains an implementation decision and must be validated separately.

## 4. Accepted source concept

The preferred source is a complete PDF because it naturally represents a closed edition.

A complete ordered set of page images (JPG/PNG) is also a valid Reference Edition when no usable standalone PDF exists.

The architectural principle inherited from v3 remains:

> **PDF is not the principle. The closed edition is the principle.**

Technician may later support other complete physical representations through explicit versioned adapters. New formats must not silently weaken the Source Bundle contract.

## 5. Universal source identity

Technician must work with previously unseen publications.

Before expensive full-document processing it performs a lightweight **IDENTIFY** stage and attempts to establish:

- `publication_name`
- `publication_id`
- `edition_date`
- `edition_variant`
- `language`
- identity confidence
- identity evidence

Filename is never authoritative identity evidence.

Identification should use a cascade from cheapest and most deterministic evidence to more expensive fallback:

1. supplied trusted intake metadata, when available;
2. PDF metadata;
3. native text from the first/identity-bearing page(s);
4. lightweight OCR of the first/identity-bearing page(s);
5. narrowly scoped multimodal identification as a fallback.

An AI fallback may identify publication, edition date, edition variant and language, but must not summarize or interpret editorial content.

If identity cannot be established with sufficient confidence, the source is preserved and the job becomes `IDENTITY_UNRESOLVED`. It must not be silently guessed, discarded or admitted as a known edition.

## 6. Publication Registry

Canonical publications are represented in a Publication Registry.

A registry record may contain:

- `publication_id`
- canonical name
- known aliases
- language(s)
- country/market where useful
- frequency where useful
- known identity patterns
- first seen
- last seen

The registry is not a hard-coded whitelist. A previously unseen publication can enter the system, be identified, receive a canonical identity and become known for later deterministic recognition.

The exact automatic-versus-reviewed policy for creating a brand-new canonical publication record remains an implementation decision. The system must preserve evidence and confidence either way.

## 7. Two levels of identity

Technician distinguishes **physical source identity** from **logical edition identity**.

### Physical identity

`source_sha256`

SHA-256 answers:

> Is this exactly the same physical source?

The original filename does not affect this identity.

### Logical edition identity

Conceptually:

```
edition_key =
    publication_id
  + edition_date
  + edition_variant
```

`edition_variant` may represent values such as daily, weekend, weekly, Europe, US, Asia, special, supplement or `default`.

The schema must remain extensible because publication schedules and regional/special editions vary.

The logical identity answers:

> Does this source claim to represent an edition we already have?

## 8. Duplicate policy

Duplicate handling happens before expensive full processing whenever possible.

### Same SHA

If the same SHA arrives again, including under a different filename, it is the same physical source.

It must not create a second edition or repeat the same Technician processing for the same Technician/contract version.

The arrival is recorded as a duplicate and linked to the existing source.

### Different SHA, same edition key

A different SHA with the same logical edition identity is **not automatically discarded**.

It may be:
- the same edition serialized differently;
- a corrected/revised edition;
- an incomplete or damaged copy;
- another legitimate physical variant.

The second source is preserved and marked as an edition collision / possible variant. Full expensive processing should not be duplicated until the collision policy determines whether it is necessary.

Technician must not decide editorially which edition is “better”.

> **SHA identifies the file. Publication + edition date + variant identifies the edition.**

## 9. Durable job queue

Every accepted source arrival is represented by a durable Technician job.

The database, not the webhook, is authoritative for work still to be done.

A conceptual job record includes:

- `job_id`
- `source_id`
- `status`
- `attempt`
- `worker_id`
- `created_at`
- `claimed_at`
- `heartbeat_at`
- `completed_at`
- failure/retry information
- Technician version
- Source Bundle contract version

A worker atomically claims one eligible job. Two workers must not process the same job concurrently.

After completing one job, Technician asks for the next eligible job. It exits only when the available queue is empty.

## 10. Lease, crash recovery and retry

A claimed job has a lease/heartbeat.

If a worker crashes, loses connectivity or disappears while a job is `PROCESSING`, the job must not remain stuck forever.

After lease expiry the system can return the job to a retryable state according to policy.

Technician operations must therefore be idempotent.

Re-running the same source with the same Technician and contract version must not create a second logical edition or expose inconsistent downstream artifacts.

A useful processing identity is conceptually:

```
source_sha256
+ technician_version
+ source_bundle_contract_version
```

This allows a historical source to be deliberately reprocessed by a later Technician version without pretending it is a new source.

## 11. Detailed processing sequence

### T00 — WAIT FOR SOURCE
No active polling worker is required. The durable system waits for source arrivals/jobs.

### T01 — DETECT / REGISTER ARRIVAL
Register a completed source upload or ordered page set. Never process a partially uploaded file.

The intake mechanism should provide an atomic completion signal, for example upload-to-temporary followed by finalize/move, or an equivalent verified mechanism.

### T02 — REGISTER SOURCE
Create or resolve `source_id`, record arrival time, intake metadata, original filename/path and provenance available from acquisition.

### T03 — FREEZE ORIGINAL
Store the received physical source as immutable evidence.

The original is never overwritten by OCR, repair, normalization, splitting or any other processing.

### T04 — HASH ORIGINAL
Compute SHA-256 for the original PDF.

For an ordered page-image source, hash individual pages and create a canonical identity for the ordered source set.

Check physical duplication immediately.

### T05 — IDENTIFY SOURCE
Determine publication identity, edition date, edition variant and language using the identification cascade defined above.

Record confidence and evidence.

### T06 — CHECK LOGICAL DUPLICATION
Resolve the logical `edition_key`.

If an edition with that identity already exists, apply the duplicate/collision policy before expensive processing.

### T07 — IDENTIFY FORMAT
Recognize the physical source type, currently at minimum:
- PDF;
- complete ordered JPG/PNG page set.

Unsupported input is preserved and blocked with an explicit reason.

### T08 — VALIDATE CONTAINER
For PDF, verify that the document opens, has pages and that pages can be accessed/rendered.

For an image set, verify files, ordering and technical readability.

### T09 — COUNT AND INVENTORY
Record page count, file size, page dimensions and relevant neutral technical metadata.

### T10 — CHECK PHYSICAL PAGE SEQUENCE
Verify technical sequence properties such as missing members or duplicates in an ordered page set.

Technician does not infer editorial reading order or article continuity.

### T11 — TEXT-LAYER PROBE
For PDF, measure whether a native text layer exists and whether it is technically usable as physical evidence.

This is not article interpretation.

### T12 — OCR DECISION
Choose `OCR_REQUIRED` or `OCR_NOT_REQUIRED` according to technical criteria.

OCR remains Technician responsibility, inherited from v3.

### T13 — OCR DERIVATIVE
If required, create an OCR derivative.

> **OCR never overwrites the immutable original.**

### T14 — PREPARED SOURCE
Select/build the canonical prepared physical representation used downstream while retaining links to the immutable original.

### T15 — RENDER PAGE IMAGES
Produce normalized page images according to the frozen rendering specification required downstream.

Every page image must map unambiguously to its source page.

### T16 — MECHANICAL SPLIT DECISION
Determine whether technical limits require the prepared PDF/container to be split.

### T17 — MECHANICAL SPLIT
If splitting is required, split only according to physical/technical limits.

> **Splitting is mechanical only.**

Technician must never split by article, section, topic, importance or meaning.

The v3 lesson remains valid: byte hashes of split PDF artifacts are not a correctness gate because PDF serialization may not be byte-stable across runs.

### T18 — ARTIFACT VALIDATION
Verify all generated derivatives and ensure page count/order correspondence with the frozen source.

A derivative that cannot be validated must not be exposed downstream as ready.

### T19 — BUILD MANIFEST
Create the canonical Source Bundle manifest containing identity, provenance, technical evidence, paths, hashes, OCR decision, split information, warnings, versions and validation results.

### T20 — SOURCE BUNDLE VALIDATION
Validate the complete output against the versioned `source-bundle-v4` contract.

### T21 — ATOMIC FINALIZE
Build artifacts in a working/staging location.

Only after all mandatory validation passes may the bundle be atomically finalized into its canonical ready location.

Ingestor must never observe a partially constructed Source Bundle.

### T22 — HANDOFF
Mark the bundle `READY_FOR_INGESTOR`.

Only this state authorizes downstream Ingestor processing.

### T23 — DRAIN QUEUE
Claim the next eligible Technician job.

If work remains, repeat. If not, exit the Railway worker.

### T24 — EVENT LOG
Persist operational evidence including timings, input/output sizes, source identity, hashes, OCR decision, splitting, warnings, retries, failures and component/contract versions.

## 12. Source Bundle v4

The exact JSON Schema will be frozen during implementation, but the canonical contract must at least represent:

```
source-bundle-v4/
    manifest.json
    original/
        ...
    prepared/
        ...
    pages/
        page-0001.*
        page-0002.*
        ...
    parts/
        ... optional mechanical parts ...
```

Conceptual manifest fields include:

```json
{
  "contract": "source-bundle-v4",
  "source_id": "...",
  "source_sha256": "...",
  "received_at": "...",

  "publication": {
    "publication_id": "...",
    "canonical_name": "...",
    "edition_date": "YYYY-MM-DD",
    "edition_variant": "default",
    "language": "...",
    "identity_confidence": 0.99,
    "identity_evidence": []
  },

  "original": {
    "filename": "...",
    "mime_type": "application/pdf",
    "file_size": 0,
    "page_count": 0
  },

  "native_text": {
    "available": true,
    "usable": true
  },

  "ocr": {
    "required": false,
    "performed": false
  },

  "split": {
    "performed": false,
    "parts": []
  },

  "prepared_source": "...",
  "page_images": [],

  "technician_version": "...",
  "status": "READY_FOR_INGESTOR"
}
```

The schema above is conceptual, not yet the frozen machine JSON Schema.

## 13. Status model

At minimum the component must distinguish:

- `PENDING`
- `PROCESSING`
- `READY_FOR_INGESTOR`
- `DUPLICATE_SOURCE`
- `EDITION_COLLISION`
- `IDENTITY_UNRESOLVED`
- `RETRY_PENDING`
- `BLOCKED`
- `FAILED`

Warnings may coexist with a successful bundle when they do not violate the contract.

Exact state-machine names may be normalized during implementation, but the semantic distinctions must remain.

## 14. Failure policy

Technician must fail visibly.

Examples of blocking conditions:
- corrupt/unreadable source;
- incomplete physical source representation;
- page that cannot be rendered when page evidence is required;
- unsupported source format;
- unresolved source identity where identity is required for safe edition processing;
- failed mandatory OCR;
- derivative/source page mismatch;
- Source Bundle contract validation failure.

A blocked source remains preserved with its evidence and failure reason.

Technician must never silently create a “good enough” bundle that violates the contract.

## 15. What Technician may know

Technician may know:
- publication identity;
- edition date and variant;
- language;
- physical page count and sequence;
- file/container metadata;
- text-layer availability/technical usability;
- OCR state;
- physical hashes;
- provenance of source acquisition supplied by upstream systems.

This knowledge exists to establish identity and prepare evidence.

## 16. What Technician must not do

Technician must not:
- select articles;
- identify important stories;
- summarize articles;
- classify topics;
- determine editorial importance;
- detect article boundaries as an editorial operation;
- reconcile article continuations;
- build Issue Maps;
- create Article Records;
- perform editorial reading order;
- decide what belongs in Brief or Detail;
- acquire/download publications from publishers;
- silently choose between competing logical edition variants based on editorial content.

Those responsibilities belong to downstream or upstream components.

## 17. Inherited v3 principles

The following v3 decisions are explicitly retained:

1. **Immutable input.**
2. **SHA/provenance are first-class evidence.**
3. **OCR belongs to Technician.**
4. **OCR output is a derivative, never a replacement for the original.**
5. **Splitting is mechanical only.**
6. **Split-PDF byte hashes are not a correctness gate.**
7. **Page images are part of the technical evidence layer.**
8. **Technician prepares physical evidence; semantic interpretation begins downstream.**

The v3 `source-bundle-v2` was frozen and accepted for PDF sources. V4 does not silently mutate it. V4 introduces a new explicit `source-bundle-v4` contract because universal publication identity, durable jobs, duplicate handling, autonomous operation and broader Reference Edition inputs are now first-class requirements.

## 18. Observability and dashboard

Technician must expose enough structured state for the morning dashboard to answer:

- how many sources arrived;
- what publication/edition each source represents;
- which are pending, processing, ready, duplicate, collision or blocked;
- current worker/job;
- processing duration;
- OCR/split status;
- retry count;
- failure reason;
- whether Ingestor is authorized to proceed.

Healthy detail stays in the dashboard/event log. Critical integrity or deadline threats may feed the exception-only alert policy defined in `AUTONOMOUS_MORNING.md`.

## 19. Non-goals

Technician is not:
- a newspaper downloader;
- a crawler;
- an editorial agent;
- a publication-specific FT/WSJ/HB parser;
- an article detector;
- an Ingestor;
- a permanent polling daemon.

Its design should remain usable if the platform processes five, twenty or one hundred different publications.

## 20. Canonical summary

> **Technician v4 is the universal, idempotent technical gateway from a closed source edition to validated physical evidence. It identifies the publication and edition, prevents accidental duplicate processing, preserves the immutable source, performs technical preparation including OCR and mechanical splitting, validates every derivative, and exposes a Source Bundle to Ingestor only after an atomic successful handoff.**

Operational shorthand:

```
ARRIVE
→ REGISTER
→ FREEZE
→ HASH
→ IDENTIFY
→ DEDUPLICATE
→ VALIDATE
→ OCR IF NEEDED
→ PREPARE
→ RENDER
→ SPLIT IF NEEDED
→ VALIDATE ARTIFACTS
→ MANIFEST
→ ATOMIC FINALIZE
→ READY FOR INGESTOR
→ NEXT JOB / EXIT
```
