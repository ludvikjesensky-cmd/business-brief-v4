from __future__ import annotations
import argparse,json,tempfile
from pathlib import Path
from uuid import uuid4
from .contracts import SOURCE_BUNDLE_SCHEMA
from .database import TechnicianRepository
from .storage import SupabaseArchive
from .technician import TECHNICIAN_VERSION, prepare_pdf, sha256_file
from .events import EventLogger

def process_inbox_object(object_key,*,publication=None,edition_date=None,variant="default",object_version=None):
    archive=SupabaseArchive.from_env(); repo=TechnicianRepository(archive.client); log=EventLogger(archive.client)
    current_version=archive.inbox_version(object_key)
    if object_version and current_version != object_version:
        return {"status":"STALE"}
    object_version=current_version
    log.emit("SOURCE_DETECTED",stage="T01",status="PROCESSING",metadata={"object_key":object_key})
    with tempfile.TemporaryDirectory(prefix="bbv4-tech-") as td:
        root=Path(td)
        with log.timed("SOURCE_DOWNLOADED",stage="T01",metadata={"object_key":object_key}): local=archive.download_inbox(object_key,root/Path(object_key).name)
        arrival=repo.register_arrival(object_key,Path(object_key).name,local.stat().st_size,object_version)
        digest=sha256_file(local); log.emit("SHA256_COMPLETE",stage="T04",status="OK",metadata={"sha256":digest}); blob=repo.blob_by_sha(digest)
        if blob:
            old=repo.source_for_blob(blob["id"]); repo.mark_duplicate(arrival["id"],blob,old)
            if old and old.get("status")=="READY_FOR_INGESTOR":
                log.emit("DUPLICATE_SOURCE",stage="T06",status="DUPLICATE_SOURCE",source_id=old["id"],metadata={"sha256":digest})
                archive.remove_inbox(object_key) if archive.inbox_version(object_key)==object_version else None
                log.emit("INBOX_REMOVED",stage="T22",status="DUPLICATE_SOURCE",source_id=old["id"],metadata={"object_key":object_key})
                return {"status":"DUPLICATE_SOURCE","source_id":old["id"],"sha256":digest}
        with log.timed("SOURCE_PREPARED",stage="T07-T20"):
            bundle=prepare_pdf(local,workspace=root/"work",publication=publication,edition_date=edition_date,edition_variant=variant,received_at=arrival["received_at"])
        log.emit("IDENTITY_RESOLVED",stage="T05",status="OK",metadata=bundle.identity.to_dict())
        pub=repo.create_publication(bundle.identity); edition,edition_existed=repo.get_or_create_edition(pub["id"],bundle.identity)
        source_id_placeholder=None
        prefix_base=f"{bundle.identity.publication_id}/{bundle.identity.edition_date[:4]}/{bundle.identity.edition_date}"
        # Source id is the physical SHA identity for storage; DB source remains UUID.
        prefix=f"{prefix_base}/sha256-{bundle.source_sha256}/{TECHNICIAN_VERSION}/attempt-{uuid4()}"
        bundle_dir=Path(bundle.original_path).parent
        with log.timed("ARCHIVE_UPLOAD_COMPLETE",stage="T21",metadata={"archive_prefix":prefix,"original_filename":bundle.original_filename,"identity":bundle.identity.to_dict(),"page_count":bundle.page_count}): uploaded=archive.upload_bundle(bundle_dir,prefix)
        original_remote=f"{prefix}/original.pdf"; manifest_remote=f"{prefix}/manifest.json"
        if not blob: blob=repo.create_blob(bundle,original_remote)
        existing=repo.source_for_blob(blob["id"])
        if existing:
            source=existing
            repo.db.table("sources").update({"edition_id":edition["id"],"source_bundle_path":manifest_remote,"page_count":bundle.page_count}).eq("id",source["id"]).execute()
        else:
            collision=edition_existed and bool(edition.get("active_source_id"))
            source=repo.create_source(edition["id"],blob["id"],bundle,manifest_remote,"EDITION_COLLISION" if collision else "PROCESSING")
        job=repo.create_job(source["id"])
        try:
            # All durable artifacts exist before READY is committed.
            final_status=repo.finalize(source["id"],edition["id"],arrival["id"],job)
        except Exception as e:
            repo.finish_job(job,"FAILED",str(e))
            log.emit("TECHNICIAN_FAILED",stage="T24",severity="ERROR",status="FAILED",edition_id=edition["id"],source_id=source["id"],job_id=job,message=str(e))
            raise
        log.emit("TECHNICIAN_FINALIZED",stage="T22",status=final_status,edition_id=edition["id"],source_id=source["id"],job_id=job)
        if final_status == "READY_FOR_INGESTOR" and archive.inbox_version(object_key)==object_version:
            archive.remove_inbox(object_key)
            log.emit("INBOX_REMOVED",stage="T22",status=final_status,edition_id=edition["id"],source_id=source["id"],job_id=job,metadata={"object_key":object_key})
        return {"status":final_status,"source_id":source["id"],"edition_id":edition["id"],"archive_prefix":prefix,"uploaded_count":len(uploaded)}

def main():
    p=argparse.ArgumentParser(prog="bb-technician-worker");p.add_argument("object_key");p.add_argument("--publication");p.add_argument("--date");p.add_argument("--variant",default="default");a=p.parse_args()
    print(json.dumps(process_inbox_object(a.object_key,publication=a.publication,edition_date=a.date,variant=a.variant),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
