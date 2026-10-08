from __future__ import annotations
from datetime import datetime, timezone
from .contracts import SOURCE_BUNDLE_SCHEMA
from .technician import TECHNICIAN_VERSION

def now(): return datetime.now(timezone.utc).isoformat()

class TechnicianRepository:
    def __init__(self, client): self.db=client

    def register_arrival(self, object_key, original_filename, byte_size=None):
        existing=(self.db.table("source_arrivals").select("*").eq("bucket_id","source-inbox").eq("object_key",object_key).execute().data or [])
        if existing: return existing[0]
        return self.db.table("source_arrivals").insert({"bucket_id":"source-inbox","object_key":object_key,"original_filename":original_filename,"byte_size":byte_size,"disposition":"RECEIVED"}).execute().data[0]

    def blob_by_sha(self, sha):
        rows=self.db.table("source_blobs").select("*").eq("sha256",sha).execute().data or []
        return rows[0] if rows else None

    def source_for_blob(self, blob_id):
        rows=(self.db.table("sources").select("*").eq("blob_id",blob_id).eq("technician_version",TECHNICIAN_VERSION).eq("source_bundle_contract",SOURCE_BUNDLE_SCHEMA).execute().data or [])
        return rows[0] if rows else None

    def create_publication(self, ident):
        rows=self.db.table("publications").select("*").eq("publication_id",ident.publication_id).execute().data or []
        if rows:
            self.db.table("publications").update({"last_seen_at":now()}).eq("id",rows[0]["id"]).execute(); return rows[0]
        return self.db.table("publications").insert({"publication_id":ident.publication_id,"canonical_name":ident.canonical_name,"languages":[ident.language] if ident.language else []}).execute().data[0]

    def get_or_create_edition(self,pub_id,ident):
        rows=(self.db.table("editions").select("*").eq("publication_id",pub_id).eq("edition_date",ident.edition_date).eq("edition_variant",ident.edition_variant).execute().data or [])
        if rows:return rows[0],True
        return self.db.table("editions").insert({"publication_id":pub_id,"edition_date":ident.edition_date,"edition_variant":ident.edition_variant,"status":"DISCOVERED"}).execute().data[0],False

    def create_blob(self,bundle,original_path):
        return self.db.table("source_blobs").insert({"sha256":bundle.source_sha256,"byte_size":bundle.byte_size,"mime_type":"application/pdf","immutable_original_path":original_path}).execute().data[0]

    def create_source(self,edition_id,blob_id,bundle,bundle_path,status):
        return self.db.table("sources").insert({"edition_id":edition_id,"blob_id":blob_id,"identity_confidence":bundle.identity.confidence,"identity_evidence":list(bundle.identity.evidence),"language":bundle.identity.language,"status":status,"technician_version":bundle.technician_version,"source_bundle_contract":bundle.schema_version,"source_bundle_path":bundle_path,"page_count":bundle.page_count,"received_at":bundle.received_at}).execute().data[0]

    def create_job(self,source_id,status="PROCESSING"):
        rows=(self.db.table("technician_jobs").select("*").eq("source_id",source_id).eq("technician_version",TECHNICIAN_VERSION).eq("contract_version",SOURCE_BUNDLE_SCHEMA).execute().data or [])
        if rows:
            self.db.table("technician_jobs").update({"status":status,"attempt":int(rows[0]["attempt"])+1,"heartbeat_at":now(),"updated_at":now()}).eq("id",rows[0]["id"]).execute()
            return rows[0]["id"]
        return self.db.table("technician_jobs").insert({"source_id":source_id,"technician_version":TECHNICIAN_VERSION,"contract_version":SOURCE_BUNDLE_SCHEMA,"status":status,"attempt":1,"claimed_at":now(),"heartbeat_at":now()}).execute().data[0]["id"]

    def finish_job(self,job_id,status,error=None):
        self.db.table("technician_jobs").update({"status":status,"completed_at":now() if status=="READY_FOR_INGESTOR" else None,"last_error":error,"updated_at":now()}).eq("id",job_id).execute()

    def finalize_ready(self,source_id,edition_id,arrival_id):
        self.db.table("sources").update({"status":"READY_FOR_INGESTOR"}).eq("id",source_id).execute()
        edition=self.db.table("editions").select("active_source_id").eq("id",edition_id).execute().data[0]
        if not edition.get("active_source_id"):
            self.db.table("editions").update({"active_source_id":source_id,"status":"READY"}).eq("id",edition_id).execute()
        self.db.table("source_arrivals").update({"source_id":source_id,"disposition":"ARCHIVED"}).eq("id",arrival_id).execute()

    def mark_duplicate(self,arrival_id,blob,source):
        self.db.table("source_arrivals").update({"blob_id":blob["id"],"source_id":source["id"] if source else None,"disposition":"DUPLICATE_SOURCE"}).eq("id",arrival_id).execute()
