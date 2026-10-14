import json
from pathlib import Path
import pymupdf as fitz
import pytest
from business_brief.technician import TechnicianError, bundle_from_manifest, prepare_pdf, sha256_file
from business_brief.technician_evidence import check_text_layers
from business_brief.storage import SupabaseArchive


def scan(path, *, overlay=False, rotation=0, cropped=False):
    with fitz.open() as picture:
        p=picture.new_page(width=300,height=450)
        p.insert_text((20,60),'Financial Times 14 October 2026',fontsize=12)
        p.insert_text((20,90),'Business and economic news for OCR verification.',fontsize=10)
        payload=p.get_pixmap(matrix=fitz.Matrix(2,2)).tobytes('png')
    with fitz.open() as pdf:
        p=pdf.new_page(width=300,height=450);p.insert_image(p.rect,stream=payload)
        if overlay:p.draw_rect(fitz.Rect(30,30,100,100),color=(1,0,0))
        if cropped:p.set_cropbox(fitz.Rect(10,10,290,440))
        p.set_rotation(rotation);pdf.save(path)
    return payload


def native(path,text='Financial Times\n14 October 2026\nNative text is available for this test.'):
    with fitz.open() as d:
        d.new_page().insert_text((72,72),text);d.save(path)


def prepare(path,tmp,**kw):
    return prepare_pdf(path,workspace=tmp/'work',publication='Financial Times',edition_date='2026-10-14',ocr_mode='never',**kw)


def test_original_image_and_previews(tmp_path):
    src=tmp_path/'scan.pdf';payload=scan(src);b=prepare(src,tmp_path);image=b.page_images[0]
    assert image.acquisition_method=='embedded_original'
    assert (image.width_px,image.height_px)==(600,900)
    assert Path(image.path).read_bytes()==payload
    assert b.previews[0].width_px==360
    for p in (*b.previews,b.contact_sheet):assert sha256_file(Path(p.path))==p.sha256
    assert b.ocr.page_checks[0].status=='LOW_TEXT_REVIEW'
    assert b.ocr.pages_needing_review==(1,)
    assert b.status=='READY_FOR_INGESTOR'


@pytest.mark.parametrize('kw',[{'overlay':True},{'rotation':90},{'cropped':True}])
def test_nontrivial_page_is_rendered(tmp_path,kw):
    src=tmp_path/'scan.pdf';scan(src,**kw)
    assert prepare(src,tmp_path).page_images[0].acquisition_method=='render'


def test_render_mode_and_pixel_budget(tmp_path):
    src=tmp_path/'scan.pdf';scan(src)
    p=prepare(src,tmp_path,image_mode='render',dpi=300,max_render_pixels=100_000).page_images[0]
    assert p.width_px*p.height_px<102_000 and p.effective_dpi<300


def test_clipped_full_page_image_is_rendered(tmp_path):
    src=tmp_path/'scan.pdf';scan(src)
    with fitz.open(src) as doc:
        xref=doc[0].get_contents()[0]
        data=doc.xref_stream(xref)
        doc.update_stream(xref,b'q 0 0 100 100 re W n\n'+data+b'\nQ')
        doc.save(tmp_path/'clipped.pdf')
    assert prepare(tmp_path/'clipped.pdf',tmp_path).page_images[0].acquisition_method=='render'


def test_cache_configuration_and_identity_overrides(tmp_path):
    src=tmp_path/'native.pdf';native(src)
    a=prepare(src,tmp_path,dpi=72);same=prepare(src,tmp_path,dpi=72)
    higher=prepare(src,tmp_path,dpi=144);thumb=prepare(src,tmp_path,dpi=72,preview_width=200)
    identity=prepare_pdf(src,workspace=tmp_path/'work',publication='Example Daily',edition_date='2026-10-14',ocr_mode='never',dpi=72)
    assert a.bundle_id==same.bundle_id
    assert len({x.bundle_id for x in (a,higher,thumb,identity)})==4
    assert a.source_sha256==higher.source_sha256
    assert a.configuration['tool_versions']==a.tool_versions
    assert a.timings_seconds['total']>0
    assert '.staging' not in json.dumps(a.to_dict())


def test_corrupt_cache_rejected(tmp_path):
    src=tmp_path/'native.pdf';native(src);b=prepare(src,tmp_path)
    Path(b.previews[0].path).write_bytes(b'corrupt')
    with pytest.raises(TechnicianError,match='Cached artifact'):prepare(src,tmp_path)


@pytest.mark.parametrize('options',[{'ocr_languages':'eng+deu'}, {'min_native_chars_per_page':200}, {'max_pages_per_part':1}])
def test_other_preparation_options_invalidate_cache(tmp_path,options):
    src=tmp_path/'native.pdf';native(src)
    a=prepare(src,tmp_path);b=prepare(src,tmp_path,**options)
    assert a.configuration_sha256!=b.configuration_sha256


@pytest.mark.parametrize('kw',[{'dpi':0},{'preview_width':-1},{'ocr_jobs':0},{'min_native_chars_per_page':0}])
def test_invalid_configuration(tmp_path,kw):
    src=tmp_path/'native.pdf';native(src)
    with pytest.raises(TechnicianError):prepare(src,tmp_path,**kw)


def test_text_loss_and_blank_review(tmp_path):
    src=tmp_path/'native.pdf';native(src);blank=tmp_path/'blank.pdf'
    with fitz.open() as empty:empty.new_page();empty.save(blank)
    assert check_text_layers(src,blank,[100],min_chars=30,ocr_pages=(1,))[0].status=='TEXT_LAYER_LOST'
    assert check_text_layers(blank,blank,[0],min_chars=30,ocr_pages=(1,))[0].status=='OCR_NO_TEXT_REVIEW'


def test_bad_geometry_blocks_manifest(tmp_path,monkeypatch):
    from business_brief import technician
    src=tmp_path/'scan.pdf';scan(src)
    def broken(src,dst,*args,**kwargs):
        dst.parent.mkdir(parents=True,exist_ok=True)
        with fitz.open() as d:d.new_page(width=100,height=100);d.save(dst)
    monkeypatch.setattr(technician,'_ocr',broken)
    with pytest.raises(TechnicianError,match='failed validation'):
        prepare_pdf(src,workspace=tmp_path/'work',publication='Financial Times',edition_date='2026-10-14')
    assert not list((tmp_path/'work'/'sources').rglob('manifest.json'))


def test_auto_ocr_does_not_skip_sparse_existing_text(tmp_path,monkeypatch):
    from business_brief import technician
    src=tmp_path/'sparse.pdf';native(src,text='Label');seen=[]
    monkeypatch.setattr(technician.shutil,'which',lambda x:'/bin/ocrmypdf')
    class Run:returncode=0;stderr='';stdout=''
    monkeypatch.setattr(technician.subprocess,'run',lambda cmd,**kw:seen.append(cmd) or Run())
    technician._ocr(src,tmp_path/'out.pdf','auto','eng','ocrmypdf',pages=(1,),jobs=2)
    assert '--force-ocr' in seen[0] and '--skip-text' not in seen[0]
    assert seen[0][seen[0].index('--pages')+1]=='1'


def test_archive_paths_and_jpeg_mime(tmp_path):
    src=tmp_path/'scan.pdf';scan(src);b=prepare(src,tmp_path)
    class Archive(SupabaseArchive):
        def __init__(self):self.items=[]
        def upload_file(self,local,remote,content_type):
            self.items.append((remote,content_type))
            if remote.endswith('/manifest.json'):self.manifest=json.loads(local.read_text())
    a=Archive();a.upload_bundle(Path(b.original_path).parent,'ft/test')
    assert str(tmp_path) not in json.dumps(a.manifest)
    assert a.manifest['contact_sheet']['path']=='ft/test/previews/contact-sheet.jpg'
    assert a.manifest['previews'][0]['path'].startswith('ft/test/previews/')
    assert any(mime=='image/jpeg' for _,mime in a.items)
    assert a.items[-1][0]=='ft/test/manifest.json'


def test_manifest_roundtrip_and_legacy(tmp_path):
    src=tmp_path/'native.pdf';native(src);b=prepare(src,tmp_path)
    assert bundle_from_manifest(json.loads(json.dumps(b.to_dict())))==b
    old=b.to_dict()
    for k in ['configuration','configuration_sha256','tool_versions','timings_seconds','previews','contact_sheet','bundle_id']:old.pop(k)
    old['ocr'].pop('page_checks');old['ocr'].pop('pages_needing_review')
    old['page_images'][0].pop('acquisition_method');old['page_images'][0].pop('effective_dpi')
    restored=bundle_from_manifest(old)
    assert restored.previews==() and restored.configuration_sha256==''


def test_masthead_beats_later_citation_of_another_paper(tmp_path):
    src=tmp_path/'transport.pdf'
    native(src,text='Financial Times\n14 October 2026\nThe Wall Street Journal has reported another story.')
    b=prepare_pdf(src,workspace=tmp_path/'work',ocr_mode='never')
    assert b.identity.publication_id=='financial-times'
    assert b.identity.edition_date=='2026-10-14'


def test_worker_rechecks_configuration_before_reusing_duplicate(tmp_path,monkeypatch):
    from contextlib import nullcontext
    from business_brief import technician_worker as worker
    src=tmp_path/'native.pdf';native(src)
    class Archive:
        client=None
        deleted=False
        def inbox_version(self,key):return 'v1'
        def download_inbox(self,key,target):target.write_bytes(src.read_bytes());return target
        def bundle_configuration_matches(self,*args):return False
        def remove_inbox(self,key):self.deleted=True
    archive=Archive()
    class Repo:
        def __init__(self,*args):pass
        def register_arrival(self,*args):return {'id':'arrival','received_at':'2026-10-14T00:00:00Z'}
        def blob_by_sha(self,*args):return {'id':'blob'}
        def source_for_blob(self,*args):return {'id':'source','status':'READY_FOR_INGESTOR'}
        def mark_duplicate(self,*args):raise AssertionError('Changed config must not be reused')
    class Log:
        def __init__(self,*args):pass
        def emit(self,*args,**kw):pass
        def timed(self,*args,**kw):return nullcontext()
    monkeypatch.setattr(worker.SupabaseArchive,'from_env',lambda:archive)
    monkeypatch.setattr(worker,'TechnicianRepository',Repo)
    monkeypatch.setattr(worker,'EventLogger',Log)
    def reprepare(*args,**kw):raise RuntimeError('preparation selected')
    monkeypatch.setattr(worker,'prepare_pdf',reprepare)
    with pytest.raises(RuntimeError,match='preparation selected'):
        worker.process_inbox_object('input.pdf',object_version='v1')
    assert not archive.deleted


def test_archive_verification_checks_preview_hash(tmp_path):
    import hashlib
    from business_brief.storage import StorageError
    src=tmp_path/'scan.pdf';scan(src);b=prepare(src,tmp_path)
    class Client:
        def __init__(self):self.objects={}
        @property
        def storage(self):return self
        def from_(self,*args):return self
        def download(self,key):return self.objects[key]
    c=Client()
    class Archive(SupabaseArchive):
        def upload_file(self,local,remote,content_type):c.objects[remote]=local.read_bytes()
    a=Archive(c);a.upload_bundle(Path(b.original_path).parent,'ft/test')
    source={'source_bundle_path':'ft/test/manifest.json'}
    a.verify_archived_source(source,b.source_sha256)
    assert a.bundle_configuration_matches(source,b.configuration_sha256)
    assert not a.bundle_configuration_matches(source,'different')
    c.objects['ft/test/previews/page-0001.jpg']=b'corrupt'
    with pytest.raises(StorageError,match='hash mismatch'):
        a.verify_archived_source(source,b.source_sha256)
