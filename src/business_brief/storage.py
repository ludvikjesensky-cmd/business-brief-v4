from __future__ import annotations
import os
from pathlib import Path
from supabase import Client, create_client

class StorageError(RuntimeError): pass

class SupabaseArchive:
    def __init__(self, client: Client, inbox="source-inbox", archive="source-archive"):
        self.client=client; self.inbox=inbox; self.archive=archive

    @classmethod
    def from_env(cls):
        url=os.environ.get("SUPABASE_URL"); key=os.environ.get("SUPABASE_SECRET_KEY")
        if not url or not key: raise StorageError("SUPABASE_URL and SUPABASE_SECRET_KEY are required")
        return cls(create_client(url,key))

    def download_inbox(self, object_key:str, target:Path)->Path:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(self.client.storage.from_(self.inbox).download(object_key))
        return target

    def upload_file(self, local:Path, remote:str, content_type:str):
        with local.open("rb") as fh:
            self.client.storage.from_(self.archive).upload(remote,fh,{"content-type":content_type,"upsert":"false"})

    def upload_bundle(self,bundle_dir:Path,prefix:str):
        mapping=[]
        for p in sorted(bundle_dir.rglob("*")):
            if not p.is_file(): continue
            rel=p.relative_to(bundle_dir).as_posix(); remote=f"{prefix}/{rel}"
            mime="application/pdf" if p.suffix.lower()==".pdf" else "image/png" if p.suffix.lower()==".png" else "application/json"
            self.upload_file(p,remote,mime); mapping.append(remote)
        return mapping

    def remove_inbox(self, object_key:str):
        self.client.storage.from_(self.inbox).remove([object_key])
