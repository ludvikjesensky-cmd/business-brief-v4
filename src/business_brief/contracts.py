from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

SOURCE_BUNDLE_SCHEMA = "source-bundle-v4"

@dataclass(frozen=True)
class PublicationIdentity:
    publication_id: str
    canonical_name: str
    edition_date: str
    edition_variant: str = "default"
    language: str | None = None
    confidence: float = 1.0
    evidence: tuple[str, ...] = ()
    @property
    def edition_key(self) -> str:
        return f"{self.publication_id}:{self.edition_date}:{self.edition_variant}"
    def to_dict(self) -> dict[str, Any]:
        d = asdict(self); d["evidence"] = list(self.evidence); d["edition_key"] = self.edition_key; return d

@dataclass(frozen=True)
class PageImage:
    page_no: int
    path: str
    width_px: int
    height_px: int
    sha256: str

@dataclass(frozen=True)
class OcrInfo:
    mode: str
    required: bool
    performed: bool
    engine: str | None
    languages: str | None
    pages_requiring_ocr: tuple[int, ...]
    prepared_pdf_path: str
    prepared_sha256: str

@dataclass(frozen=True)
class SourcePart:
    part_no: int
    page_start: int
    page_end: int
    path: str
    sha256: str
    byte_size: int

@dataclass(frozen=True)
class SourceBundle:
    source_id: str
    source_sha256: str
    identity: PublicationIdentity
    original_filename: str
    byte_size: int
    page_count: int
    original_path: str
    prepared_pdf_path: str
    page_images: tuple[PageImage, ...]
    ocr: OcrInfo
    parts: tuple[SourcePart, ...]
    received_at: str
    technician_version: str
    schema_version: str = SOURCE_BUNDLE_SCHEMA
    status: str = "READY_FOR_INGESTOR"
    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["identity"] = self.identity.to_dict()
        d["ocr"]["pages_requiring_ocr"] = list(self.ocr.pages_requiring_ocr)
        return d
