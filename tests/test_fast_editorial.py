import copy
import json
from io import BytesIO
from urllib.error import HTTPError

import pytest

from business_brief.fast_editorial import (EditorialError,ResponsesProvider,neutral_page,
    validate_page,freeze_issue,PAGE_SCHEMA)
from business_brief.fast_editorial_worker import checked_download


@pytest.fixture
def sample():
    page = {'page_no':1,'width':100,'height':100,
            'blocks':[{'block_id':'b1','text':'Acme reports profits','bbox':[0,0,90,10],
                       'fonts':[],'source_order':9}], 'relations':[{'relation':'below'}]}
    item = {'local_id':'a','headline_original':'Acme reports profits','summary_cs':'Výsledky Acme.',
            'author_angle_cs':'Vývoj zisků.','new_information_cs':'Výsledky za čtvrtletí.',
            'object_type':'article','evidence':[{'block_id':'b1','quote':'Acme reports profits'}],
            'continuation_note':'','uncertainties':[]}
    result = {'page_no':1,'page_note_cs':'Jedna zpráva.','needs_review':False,'items':[item]}
    group = {'fragment_ids':['p0001:a'],'headline_original':item['headline_original'],
             'summary_cs':item['summary_cs'],'author_angle_cs':item['author_angle_cs'],
             'new_information_cs':item['new_information_cs'],'priority':'candidate',
             'importance_reason_cs':'Firemní výsledky.','reading_value_reason_cs':'Rozbor marží.',
             'deep_read_reason_cs':'Ověřit čísla.','uncertainties':[]}
    return page,result,{'edition_note_cs':'Vydání s firemní zprávou.','items':[group]}


def test_no_physical_hints_leak_into_discovery(sample):
    data = neutral_page(sample[0])
    assert 'relations' not in data
    assert 'source_order' not in data['blocks'][0]
    assert data['blocks'][0]['text']=='Acme reports profits'


@pytest.mark.parametrize('fault',['quote','block','no_evidence','duplicate','wrong_page','review'])
def test_reject_unsupported_discovery_evidence(sample,fault):
    page,result,_=copy.deepcopy(sample)
    if fault=='quote': result['items'][0]['evidence'][0]['quote']='invented profits'
    if fault=='block': result['items'][0]['evidence'][0]['block_id']='b999'
    if fault=='no_evidence': result['items'][0]['evidence']=[]
    if fault=='duplicate': result['items'].append(copy.deepcopy(result['items'][0]))
    if fault=='wrong_page': result['page_no']=2
    if fault=='review': result['needs_review']=True
    with pytest.raises(EditorialError): validate_page(result,page)


@pytest.mark.parametrize('refs',[[],['p0001:a','p0001:a'],['p0009:a']])
def test_no_omitted_duplicated_or_foreign_fragments(sample,refs):
    page,result,synthesis=sample
    synthesis['items'][0]['fragment_ids']=refs
    with pytest.raises(EditorialError): freeze_issue('uuid','sha',[page],{1:result},synthesis)


def test_freeze_is_provisional_and_preserves_references(sample):
    page,result,synthesis=sample
    out=freeze_issue('uuid','sha',[page],{1:result},synthesis)
    assert out['provisional'] is True
    assert out['items'][0]['page_refs']==[1]
    assert out['items'][0]['canonical_match_status']=='not_checked'
    assert out['items'][0]['deep_read_status']=='not_started'
    with pytest.raises(EditorialError): freeze_issue('uuid','sha',[page],{},synthesis)


def test_corrupt_storage_input_is_rejected():
    class Bucket:
        def download(self,_): return b'bad'
    with pytest.raises(EditorialError): checked_download(Bucket(),'safe/file','0'*64)


def test_provider_uses_strict_schema_and_no_secret_output(monkeypatch):
    from business_brief import fast_editorial as mod
    def urlopen(req,timeout):
        body=json.loads(req.data)
        assert body['store'] is False
        assert body['text']['format']['strict'] is True
        assert body['input'][0]['content'][1]['image_url'].startswith('data:image/png;base64,')
        return BytesIO(json.dumps({'id':'r','status':'completed','model':'test-model',
            'output':[{'content':[{'type':'output_text','text':'{"ok":true}'}]}],
            'usage':{'input_tokens':12}}).encode())
    monkeypatch.setattr(mod.request,'urlopen',urlopen)
    result=ResponsesProvider('test-model','secret').generate('prompt',{},PAGE_SCHEMA,image=b'image')
    assert result['usage']['input_tokens']==12
    assert 'secret' not in json.dumps(result)


@pytest.mark.parametrize('status',['incomplete','failed','completed'])
def test_incomplete_or_refused_response_is_not_accepted(monkeypatch,status):
    from business_brief import fast_editorial as mod
    monkeypatch.setattr(mod.request,'urlopen',lambda *a,**k:BytesIO(json.dumps({'status':status,'output':[]}).encode()))
    with pytest.raises(EditorialError): ResponsesProvider('test','secret').generate('',{},PAGE_SCHEMA)


def test_api_error_does_not_leak_response_body(monkeypatch):
    from business_brief import fast_editorial as mod
    def fail(*args,**kwargs):
        raise HTTPError('https://api.openai.com/v1/responses',401,'private message',{},None)
    monkeypatch.setattr(mod.request,'urlopen',fail)
    with pytest.raises(EditorialError,match='HTTP 401') as caught:
        ResponsesProvider('test','secret').generate('',{},PAGE_SCHEMA)
    assert 'private message' not in str(caught.value)
