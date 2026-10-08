from __future__ import annotations
import argparse, json, shutil, tempfile
from pathlib import Path
from .storage import SupabaseArchive
from .technician import prepare_pdf

def process_inbox_object(object_key:str, *, publication=None, edition_date=None, variant="default"):
    archive=SupabaseArchive.from_env()
    with tempfile.TemporaryDirectory(prefix="bbv4-tech-") as td:
        root=Path(td); local=archive.download_inbox(object_key,root/"input.pdf")
        bundle=prepare_pdf(local,workspace=root/"work",publication=publication,edition_date=edition_date,edition_variant=variant)
        bundle_dir=Path(bundle.original_path).parent
        prefix=f"{bundle.identity.publication_id}/{bundle.identity.edition_date[:4]}/{bundle.identity.edition_date}/{bundle.source_id.replace(':','-')}"
        uploaded=archive.upload_bundle(bundle_dir,prefix)
        # Inbox deletion is the final commit step. Never delete before the durable archive exists.
        archive.remove_inbox(object_key)
        return {"status":"ARCHIVED","object_key":object_key,"archive_prefix":prefix,"uploaded":uploaded,"bundle":bundle.to_dict()}

def main():
    p=argparse.ArgumentParser(prog="bb-technician-worker");p.add_argument("object_key");p.add_argument("--publication");p.add_argument("--date");p.add_argument("--variant",default="default");a=p.parse_args()
    print(json.dumps(process_inbox_object(a.object_key,publication=a.publication,edition_date=a.date,variant=a.variant),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
