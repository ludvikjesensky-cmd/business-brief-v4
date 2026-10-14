# Technician v4.3 — technical preparation contract

Technician receives a closed PDF edition and returns a validated `SourceBundle`.
It does not classify pages, discover articles, choose reading order, select
relevance, reconstruct continuations or certify OCR transcription accuracy.
Word/block evidence remains the Ingestor's responsibility.

## Images

The default `image_mode=auto` extracts the original embedded PNG/JPEG only when
the page consists of one full-page, unrotated image with no text, drawing, mask,
annotation, widget, crop, clipping, graphics-state transparency or Form XObject.
The original encoded image bytes are preserved. All other pages are rendered.
`image_mode=render` forces rendering. Render size is bounded by
`max_render_pixels=20000000`; actual DPI is recorded, never silently advertised
as the requested DPI. Original extraction does not invent pixels by upscaling.

Every page has a JPEG preview (maximum width 360 px, no upscaling), and the bundle
has a labelled contact sheet (five columns by default). These are orientation
assets, not OCR input or evidence that the body is legible at thumbnail size.
`PageImage` records `acquisition_method`, dimensions, actual DPI and SHA-256.
Previews and contact sheet record dimensions, SHA-256 and page identity where
applicable. All paths are rewritten and all hashes checked during archiving.

## OCR and per-page checks

Modes remain `auto`, `always`, `never`. `auto` selects pages below the configured
native non-whitespace character threshold (default 30). OCRmyPDF force-OCRs only
those pages via `--pages`; this avoids `--skip-text` silently skipping a scan
because it happens to have a short digital label. `always` processes all pages.
OCR uses two jobs by default, deskew/rotation and PDF output with optimization
disabled. No paid model calls are involved.

After OCR, Technician reopens the prepared PDF and checks every page:

- Native and prepared non-whitespace character counts and prepared word count.
- Original and prepared geometry; finite, nonempty word boxes inside the page.
- Status `TEXT_AVAILABLE`, `LOW_TEXT_REVIEW`, `OCR_NO_TEXT_REVIEW`,
  `TEXT_LAYER_LOST` or `INVALID_TEXT_GEOMETRY`.

Lost text layers and incompatible geometry block publication of the bundle.
In particular, an OCR rotation that changes source/image coordinates is blocked
rather than handing an unaligned pair to Ingestor. An explicit geometry mapping
would be needed to support that case automatically.

Low/no text is a visible review signal, not an automatic error: an advertisement
or image-only page may legitimately contain little text. Those pages are listed
in `ocr.pages_needing_review`. `READY_FOR_INGESTOR` means the technical bundle
is complete, not that every page has meaningful text or that OCR has been
verified character by character. A caller must inspect the review list.

## Identity, reproducibility and cache

Source identity remains the immutable original's SHA-256. Bundle identity is:

`sha256:<source>:technician-v4.3:<configuration-sha256>`

Publication matching uses the first known publication occurrence rather than
the ordering of the known-publication list. This fixes the FT acceptance case
where a later WSJ citation previously overrode the FT masthead. Filename still
does not establish identity; the policy is included in the configuration hash.

The cache path includes the configuration hash. It covers intake identity
overrides, OCR mode/languages/threshold/options/jobs, render policy/DPI/pixel cap,
preview configuration, split size and recorded tool versions (Python, PyMuPDF,
OCRmyPDF, Tesseract, Ghostscript). Filenames and received timestamps do not
change the preparation identity. Unknown/unavailable tool versions are recorded
as null. Custom Tesseract traineddata and binary-build checksums are not pinned
by this fingerprint; deployment packaging must pin those for byte reproducibility.

Cache hits validate artifact hashes. The remote worker reuses an existing source
only if the archived configuration matches, and verifies archived artifacts
before clearing a duplicate arrival. Original copies, prepared PDFs, images,
previews and manifests retain provenance. Final paths are written before the
staging directory is published atomically.

`timings_seconds` records configuration, validation/hash, identity, copy/probe,
OCR, text checks, image/preview generation, split and total preparation time.
These are preparation timings, not upload time or editorial processing time.

The schema stays `source-bundle-v4` with additive fields; the reader accepts older
manifests with no new fields. Technician's version increments to `technician-v4.3`
so old source records are not silently reused. No database migration is needed.

## Local invocation

```sh
bb-technician edition.pdf --workspace ./workspace --ocr auto \
  --image-mode auto --preview-width 360 --contact-columns 5 --ocr-jobs 2
```

Tests cover native and scanned pages, byte-preserved extraction, overlays,
rotation, crop/clipping fallback, pixel budgets, sparse-page OCR selection,
post-OCR validation, configuration cache isolation/corruption, legacy manifests,
preview paths/MIME/hashes and existing Ingestor compatibility.

Implementation references: [PyMuPDF page API](https://pymupdf.readthedocs.io/en/latest/page.html)
and [OCRmyPDF 16 advanced options](https://ocrmypdf.readthedocs.io/en/v16.0.0/advanced.html).

This change does not deploy a service or establish current Railway/Supabase health.
