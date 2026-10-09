from __future__ import annotations
import os, json, hashlib
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

    def inbox_version(self, object_key):
        return self.client.rpc("technician_inbox_version", {"p_object_key":object_key}).execute().data

    def list_inbox(self) -> list[str]:
        rows=self.client.storage.from_(self.inbox).list("",{"limit":1000,"sortBy":{"column":"created_at","order":"asc"}})
        return [row["name"] for row in rows if row.get("name") and Path(row["name"]).name != ".emptyFolderPlaceholder"]

    def cleanup_folder_placeholders(self):
        rows=self.client.storage.from_(self.inbox).list("",{"limit":1000})
        for row in rows:
            if row.get("name")==".emptyFolderPlaceholder" and (row.get("metadata") or {}).get("size")==0:
                self.remove_inbox(row["name"])

    def verify_archived_source(self, source, digest):
        manifest_path=source["source_bundle_path"]
        data=json.loads(self.client.storage.from_(self.archive).download(manifest_path))
        if data["source_sha256"] != digest:
            raise StorageError("Archived manifest source hash mismatch")
        prefix=manifest_path.rsplit("/",1)[0]+"/"
        artifacts={data["original_path"]:digest,data["prepared_pdf_path"]:data["ocr"]["prepared_sha256"]}
        artifacts.update({item["path"]:item["sha256"] for item in data["page_images"]+data.get("parts",[])})
        if len(data["page_images"]) != data["page_count"]:
            raise StorageError("Archived page count mismatch")
        for key,expected in artifacts.items():
            if not key.startswith(prefix) or ".." in Path(key).parts:
                raise StorageError("Invalid archived artifact path")
            payload=self.client.storage.from_(self.archive).download(key)
            if hashlib.sha256(payload).hexdigest()!=expected:
                raise StorageError(f"Archived artifact hash mismatch: {key}")

    def download_inbox(self, object_key:str, target:Path)->Path:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(self.client.storage.from_(self.inbox).download(object_key))
        return target

    def object_exists(self, remote:str) -> bool:
        parent,name=remote.rsplit("/",1)
        rows=self.client.storage.from_(self.archive).list(parent,{"search":name,"limit":100})
        return any(row.get("name")==name for row in rows)

    def verify_file(self, local:Path, remote:str):
        stored = self.client.storage.from_(self.archive).download(remote)
        if hashlib.sha256(stored).hexdigest() != hashlib.sha256(local.read_bytes()).hexdigest():
            raise StorageError(f"Archive verification failed: {remote}")

    def upload_file(self, local:Path, remote:str, content_type:str):
        # Archive paths are immutable. A retry reuses an already present object;
        # it never overwrites it.
        if self.object_exists(remote):
            self.verify_file(local, remote)
            return
        with local.open("rb") as fh:
            self.client.storage.from_(self.archive).upload(remote,fh,{"content-type":content_type,"upsert":"false"})
        self.verify_file(local, remote)

    def upload_bundle(self,bundle_dir:Path,prefix:str):
        manifest = bundle_dir / "manifest.json"
        data = json.loads(manifest.read_text())
        def remote_path(value):
            return f"{prefix}/{Path(value).relative_to(bundle_dir).as_posix()}"
        data["original_path"] = remote_path(data["original_path"])
        data["prepared_pdf_path"] = remote_path(data["prepared_pdf_path"])
        data["ocr"]["prepared_pdf_path"] = remote_path(data["ocr"]["prepared_pdf_path"])
        for item in data["page_images"] + data["parts"]:
            item["path"] = remote_path(item["path"])
        archive_manifest = bundle_dir / ".archive-manifest.json"
        archive_manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        mapping=[]
        for p in sorted(bundle_dir.rglob("*")):
            if not p.is_file() or p.name.startswith(".") or p == manifest: continue
            rel=p.relative_to(bundle_dir).as_posix(); remote=f"{prefix}/{rel}"
            mime="application/pdf" if p.suffix.lower()==".pdf" else "image/png" if p.suffix.lower()==".png" else "application/json"
            self.upload_file(p,remote,mime); mapping.append(remote)
        self.upload_file(archive_manifest, f"{prefix}/manifest.json", "application/json")
        mapping.append(f"{prefix}/manifest.json")
        archive_manifest.unlink()
        return mapping

    def remove_inbox(self, object_key:str):
        self.client.storage.from_(self.inbox).remove([object_key])
