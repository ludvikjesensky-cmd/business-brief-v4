import pytest
from business_brief.article_blocks import assemble,digest,VERSION

def fixture():
    data={'version':VERSION,'pdf_sha256':'pdf','page_no':2,'lines':[
      {'id':'L1','text':'Title','bbox':[0,0,10,1]},
      {'id':'L2','text':'An invest-','bbox':[0,2,10,3]},
      {'id':'L3','text':'ment and a son-in-','bbox':[0,4,10,5]},
      {'id':'L4','text':'law.','bbox':[0,6,10,7]},
      {'id':'L5','text':'Advertisement','bbox':[20,0,30,1]}]}
    data['page_digest']=digest(data)
    plan={'version':VERSION,'page_digest':data['page_digest'],'articles':[
      {'id':'a','title_ids':['L1'],'paragraphs':[['L2','L3','L4']]}],
      'excluded':[{'ids':['L5'],'reason':'advertisement'}],
      'hyphenation':{'L2':'remove','L3':'keep'}}
    return data,plan

def test_reviewed_hyphens_preserve_content_and_exclude_ad():
    data,plan=fixture();articles,audit=assemble(data,plan)
    assert articles==[{'title':'Title','text':'An investment and a son-in-law.'}]
    assert not audit['needs_review']

@pytest.mark.parametrize('mutation',['source','binding','unknown','duplicate','unused_join'])
def test_corruption_and_wrong_ownership_rejected(mutation):
    data,plan=fixture()
    if mutation=='source':data['lines'][1]['text']='invented text'
    if mutation=='binding':plan['page_digest']='different page'
    if mutation=='unknown':plan['articles'][0]['paragraphs'][0].append('missing')
    if mutation=='duplicate':plan['excluded'][0]['ids'].append('L2')
    if mutation=='unused_join':plan['hyphenation']['L1']='remove'
    with pytest.raises(ValueError):assemble(data,plan)

def test_unreviewed_hyphen_keeps_original_and_marks_review():
    data,plan=fixture();plan['hyphenation']={}
    articles,audit=assemble(data,plan)
    assert 'invest-\nment' in articles[0]['text']
    assert audit['needs_review']
    assert len(audit['warnings'])==2


def test_drop_cap_and_title_spacing_are_explicit_character_preserving_edits():
    data,plan=fixture()
    data['lines'][0]['text']='FactoryFloor'
    data['lines'][1]['text']='S'
    data['lines'][2]['text']='ome economic shocks.'
    data['page_digest']=digest({k:v for k,v in data.items() if k!='page_digest'})
    plan['page_digest']=data['page_digest']
    plan['articles'][0]['title_text']='Factory Floor'
    plan['articles'][0]['paragraphs']=[['L2','L3'],['L4']]
    plan['hyphenation']={};plan['no_space_after']=['L2']
    articles,audit=assemble(data,plan)
    assert articles[0]=={'title':'Factory Floor','text':'Some economic shocks.\n\nlaw.'}
    plan['articles'][0]['title_text']='Invented Floor'
    with pytest.raises(ValueError,match='source characters'):assemble(data,plan)


def test_missing_source_ids_are_visible_and_empty_plan_is_rejected():
    data,plan=fixture();plan['excluded']=[]
    _,audit=assemble(data,plan)
    assert audit['unassigned_ids']==['L5'] and audit['needs_review']
    plan['articles']=[]
    with pytest.raises(ValueError,match='no articles'):assemble(data,plan)


def test_prepare_and_assemble_real_pdf_with_source_binding(tmp_path):
    import fitz
    from business_brief.article_blocks import prepare,load
    pdf=tmp_path/'source.pdf'
    with fitz.open() as doc:
        page=doc.new_page();page.insert_text((40,40),'Headline')
        page.insert_text((40,100),'Actual source sentence.');doc.save(pdf)
    prepare(pdf,1,tmp_path/'prepared')
    data=load(tmp_path/'prepared/blocks.json')
    ids={line['text']:line['id'] for line in data['lines']}
    plan={'version':VERSION,'page_digest':data['page_digest'],'articles':[
      {'id':'a','title_ids':[ids['Headline']],'paragraphs':[[ids['Actual source sentence.']]]}],
      'excluded':[],'hyphenation':{}}
    articles,audit=assemble(data,plan)
    assert articles==[{'title':'Headline','text':'Actual source sentence.'}]
    assert audit['accounted_lines']==2 and not audit['needs_review']
