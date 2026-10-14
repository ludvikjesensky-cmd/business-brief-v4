"""Deterministic geometry only: execute a visual map over Physical Map evidence."""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from .visual_page_map import PageMapError, validate_box, validate_layout

EPSILON = 1e-9


def exceeds(value, threshold):
    return value > threshold + EPSILON


@dataclass(frozen=True)
class MatchingPolicy:
    region_overlap: float = 0.5
    photo_overlap: float = 0.6
    object_overlap: float = 0.5
    exclusion_overlap: float = 0.5
    ambiguity_margin: float = 0.05

    def __post_init__(self):
        for name, value in asdict(self).items():
            if type(value) not in (int, float) or not math.isfinite(value) or not 0 < value < 1:
                raise PageMapError(f"invalid matching policy {name}")


def _intersection(a, b):
    x0, y0, x1, y1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    return (x0, y0, x1, y1) if x1 > x0 and y1 > y0 else None


def overlap(block, footprints):
    """Area of union of footprint intersections / area of TEXT bbox (not IoU).

    Union prevents overlapping chart rectangles from double counting a text line.
    """
    clipped = [c for box in footprints if (c := _intersection(block, box))]
    xs = sorted({c[i] for c in clipped for i in (0, 2)})
    area = 0.0
    for left, right in zip(xs, xs[1:]):
        ys = sorted((c[1], c[3]) for c in clipped if c[0] < right and c[2] > left)
        total = 0.0
        end = -math.inf
        for bottom, top in ys:
            total += max(0.0, top - max(bottom, end))
            end = max(end, top)
        area += (right - left) * total
    return min(1.0, area / ((block[2] - block[0]) * (block[3] - block[1])))


def _validate_page(page):
    if type(page.get("page_no")) is not int or page["page_no"] < 1:
        raise PageMapError("invalid physical page number")
    for dim in ("width", "height"):
        value = page.get(dim)
        if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
            raise PageMapError("invalid physical page dimensions")
    ids = set()
    for block in page["blocks"]:
        if not isinstance(block.get("block_id"), str) or not block["block_id"] or block["block_id"] in ids:
            raise PageMapError("duplicate/empty physical block identity")
        ids.add(block["block_id"])
        validate_box(block["bbox"], normalized=False)
        if not isinstance(block.get("text"), str):
            raise PageMapError("physical text must be a string")


def assemble_page(page, layout, policy=None):
    policy = policy or MatchingPolicy()
    _validate_page(page)
    validate_layout(layout, page["page_no"])
    warnings, assignments = [], {}
    candidates = []
    # Each candidate owns an ordered region, never an inferred column.
    for article in layout["articles"]:
        aid = article["article_id"]
        for role in ("headline", "byline", "body_flow"):
            for region in article[role]:
                candidates.append((aid, role, region, None))
        for embedded in article["embedded_objects"]:
            for region in embedded["caption_regions"]:
                candidates.append((aid, "caption", region, embedded["object_id"]))
    global_exclusions = [e["bbox"] for e in layout["exclusions"]]
    articles_by_id = {a["article_id"]: a for a in layout["articles"]}
    excluded, unmatched, ambiguous = [], [], []
    for block in page["blocks"]:
        bbox = [block["bbox"][i] / (page["width"] if i % 2 == 0 else page["height"]) for i in range(4)]
        bid = block["block_id"]
        if exceeds(overlap(bbox, global_exclusions), policy.exclusion_overlap):
            excluded.append({"block_id": bid, "reason": "page_exclusion"})
            continue
        matches, vetoes = [], []
        for aid, role, region, oid in candidates:
            score = overlap(bbox, [region["bbox"]])
            if score + EPSILON < policy.region_overlap:
                continue
            article = articles_by_id[aid]
            reason = None
            if exceeds(overlap(bbox, [e["bbox"] for e in article["exclusions"]]), policy.exclusion_overlap):
                reason = "article_exclusion"
            if role == "body_flow":
                for embedded in article["embedded_objects"]:
                    threshold = policy.photo_overlap if embedded["kind"] == "photo" else policy.object_overlap
                    if exceeds(overlap(bbox, embedded["footprint"]), threshold):
                        reason = embedded["kind"]
                        break
                    if any(overlap(bbox, [c["bbox"]]) + EPSILON >= policy.region_overlap for c in embedded["caption_regions"]):
                        reason = "caption"
                        break
            if reason:
                vetoes.append({"article_id": aid, "region_id": region["region_id"], "reason": reason})
            else:
                matches.append((score, aid, role, region["region_id"], oid))
        matches.sort(key=lambda m: (-m[0], m[1], m[2], m[3]))
        if not matches:
            # Embedded labels outside body regions still need an accounted-for home.
            if not vetoes:
                for article in layout["articles"]:
                    for embedded in article["embedded_objects"]:
                        threshold = policy.photo_overlap if embedded["kind"] == "photo" else policy.object_overlap
                        if exceeds(overlap(bbox, embedded["footprint"]), threshold):
                            vetoes.append({"article_id": article["article_id"], "reason": embedded["kind"]})
            if vetoes:
                excluded.append({"block_id": bid, "reasons": vetoes})
            else:
                unmatched.append(bid)
            continue
        if len(matches) > 1 and matches[0][0] - matches[1][0] <= policy.ambiguity_margin + EPSILON:
            ambiguous.append({"block_id": bid, "candidates": [
                {"article_id": m[1], "role": m[2], "region_id": m[3], "overlap": round(m[0], 6)} for m in matches]})
            continue  # Never silently duplicate or guess ownership.
        score, aid, role, rid, oid = matches[0]
        assignments[bid] = {"article_id": aid, "role": role, "region_id": rid,
                            "object_id": oid, "overlap": round(score, 6)}
    block_by_id = {b["block_id"]: b for b in page["blocks"]}

    # Report coincident duplicate source text; never silently delete source evidence.
    by_text = {}
    for block in page["blocks"]:
        if len(block["text"].strip()) < 8:
            continue
        for previous in by_text.get(block["text"], []):
            if max(abs(x - y) for x, y in zip(block["bbox"], previous["bbox"])) <= 0.25:
                match = assignments.get(block["block_id"], {})
                warnings.append({"kind": "coincident_duplicate_source_text",
                    "block_ids": [previous["block_id"], block["block_id"]],
                    "article_id": match.get("article_id")})
                break
        by_text.setdefault(block["text"], []).append(block)

    def read(aid, role, regions):
        result = []
        for region in regions:
            selected = [block_by_id[bid] for bid, match in assignments.items()
                        if match["article_id"] == aid and match["role"] == role and match["region_id"] == region["region_id"]]
            selected.sort(key=lambda b: (b["bbox"][1], b["bbox"][0], b.get("source_order", 0), b["block_id"]))
            if not selected:
                warnings.append({"kind": "empty_region", "article_id": aid, "region_id": region["region_id"]})
            result.append({"region_id": region["region_id"], "text": "\n".join(b["text"] for b in selected),
                           "block_ids": [b["block_id"] for b in selected]})
        return result

    result_articles = []
    for article in layout["articles"]:
        aid = article["article_id"]
        result = {"article_id": aid, "fragment_id": f"p{page['page_no']:04d}:{aid}", "kind": article["kind"],
                  "continuations": article["continuations"], "notes": article["notes"],
                  "needs_review": article["needs_review"] or bool(article["continuations"])}
        for role in ("headline", "byline", "body_flow"):
            result[role] = read(aid, role, article[role])
        result["body_text"] = "\n\n".join(r["text"] for r in result["body_flow"] if r["text"])
        result["embedded_objects"] = [{"object_id": embedded["object_id"], "kind": embedded["kind"],
            "captions": read(aid, "caption", embedded["caption_regions"])} for embedded in article["embedded_objects"]]
        if not any(article[role] for role in ("headline", "byline", "body_flow", "embedded_objects")):
            warnings.append({"kind": "empty_item", "article_id": aid})
        result_articles.append(result)
    for result in result_articles:
        aid = result["article_id"]
        result["needs_review"] = bool(result["needs_review"] or layout["needs_review"] or unmatched
            or any(w.get("article_id") == aid for w in warnings)
            or any(c["article_id"] == aid for b in ambiguous for c in b["candidates"]))
    review = bool(layout["needs_review"] or warnings or unmatched or ambiguous or any(a["needs_review"] for a in result_articles))
    return {"page_no": page["page_no"], "articles": result_articles, "policy": asdict(policy),
            "needs_review": review, "notes": layout["notes"], "warnings": warnings,
            "assignments": assignments, "excluded_blocks": excluded,
            "unmatched_block_ids": unmatched, "ambiguous_blocks": ambiguous,
            "coverage": {"total": len(page["blocks"]), "assigned": len(assignments),
                         "excluded": len(excluded), "unmatched": len(unmatched), "ambiguous": len(ambiguous)}}
