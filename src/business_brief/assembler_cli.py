"""Assembler entrypoint: consume both maps; never perform vision/model calls."""
from __future__ import annotations

import argparse
import json
import sys

from .visual_assembly import MatchingPolicy
from .visual_page_map import PageMapError
from .visual_pipeline import load_json
from .assembler import assemble_issue


def main(argv=None):
    parser = argparse.ArgumentParser(description="Assemble source article text from Physical Map + Visual Page Map")
    parser.add_argument("--issue-dir", required=True)
    parser.add_argument("--links")
    parser.add_argument("--photo-overlap", type=float, default=0.6)
    parser.add_argument("--region-overlap", type=float, default=0.5)
    parser.add_argument("--object-overlap", type=float, default=0.5)
    parser.add_argument("--exclusion-overlap", type=float, default=0.5)
    parser.add_argument("--ambiguity-margin", type=float, default=0.05)
    parser.add_argument("--require-full-issue", action="store_true")
    args = parser.parse_args(argv)
    try:
        policy = MatchingPolicy(args.region_overlap, args.photo_overlap, args.object_overlap,
                                args.exclusion_overlap, args.ambiguity_margin)
        result = assemble_issue(args.issue_dir, policy=policy, links=load_json(args.links) if args.links else None,
                                require_ingestor_handoff=True)
        print(json.dumps({key: result[key] for key in ("processed_pages", "all_pages_processed", "needs_review", "coverage")}))
        return 2 if args.require_full_issue and not result["all_pages_processed"] else 0
    except (PageMapError, OSError, KeyError, TypeError) as exc:
        print(f"Assembler failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
