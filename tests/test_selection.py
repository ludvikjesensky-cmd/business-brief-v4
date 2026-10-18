import copy
import json
from uuid import UUID
import pytest
from test_bridge import bridge, page, page_v3, wrapper, KEY, SID, assert_failure
from test_article_assets import page_v4, asset_page
from test_asset_persistence import live
from bridge.core import jcs, digest
from bridge.selection import (revision_schema, get_artifact, list_artifacts, manifest_schema,
    persist_manifest, assembly_input, artifact_key, BLOCKED_SHA256)
from bridge.validation import Failure, generation_prefix
from bridge.server import Application

TIME='2026-10-18T20:00:00Z'

def revision(live):
    b,p,m,_=live
    original=b.post(wrapper(p),KEY,'test',['paper'])[1]
    corrected=copy.deepcopy(p)
    a=corrected['items'][0]['assets'][0]
    a['page_anchor'].update(bbox_norm=[.1,.2,.6,.6],bbox_px=None)
    from bridge.assets import prepare_assets
    expected=copy.deepcopy(corrected)
    crops=prepare_assets(expected,m,b.storage,'source','page-ingest','r1')
    rev={'schema_version':'page-revision-v1','revision_id':'r1',
         'supersedes':{'key':original['artifact']['storage_key'],'sha256':original['artifact']['artifact_sha256']},
         'reason':'incomplete infographic crop','created_by':'test','created_at':TIME,
         'crop_previews':[{'asset_id':a['asset_id'],'sha256':crops[0][0]['artifact']['sha256'],'inspected_by':'test','inspected_at':TIME}],
         'page':corrected}
    return rev

def write_revision(b,rev,key=str(UUID(int=90))):
    revision_schema(rev,submission=True)
    return b.post(wrapper(rev['page']),key,'test',['paper'],revision={k:v for k,v in rev.items() if k!='page'})


def read(b,no=1,gen='ingestor-v2.2',rid=None):
    return get_artifact(b,SID,no,gen,rid,['paper'])


def test_revision_full_snapshot_replay_no_overwrite(live):
    b,_,_,_=live; rev=revision(live); original=dict(b.storage.data)
    assert write_revision(b,rev)[0]==201
    assert write_revision(b,rev)[0]==200
    assert write_revision(b,rev,str(UUID(int=91)))[0]==200
    assert all(b.storage.data[k]==v for k,v in original.items())
    a=read(b,rid='r1'); assert a['kind']=='revision' and a['usable_for_assembly']
    assert '/revisions/page-0001/r1/assets/' in a['assets'][0]['key']
    rev['page']['page_notes']=['changed']
    assert_failure('IDEMPOTENCY_CONFLICT',lambda:write_revision(b,rev))
    assert_failure('ASSET_SET_CONFLICT',lambda:write_revision(b,rev,str(UUID(int=92))))


@pytest.mark.parametrize('mutate',[
    lambda r:r.pop('reason'),lambda r:r.update(page={'patch':{}}),
    lambda r:r.update(revision_id='../r1'),lambda r:r.update(created_at='yesterday'),
    lambda r:r.update(crop_previews=[]),lambda r:r['supersedes'].update(key='other/page.json')])
def test_revision_schema(live,mutate):
    rev=revision(live); mutate(rev)
    with pytest.raises(Failure): revision_schema(rev,submission=True)


def test_supersedes_sha_and_preview_mismatch(live):
    b,_,_,_=live; rev=revision(live); rev['supersedes']['sha256']='f'*64
    assert_failure('SUPERSEDES_MISMATCH',lambda:write_revision(b,rev))
    rev=revision(live); rev['crop_previews'][0]['sha256']='f'*64
    assert_failure('CROP_PREVIEW_MISMATCH',lambda:write_revision(b,rev))


@pytest.mark.parametrize('stage',['crop','json'])
def test_revision_interrupted_recovery(live,stage):
    b,_,_,_=live; rev=revision(live); create=b.storage.create; failed=False
    def fault(bucket,key,data,media_type='application/json'):
        nonlocal failed
        made=create(bucket,key,data,media_type)
        if not failed and '/revisions/' in key and key.endswith('.png' if stage=='crop' else '.json'):
            failed=True; raise Failure('UPSTREAM_UNAVAILABLE',503)
        return made
    b.storage.create=fault
    with pytest.raises(Failure) as e:write_revision(b,rev)
    assert e.value.persistence=='UNKNOWN'
    assert write_revision(b,rev)[0] in (200,201)


def selection(a):
    return {**{k:a[k] for k in ('page_no','generation','schema_version','kind','revision_id','key','sha256','page_status','usable_for_assembly')},
            'evidence':{k:a['verification'][k] for k in ('receipt_id','verified_at')},'selection_reason':None}


def manifest(b,artifacts):
    return {'schema_version':'edition-selection-v1','manifest_id':'first','source':artifacts[0]['source'],
            'created_by':'test','created_at':TIME,'status':'ACCEPTED_FOR_ASSEMBLY',
            'pages':[selection(a) for a in artifacts]}


def test_heterogeneous_manifest_assembly_only_explicit(live,page_v3):
    b,p,m,_=live; rev=revision(live); write_revision(b,rev)
    b.db.rowdata['page_count']=3
    p2=copy.deepcopy(p); p2['publication']['page_no']=2
    for a in p2['items'][0]['assets']: a['page_no']=2
    m['page_images'].append({**m['page_images'][0],'page_no':2})
    b.post(wrapper(p2),str(UUID(int=101)),'test',['paper'])
    p3=copy.deepcopy(page_v3); p3['publication']['page_no']=3
    b.post(wrapper(p3),str(UUID(int=102)),'test',['paper'])
    arts=[read(b,rid='r1'),read(b,2),read(b,3,'ingestor-v2.1')]
    doc=manifest(b,arts)
    code,receipt=persist_manifest(b,doc,str(UUID(int=103)),'test',['paper'])
    assert code==201
    assert persist_manifest(b,doc,str(UUID(int=103)),'test',['paper'])[0]==200
    # Any scan is forbidden on Assembler's explicit input path.
    b.storage.list=lambda *a:pytest.fail('latest scan is forbidden')
    result=assembly_input(b,SID,'first',receipt['sha256'],['paper'])
    assert [a['generation'] for a in result['pages']]==['ingestor-v2.2','ingestor-v2.2','ingestor-v2.1']
    assert_failure('ARTIFACT_HASH_MISMATCH',lambda:assembly_input(b,SID,'first','f'*64,['paper']))
    doc['created_by']='other'
    assert_failure('IDEMPOTENCY_CONFLICT',lambda:persist_manifest(b,doc,str(UUID(int=104)),'test',['paper']))
    assert digest(b.storage.data[receipt['key']])==receipt['sha256']


@pytest.mark.parametrize('defect',['missing','unusable','unverified','hash','duplicate','count','blocked'])
def test_manifest_acceptance_fail_closed(live,defect,monkeypatch):
    b,_,_,_=live; revision(live); a=read(b); doc=manifest(b,[a])
    if defect=='missing':
        b.storage.download_bounded=lambda *a:(_ for _ in ()).throw(Failure('ARTIFACT_MISSING',409))
    if defect=='unusable': doc['pages'][0]['usable_for_assembly']=False
    if defect=='unverified': doc['pages'][0]['evidence']['receipt_id']='0'*64
    if defect=='hash': doc['pages'][0]['sha256']='0'*64
    if defect=='duplicate': doc['pages']*=2
    if defect=='count': doc['source']['page_count']=2
    if defect=='blocked': monkeypatch.setattr('bridge.selection.BLOCKED_SHA256',frozenset({a['sha256']}))
    with pytest.raises(Failure):persist_manifest(b,doc,str(UUID(int=110)),'test',['paper'])
    assert not any('/edition-selection/' in k for k in b.storage.data)


def test_readback_hash_and_asset_failure(live):
    b,_,_,_=live; revision(live); a=read(b)
    b.storage.data[a['assets'][0]['key']]=b'corrupt'
    assert_failure('PERSISTENCE_UNVERIFIED',lambda:read(b))


def test_http_readback_and_list_no_secret(live):
    b,_,_,_=live; rev=revision(live); write_revision(b,rev)
    def listing(bucket,prefix):
        return [{'name':k[len(prefix)+1:].split('/')[0]} for k in b.storage.data if k.startswith(prefix+'/') and ('/' not in k[len(prefix)+1:] or prefix.endswith('revisions') or prefix.endswith('page-0001'))]
    b.storage.list=listing
    app=Application(b,[{'id':'test','token':'x'*43,'scopes':['source:read'],'publications':['paper']}])
    for path in (f'/ingestor-v2/source/{SID}/artifacts',f'/ingestor-v2/source/{SID}/artifact?page_no=1&generation=ingestor-v2.2&revision_id=r1'):
        code,result=app.dispatch('GET',path,{'Authorization':'Bearer '+'x'*43},None)
        assert code==200
        serialized=json.dumps(result)
        assert all(x not in serialized for x in ('https://','Bearer','x'*43,'signedURL','secret'))
    assert_failure('SOURCE_NOT_FOUND',lambda:get_artifact(b,SID,1,'ingestor-v2.2',None,['other']))
    assert_failure('INVALID_REQUEST',lambda:app.dispatch('GET',f'/ingestor-v2/source/{SID}/artifact?page_no=1&generation=latest',{'Authorization':'Bearer '+'x'*43},None))


def test_manifest_interrupted_recovery_and_source_fence(live):
    b,_,_,_=live; revision(live); doc=manifest(b,[read(b)])
    b.storage.fail_create=True
    with pytest.raises(Failure) as e:persist_manifest(b,doc,str(UUID(int=130)),'test',['paper'])
    assert e.value.persistence=='UNKNOWN'
    assert persist_manifest(b,doc,str(UUID(int=130)),'test',['paper'])[0]==200
    b.db.rowdata['status']='PROCESSING'
    assert_failure('SOURCE_NOT_READY',lambda:persist_manifest(b,doc,str(UUID(int=131)),'test',['paper']))


def test_manifest_concurrent_no_overwrite(live):
    from concurrent.futures import ThreadPoolExecutor
    b,_,_,_=live; revision(live); doc=manifest(b,[read(b)])
    with ThreadPoolExecutor(4) as pool:
        results=list(pool.map(lambda n:persist_manifest(b,doc,str(UUID(int=n)),'test',['paper'])[0],range(140,144)))
    assert sorted(results)==[200,200,200,201]


def test_draft_cannot_be_assembler_input(live):
    b,_,_,_=live; revision(live); doc=manifest(b,[read(b)]); doc['status']='DRAFT'
    receipt=persist_manifest(b,doc,str(UUID(int=150)),'test',['paper'])[1]
    assert_failure('MANIFEST_NOT_ACCEPTED',lambda:assembly_input(b,SID,'first',receipt['sha256'],['paper']))
