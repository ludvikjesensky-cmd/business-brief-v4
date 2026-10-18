"""Fault-injected set-wide persistence with real PNG decoding and pixel checks."""
import copy
import json
from io import BytesIO
from uuid import UUID
from concurrent.futures import ThreadPoolExecutor

import pytest
from PIL import Image
from test_bridge import bridge, page, page_v3, wrapper, KEY, assert_failure
from test_article_assets import page_v4, asset_page
from bridge.assets import canonical_png, png, prepare_assets
from bridge.core import digest, jcs
from bridge.validation import page_schema, Failure
from bridge.server import Application


@pytest.fixture
def live(bridge, asset_page):
    p=asset_page
    image=Image.new('RGBA',(100,100))
    image.putdata([(x,y,(x+y)%256,255) for y in range(100) for x in range(100)])
    raw=canonical_png(image); image_sha=digest(raw)
    manifest={'page_images':[{'page_no':1,'path':'authoritative.png','sha256':image_sha,'width_px':100,'height_px':100}]}
    bridge.bundle=lambda r:(manifest,'c'*64)
    bridge.output_bucket='page-ingest'
    source={'authoritative.png':raw}
    storage=bridge.storage
    storage.private=lambda b:None
    storage.download_bounded=lambda b,k,limit: source[k] if b=='source' else storage.download(b,k)
    original_create=storage.create
    storage.create=lambda b,k,data,media_type='application/json':original_create(b,k,data)
    a=p['items'][0]['assets'][0]; a['artifact']=None
    a['page_anchor']['source_page_image_sha256']=image_sha
    return bridge,p,manifest,source


def persist(live,key=KEY):
    b,p,_,_=live
    return b.post(wrapper(p),key,'test',['paper'])


@pytest.mark.parametrize('count',[1,2])
def test_happy_path_set(live,count):
    b,p,m,source=live
    if count==2:
        second=copy.deepcopy(p['items'][0]['assets'][0]); second['asset_id']='p0001-i1-chart-02'
        second['page_anchor'].update(bbox_norm=[.5,.6,1,1],bbox_px=[50,60,100,100])
        p['items'][0]['assets'].append(second)
    original=copy.deepcopy(p)
    code,receipt=persist(live)
    assert code==201 and receipt['usable_for_assembly'] and len(receipt['assets'])==count
    canonical=json.loads(b.storage.data[receipt['artifact']['storage_key']]); page_schema(canonical)
    assert p==original  # submission and its durable hash never mutated
    for a in canonical['items'][0]['assets']:
        ar=a['artifact']; data=b.storage.data[ar['key']]
        assert digest(data)==ar['sha256'] and len(data)==ar['byte_size']
        crop=png(data); bounds=a['page_anchor']['bbox_px']
        assert crop.size==(bounds[2]-bounds[0],bounds[3]-bounds[1])
        assert crop.tobytes()==png(source['authoritative.png']).crop(bounds).tobytes()
    assert persist(live)[0]==200
    assert persist(live,str(UUID(int=80)))[0]==200


@pytest.mark.parametrize('field,value,code',[
    ('source_page_image_sha256','e'*64,'SOURCE_PNG_HASH_MISMATCH'),
    ('bbox_px',[10,20,51,60],'ASSET_BBOX_MISMATCH'),
])
def test_source_bound_errors(live,field,value,code):
    b,p,_,_=live; p['items'][0]['assets'][0]['page_anchor'][field]=value
    assert_failure(code,lambda:persist(live)); assert not b.storage.data


@pytest.mark.parametrize('part',['sha256','width_px'])
def test_manifest_png_mismatch(live,part):
    b,p,m,_=live; m['page_images'][0][part]='f'*64 if part=='sha256' else 99
    assert_failure('SOURCE_PNG_HASH_MISMATCH' if part=='sha256' else 'SOURCE_PNG_DIMENSIONS_MISMATCH',lambda:persist(live))
    assert not b.storage.data


def test_rounding_and_whole_page(live):
    b,p,m,_=live; a=p['items'][0]['assets'][0]
    for bounds,expected in [([0,0,1,1],[0,0,100,100]),([.101,.201,.499,.599],[10,20,50,60])]:
        a['page_anchor'].update(bbox_norm=bounds,bbox_px=None)
        prepared=prepare_assets(p,m,b.storage,'source','page-ingest')
        assert prepared[0][0]['page_anchor']['bbox_px']==expected
        a['artifact']=None


@pytest.mark.parametrize('stage',['asset-create','asset-read','page-create','page-read'])
def test_interrupted_reconciliation(live,stage):
    b,_,_,_=live; storage=b.storage; create=storage.create; download=storage.download
    tripped=False
    def fail_create(bucket,key,data,media_type='application/json'):
        nonlocal tripped
        made=create(bucket,key,data,media_type)
        if not tripped and ((stage=='asset-create' and key.endswith('.png')) or (stage=='page-create' and key.endswith('.json'))):
            tripped=True; raise Failure('UPSTREAM_UNAVAILABLE',503)
        return made
    def fail_read(bucket,key):
        nonlocal tripped
        if not tripped and ((stage=='asset-read' and key.endswith('.png')) or (stage=='page-read' and key.endswith('.json'))):
            tripped=True; raise Failure('UPSTREAM_UNAVAILABLE',503)
        return download(bucket,key)
    storage.create=fail_create; storage.download=fail_read
    with pytest.raises(Failure) as error:persist(live)
    assert error.value.persistence=='UNKNOWN'
    if stage.startswith('asset'):assert not any(k.endswith('.json') for k in storage.data)
    retained=dict(storage.data)
    assert persist(live)[1]['status']=='STORED'
    assert all(storage.data[k]==v for k,v in retained.items())


def test_existing_different_crop(live):
    b,p,_,_=live
    from bridge.validation import asset_key
    key=asset_key(p,p['items'][0]['assets'][0]['asset_id'])
    b.storage.data[key]=b'different'
    assert_failure('ASSET_CONFLICT',lambda:persist(live))
    assert b.storage.data=={key:b'different'}


def test_corrupt_readback_prevents_json(live):
    b,_,_,_=live; b.storage.corrupt=True
    assert_failure('PERSISTENCE_UNVERIFIED',lambda:persist(live))
    assert not any(k.endswith('.json') for k in b.storage.data)


def test_durable_set_rejects_altered_request_or_identity(live):
    b,p,_,_=live; b.storage.fail_create=True
    assert_failure('PERSISTENCE_UNVERIFIED',lambda:persist(live))
    p['page_notes']=['different request']
    assert_failure('IDEMPOTENCY_CONFLICT',lambda:persist(live))
    assert_failure('ASSET_SET_CONFLICT',lambda:persist(live,str(UUID(int=91))))
    assert not any(k.endswith('.json') for k in b.storage.data)


def test_source_change_before_json(live):
    b,_,_,_=live; create=b.storage.create
    def mutate(bucket,key,data,media_type='application/json'):
        result=create(bucket,key,data,media_type)
        b.db.rowdata['status']='PROCESSING'
        return result
    b.storage.create=mutate
    assert_failure('SOURCE_NOT_READY',lambda:persist(live))
    assert not any(k.endswith('.json') for k in b.storage.data)


def test_concurrent_set(live):
    with ThreadPoolExecutor(4) as pool:
        codes=list(pool.map(lambda n:persist(live,str(UUID(int=n)))[0],range(21,25)))
    assert sorted(codes)==[200,200,200,201]
    assert len(live[0].storage.data)==2


def test_null_submission_only(live):
    p=live[1]; page_schema(p,submission=True)
    assert_failure('PAGE_SCHEMA_INVALID',lambda:page_schema(p))


def test_generic_transport_v4(live):
    b,p,_,_=live
    app=Application(b,[{'id':'test','token':'x'*43,'scopes':['source:read','page:write'],'publications':['paper']}])
    raw=jcs(wrapper(p))
    headers={'Authorization':'Bearer '+'x'*43,'Content-Type':'application/json','Idempotency-Key':KEY,'Content-Length':str(len(raw))}
    code,receipt=app.dispatch('POST','/ingestor-v2/page',headers,lambda n:raw)
    assert code==201 and receipt['assets'][0]['verification']=='VERIFIED'
    serialized=json.dumps(receipt)
    assert all(secret not in serialized for secret in ['https://','token','Bearer','x'*43,'url'])


def test_encoder_preserves_palette_transparency():
    image=Image.new('P',(2,2)); image.putpalette([255,0,0]+[0]*765); image.info['transparency']=0
    assert png(canonical_png(image.convert('RGBA'))).getpixel((0,0))==(255,0,0,0)


def test_second_asset_failure_retains_first_and_retries(live):
    b,p,_,_=live
    second=copy.deepcopy(p['items'][0]['assets'][0]); second['asset_id']='second-chart'
    p['items'][0]['assets'].append(second)
    create=b.storage.create; seen=[]
    def fail_second(bucket,key,data,media_type='application/json'):
        seen.append(key)
        if key.endswith('second-chart.png') and seen.count(key)==1:raise Failure('UPSTREAM_UNAVAILABLE',503)
        return create(bucket,key,data,media_type)
    b.storage.create=fail_second
    assert_failure('PERSISTENCE_UNVERIFIED',lambda:persist(live))
    assert len(b.storage.data)==1 and not any(k.endswith('.json') for k in b.storage.data)
    assert persist(live)[0]==201 and len(b.storage.data)==3


@pytest.mark.parametrize('mode',['wrong-bucket','expected-metadata','too-many','bad-png','oversize'])
def test_rejects_before_writes(live,mode,monkeypatch):
    b,p,m,source=live; a=p['items'][0]['assets'][0]
    expected='ASSET_LIMIT_EXCEEDED'
    if mode=='wrong-bucket':b.output_bucket='other';expected='CONFIGURATION_MISSING'
    if mode=='expected-metadata':
        prepared=prepare_assets(copy.deepcopy(p),m,b.storage,'source','page-ingest')
        a['artifact']=prepared[0][0]['artifact'];a['artifact']['sha256']='d'*64
        expected='ASSET_ARTIFACT_MISMATCH'
    if mode=='too-many':
        for n in range(32):
            other=copy.deepcopy(a);other['asset_id']=f'chart-{n}';p['items'][0]['assets'].append(other)
    if mode=='bad-png':
        source['authoritative.png']=b'not png';h=digest(source['authoritative.png'])
        m['page_images'][0]['sha256']=h;a['page_anchor']['source_page_image_sha256']=h
        expected='SOURCE_PNG_INVALID'
    if mode=='oversize':monkeypatch.setattr('bridge.assets.MAX_PIXELS',99)
    assert_failure(expected,lambda:persist(live)); assert not b.storage.data


def test_empty_page_cannot_bypass_partial_asset_set(live):
    b,p,_,_=live;b.storage.fail_create=True
    assert_failure('PERSISTENCE_UNVERIFIED',lambda:persist(live))
    p['items'][0]['assets']=[]
    assert_failure('ASSET_SET_CONFLICT',lambda:persist(live,str(UUID(int=81))))
    assert not any(k.endswith('.json') for k in b.storage.data)


def test_uuid_identity_collision_rejected(live):
    b,_,_,_=live; persist(live)
    b.db.rowdata['id']=UUID(int=123)
    assert_failure('ASSET_SET_CONFLICT',lambda:persist(live,str(UUID(int=82))))


def test_storage_binary_content_type():
    import httpx
    from bridge.core import Storage
    captured=[]
    s=Storage('https://example.test','secret')
    s.client=httpx.Client(transport=httpx.MockTransport(lambda req:(captured.append(req) or httpx.Response(200))))
    assert s.create('page-ingest','key.png',b'png','image/png')
    assert captured[0].headers['content-type']=='image/png' and captured[0].headers['x-upsert']=='false'


def test_storage_stream_is_bounded():
    import httpx
    from bridge.core import Storage
    s=Storage('https://example.test','secret')
    s.client=httpx.Client(transport=httpx.MockTransport(lambda req:httpx.Response(200,content=b'12345')))
    assert_failure('ASSET_LIMIT_EXCEEDED',lambda:s.download_bounded('b','k',4))
