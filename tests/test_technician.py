from pathlib import Path
import fitz
from business_brief.technician import prepare_pdf, sha256_file

def make_pdf(path:Path,title="Nikkei Asia",date="8 October 2026",pages=2):
    d=fitz.open();d.set_metadata({"title":title})
    try:
        for i in range(pages):
            p=d.new_page();p.insert_text((72,72),f"{title}\n{date}\nEnough native text for the Technician test page {i+1}.")
        d.save(path)
    finally:d.close()

def test_unknown_title_and_date(tmp_path):
    src=tmp_path/"download-17.pdf";make_pdf(src)
    b=prepare_pdf(src,workspace=tmp_path/"work",dpi=72)
    assert b.identity.publication_id=="nikkei-asia"
    assert b.identity.edition_date=="2026-10-08"
    assert b.status=="READY_FOR_INGESTOR"

def test_same_bytes_different_name_are_same_source(tmp_path):
    a=tmp_path/"a.pdf";b=tmp_path/"renamed.pdf";make_pdf(a);b.write_bytes(a.read_bytes())
    x=prepare_pdf(a,workspace=tmp_path/"work",dpi=72);y=prepare_pdf(b,workspace=tmp_path/"work",dpi=72)
    assert x.source_sha256==y.source_sha256
    assert x.original_path==y.original_path
    assert sha256_file(Path(x.original_path))==x.source_sha256

def test_mechanical_split(tmp_path):
    src=tmp_path/"paper.pdf";make_pdf(src,title="Example Daily",date="2026-10-08",pages=5)
    b=prepare_pdf(src,workspace=tmp_path/"work",dpi=72,max_pages_per_part=2)
    assert [(x.page_start,x.page_end) for x in b.parts]==[(1,2),(3,4),(5,5)]


def test_filename_cannot_supply_or_override_identity(tmp_path):
    a=tmp_path/"Financial Times EU - 30.09.2026.pdf"
    make_pdf(a,title="Nikkei Asia",date="8 October 2026")
    b=prepare_pdf(a,workspace=tmp_path/"work2",dpi=72)
    assert b.identity.publication_id=="nikkei-asia"
    assert b.identity.edition_date=="2026-10-08"

def test_filename_only_identity_is_rejected(tmp_path):
    src=tmp_path/"Financial Times EU - 30.09.2026.pdf"
    d=fitz.open()
    try:
        p=d.new_page(); p.insert_text((72,72),"Document without publication identity or edition date")
        d.save(src)
    finally: d.close()
    import pytest
    from business_brief.technician import IdentityUnresolved
    with pytest.raises(IdentityUnresolved):
        prepare_pdf(src,workspace=tmp_path/"work3",dpi=72)
