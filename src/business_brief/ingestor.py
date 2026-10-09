from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path

import fitz

from .physical_map import (
    FontEvidence,
    PhysicalBlock,
    PhysicalMap,
    PhysicalPage,
    PhysicalRelation,
    PHYSICAL_MAP_SCHEMA,
    assert_semantically_neutral,
)


INGESTOR_VERSION = "ingestor-v4-physical-map-v1.1"


class IngestorError(RuntimeError):
    pass


def _round_bbox(bbox: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    return tuple(round(float(v), 3) for v in bbox)


def _block_fingerprint(page_no: int, text: str, bbox: tuple[float, float, float, float]) -> str:
    raw = f"{page_no}|{bbox[0]:.3f}|{bbox[1]:.3f}|{bbox[2]:.3f}|{bbox[3]:.3f}|{text}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]


def _line_text(line: dict) -> str:
    return "".join(span.get("text", "") for span in line.get("spans", [])).strip()


def _width(block: PhysicalBlock) -> float:
    return max(0.001, block.bbox[2] - block.bbox[0])


def _height(block: PhysicalBlock) -> float:
    return max(0.001, block.bbox[3] - block.bbox[1])


def _center_x(block: PhysicalBlock) -> float:
    return (block.bbox[0] + block.bbox[2]) / 2.0


def _center_y(block: PhysicalBlock) -> float:
    return (block.bbox[1] + block.bbox[3]) / 2.0


def _overlap_ratio(a0: float, a1: float, b0: float, b1: float) -> float:
    overlap = max(0.0, min(a1, b1) - max(a0, b0))
    denominator = max(0.001, min(a1 - a0, b1 - b0))
    return min(1.0, overlap / denominator)


def _representative_font_size(block: PhysicalBlock) -> float | None:
    sizes = [f.size for f in block.fonts if f.size > 0]
    if not sizes:
        return None
    return float(statistics.median(sizes))


def _relation(
    kind: str,
    source: PhysicalBlock,
    target: PhysicalBlock,
    *,
    edge_gap: float,
) -> PhysicalRelation:
    source_font = _representative_font_size(source)
    target_font = _representative_font_size(target)
    font_delta = None
    if source_font is not None and target_font is not None:
        font_delta = round(abs(source_font - target_font), 3)

    return PhysicalRelation(
        relation=kind,
        source_block_id=source.block_id,
        target_block_id=target.block_id,
        delta_x=round(_center_x(target) - _center_x(source), 3),
        delta_y=round(_center_y(target) - _center_y(source), 3),
        edge_gap=round(max(0.0, edge_gap), 3),
        horizontal_overlap_ratio=round(
            _overlap_ratio(source.bbox[0], source.bbox[2], target.bbox[0], target.bbox[2]),
            4,
        ),
        vertical_overlap_ratio=round(
            _overlap_ratio(source.bbox[1], source.bbox[3], target.bbox[1], target.bbox[3]),
            4,
        ),
        font_size_delta=font_delta,
    )


def _build_relations(blocks: list[PhysicalBlock]) -> tuple[PhysicalRelation, ...]:
    """Create only local, geometry-derived evidence.

    No relation represents an article, headline, caption, or semantic reading order.
    The successor relation is explicitly a *physical* local hypothesis that the
    Comparator may later test against the LLM's semantic reading order.
    """
    relations: list[PhysicalRelation] = []
    seen: set[tuple[str, str, str]] = set()

    def add(rel: PhysicalRelation) -> None:
        key = (rel.relation, rel.source_block_id, rel.target_block_id)
        if key not in seen:
            seen.add(key)
            relations.append(rel)

    for source in blocks:
        below_candidates: list[tuple[tuple[float, float, float, str], PhysicalBlock]] = []
        right_candidates: list[tuple[tuple[float, float, str], PhysicalBlock]] = []

        source_height = _height(source)

        for target in blocks:
            if source.block_id == target.block_id:
                continue

            horizontal_overlap = _overlap_ratio(
                source.bbox[0], source.bbox[2], target.bbox[0], target.bbox[2]
            )
            vertical_overlap = _overlap_ratio(
                source.bbox[1], source.bbox[3], target.bbox[1], target.bbox[3]
            )

            # Nearest block physically below the current line.
            if target.bbox[1] >= source.bbox[3] - 1.5 and _center_y(target) > _center_y(source):
                gap = max(0.0, target.bbox[1] - source.bbox[3])
                max_gap = max(36.0, 4.0 * max(source_height, _height(target)))
                if gap <= max_gap and horizontal_overlap >= 0.20:
                    score = (
                        gap,
                        -horizontal_overlap,
                        abs(_center_x(target) - _center_x(source)),
                        target.block_id,
                    )
                    below_candidates.append((score, target))

            # Nearest block physically to the right on the same visual row.
            if target.bbox[0] >= source.bbox[2] - 1.5 and _center_x(target) > _center_x(source):
                gap = max(0.0, target.bbox[0] - source.bbox[2])
                if gap <= 60.0 and vertical_overlap >= 0.50:
                    score = (gap, -vertical_overlap, target.block_id)
                    right_candidates.append((score, target))

        if below_candidates:
            below_candidates.sort(key=lambda item: item[0])
            target = below_candidates[0][1]
            gap = max(0.0, target.bbox[1] - source.bbox[3])
            below = _relation("below", source, target, edge_gap=gap)
            add(below)

            # Same lane is based only on shared x geometry.
            if (
                below.horizontal_overlap_ratio >= 0.50
                and abs(target.bbox[0] - source.bbox[0]) <= 8.0
            ):
                add(_relation("same_physical_lane", source, target, edge_gap=gap))

            # Local physical successor is deliberately conservative.
            source_font = _representative_font_size(source)
            target_font = _representative_font_size(target)
            font_delta_ok = (
                source_font is None
                or target_font is None
                or abs(source_font - target_font) <= 1.25
            )
            max_successor_gap = max(6.0, 1.8 * max(_height(source), _height(target)))
            if (
                gap <= max_successor_gap
                and below.horizontal_overlap_ratio >= 0.65
                and font_delta_ok
            ):
                add(_relation("probable_physical_successor", source, target, edge_gap=gap))

        if right_candidates:
            right_candidates.sort(key=lambda item: item[0])
            target = right_candidates[0][1]
            gap = max(0.0, target.bbox[0] - source.bbox[2])
            add(_relation("right_of", source, target, edge_gap=gap))

    relations.sort(
        key=lambda r: (
            r.source_block_id,
            r.relation,
            r.target_block_id,
        )
    )
    return tuple(relations)


def extract_physical_map(manifest_path: str | Path, *, pdf_path: str | Path | None = None, source_id: str | None = None) -> PhysicalMap:
    manifest_file = Path(manifest_path).expanduser().resolve()
    if not manifest_file.is_file():
        raise IngestorError(f"Manifest does not exist: {manifest_file}")

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "source-bundle-v4":
        raise IngestorError("Unsupported source bundle schema")

    source_path = Path(pdf_path or manifest["prepared_pdf_path"])
    if not source_path.is_absolute():
        source_path = manifest_file.parent / source_path
    if not source_path.is_file():
        raise IngestorError(f"Source PDF not found: {source_path}")
    if hashlib.sha256(source_path.read_bytes()).hexdigest() != manifest["ocr"]["prepared_sha256"]:
        raise IngestorError("Prepared PDF hash mismatch")
    if manifest.get("status") != "READY_FOR_INGESTOR":
        raise IngestorError("Source bundle is not ready")

    doc = fitz.open(source_path)
    pages: list[PhysicalPage] = []
    try:
        if doc.page_count != int(manifest["page_count"]):
            raise IngestorError("Source bundle page count mismatch")

        for page_index, page in enumerate(doc, start=1):
            raw = page.get_text(
                "dict",
                flags=fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE,
            )
            candidates: list[
                tuple[
                    tuple[float, float, float, float],
                    str,
                    tuple[FontEvidence, ...],
                    int,
                ]
            ] = []
            source_order = 0

            for block in raw.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    text = _line_text(line)
                    if not text:
                        continue

                    spans = line.get("spans", [])
                    fonts: list[FontEvidence] = []
                    seen_fonts: set[tuple[str, float, int, int]] = set()
                    for span in spans:
                        item = (
                            str(span.get("font", "")),
                            round(float(span.get("size", 0.0)), 3),
                            int(span.get("flags", 0)),
                            int(span.get("color", 0)),
                        )
                        if item not in seen_fonts:
                            seen_fonts.add(item)
                            fonts.append(FontEvidence(*item))

                    bbox = _round_bbox(tuple(line.get("bbox", (0, 0, 0, 0))))
                    candidates.append((bbox, text, tuple(fonts), source_order))
                    source_order += 1

            # Stable IDs are based on physical coordinates/text, not article semantics.
            # Sorting only establishes reproducible serialization.
            candidates.sort(
                key=lambda x: (
                    x[0][1],
                    x[0][0],
                    x[0][3],
                    x[0][2],
                    x[3],
                    x[1],
                )
            )

            blocks: list[PhysicalBlock] = []
            used_ids: set[str] = set()
            for ordinal, (bbox, text, fonts, original_order) in enumerate(candidates, start=1):
                fp = _block_fingerprint(page_index, text, bbox)
                block_id = f"p{page_index:04d}-b{ordinal:04d}-{fp}"
                if block_id in used_ids:
                    raise IngestorError(f"Duplicate block id generated: {block_id}")
                used_ids.add(block_id)
                blocks.append(
                    PhysicalBlock(
                        block_id=block_id,
                        text=text,
                        bbox=bbox,
                        fonts=fonts,
                        source_order=original_order,
                    )
                )

            pages.append(
                PhysicalPage(
                    page_no=page_index,
                    width=round(float(page.rect.width), 3),
                    height=round(float(page.rect.height), 3),
                    blocks=tuple(blocks),
                    relations=_build_relations(blocks),
                )
            )
    finally:
        doc.close()

    result = PhysicalMap(
        schema_version=PHYSICAL_MAP_SCHEMA,
        source_id=source_id or manifest["source_id"],
        source_sha256=manifest["source_sha256"],
        ingestor_version=INGESTOR_VERSION,
        pages=tuple(pages),
    )
    assert_semantically_neutral(result.to_dict())
    return result


def write_physical_map(manifest_path: str | Path, output_path: str | Path | None = None) -> Path:
    manifest_file = Path(manifest_path).expanduser().resolve()
    result = extract_physical_map(manifest_file)

    if output_path is None:
        output = manifest_file.parent / "physical-map.json"
    else:
        output = Path(output_path).expanduser().resolve()

    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(output.suffix + ".tmp")
    temp.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temp.replace(output)
    return output
