from __future__ import annotations

import argparse
import json
import sys

from .visual_assembly import MatchingPolicy
from .visual_continuations import LINK_SCHEMA
from .visual_mapper import VisualResponsesProvider
from .visual_page_map import LAYOUT_SCHEMA, PageMapError
from .visual_pipeline import assemble_issue, load_json, map_issue, prepare_issue


def _pages(value):
    try:
        result = []
        for part in value.split(","):
            ends = part.split("-")
            if len(ends) == 1:
                result.append(int(part))
            elif len(ends) == 2 and 1 <= int(ends[0]) <= int(ends[1]) <= 10000:
                result.extend(range(int(ends[0]), int(ends[1]) + 1))
            else:
                raise ValueError()
        if not result or len(result) != len(set(result)) or min(result) < 1:
            raise ValueError()
        return result
    except ValueError:
        raise argparse.ArgumentTypeError("pages must be unique positive numbers/ranges, e.g. 2,5-8") from None


def main(argv=None):
    parser = argparse.ArgumentParser(description="Visual layout → geometric article assembly (no production writes)")
    sub = parser.add_subparsers(dest="command", required=True)
    schema = sub.add_parser("schema", help="print the machine-readable layout or reviewed-link schema")
    schema.add_argument("--kind", choices=["layout", "links"], default="layout")
    prepare = sub.add_parser("prepare", help="verify PDF/Physical Map and render low-res JPEGs locally")
    prepare.add_argument("--pdf", required=True)
    prepare.add_argument("--physical-map", required=True)
    prepare.add_argument("--output", required=True)
    prepare.add_argument("--prepared-sha256", help="verified prepared/OCR PDF hash if different from original")
    prepare.add_argument("--pages", type=_pages)
    prepare.add_argument("--width", type=int, default=600)
    prepare.add_argument("--jpeg-quality", type=int, default=75)
    mapping = sub.add_parser("map", help="import offline layouts or explicitly call a vision model")
    mapping.add_argument("--issue-dir", required=True)
    mode = mapping.add_mutually_exclusive_group(required=True)
    mode.add_argument("--maps-dir", help="p0001.json etc.; offline layouts or verified envelopes")
    mode.add_argument("--live", action="store_true")
    mapping.add_argument("--allow-paid", action="store_true")
    mapping.add_argument("--model")
    mapping.add_argument("--max-api-calls", type=int, default=1, help="per invocation, default 1; no retries")
    mapping.add_argument("--max-output-tokens", type=int, default=6000)
    mapping.add_argument("--detail", choices=["low", "high", "auto"], default="low")
    assembly = sub.add_parser("assemble", help="execute maps; write article evidence, coverage and previews")
    assembly.add_argument("--issue-dir", required=True)
    assembly.add_argument("--links", help="reviewed, provenance-bound cross-page continuation links JSON")
    assembly.add_argument("--photo-overlap", type=float, default=0.6)
    assembly.add_argument("--region-overlap", type=float, default=0.5)
    assembly.add_argument("--object-overlap", type=float, default=0.5)
    assembly.add_argument("--exclusion-overlap", type=float, default=0.5)
    assembly.add_argument("--ambiguity-margin", type=float, default=0.05)
    assembly.add_argument("--require-full-issue", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "schema":
            print(json.dumps(LAYOUT_SCHEMA if args.kind == "layout" else LINK_SCHEMA, indent=2))
            return 0
        elif args.command == "prepare":
            result = prepare_issue(args.pdf, args.physical_map, args.output, pages=args.pages,
                width=args.width, quality=args.jpeg_quality, prepared_sha256=args.prepared_sha256)
            summary = {"prepared_pages": [p["page_no"] for p in result["pages"]],
                       "image_bytes": sum(p["image_bytes"] for p in result["pages"]), "api_calls": 0}
        elif args.command == "map":
            provider = VisualResponsesProvider(args.model, allow_paid=args.allow_paid,
                max_output_tokens=args.max_output_tokens, detail=args.detail) if args.live else None
            summary = map_issue(args.issue_dir, maps_dir=args.maps_dir, provider=provider, max_api_calls=args.max_api_calls)
        else:
            policy = MatchingPolicy(args.region_overlap, args.photo_overlap, args.object_overlap,
                                    args.exclusion_overlap, args.ambiguity_margin)
            result = assemble_issue(args.issue_dir, policy=policy, links=load_json(args.links) if args.links else None)
            summary = {k: result[k] for k in ("processed_pages", "all_pages_processed", "needs_review", "coverage")}
            if args.require_full_issue and not result["all_pages_processed"]:
                print(json.dumps(summary), flush=True)
                return 2
        print(json.dumps(summary, ensure_ascii=False), flush=True)
        return 0
    except (PageMapError, OSError, KeyError, TypeError) as exc:
        # Input/transport failures never become a successful partial publication.
        print(f"Visual Page Map failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
