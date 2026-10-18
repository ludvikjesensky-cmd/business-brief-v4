import hashlib
import os
import types
from contextlib import contextmanager
from dataclasses import fields as dcfields, is_dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path, PurePosixPath
from typing import get_args, get_origin, get_type_hints, Literal
from urllib.parse import quote, urlsplit

import httpx
import psycopg
from psycopg.rows import dict_row
import rfc8785
from .validation import Failure, require, strict_json, sha, slug, verification, page_schema, generation_prefix
try:
    from .contracts import SourceBundle
except ImportError:
    from business_brief.contracts import SourceBundle

CONTRACT = 'ingestor-access-v1'
def digest(data): return hashlib.sha256(data).hexdigest()
def stamp(t=None): return (t or datetime.now(timezone.utc)).isoformat().replace('+00:00', 'Z')
def jcs(value):
    try: return rfc8785.dumps(value)
    except (ValueError, TypeError): raise Failure('PAGE_SCHEMA_INVALID', 422) from None

def datashape(value, annotation):
    """Validate SourceBundle's serialized dataclasses, including tuple-to-JSON arrays."""
    origin, args = get_origin(annotation), get_args(annotation)
    if origin in (types.UnionType,):
        if value is None and type(None) in args: return
        return datashape(value, next(a for a in args if a is not type(None)))
    if is_dataclass(annotation):
        expected = {f.name for f in dcfields(annotation)}
        if annotation.__name__ == 'PublicationIdentity': expected.add('edition_key')
        require(type(value) is dict and set(value) == expected, 'BUNDLE_INVALID', 409)
        for k, a in get_type_hints(annotation).items(): datashape(value[k], a)
        if 'edition_key' in expected: require(type(value['edition_key']) is str, 'BUNDLE_INVALID', 409)
    elif origin is tuple:
        require(type(value) is list, 'BUNDLE_INVALID', 409)
        for v in value: datashape(v, args[0])
    elif annotation is float: require(type(value) in (float, int), 'BUNDLE_INVALID', 409)
    else: require(type(value) is annotation, 'BUNDLE_INVALID', 409)

def bundle_validate(m, row):
    try:
        datashape(m, SourceBundle)
        identity = m['identity']
        require(m['status'] == 'READY_FOR_INGESTOR' and m['schema_version'] == 'source-bundle-v4', 'BUNDLE_INVALID', 409)
        expected = {'publication_id':row['publication_id'], 'canonical_name':row['canonical_name'], 'edition_date':str(row['edition_date']), 'edition_variant':row['edition_variant']}
        require(all(identity[k] == v for k,v in expected.items()), 'BUNDLE_INVALID', 409)
        require(identity['edition_key'] == ':'.join([row['publication_id'],str(row['edition_date']),row['edition_variant']]), 'BUNDLE_INVALID', 409)
        require(m['source_id'] == 'sha256:'+row['sha256'] and m['source_sha256'] == row['sha256'], 'BUNDLE_INVALID', 409)
        require(m['page_count'] == row['page_count'] and 0 < m['page_count'] <= 9999 and m['technician_version'] == row['technician_version'], 'BUNDLE_INVALID', 409)
        require(m['byte_size'] == row['byte_size'], 'BUNDLE_INVALID', 409)
        o = m['ocr']; sha(o['prepared_sha256'])
        require(m['prepared_pdf_path'] == o['prepared_pdf_path'], 'BUNDLE_INVALID', 409)
        require(all(1 <= p <= m['page_count'] for p in o['pages_requiring_ocr']), 'BUNDLE_INVALID', 409)
        require(len(set(o['pages_requiring_ocr'])) == len(o['pages_requiring_ocr']), 'BUNDLE_INVALID', 409)
        require(sorted(i['page_no'] for i in m['page_images']) == list(range(1,m['page_count']+1)), 'BUNDLE_INVALID', 409)
        for image in m['page_images']:
            require(image['width_px'] > 0 and image['height_px'] > 0, 'BUNDLE_INVALID', 409); sha(image['sha256'])
        ranges=[]
        for part in m['parts']:
            require(1 <= part['page_start'] <= part['page_end'] <= m['page_count'] and part['part_no'] > 0 and part['byte_size'] > 0, 'BUNDLE_INVALID', 409)
            sha(part['sha256']); ranges.extend(range(part['page_start'],part['page_end']+1))
        require(len({part['part_no'] for part in m['parts']})==len(m['parts']), 'BUNDLE_INVALID', 409)
        prefix = row['source_bundle_path'].rsplit('/',1)[0]+'/'
        paths = [m['original_path'],m['prepared_pdf_path']] + [i['path'] for i in m['page_images']+m['parts']]
        for key in paths:
            require(type(key) is str and key.startswith(prefix) and key == str(PurePosixPath(key)) and not any(x in key for x in ['..','\\',':','%','?','#']) and not key.startswith('/'), 'BUNDLE_INVALID', 409)
        slug(row['publication_id']); sha(row['sha256'])
    except Failure:
        raise Failure('BUNDLE_INVALID',409) from None

class Storage:
    def __init__(self, base, secret):
        require(urlsplit(base).scheme == 'https', 'CONFIGURATION_MISSING', 503)
        self.base = base.rstrip('/')+'/storage/v1'
        self.client = httpx.Client(headers={'apikey':secret,'Authorization':'Bearer '+secret},timeout=30,follow_redirects=False)
    def path(self,bucket,key): return '/'+quote(bucket,safe='')+'/'+quote(key,safe='/')
    def call(self,method,path,**kw):
        try: return self.client.request(method,self.base+path,**kw)
        except httpx.HTTPError: raise Failure('UPSTREAM_UNAVAILABLE',503) from None
    def private(self,bucket):
        r = self.call('GET','/bucket/'+quote(bucket,safe=''))
        require(r.status_code == 200 and r.json().get('public') is False,'CONFIGURATION_MISSING',503)
    def download(self,bucket,key):
        r = self.call('GET','/object/authenticated'+self.path(bucket,key))
        if r.status_code in (400,404): raise Failure('ARTIFACT_MISSING',409)
        require(r.status_code == 200,'UPSTREAM_UNAVAILABLE',503)
        return r.content
    def access(self,bucket,key,media,expected=None):
        data = self.download(bucket,key)
        require(len(data)>0,'ARTIFACT_MISSING',409)
        if expected: require(digest(data)==expected,'ARTIFACT_HASH_MISMATCH',409)
        issued = datetime.now(timezone.utc)
        r = self.call('POST','/object/sign'+self.path(bucket,key),json={'expiresIn':300})
        require(r.status_code == 200,'UPSTREAM_UNAVAILABLE',503)
        url = r.json()['signedURL']
        if url.startswith('/'): url=self.base+url
        require(urlsplit(url).scheme == 'https' and urlsplit(url).netloc == urlsplit(self.base).netloc,'UPSTREAM_UNAVAILABLE',503)
        return {'bucket':bucket,'storage_key':key,'media_type':media,'sha256':digest(data),'byte_size':len(data),'url':url,'expires_at':stamp(issued+timedelta(seconds=300))}
    def create(self,bucket,key,data):
        # Storage returns 400 Duplicate in some versions, 409 in others.
        r=self.call('POST','/object'+self.path(bucket,key),content=data,headers={'Content-Type':'application/json','x-upsert':'false'})
        if 200 <= r.status_code < 300: return True
        if r.status_code in (400,409) and (r.json().get('statusCode') in ('409',409) or r.json().get('error') in ('Duplicate','Asset Already Exists')): return False
        raise Failure('PERSISTENCE_UNVERIFIED',503,'UNKNOWN')

JOIN = '''select s.*, e.active_source_id,e.edition_date,e.edition_variant,
 e.publication_id as publication_uuid,p.publication_id,p.canonical_name,
 b.sha256,b.byte_size from public.sources s
 join public.editions e on e.id=s.edition_id
 join public.publications p on p.id=e.publication_id
 join public.source_blobs b on b.id=s.blob_id where s.id=%s'''

class Database:
    def __init__(self, url, ca): self.url,self.ca=url,ca
    @contextmanager
    def connection(self):
        try:
            with psycopg.connect(self.url,connect_timeout=10,sslmode='verify-full',sslrootcert=self.ca,row_factory=dict_row) as c:
                c.execute("set lock_timeout='5s'")
                c.execute("set statement_timeout='20s'")
                # No idle transaction timeout: an I/O wait must not silently drop the row fence.
                c.execute("set idle_in_transaction_session_timeout='0'")
                yield c
        except Failure: raise
        except psycopg.errors.LockNotAvailable: raise Failure('WRITE_IN_PROGRESS',503) from None
        except psycopg.Error: raise Failure('UPSTREAM_UNAVAILABLE',503) from None
    def authorize(self,c,sid,allowed):
        r=c.execute(JOIN,(sid,)).fetchone()
        if not r or r['publication_id'] not in allowed: raise Failure('SOURCE_NOT_FOUND',404)
        return r
    def row(self,c,sid,allowed,lock=True):
        r=self.authorize(c,sid,allowed)
        if lock:
            # Same edition -> source order as finalize_technician_source. Re-read after waiting.
            for table, ident in [('editions',r['edition_id']),('sources',sid),('source_blobs',r['blob_id']),('publications',r['publication_uuid'])]:
                c.execute('select id from public.'+table+' where id=%s for update',(ident,)).fetchone()
            again=c.execute(JOIN,(sid,)).fetchone()
            require(again == r,'SOURCE_CHANGED',409)
        require(r['status']=='READY_FOR_INGESTOR','SOURCE_NOT_READY',409)
        require(r['active_source_id']==r['id'],'SOURCE_CHANGED',409)
        require(r['source_bundle_contract']=='source-bundle-v4' and r['technician_version']=='technician-v4.2','BUNDLE_INVALID',409)
        return r
    def current(self,c,pub,allowed):
        if pub not in allowed: raise Failure('SOURCE_NOT_FOUND',404)
        rows=c.execute('''select e.id,e.active_source_id from public.editions e join public.publications p on p.id=e.publication_id
         where p.publication_id=%s and e.active_source_id is not null and e.edition_date=(select max(e2.edition_date) from public.editions e2 where e2.publication_id=p.id and e2.active_source_id is not null)''',(pub,)).fetchall()
        if not rows: raise Failure('SOURCE_NOT_FOUND',404)
        require(len(rows)==1,'SOURCE_AMBIGUOUS',409)
        row=self.row(c,rows[0]['active_source_id'],allowed)
        require(row['edition_id']==rows[0]['id'] and row['publication_id']==pub,'SOURCE_CHANGED',409)
        return row

class Bridge:
    def __init__(self, db, storage, source_bucket, output_bucket):
        self.db,self.storage,self.source_bucket,self.output_bucket=db,storage,source_bucket,output_bucket
    def bundle(self,r):
        raw=self.storage.download(self.source_bucket,r['source_bundle_path'])
        try: m=strict_json(raw)
        except Failure: raise Failure('BUNDLE_INVALID',409) from None
        bundle_validate(m,r)
        return m,digest(raw)
    def identity(self,r,h):
        return {'source_id':str(r['id']),'source_sha256':r['sha256'],'publication_id':r['publication_id'],'canonical_name':r['canonical_name'],'edition_id':str(r['edition_id']),'edition_date':str(r['edition_date']),'edition_variant':r['edition_variant'],'page_count':r['page_count'],'technician_version':r['technician_version'],'source_bundle_schema':'source-bundle-v4','source_bundle_sha256':h,'readiness':'READY_FOR_INGESTOR'}
    def current(self,pub,allowed):
        with self.db.connection() as c:
            r=self.db.current(c,pub,allowed); m,h=self.bundle(r)
            return {'status':'READY','selection':{'publication':pub,'rule':'latest-active-edition-date-unique'},'source':self.identity(r,h)}
    def page(self,sid,no,allowed):
        with self.db.connection() as c:
            r=self.db.row(c,sid,allowed); m,h=self.bundle(r)
            require(1<=no<=r['page_count'],'PAGE_NOT_FOUND',404)
            image=next(i for i in m['page_images'] if i['page_no']==no)
            def access(key,media,sha): return self.storage.access(self.source_bucket,key,media,sha)
            result={'status':'READY','source':self.identity(r,h),'page_no':no,
              'manifest':access(r['source_bundle_path'],'application/json',h),
              'page_image':{'artifact':access(image['path'],'image/png',image['sha256']),'width_px':image['width_px'],'height_px':image['height_px']},
              'prepared_evidence':{'artifact':access(m['prepared_pdf_path'],'application/pdf',m['ocr']['prepared_sha256']),'pdf_page_no':no,'ocr':m['ocr']},
              'original_pdf':access(m['original_path'],'application/pdf',r['sha256'])}
            # Manifest bytes are pinned again before access leaves the lock boundary.
            require(self.bundle(r)[1]==h,'SOURCE_CHANGED',409)
            return result
    def post(self,wrapper,key,principal,allowed):
        p=wrapper['page']; sid=p['source']['source_id']; no=p['publication']['page_no']
        page_schema(p)
        canonical=jcs(p); request_hash=digest(jcs(wrapper)); artifact_hash=digest(canonical)
        target=f"{generation_prefix(p)}/page-{no:04d}.json"
        def eligible(c):
            r=self.db.row(c,sid,allowed); m,h=self.bundle(r)
            require(h==wrapper['source_bundle_sha256'],'SOURCE_CHANGED',409)
            ident=self.identity(r,h)
            require(p['source']['source_sha256']==r['sha256'] and all(p['publication'][k]==ident[k] for k in ['publication_id','canonical_name','edition_date','edition_variant']) and no<=r['page_count'],'IDENTITY_MISMATCH',409)
            verification(p)
            # This consolidation defines v4, not a new binary upload protocol.
            # Never store a page pointing to unverified/unfenced crops.
            require(not any(i.get('assets') for i in p['items']), 'CONFIGURATION_MISSING', 503)
            return r,ident
        # Session advisory lock covers both transactions; durable PENDING claim covers session loss.
        with self.db.connection() as c:
            c.execute('select pg_advisory_lock(hashtextextended(%s,0))',(target,))
            try:
                r,ident=eligible(c)
                old=c.execute('select request_sha256,target_key from bridge_private.bindings where principal=%s and idempotency_key=%s',(principal,key)).fetchone()
                if old: require(old['request_sha256']==request_hash and old['target_key']==target,'IDEMPOTENCY_CONFLICT',409)
                c.execute('''insert into bridge_private.bindings(principal,idempotency_key,request_sha256,target_key,source_id,edition_id,blob_id,publication_id)
                values(%s,%s,%s,%s,%s,%s,%s,%s) on conflict(principal,idempotency_key) do nothing''',(principal,key,request_hash,target,r['id'],r['edition_id'],r['blob_id'],r['publication_uuid']))
                # Recheck after uniqueness wait (another target can race with the same key).
                old=c.execute('select request_sha256,target_key from bridge_private.bindings where principal=%s and idempotency_key=%s for update',(principal,key)).fetchone()
                require(old['request_sha256']==request_hash and old['target_key']==target,'IDEMPOTENCY_CONFLICT',409)
                c.execute("update bridge_private.bindings set state='PENDING' where principal=%s and idempotency_key=%s",(principal,key))
                c.commit()  # Claim survives a crash. No Storage mutation has started yet.
                r,ident=eligible(c)
                try:
                    created=self.storage.create(self.output_bucket,target,canonical)
                    stored=self.storage.download(self.output_bucket,target)
                except Failure:
                    raise Failure('PERSISTENCE_UNVERIFIED',503,'UNKNOWN') from None
                if stored!=canonical:
                    if created: raise Failure('PERSISTENCE_UNVERIFIED',503,'UNKNOWN')
                    # Existing immutable winner resolves this claim, but never overwrites it.
                    c.execute("update bridge_private.bindings set state='CONFLICT' where principal=%s and idempotency_key=%s",(principal,key)); c.commit()
                    raise Failure('CANONICAL_CONFLICT',409,'EXISTING_UNCHANGED')
                try:
                    page_schema(strict_json(stored))
                    require(digest(stored)==artifact_hash,'PERSISTENCE_UNVERIFIED',503)
                    require(self.bundle(r)[1]==ident['source_bundle_sha256'],'SOURCE_CHANGED',409)
                except Failure: raise Failure('PERSISTENCE_UNVERIFIED',503,'UNKNOWN') from None
                c.execute("update bridge_private.bindings set state='VERIFIED',artifact_sha256=%s where principal=%s and idempotency_key=%s",(artifact_hash,principal,key))
                try: c.commit()
                except psycopg.Error: raise Failure('PERSISTENCE_UNVERIFIED',503,'UNKNOWN') from None
                return (201 if created else 200),{'status':'STORED','disposition':'CREATED' if created else 'REPLAYED','idempotency_key':key,'source':ident,'page_no':no,'page_status':p['page_status'],'usable_for_assembly':p['page_status'] in ['VERIFIED','VERIFIED_WITH_NOTES'],
                  'artifact':{'bucket':self.output_bucket,'storage_key':target,'media_type':'application/json','artifact_sha256':artifact_hash,'byte_size':len(stored),'serialization':'RFC8785-JCS'},
                  'verification':{'status':'VERIFIED','method':'storage-download-sha256-and-identity','stored_sha256':digest(stored),'identity_matches':True,'verified_at':stamp()}}
            except psycopg.Error:
                raise Failure('PERSISTENCE_UNVERIFIED',503,'UNKNOWN') from None
            finally:
                # A broken connection is already closing; never mask persistence UNKNOWN.
                if not c.closed:
                    try:
                        c.rollback(); c.execute('select pg_advisory_unlock(hashtextextended(%s,0))',(target,)); c.commit()
                    except psycopg.Error: pass
