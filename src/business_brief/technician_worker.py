from __future__ import annotations
import argparse,json,tempfile
from pathlib import Path
from .contracts import SOURCE_BUNDLE_SCHEMA
from .database import TechnicianRepository
from .storage import SupabaseArchive
from .technician import TECHNICIAN_VERSION, prepare_pdf, sha256_file

def process_inbox_object(object_key,*,publication=None,edition_date=None,variant="default"):
    archive=SupabaseArchive.from_env(); repo=TechnicianRepository(archive.client)
    with tempfile.TemporaryDirectory(prefix="bbv4-tech-") as td:
        root=Path(td); local=archive.download_inbox(object_key,root/"input.pdf")
        arrival=repo.register_arrival(object_key,Path(object_key).name,local.stat().st_size)
        digest=sha256_file(local); blob=repo.blob_by_sha(digest)
        if blob:
            old=repo.source_for_blob(blob["id"]); repo.mark_duplicate(arrival["id"],blob,old)
            if old and old.get("status")=="READY_FOR_INGESTOR":
                archive.remove_inbox(object_key)
                return {"status":"DUPLICATE_SOURCE","source_id":old["id"],"sha256":digest}
        bundle=prepare_pdf(local,workspace=root/"work",publication=publication,edition_date=edition_date,edition_variant=variant)
        pub=repo.create_publication(bundle.identity); edition,edition_existed=repo.get_or_create_edition(pub["id"],bundle.identity)
        source_id_placeholder=None
        prefix_base=f"{bundle.identity.publication_id}/{bundle.identity.edition_date[:4]}/{bundle.identity.edition_date}"
        # Source id is the physical SHA identity for storage; DB source remains UUID.
        prefix=f"{prefix_base}/sha256-{bundle.source_sha256}"
        bundle_dir=Path(bundle.original_path).parent
        uploaded=archive.upload_bundle(bundle_dir,prefix)
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
            repo.finalize_ready(source["id"],edition["id"],arrival["id"])
            repo.finish_job(job,"READY_FOR_INGESTOR")
            archive.remove_inbox(object_key)
            return {"status":"READY_FOR_INGESTOR","source_id":source["id"],"edition_id":edition["id"],"archive_prefix":prefix,"uploaded_count":len(uploaded)}
        except Exception as e:
            repo.finish_job(job,"FAILED",str(e)); raise

def main():
    p=argparse.ArgumentParser(prog="bb-technician-worker");p.add_argument("object_key");p.add_argument("--publication");p.add_argument("--date");p.add_argument("--variant",default="default");a=p.parse_args()
    print(json.dumps(process_inbox_object(a.object_key,publication=a.publication,edition_date=a.date,variant=a.variant),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
