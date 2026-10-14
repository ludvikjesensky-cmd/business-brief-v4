"""Local two-map Ingestor. Does not invoke the Assembler or production queue."""
from __future__ import annotations

import argparse
import json
import sys

from .ingestor import IngestorError, extract_maps
from .visual_mapper import VisualResponsesProvider
from .visual_page_map import PageMapError
from .visual_page_map_cli import _pages


def main(argv=None):
    parser = argparse.ArgumentParser(description="Ingest a Source Bundle into Physical Map AND Visual Page Map")
    parser.add_argument("--bundle", required=True, help="verified Source Bundle manifest.json")
    parser.add_argument("--pdf", help="local prepared PDF override")
    parser.add_argument("--source-id", help="source identity override, e.g. database UUID")
    parser.add_argument("--output", required=True)
    parser.add_argument("--pages", type=_pages)
    parser.add_argument("--width", type=int, default=600)
    parser.add_argument("--jpeg-quality", type=int, default=75)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--maps-dir", help="offline pNNNN.json layouts or bound envelopes")
    mode.add_argument("--live", action="store_true")
    parser.add_argument("--allow-paid", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--max-api-calls", type=int, default=1)
    parser.add_argument("--max-output-tokens", type=int, default=6000)
    parser.add_argument("--detail", choices=["low", "high", "auto"], default="low")
    parser.add_argument("--reasoning-effort", choices=["none", "minimal", "low", "medium", "high", "xhigh", "max"])
    args = parser.parse_args(argv)
    try:
        provider = VisualResponsesProvider(args.model, allow_paid=args.allow_paid,
            max_output_tokens=args.max_output_tokens, detail=args.detail, reasoning_effort=args.reasoning_effort) if args.live else None
        result = extract_maps(args.bundle, args.output, pdf_path=args.pdf, source_id=args.source_id,
            pages=args.pages, maps_dir=args.maps_dir, provider=provider, max_api_calls=args.max_api_calls,
            width=args.width, quality=args.jpeg_quality)
        print(json.dumps({key: result[key] for key in ("source_id", "status", "mapped_pages", "all_pages_mapped",
                                                     "needs_review", "api_calls_this_run", "assembly_status")}))
        return 0 if result["all_pages_mapped"] else 2
    except (IngestorError, PageMapError, OSError, KeyError, TypeError) as exc:
        print(f"Ingestor failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
