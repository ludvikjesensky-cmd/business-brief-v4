from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


PHYSICAL_MAP_SCHEMA = "physical-map-v1"


FORBIDDEN_SEMANTIC_KEYS = {
    "article",
    "article_id",
    "headline",
    "caption",
    "relevance",
    "continuation",
    "editorial_disposition",
}


@dataclass(frozen=True)
class FontEvidence:
    font: str
    size: float
    flags: int
    color: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhysicalBlock:
    block_id: str
    text: str
    bbox: tuple[float, float, float, float]
    fonts: tuple[FontEvidence, ...]
    source_order: int

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["bbox"] = list(self.bbox)
        data["fonts"] = [f.to_dict() for f in self.fonts]
        return data


@dataclass(frozen=True)
class PhysicalRelation:
    relation: str
    source_block_id: str
    target_block_id: str
    delta_x: float
    delta_y: float
    edge_gap: float
    horizontal_overlap_ratio: float
    vertical_overlap_ratio: float
    font_size_delta: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhysicalPage:
    page_no: int
    width: float
    height: float
    blocks: tuple[PhysicalBlock, ...]
    relations: tuple[PhysicalRelation, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["blocks"] = [b.to_dict() for b in self.blocks]
        data["relations"] = [r.to_dict() for r in self.relations]
        return data


@dataclass(frozen=True)
class PhysicalMap:
    schema_version: str
    source_id: str
    source_sha256: str
    ingestor_version: str
    pages: tuple[PhysicalPage, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["pages"] = [p.to_dict() for p in self.pages]
        return data


def assert_semantically_neutral(payload: Any, path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_SEMANTIC_KEYS:
                raise ValueError(f"Forbidden semantic key {key!r} at {path}")
            assert_semantically_neutral(value, f"{path}.{key}")
    elif isinstance(payload, list):
        for idx, value in enumerate(payload):
            assert_semantically_neutral(value, f"{path}[{idx}]")
