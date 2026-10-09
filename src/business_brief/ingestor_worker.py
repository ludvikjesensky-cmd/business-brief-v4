"""Durable Ingestor worker. Storage keys never become local file paths."""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
from pathlib import Path, PurePosixPath
import tempfile
import threading

from .events import EventLogger
from .ingestor import INGESTOR_VERSION, IngestorError, extract_physical_map
from .storage import SupabaseArchive


def archive_key(key: str, prefix: str = "") -> str:
    path = PurePosixPath(key)
    if not key or path.is_absolute() or ".." in path.parts or "\\" in key:
        raise IngestorError("Invalid archive key")
    if prefix and not key.startswith(prefix):
        raise IngestorError("Artifact outside source bundle")
    return key


def build_archived_map(archive, source: dict, blob: dict, workspace: Path) -> dict:
    """Validate provenance, materialize a verified PDF, and preserve DB identity."""
    if source["status"] != "READY_FOR_INGESTOR":
        raise IngestorError("Source is not READY_FOR_INGESTOR")
    key = archive_key(source["source_bundle_path"])
    bucket = archive.client.storage.from_(archive.archive)
    raw = bucket.download(key)
    manifest = json.loads(raw)
    if manifest.get("schema_version") != "source-bundle-v4":
        raise IngestorError("Unsupported source bundle schema")
    if manifest["source_sha256"] != blob["sha256"] or manifest["source_id"] != f"sha256:{blob['sha256']}":
        raise IngestorError("Source bundle identity mismatch")
    if manifest["page_count"] != source["page_count"]:
        raise IngestorError("Source bundle page count mismatch")
    images = manifest["page_images"]
    if [p["page_no"] for p in images] != list(range(1, source["page_count"] + 1)):
        raise IngestorError("Source bundle page sequence mismatch")
    prepared = archive_key(manifest["prepared_pdf_path"], key.rsplit("/", 1)[0] + "/")
    pdf = workspace / "prepared.pdf"
    pdf.write_bytes(bucket.download(prepared))
    local_manifest = workspace / "manifest.json"
    local_manifest.write_bytes(raw)
    physical = extract_physical_map(local_manifest, pdf_path=pdf, source_id=source["id"])
    return physical.to_dict()


def process_job(archive, task: dict) -> dict:
    db = archive.client
    log = EventLogger(db, component="INGESTOR")
    source = db.table("sources").select("*").eq("id", task["source_id"]).single().execute().data
    blob = db.table("source_blobs").select("*").eq("id", source["blob_id"]).single().execute().data
    log.emit("INGESTOR_STARTED", source_id=source["id"], metadata={"ingestor_version": INGESTOR_VERSION})
    with tempfile.TemporaryDirectory(prefix="bbv4-ingestor-") as temp:
        workspace = Path(temp)
        payload = build_archived_map(archive, source, blob, workspace)
        encoded = (json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        digest = hashlib.sha256(encoded).hexdigest()
        key = f"ingestor/{source['id']}/{INGESTOR_VERSION}/sha256-{digest}/physical-map.json"
        output = workspace / "physical-map.json"
        output.write_bytes(encoded)
        archive.upload_file(output, key, "application/json")
        metrics = {"page_count":len(payload["pages"]),
                   "block_count":sum(len(p["blocks"]) for p in payload["pages"]),
                   "text_characters":sum(len(b["text"]) for p in payload["pages"] for b in p["blocks"])}
        db.rpc("finalize_ingestor_job", {"p_job_id":task["id"], "p_lease_token":task["lease_token"],
               "p_path":key, "p_sha256":digest, "p_metrics":metrics}).execute()
    log.emit("INGESTOR_FINALIZED", status="DONE", source_id=source["id"],
             metadata={"physical_map_path":key, "sha256":digest, **metrics})
    return {"source_id":source["id"], "status":"DONE", "sha256":digest, **metrics}


def drain(archive=None) -> list[dict]:
    archive = archive or SupabaseArchive.from_env()
    db = archive.client
    db.rpc("reconcile_ingestor_queue", {"p_version":INGESTOR_VERSION}).execute()
    results = []
    while True:
        rows = db.rpc("claim_ingestor_job", {"p_version":INGESTOR_VERSION}).execute().data or []
        if not rows:
            return results
        task = rows[0]
        stop = threading.Event()
        def heartbeat():
            while not stop.wait(60):
                try:
                    db.rpc("heartbeat_ingestor_job", {"p_job_id":task["id"], "p_lease_token":task["lease_token"]}).execute()
                except Exception:
                    logging.exception("Ingestor heartbeat failed")
        thread = threading.Thread(target=heartbeat, daemon=True)
        thread.start()
        try:
            results.append(process_job(archive, task))
        except Exception as exc:
            db.rpc("fail_ingestor_job", {"p_job_id":task["id"], "p_lease_token":task["lease_token"],
                   "p_error":str(exc), "p_blocked":isinstance(exc, IngestorError)}).execute()
            EventLogger(db, component="INGESTOR").emit("INGESTOR_FAILED", severity="ERROR", status="FAILED",
                 source_id=task["source_id"], message=str(exc))
            results.append({"source_id":task["source_id"], "status":"FAILED", "error":str(exc)})
        finally:
            stop.set()
            thread.join()


def main() -> int:
    argparse.ArgumentParser(description="Drain the durable Ingestor queue").parse_args()
    results = drain()
    print(json.dumps(results, ensure_ascii=False))
    return int(any(r["status"] == "FAILED" for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
