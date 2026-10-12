"""Join fragments only through reviewed links with explicit printed page cues."""
from __future__ import annotations

from .visual_page_map import PageMapError, array, obj, validate_schema

LINK_SCHEMA = obj(source_sha256={"type": "string"}, physical_map_sha256={"type": "string"},
    approved={"type": "boolean"}, links=array(obj(from_fragment={"type": "string"},
        to_fragment={"type": "string"}, printed_label={"type": "string"})))


def assemble_articles(pages, source_sha256, physical_map_sha256, links=None):
    fragments = {a["fragment_id"]: (p["page_no"], a) for p in pages for a in p["articles"]}
    edges, incoming = {}, {}
    if links is not None:
        validate_schema(links, LINK_SCHEMA)
        if not links["approved"] or links["source_sha256"] != source_sha256 or links["physical_map_sha256"] != physical_map_sha256:
            raise PageMapError("continuation links need approval and matching issue provenance")
        for link in links["links"]:
            start, end = link["from_fragment"], link["to_fragment"]
            if start not in fragments or end not in fragments or start == end:
                raise PageMapError("continuation refers to unknown or identical fragments")
            if start in edges or end in incoming:
                raise PageMapError("duplicate or branching continuation links")
            start_page, start_item = fragments[start]
            end_page, end_item = fragments[end]
            if start_item["kind"] != end_item["kind"]:
                raise PageMapError("continuation cannot join different item kinds")
            cues = [c for c in start_item["continuations"] if c["direction"] == "to" and c["page_no"] == end_page]
            cues += [c for c in end_item["continuations"] if c["direction"] == "from" and c["page_no"] == start_page]
            if not any(c["printed_label"] == link["printed_label"] for c in cues):
                raise PageMapError("continuation has no matching printed page cue")
            edges[start], incoming[end] = end, start
    used, articles = set(), []
    for root in fragments:
        if root in incoming:
            continue
        chain, current = [], root
        while current is not None:
            if current in used:
                raise PageMapError("cyclic or duplicate continuation ownership")
            used.add(current)
            chain.append(current)
            current = edges.get(current)
        items = [fragments[f][1] for f in chain]
        articles.append({"article_id": root, "fragment_ids": chain,
            "page_refs": list(dict.fromkeys(fragments[f][0] for f in chain)),
            "headline": items[0]["headline"], "byline": items[0]["byline"], "kind": items[0]["kind"],
            "body_text": "\n\n".join(a["body_text"] for a in items if a["body_text"]),
            "needs_review": any(a["needs_review"] for a in items),
            "join_status": "reviewed_explicit_links" if len(chain) > 1 else "single_fragment",
            "continuations": [{"fragment_id": f, **c} for f in chain for c in fragments[f][1]["continuations"]]})
    if used != set(fragments):
        raise PageMapError("cyclic continuation links")
    unresolved = []
    for fragment, (n, a) in fragments.items():
        for cue in a["continuations"]:
            neighbor = edges.get(fragment) if cue["direction"] == "to" else incoming.get(fragment)
            if neighbor is None or fragments[neighbor][0] != cue["page_no"]:
                unresolved.append({"fragment_id": fragment, **cue})
    return articles, unresolved
