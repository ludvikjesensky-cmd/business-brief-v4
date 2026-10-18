"""v4 contract isolation and fail-closed persistence; no production I/O."""
import copy
from uuid import UUID

import pytest
from test_bridge import (page, page_v3, bridge, wrapper, KEY, SHA, SID,
                         assert_failure)
from bridge.validation import asset_key, page_schema, verification
from business_brief.contracts import (
    ArticleAsset, AssetPageAnchor, AssetTextAnchor, AssetArtifact,
    AssetVerification, PageItemV4, PageIngestV4, RelevanceAssessment,
    ContinuationEvidence, Verification,
)


@pytest.fixture
def page_v4(page_v3):
    p = copy.deepcopy(page_v3)
    p.update(schema_version='page-ingest-v4', producer='ingestor-v2.2-chat', instruction_version='2.2')
    p['items'][0]['assets'] = []
    return p


@pytest.fixture
def asset_page(page_v4):
    p = page_v4
    asset = ArticleAsset(
        'p0001-i1-chart-01', 'chart', 'p1-i1', 1,
        AssetPageAnchor((0.1, 0.2, 0.5, 0.6), 'b'*64, (10, 20, 50, 60)),
        AssetTextAnchor('after_paragraph', 0, 'Synthetic text', 'anchored'),
        AssetArtifact('page-ingest', asset_key(p, 'p0001-i1-chart-01'), 'image/png', 'd'*64, 123, 40, 40),
        AssetVerification('VERIFIED', True, True, True, True),
    )
    p['items'][0]['assets'] = [asset.to_dict()]
    return p


def test_v4_serialization(asset_page):
    a = asset_page['items'][0]['assets'][0]
    asset = ArticleAsset(a['asset_id'], a['asset_type'], a['page_item_id'], a['page_no'],
                         AssetPageAnchor((0.1, 0.2, 0.5, 0.6), 'b'*64, (10,20,50,60)),
                         AssetTextAnchor('after_paragraph', 0, 'Synthetic text', 'anchored'),
                         AssetArtifact(**a['artifact']), AssetVerification('VERIFIED', True, True, True, True))
    item = PageItemV4('p1-i1', 'article', 'Title', None, None, None, 'Synthetic text',
                      RelevanceAssessment('relevant', 'Synthetic reason'),
                      ContinuationEvidence(True,False,False),
                      Verification('VERIFIED',True,True,True,None,True,True,True), (asset,))
    serialized = PageIngestV4(SID,SHA,'paper','Paper','2026-10-14','default',1,(item,),'VERIFIED').to_dict()
    assert serialized == asset_page
    page_schema(serialized); verification(serialized)


@pytest.mark.parametrize('value', [
    [-0.1,0,1,1], [0,0,1.1,1], [0.5,0,0.1,1], [0,0,0,1],
    [0,1,1,0], [False,0,1,1], [0,0,float('nan'),1], [0,0,float('inf'),1], [0,1],
])
def test_bbox_bounds(asset_page, value):
    asset_page['items'][0]['assets'][0]['page_anchor']['bbox_norm'] = value
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(asset_page))


@pytest.mark.parametrize('field,value', [
    ('asset_id','../escape'), ('asset_type','ocr'), ('page_no',2), ('page_no',True),
    ('page_item_id','another-article'), ('artifact.key','other/crop.png'),
    ('artifact.media_type','text/plain'), ('artifact.width',41), ('artifact.sha256','bad'),
    ('page_anchor.bbox_px',[0,0,False,1]),
    ('text_anchor.position','best_guess'), ('text_anchor.paragraph_index',True),
    ('text_anchor.paragraph_index',1), ('text_anchor.anchor_text','Missing text'),
    ('text_anchor.anchor_text',None), ('text_anchor.anchor_text',''),
])
def test_asset_schema(asset_page, field, value):
    obj=asset_page['items'][0]['assets'][0]; keys=field.split('.')
    for key in keys[:-1]: obj=obj[key]
    obj[keys[-1]]=value
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(asset_page))


def test_duplicate_asset_rejected(asset_page):
    asset_page['items'][0]['assets'] *= 2
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(asset_page))


@pytest.mark.parametrize('field', ['visual_checked','ownership_verified','page_anchor_verified','text_anchor_verified'])
def test_asset_required_checks(asset_page, field):
    asset_page['items'][0]['assets'][0]['verification'][field] = False
    assert_failure('PAGE_VERIFICATION_INVALID', lambda: verification(asset_page))


def test_ambiguous_anchor_requires_explicit_review(asset_page):
    i=asset_page['items'][0]; a=i['assets'][0]
    i['text_on_page']='Synthetic text\n\nSynthetic text'
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(asset_page))
    a['text_anchor'].update(status='placement_needs_review', paragraph_index=None)
    a['verification'].update(status='NEEDS_REVIEW', text_anchor_verified=False, notes=['Ambiguous anchor'])
    page_schema(asset_page)
    assert_failure('PAGE_VERIFICATION_INVALID', lambda: verification(asset_page))
    i['verification'].update(status='NEEDS_REVIEW', notes=['Unplaced chart'])
    asset_page.update(page_status='NEEDS_REVIEW', page_notes=['Placement review'])
    verification(asset_page)
    a['text_anchor']['anchor_text']=None
    page_schema(asset_page); verification(asset_page)


def test_anchor_text_is_authority_index_optional(asset_page):
    a=asset_page['items'][0]['assets'][0]
    a['text_anchor']['paragraph_index']=None
    a['page_anchor']['bbox_px']=None
    for position in ['before_paragraph','after_paragraph','inline_after_anchor']:
        a['text_anchor']['position']=position
        page_schema(asset_page); verification(asset_page)


def test_asset_paths_are_generation_and_source_bound(asset_page):
    a=asset_page['items'][0]['assets'][0]
    assert asset_key(asset_page,a['asset_id']) == f'page-ingest/paper/2026-10-14/{SHA}/ingestor-v2.2/assets/page-0001/p0001-i1-chart-01.png'
    asset_page['source']['source_sha256']='e'*64
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(asset_page))
    for bad in ['../escape','x/y','a.png','%2e%2e','A','a\\b']:
        assert_failure('PAGE_SCHEMA_INVALID', lambda: asset_key(asset_page,bad))


def test_v2_v3_v4_isolated(bridge, page, page_v3, page_v4):
    # Fixtures share input; reconstruct v2 from the v3 copy.
    from business_brief.contracts import PerspectiveEvidence
    v2=copy.deepcopy(page_v3)
    v2.update(schema_version='page-ingest-v2',producer='ingestor-v2.0-chat',instruction_version='2.0')
    v2['items'][0]['perspective']=PerspectiveEvidence().to_dict()
    pages=[v2,page_v3,page_v4]; original={}
    for n,p in enumerate(pages,20):
        page_schema(p); verification(p)
        _,receipt=bridge.post(wrapper(p),str(UUID(int=n)),'test',['paper'])
        key=receipt['artifact']['storage_key']
        assert f'/ingestor-v2.{n-20}/' in key
        assert all(bridge.storage.data[k]==v for k,v in original.items())
        original=dict(bridge.storage.data)
        assert bridge.post(wrapper(p),str(UUID(int=n)),'test',['paper'])[0]==200
    assert len(original)==3
    assert_failure('IDEMPOTENCY_CONFLICT', lambda: bridge.post(wrapper(page_v4),str(UUID(int=20)),'test',['paper']))
    page_v4['page_notes']=['Changed']
    assert_failure('CANONICAL_CONFLICT', lambda: bridge.post(wrapper(page_v4),str(UUID(int=40)),'test',['paper']))
    for p in pages[:2]:
        p['items'][0]['assets']=[]
        assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(p))


@pytest.mark.parametrize('field,value', [('producer','ingestor-v2.1-chat'),('instruction_version','2.1')])
def test_v4_mixed_generation(page_v4, field, value):
    page_v4[field]=value
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(page_v4))


def test_v4_requires_assets_array_rejects_perspective(page_v4):
    del page_v4['items'][0]['assets']
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(page_v4))
    page_v4['items'][0]['assets']=[]
    page_v4['items'][0]['perspective']={}
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(page_v4))


def test_no_unverified_asset_reference_persist(bridge, asset_page):
    page_schema(asset_page); verification(asset_page)
    assert_failure('CONFIGURATION_MISSING', lambda: bridge.post(wrapper(asset_page),KEY,'test',['paper']))
    assert not bridge.storage.data and not bridge.db.bindings


@pytest.mark.parametrize('kind', ['chart','table','photo','infographic','illustration','other'])
def test_all_visual_types(asset_page, kind):
    asset_page['items'][0]['assets'][0]['asset_type']=kind
    page_schema(asset_page); verification(asset_page)


@pytest.mark.parametrize('part', ['', 'page_anchor', 'text_anchor', 'artifact', 'verification'])
def test_exact_asset_fields(asset_page, part):
    a=asset_page['items'][0]['assets'][0]
    obj=a[part] if part else a
    obj['unexpected']=None
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(asset_page))
    del obj['unexpected']
    del obj[next(iter(obj))]
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(asset_page))


@pytest.mark.parametrize('text,anchor', [('aaaa','aaa'),('one\n\ntwo','one\n\ntwo')])
def test_overlapping_or_cross_paragraph_anchor(asset_page, text, anchor):
    i=asset_page['items'][0]; i['text_on_page']=text
    i['assets'][0]['text_anchor'].update(anchor_text=anchor,paragraph_index=None)
    assert_failure('PAGE_SCHEMA_INVALID', lambda: page_schema(asset_page))


def test_blocked_asset_prevents_page_write(bridge, asset_page):
    asset_page['items'][0]['assets'][0]['verification'].update(status='BLOCKED',notes=['Source unavailable'])
    assert_failure('PAGE_BLOCKED', lambda: bridge.post(wrapper(asset_page),KEY,'test',['paper']))
    assert not bridge.storage.data and not bridge.db.bindings
