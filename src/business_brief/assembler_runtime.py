from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from supabase import Client, create_client

from .assembler import (
    ARTICLE_RECORD_SCHEMA,
    ASSEMBLER_VERSION,
    IntegrityError,
    SelectedPage,
    article_storage_key,
    assemble,
    canonical_json,
    eligible_for_persistence,
    sha256_bytes,
    verify_manifest,
    verify_png_artifact,
    verify_selected_page,
)


PAGE_BUCKET = "page-ingest"
ARTICLE_BUCKET = "article-records"


class RuntimeErrorAssembler(RuntimeError):
    pass


@dataclass(frozen=True)
class PersistenceReceipt:
    article_id: str
    storage_key: str
    artifact_sha256: str
    artifact_byte_size: int
    disposition: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "article_id": self.article_id,
            "storage_bucket": ARTICLE_BUCKET,
            "storage_key": self.storage_key,
            "artifact_sha256": self.artifact_sha256,
            "artifact_byte_size": self.artifact_byte_size,
            "disposition": self.disposition,
        }


class BridgeAssemblyClient:
    def __init__(self, base_url: str, token: str):
        if not base_url.startswith("https://"):
            raise RuntimeErrorAssembler("INGESTOR_BRIDGE_URL must be https")
        self.base_url = base_url.rstrip("/")
        self.token = token

    @classmethod
    def from_env(cls) -> "BridgeAssemblyClient":
        base = os.environ.get("INGESTOR_BRIDGE_URL")
        token = os.environ.get("INGESTOR_BRIDGE_TOKEN")
        if not base or not token:
            raise RuntimeErrorAssembler("INGESTOR_BRIDGE_URL and INGESTOR_BRIDGE_TOKEN are required")
        return cls(base, token)

    def assembly_input(self, source_id: str, manifest_id: str, manifest_sha256: str) -> dict[str, Any]:
        query = urlencode({"manifest_id": manifest_id, "sha256": manifest_sha256})
        request = Request(
            f"{self.base_url}/ingestor-v2/source/{source_id}/assembly-input?{query}",
            headers={"Authorization": f"Bearer {self.token}"},
            method="GET",
        )
        try:
            with urlopen(request, timeout=60) as response:
                raw = response.read()
                status = response.status
        except HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")[:500]
            raise RuntimeErrorAssembler(f"assembly-input failed: HTTP {exc.code} {body}") from exc
        except URLError as exc:
            raise RuntimeErrorAssembler("assembly-input upstream request failed") from exc
        if status != 200:
            raise RuntimeErrorAssembler(f"assembly-input failed: HTTP {status}")
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeErrorAssembler("bridge returned invalid JSON") from exc
        if not isinstance(value, dict) or value.get("sha256") != manifest_sha256:
            raise RuntimeErrorAssembler("bridge returned an invalid assembly-input envelope")
        return value


class SupabaseAssemblerStore:
    def __init__(self, client: Client):
        self.client = client

    @classmethod
    def from_env(cls) -> "SupabaseAssemblerStore":
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SECRET_KEY")
        if not url or not key:
            raise RuntimeErrorAssembler("SUPABASE_URL and SUPABASE_SECRET_KEY are required")
        return cls(create_client(url, key))

    def download(self, bucket: str, key: str) -> bytes:
        try:
            data = self.client.storage.from_(bucket).download(key)
        except Exception as exc:
            raise RuntimeErrorAssembler(f"storage download failed: {bucket}/{key}") from exc
        if not isinstance(data, (bytes, bytearray)):
            raise RuntimeErrorAssembler(f"storage returned non-bytes for {bucket}/{key}")
        return bytes(data)

    def verify_private_bucket(self, bucket: str) -> None:
        try:
            rows = self.client.storage.list_buckets()
        except Exception as exc:
            raise RuntimeErrorAssembler("cannot inspect Supabase buckets") from exc
        match = next((row for row in rows if getattr(row, "id", None) == bucket or getattr(row, "name", None) == bucket), None)
        if match is None:
            raise RuntimeErrorAssembler(f"required bucket is missing: {bucket}")
        public = getattr(match, "public", None)
        if public is True:
            raise RuntimeErrorAssembler(f"bucket must be private: {bucket}")

    def load_verified_inputs(
        self,
        assembly_input: dict[str, Any],
        manifest_sha256: str,
    ) -> tuple[dict[str, Any], list[SelectedPage]]:
        manifest = assembly_input.get("manifest")
        if not isinstance(manifest, dict):
            raise RuntimeErrorAssembler("assembly input has no manifest")
        source = manifest.get("source") or {}
        manifest_key = (
            f"page-ingest/{source['publication_id']}/{source['edition_date']}/"
            f"{source['source_sha256']}/edition-selection/{manifest['manifest_id']}.json"
        )
        manifest_raw = self.download(PAGE_BUCKET, manifest_key)
        verify_manifest(manifest, manifest_raw, manifest_sha256)

        bridge_pages = assembly_input.get("pages")
        if not isinstance(bridge_pages, list):
            raise RuntimeErrorAssembler("assembly input has no selected pages")
        by_no = {int(row["page_no"]): row for row in bridge_pages}
        selected: list[SelectedPage] = []

        for selection in manifest["pages"]:
            page_no = int(selection["page_no"])
            bridge_row = by_no.get(page_no)
            if not isinstance(bridge_row, dict):
                raise IntegrityError(f"bridge omitted selected page {page_no}")
            for field in ("key", "sha256", "schema_version", "kind", "page_status", "usable_for_assembly"):
                if bridge_row.get(field) != selection.get(field):
                    raise IntegrityError(f"bridge/manifest mismatch for page {page_no}: {field}")
            raw = self.download(PAGE_BUCKET, selection["key"])
            page = verify_selected_page(selection, raw)

            for item in page.page.get("items") or []:
                for asset in item.get("assets") or []:
                    artifact = asset.get("artifact")
                    if not isinstance(artifact, dict):
                        raise IntegrityError(f"page {page_no} asset is missing immutable artifact metadata")
                    if artifact.get("bucket") != PAGE_BUCKET:
                        raise IntegrityError(f"page {page_no} asset points outside {PAGE_BUCKET}")
                    asset_raw = self.download(PAGE_BUCKET, artifact["key"])
                    verify_png_artifact(asset_raw, artifact)
            selected.append(page)

        if sorted(by_no) != sorted(page.page_no for page in selected):
            raise IntegrityError("bridge returned extra or duplicate selected pages")
        return manifest, selected

    def _existing_article(self, article_id: str) -> dict[str, Any] | None:
        rows = (
            self.client.table("articles")
            .select("*")
            .eq("article_id", article_id)
            .execute()
            .data
            or []
        )
        return rows[0] if rows else None

    def _existing_parts(self, article_id: str) -> list[dict[str, Any]]:
        return (
            self.client.table("article_source_parts")
            .select("*")
            .eq("article_id", article_id)
            .order("ordinal")
            .execute()
            .data
            or []
        )

    def _publication_uuid(self, publication_id: str) -> str:
        rows = (
            self.client.table("publications")
            .select("id")
            .eq("publication_id", publication_id)
            .execute()
            .data
            or []
        )
        if len(rows) != 1:
            raise RuntimeErrorAssembler(f"publication identity is not unique: {publication_id}")
        return rows[0]["id"]

    def _register_article(self, record: dict[str, Any], raw: bytes, key: str) -> None:
        article_id = record["article_id"]
        artifact_sha = sha256_bytes(raw)
        source_id = record["source"]["source_id"]
        edition_id = record["edition"].get("edition_id")
        if not edition_id:
            raise RuntimeErrorAssembler("Article Record lacks edition_id required by operational index")
        row = {
            "article_id": article_id,
            "publication_id": self._publication_uuid(record["publication"]["publication_id"]),
            "edition_id": edition_id,
            "source_id": source_id,
            "source_sha256": record["source"]["source_sha256"],
            "manifest_id": record["selection"]["manifest_id"],
            "manifest_sha256": record["selection"]["manifest_sha256"],
            "title": record.get("title"),
            "byline": record.get("byline"),
            "item_type": record["item_type"],
            "assembly_status": record["assembly"]["status"],
            "post_check_status": record["post_check"]["status"],
            "storage_bucket": ARTICLE_BUCKET,
            "storage_key": key,
            "artifact_sha256": artifact_sha,
            "artifact_byte_size": len(raw),
            "assembler_version": record["assembler_version"],
        }
        existing = self._existing_article(article_id)
        if existing is None:
            try:
                self.client.table("articles").insert(row).execute()
            except Exception:
                existing = self._existing_article(article_id)
                if existing is None:
                    raise
        if existing is None:
            existing = self._existing_article(article_id)
        immutable_fields = [
            "publication_id", "edition_id", "source_id", "source_sha256",
            "manifest_id", "manifest_sha256", "assembly_status", "post_check_status",
            "storage_bucket", "storage_key", "artifact_sha256", "artifact_byte_size",
            "assembler_version",
        ]
        if any(str(existing.get(field)) != str(row.get(field)) for field in immutable_fields):
            raise RuntimeErrorAssembler(f"operational article conflict for {article_id}")

        expected_parts = [
            {
                "article_id": article_id,
                "ordinal": ordinal,
                "page_no": part["page_no"],
                "page_item_id": part["page_item_id"],
                "page_artifact_key": part["page_artifact_key"],
                "page_artifact_sha256": part["page_artifact_sha256"],
                "text_sha256": part["text_sha256"],
            }
            for ordinal, part in enumerate(record["source_parts"])
        ]
        current = self._existing_parts(article_id)
        if not current:
            try:
                self.client.table("article_source_parts").insert(expected_parts).execute()
            except Exception:
                current = self._existing_parts(article_id)
                if not current:
                    raise
        current = self._existing_parts(article_id)
        projection = [
            {
                key: row[key]
                for key in (
                    "article_id", "ordinal", "page_no", "page_item_id",
                    "page_artifact_key", "page_artifact_sha256", "text_sha256",
                )
            }
            for row in current
        ]
        if projection != expected_parts:
            raise RuntimeErrorAssembler(f"operational source-parts conflict for {article_id}")

    def persist_article(self, record: dict[str, Any]) -> PersistenceReceipt:
        if not eligible_for_persistence(record):
            raise RuntimeErrorAssembler("only PASS + VERIFIED/VERIFIED_WITH_NOTES records may persist")
        if record.get("schema_version") != ARTICLE_RECORD_SCHEMA or record.get("assembler_version") != ASSEMBLER_VERSION:
            raise RuntimeErrorAssembler("unsupported Article Record identity")
        raw = canonical_json(record)
        key = article_storage_key(record)
        bucket = self.client.storage.from_(ARTICLE_BUCKET)
        disposition = "CREATED"

        try:
            existing = bucket.download(key)
        except Exception:
            existing = None

        if existing is not None:
            if bytes(existing) != raw:
                raise RuntimeErrorAssembler(f"immutable Article Record conflict: {key}")
            disposition = "REPLAYED"
        else:
            try:
                bucket.upload(
                    key,
                    raw,
                    {"content-type": "application/json", "upsert": "false"},
                )
            except Exception:
                try:
                    winner = bucket.download(key)
                except Exception as exc:
                    raise RuntimeErrorAssembler(f"Article Record persistence failed: {key}") from exc
                if bytes(winner) != raw:
                    raise RuntimeErrorAssembler(f"immutable Article Record conflict: {key}")
                disposition = "REPLAYED"

        stored = bytes(bucket.download(key))
        if stored != raw or sha256_bytes(stored) != sha256_bytes(raw):
            raise RuntimeErrorAssembler(f"Article Record readback verification failed: {key}")
        self._register_article(record, raw, key)
        return PersistenceReceipt(
            article_id=record["article_id"],
            storage_key=key,
            artifact_sha256=sha256_bytes(raw),
            artifact_byte_size=len(raw),
            disposition=disposition,
        )


def run(
    *,
    source_id: str,
    manifest_id: str,
    manifest_sha256: str,
    persist: bool = False,
    bridge: BridgeAssemblyClient | None = None,
    store: SupabaseAssemblerStore | None = None,
) -> dict[str, Any]:
    bridge = bridge or BridgeAssemblyClient.from_env()
    store = store or SupabaseAssemblerStore.from_env()
    store.verify_private_bucket(PAGE_BUCKET)
    if persist:
        store.verify_private_bucket(ARTICLE_BUCKET)

    envelope = bridge.assembly_input(source_id, manifest_id, manifest_sha256)
    manifest, pages = store.load_verified_inputs(envelope, manifest_sha256)
    report = assemble(
        manifest=manifest,
        manifest_sha256=manifest_sha256,
        selected_pages=pages,
    )

    receipts: list[dict[str, Any]] = []
    if persist:
        for record in report["records"]:
            if eligible_for_persistence(record):
                receipts.append(store.persist_article(record).to_dict())
    report["persistence"] = {
        "requested": persist,
        "eligible_count": sum(eligible_for_persistence(record) for record in report["records"]),
        "persisted_count": len(receipts),
        "receipts": receipts,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic Business Brief v4 Assembler")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--manifest-id", required=True)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument(
        "--persist",
        action="store_true",
        help="Persist only PASS + VERIFIED/VERIFIED_WITH_NOTES Article Records. Default is read-only.",
    )
    args = parser.parse_args()
    try:
        report = run(
            source_id=args.source_id,
            manifest_id=args.manifest_id,
            manifest_sha256=args.manifest_sha256,
            persist=args.persist,
        )
    except (RuntimeErrorAssembler, IntegrityError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}, ensure_ascii=False))
        return 2

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["counts"]["blocked"] or report["counts"]["needs_review"]:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
