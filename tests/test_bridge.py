import copy
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import date
from uuid import UUID
import pytest
from bridge.core import Bridge, Database, bundle_validate, digest, jcs
from bridge.server import Application
from bridge.validation import Failure, page_schema, strict_json, verification
from business_brief.contracts import (PageIngest, PageItem, RelevanceAssessment, PerspectiveEvidence, ContinuationEvidence, Verification, SourceBundle, PublicationIdentity, PageImage, SourcePart, OcrInfo)

SID='00000000-0000-4000-8000-000000000001'
EID='00000000-0000-4000-8000-000000000002'
BID='00000000-0000-4000-8000-000000000003'
PID='00000000-0000-4000-8000-000000000004'
KEY='00000000-0000-4000-8000-000000000005'
SHA='a'*64
PREFIX='paper/2026/2026-10-14/sha256-'+SHA+'/technician-v4.2/attempt-test/'
ROW={'id':UUID(SID),'edition_id':UUID(EID),'blob_id':UUID(BID),'publication_uuid':UUID(PID),'publication_id':'paper','canonical_name':'Paper','edition_date':date(2026,10,14),'edition_variant':'default','active_source_id':UUID(SID),'status':'READY_FOR_INGESTOR','page_count':1,'technician_version':'technician-v4.2','source_bundle_contract':'source-bundle-v4','source_bundle_path':PREFIX+'manifest.json','sha256':SHA,'byte_size':8}

@pytest.fixture
def page():
    item=PageItem('p1-i1','article','Title',None,None,None,'Synthetic text',RelevanceAssessment('relevant','Synthetic reason'),PerspectiveEvidence(),ContinuationEvidence(True,False,False),Verification('VERIFIED',True,True,True,None,True,True,True))
    return PageIngest(SID,SHA,'paper','Paper','2026-10-14','default',1,(item,),'VERIFIED').to_dict()

@pytest.fixture
def manifest():
    bundle = SourceBundle('sha256:'+SHA,SHA,PublicationIdentity('paper','Paper','2026-10-14'),'original.pdf',8,1,PREFIX+'original.pdf',PREFIX+'original.pdf',(PageImage(1,PREFIX+'page-1.png',10,20,'b'*64),),OcrInfo('none',False,False,None,None,(),PREFIX+'original.pdf',SHA),(SourcePart(1,1,1,PREFIX+'part-1.pdf',SHA,8),),'2026-10-15T00:00:00Z','technician-v4.2').to_dict()
    return json.loads(json.dumps(bundle))

def assert_failure(code, action):
    with pytest.raises(Failure) as e: action()
    assert e.value.code==code

@pytest.mark.parametrize('raw',[b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{} {}',b'"\xff"',b'\xef\xbb\xbf{}'])
def test_strict_json(raw): assert_failure('INVALID_JSON',lambda:strict_json(raw))

def test_page_roundtrip(page): page_schema(page); verification(page)

@pytest.mark.parametrize('path,value',[
 (('publication','page_no'),True),(('publication','page_no'),1.2),(('publication','page_no'),0),
 (('source','source_id'),SID.upper().replace('00000000','AAAAAAAA')),
 (('source','source_sha256'),'A'*64),(('publication','edition_date'),'2026-02-30'),
 (('producer',),'worker'),(('page_notes',),()),(('page_status',),{}),
 (('items',0,'verification','visual_checked'),1),(('items',0,'relevance','state'),[]),
 (('items',0,'perspective','observed_on_page'),None),(('items',0,'verification','status'),{}),
 (('items',0,'page_item_id'),''),(('items',0,'title'),12)])
def test_bad_types(page,path,value):
    d=page
    for k in path[:-1]: d=d[k]
    d[path[-1]]=value
    assert_failure('PAGE_SCHEMA_INVALID',lambda:page_schema(page))

@pytest.mark.parametrize('path',[(),('source',),('publication',),('items',0),('items',0,'relevance'),('items',0,'perspective'),('items',0,'continuation'),('items',0,'verification')])
def test_extras(page,path):
    d=page
    for k in path:d=d[k]
    d['unexpected']='value'; assert_failure('PAGE_SCHEMA_INVALID',lambda:page_schema(page))

def test_duplicate_items(page):
    page['items']*=2; assert_failure('PAGE_SCHEMA_INVALID',lambda:page_schema(page))

@pytest.mark.parametrize('check',['visual_checked','text_layer_checked','title_verified','boundaries_verified','reading_order_verified','text_on_page_complete'])
def test_failed_checks(page,check):
    page['items'][0]['verification'][check]=False
    assert_failure('PAGE_VERIFICATION_INVALID',lambda:verification(page))

def test_irrelevant_exception(page):
    i=page['items'][0];i['relevance']['state']='irrelevant';i['text_on_page']=None;i['verification']['text_on_page_complete']=False
    page_schema(page);verification(page)

def test_review_and_blocked(page):
    page['page_status']='NEEDS_REVIEW';page['page_notes']=['review'];page['items'][0]['verification']['status']='NEEDS_REVIEW';page['items'][0]['verification']['notes']=['localized']
    verification(page)
    page['page_status']='VERIFIED';assert_failure('PAGE_VERIFICATION_INVALID',lambda:verification(page))
    page['items'][0]['verification']['status']='BLOCKED';assert_failure('PAGE_BLOCKED',lambda:verification(page))

@pytest.mark.parametrize('mutation',[
 lambda m:m.update(source_id=SID),lambda m:m.update(source_sha256='c'*64),
 lambda m:m['identity'].update(edition_variant='other'),lambda m:m['identity'].update(canonical_name='Other'),
 lambda m:m.update(status='PROCESSING'),lambda m:m.update(page_count=True),
 lambda m:m['page_images'][0].update(page_no=True),lambda m:m['page_images'][0].update(width_px=0),
 lambda m:m['page_images'].append(m['page_images'][0]),lambda m:m.update(original_path='/etc/passwd'),
 lambda m:m.update(original_path=PREFIX+'../other.pdf'),lambda m:m['parts'][0].update(page_end=2),
 lambda m:m['ocr'].update(pages_requiring_ocr=[2]),lambda m:m['ocr'].update(prepared_pdf_path=PREFIX+'other.pdf'),
 lambda m:m['page_images'][0].update(path='https://evil.test/a'),lambda m:m['page_images'][0].update(path='other/p.png')])
def test_manifest_bad(manifest,mutation):
    mutation(manifest);assert_failure('BUNDLE_INVALID',lambda:bundle_validate(manifest,ROW))

def test_manifest_identity_mapping(manifest): bundle_validate(manifest,ROW)

def test_jcs():
    assert jcs({'b':2,'a':'é'})==b'{"a":"\xc3\xa9","b":2}'
    assert jcs({'n':1e-7})==b'{"n":1e-7}'
    assert jcs({'n':1.0})==b'{"n":1}'
    assert jcs({'é':'e\u0301'})!=jcs({'é':'é'})

class Cursor:
    def __init__(self,result=None): self.result=result
    def fetchone(self):return self.result
class Connection:
    closed=False
    def __init__(self,db):self.db=db
    def execute(self,query,params=()):
        if query.startswith('select request_sha256'):return Cursor(self.db.bindings.get((params[0],params[1])))
        if query.startswith('insert into bridge_private.bindings'):
            principal,key,rh,target,*_=params
            self.db.bindings.setdefault((principal,key),{'request_sha256':rh,'target_key':target})
        return Cursor()
    def commit(self):pass
    def rollback(self):pass
class DB:
    def __init__(self):self.bindings={};self.lock=threading.Lock();self.rowdata=copy.deepcopy(ROW)
    @contextmanager
    def connection(self):
        with self.lock:yield Connection(self)
    def row(self,c,sid,allowed,lock=True):
        if 'paper' not in allowed:raise Failure('SOURCE_NOT_FOUND',404)
        if self.rowdata['status']!='READY_FOR_INGESTOR':raise Failure('SOURCE_NOT_READY',409)
        return self.rowdata
class MemoryStorage:
    def __init__(self):self.data={};self.fail_create=False;self.fail_read=False;self.corrupt=False
    def create(self,b,k,data):
        created=k not in self.data
        self.data.setdefault(k,data)
        if self.fail_create:self.fail_create=False;raise Failure('UPSTREAM_UNAVAILABLE',503)
        return created
    def download(self,b,k):
        if self.fail_read:self.fail_read=False;raise Failure('UPSTREAM_UNAVAILABLE',503)
        return b'corrupt' if self.corrupt else self.data[k]
class TestBridge(Bridge):
    __test__=False
    def bundle(self,r):return {},'c'*64
@pytest.fixture
def bridge():return TestBridge(DB(),MemoryStorage(),'source','output')
def wrapper(page):return {'contract_version':'ingestor-access-v1','source_bundle_sha256':'c'*64,'page':page}

def test_create_replay_conflict(bridge,page):
    w=wrapper(page);code,r=bridge.post(w,KEY,'test',['paper']);assert code==201 and r['verification']['identity_matches']
    code,r=bridge.post(w,KEY,'test',['paper']);assert code==200 and r['disposition']=='REPLAYED'
    page['page_notes']=['changed'];assert_failure('IDEMPOTENCY_CONFLICT',lambda:bridge.post(w,KEY,'test',['paper']))
    assert_failure('CANONICAL_CONFLICT',lambda:bridge.post(w,str(UUID(int=6)),'test',['paper']))

def test_concurrent_create(bridge,page):
    with ThreadPoolExecutor(4) as pool:
        codes=list(pool.map(lambda n:bridge.post(wrapper(page),str(UUID(int=n)),'test',['paper'])[0],range(1,5)))
    assert sorted(codes)==[200,200,200,201] and len(bridge.storage.data)==1

@pytest.mark.parametrize('mode',['fail_create','fail_read'])
def test_timeout_recovery(bridge,page,mode):
    setattr(bridge.storage,mode,True)
    with pytest.raises(Failure) as e:bridge.post(wrapper(page),KEY,'test',['paper'])
    assert e.value.code=='PERSISTENCE_UNVERIFIED' and e.value.persistence=='UNKNOWN'
    assert bridge.post(wrapper(page),KEY,'test',['paper'])[0]==200

def test_corrupt_new_readback(bridge,page):
    bridge.storage.corrupt=True
    assert_failure('PERSISTENCE_UNVERIFIED',lambda:bridge.post(wrapper(page),KEY,'test',['paper']))

def test_stale_source_and_hash(bridge,page):
    w=wrapper(page);w['source_bundle_sha256']='d'*64
    assert_failure('SOURCE_CHANGED',lambda:bridge.post(w,KEY,'test',['paper']))
    bridge.db.rowdata['status']='PROCESSING'
    assert_failure('SOURCE_NOT_READY',lambda:bridge.post(wrapper(page),KEY,'test',['paper']))
    assert not bridge.storage.data

@pytest.fixture
def app(bridge):
    return Application(bridge,[{'id':'test','token':'x'*43,'scopes':['source:read','page:write'],'publications':['paper']},{'id':'read','token':'r'*43,'scopes':['source:read'],'publications':['paper']}])

def test_auth(app):
    assert_failure('UNAUTHENTICATED',lambda:app.auth(None,False))
    assert_failure('UNAUTHENTICATED',lambda:app.auth('Bearer wrong',False))
    assert_failure('FORBIDDEN',lambda:app.auth('Bearer '+'r'*43,True))

def test_post_transport(app,page):
    headers={'Authorization':'Bearer '+'x'*43,'Content-Type':'application/json','Idempotency-Key':KEY}
    data=json.dumps(wrapper(page)).encode();headers['Content-Length']=str(len(data))
    assert app.dispatch('POST','/ingestor-v2/page',headers,lambda n:data)[0]==201
    assert_failure('INVALID_REQUEST',lambda:app.dispatch('POST','/ingestor-v2/page?foo=x',headers,lambda n:data))
    headers['Content-Length']=str(5*1024*1024+1)
    assert_failure('PAYLOAD_TOO_LARGE',lambda:app.dispatch('POST','/ingestor-v2/page',headers,lambda n:data))

def test_resource_allowlist(app,page):
    page['publication']['publication_id']='private'
    data=json.dumps(wrapper(page)).encode()
    h={'Authorization':'Bearer '+'x'*43,'Content-Type':'application/json','Idempotency-Key':KEY,'Content-Length':str(len(data))}
    assert_failure('SOURCE_NOT_FOUND',lambda:app.dispatch('POST','/ingestor-v2/page',h,lambda n:data))

class CurrentConnection:
    def __init__(self,rows):self.rows=rows
    def execute(self,*args):return self
    def fetchall(self):return self.rows
@pytest.mark.parametrize('rows,code',[([],'SOURCE_NOT_FOUND'),([{'active_source_id':SID},{'active_source_id':EID}],'SOURCE_AMBIGUOUS')])
def test_latest_selection(rows,code):
    db=Database('unused','unused')
    assert_failure(code,lambda:db.current(CurrentConnection(rows),'paper',['paper']))

def test_latest_does_not_fallback():
    db=Database('unused','unused')
    def row(*args):raise Failure('SOURCE_NOT_READY',409)
    db.row=row
    assert_failure('SOURCE_NOT_READY',lambda:db.current(CurrentConnection([{'active_source_id':SID}]),'paper',['paper']))
