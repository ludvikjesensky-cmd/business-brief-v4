from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal


SOURCE_BUNDLE_SCHEMA = "source-bundle-v4"
PAGE_INGEST_SCHEMA = "page-ingest-v2"

PageStatus = Literal["VERIFIED", "VERIFIED_WITH_NOTES", "NEEDS_REVIEW", "BLOCKED"]
RelevanceState = Literal["relevant", "irrelevant", "uncertain"]


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
        d = asdict(self)
        d["evidence"] = list(self.evidence)
        d["edition_key"] = self.edition_key
        return d


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


@dataclass(frozen=True)
class RelevanceAssessment:
    state: RelevanceState
    reason: str


@dataclass(frozen=True)
class PerspectiveEvidence:
    author_question: str | None = None
    framing: str | None = None
    central_argument: str | None = None
    distinctive_angle: str | None = None
    tensions_or_counterarguments: tuple[str, ...] = ()
    open_questions: tuple[str, ...] = ()
    observed_on_page: tuple[str, ...] = ()
    interpreted_from_page: tuple[str, ...] = ()
    unresolved_until_assembly: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["tensions_or_counterarguments"] = list(self.tensions_or_counterarguments)
        d["open_questions"] = list(self.open_questions)
        d["observed_on_page"] = list(self.observed_on_page)
        d["interpreted_from_page"] = list(self.interpreted_from_page)
        d["unresolved_until_assembly"] = list(self.unresolved_until_assembly)
        return d


@dataclass(frozen=True)
class ContinuationEvidence:
    starts_here: bool
    continued_from_previous_page: bool
    continues_to_another_page: bool
    continuation_marker: str | None = None
    continuation_target: str | None = None


@dataclass(frozen=True)
class Verification:
    status: PageStatus
    visual_checked: bool
    text_layer_checked: bool
    title_verified: bool
    byline_verified: bool | None
    boundaries_verified: bool
    reading_order_verified: bool
    text_on_page_complete: bool
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["notes"] = list(self.notes)
        return d


@dataclass(frozen=True)
class PageItem:
    page_item_id: str
    item_type: str
    title: str | None
    subtitle: str | None
    kicker: str | None
    byline: str | None
    text_on_page: str | None
    relevance: RelevanceAssessment
    perspective: PerspectiveEvidence
    continuation: ContinuationEvidence
    verification: Verification

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["relevance"] = asdict(self.relevance)
        d["perspective"] = self.perspective.to_dict()
        d["continuation"] = asdict(self.continuation)
        d["verification"] = self.verification.to_dict()
        return d


@dataclass(frozen=True)
class PageIngest:
    source_id: str
    source_sha256: str
    publication_id: str
    publication_name: str
    edition_date: str
    edition_variant: str
    page_no: int
    items: tuple[PageItem, ...]
    page_status: PageStatus
    page_notes: tuple[str, ...] = ()
    ingestor_version: str = "ingestor-v2.0-chat"
    instruction_version: str = "2.0"
    schema_version: str = PAGE_INGEST_SCHEMA

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "producer": self.ingestor_version,
            "instruction_version": self.instruction_version,
            "source": {
                "source_id": self.source_id,
                "source_sha256": self.source_sha256,
            },
            "publication": {
                "publication_id": self.publication_id,
                "canonical_name": self.publication_name,
                "edition_date": self.edition_date,
                "edition_variant": self.edition_variant,
                "page_no": self.page_no,
            },
            "items": [item.to_dict() for item in self.items],
            "page_status": self.page_status,
            "page_notes": list(self.page_notes),
        }


# v2 remains immutable for existing artifacts and clients.
PAGE_INGEST_V3_SCHEMA = "page-ingest-v3"


@dataclass(frozen=True)
class PageItemV3:
    page_item_id: str
    item_type: str
    title: str | None
    subtitle: str | None
    kicker: str | None
    byline: str | None
    text_on_page: str | None
    relevance: RelevanceAssessment
    continuation: ContinuationEvidence
    verification: Verification

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["verification"] = self.verification.to_dict()
        return d


@dataclass(frozen=True)
class PageIngestV3(PageIngest):
    items: tuple[PageItemV3, ...]
    ingestor_version: str = "ingestor-v2.1-chat"
    instruction_version: str = "2.1"
    schema_version: str = PAGE_INGEST_V3_SCHEMA
