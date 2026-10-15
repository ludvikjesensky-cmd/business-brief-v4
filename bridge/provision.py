"""Operator deployment hook: create only the explicitly configured private output bucket."""
import os
from .core import Storage
from .validation import require

def main():
    storage=Storage(os.environ['SUPABASE_URL'],os.environ['SUPABASE_SECRET_KEY'])
    bucket=os.environ['BRIDGE_PAGE_INGEST_BUCKET']
    r=storage.call('GET','/bucket/'+bucket)
    if r.status_code in (400,404):
        r=storage.call('POST','/bucket',json={'id':bucket,'name':bucket,'public':False,'allowed_mime_types':['application/json'],'file_size_limit':5*1024*1024})
        require(r.status_code in (200,201),'CONFIGURATION_MISSING',503)
    storage.private(bucket);storage.private(os.environ['BRIDGE_SOURCE_BUCKET'])
    print('BRIDGE_PRIVATE_BUCKETS_PASS',flush=True)
if __name__=='__main__':main()
