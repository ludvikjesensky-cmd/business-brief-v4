"""Deployment hook: private output bucket plus additive JSON/PNG capability."""
import os
from .core import Storage
from .validation import require

LIMIT=32*1024*1024
MIMES={'application/json','image/png'}


def configure_output(storage,bucket):
    r=storage.call('GET','/bucket/'+bucket)
    if r.status_code in (400,404):
        r=storage.call('POST','/bucket',json={'id':bucket,'name':bucket,'public':False,
            'allowed_mime_types':sorted(MIMES),'file_size_limit':LIMIT})
        require(r.status_code in (200,201),'CONFIGURATION_MISSING',503)
    else:
        require(r.status_code==200 and r.json().get('public') is False,'CONFIGURATION_MISSING',503)
        current=r.json(); allowed=current.get('allowed_mime_types'); limit=current.get('file_size_limit')
        patch={}
        # null/empty means unrestricted. Preserve any existing allowed MIME types.
        if allowed and not MIMES.issubset(set(allowed)):
            patch['allowed_mime_types']=sorted(set(allowed)|MIMES)
        if limit is not None and int(limit)<LIMIT:patch['file_size_limit']=LIMIT
        if patch:
            r=storage.call('PUT','/bucket/'+bucket,json={**patch,'public':False})
            require(r.status_code in (200,201),'CONFIGURATION_MISSING',503)
    r=storage.call('GET','/bucket/'+bucket)
    require(r.status_code==200,'CONFIGURATION_MISSING',503)
    final=r.json();allowed=final.get('allowed_mime_types');limit=final.get('file_size_limit')
    require(final.get('public') is False and (not allowed or MIMES.issubset(set(allowed)))
            and (limit is None or int(limit)>=LIMIT),'CONFIGURATION_MISSING',503)


def main():
    storage=Storage(os.environ['SUPABASE_URL'],os.environ['SUPABASE_SECRET_KEY'])
    configure_output(storage,os.environ['BRIDGE_PAGE_INGEST_BUCKET'])
    storage.private(os.environ['BRIDGE_SOURCE_BUCKET'])
    print('BRIDGE_PRIVATE_BUCKETS_PASS',flush=True)
if __name__=='__main__':main()
