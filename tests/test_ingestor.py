import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import fitz
import pytest

from business_brief.ingestor import IngestorError, extract_physical_map
from business_brief.ingestor_worker import archive_key, build_archived_map


@pytest.fixture
def bundle(tmp_path):
    pdf = tmp_path / 'prepared.pdf'
    with fitz.open() as doc:
        page = doc.new_page()
        page.insert_text((72,72), 'Alpha')
        page.insert_text((72,100), 'Beta')
        page.insert_text((135,72), 'Gamma')
        doc.save(pdf)
    data = pdf.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    manifest = {'schema_version':'source-bundle-v4','status':'READY_FOR_INGESTOR',
                'source_id':f'sha256:{sha}', 'source_sha256':sha, 'page_count':1,
                'prepared_pdf_path':'edition/prepared.pdf', 'ocr':{'prepared_sha256':sha},
                'page_images':[{'page_no':1}]}
    file = tmp_path / 'manifest.json'
    file.write_text(json.dumps(manifest))
    return pdf, file, manifest


def test_repeatability_and_physical_relations(bundle):
    pdf, file, manifest = bundle
    a = extract_physical_map(file, pdf_path=pdf, source_id='db-source-uuid').to_dict()
    assert a == extract_physical_map(file, pdf_path=pdf, source_id='db-source-uuid').to_dict()
    assert a['source_id'] == 'db-source-uuid'
    assert a['source_sha256'] == manifest['source_sha256']
    blocks = {b['text']:b for b in a['pages'][0]['blocks']}
    assert set(blocks) == {'Alpha','Beta','Gamma'}
    assert any(r['relation']=='below' and r['source_block_id']==blocks['Alpha']['block_id']
               and r['target_block_id']==blocks['Beta']['block_id'] for r in a['pages'][0]['relations'])
    assert all(k not in b for b in blocks.values() for k in ('headline','article','relevance'))


@pytest.mark.parametrize('change', ['hash','pages','schema','status'])
def test_reject_invalid_bundle(bundle, change):
    pdf, file, manifest = bundle
    if change=='hash': manifest['ocr']['prepared_sha256']='0'*64
    if change=='pages': manifest['page_count']=2
    if change=='schema': manifest['schema_version']='source-bundle-v2'
    if change=='status': manifest['status']='FAILED'
    file.write_text(json.dumps(manifest))
    with pytest.raises(IngestorError): extract_physical_map(file, pdf_path=pdf)


@pytest.mark.parametrize('key', ['/tmp/a.pdf','edition/../a.pdf','edition\\a.pdf',''])
def test_reject_unsafe_archive_keys(key):
    with pytest.raises(IngestorError): archive_key(key)


def test_archive_adapter_uses_verified_bytes_and_db_identity(bundle, tmp_path):
    pdf, file, manifest = bundle
    objects = {'edition/manifest.json':file.read_bytes(), 'edition/prepared.pdf':pdf.read_bytes()}
    bucket = SimpleNamespace(download=lambda key:objects[key])
    archive = SimpleNamespace(archive='source-archive',client=SimpleNamespace(storage=SimpleNamespace(from_=lambda _:bucket)))
    source = {'id':'db-uuid', 'status':'READY_FOR_INGESTOR', 'source_bundle_path':'edition/manifest.json','page_count':1}
    blob = {'sha256':manifest['source_sha256']}
    result = build_archived_map(archive, source, blob, tmp_path)
    assert result['source_id']=='db-uuid'
    objects['edition/prepared.pdf']=b'corrupted'
    with pytest.raises(IngestorError, match='hash'): build_archived_map(archive, source, blob, tmp_path)


def test_reject_artifact_outside_bundle():
    with pytest.raises(IngestorError): archive_key('other/file.pdf','edition/')


@pytest.mark.parametrize('failure', [None, 'upload', 'finalize'])
@pytest.mark.parametrize('verify_repeat', [False, True])
def test_upload_must_succeed_before_finalize(monkeypatch, failure, verify_repeat):
    from business_brief import ingestor_worker as worker
    calls = []
    source = {'id':'db-uuid', 'blob_id':'blob'}
    class Query:
        def __init__(self, data): self.data = data
        def select(self, *_): return self
        def eq(self, *_): return self
        def single(self): return self
        def insert(self, *_): return self
        def execute(self): return SimpleNamespace(data=self.data)
    class DB:
        def table(self, name): return Query(source if name=='sources' else {})
        def rpc(self, name, args):
            calls.append(('finalize', args))
            if failure=='finalize': raise RuntimeError('lost lease')
            return Query(None)
    class Archive:
        client = DB()
        def upload_file(self, local, key, mime):
            calls.append(('upload', key))
            assert hashlib.sha256(local.read_bytes()).hexdigest() in key
            if failure=='upload': raise RuntimeError('storage unavailable')
    monkeypatch.setattr(worker, 'build_archived_map', lambda *_: {'pages':[
        {'blocks':[{'text':'exact text'}]}]})
    task = {'id':'job','source_id':'db-uuid','lease_token':'token'}
    if failure:
        with pytest.raises(RuntimeError): worker.process_job(Archive(),task,verify_repeat=verify_repeat)
    else:
        result = worker.process_job(Archive(),task,verify_repeat=verify_repeat)
        assert result['block_count']==1
        assert result.get('repeatability_verified',False)==verify_repeat
    assert [c[0] for c in calls] == (['upload'] if failure=='upload' else ['upload','finalize'])
    if failure!='upload':
        assert calls[-1][1]['p_lease_token']=='token'
