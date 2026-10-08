"""Deployment check of the real OCR toolchain, using a disposable raster PDF."""
import importlib.metadata, json, shutil, tempfile
from pathlib import Path
import pymupdf
from .technician import _ocr, _validate_pdf

def main():
    versions={name:importlib.metadata.version(name) for name in ['pymupdf','ocrmypdf','supabase']}
    for binary in ['tesseract','gs','ocrmypdf']:
        if not shutil.which(binary): raise RuntimeError(f'Missing runtime executable: {binary}')
    with tempfile.TemporaryDirectory(prefix='bb-runtime-check-') as td:
        root=Path(td)
        with pymupdf.open() as text:
            page=text.new_page(width=600,height=400)
            page.insert_text((40,80),'Business Brief runtime verification\nOctober 8 2026\nThe OCR engine reads this raster page.',fontsize=20)
            image=page.get_pixmap(matrix=pymupdf.Matrix(2,2),alpha=False).tobytes('png')
        with pymupdf.open() as raster:
            page=raster.new_page(width=600,height=400);page.insert_image(page.rect,stream=image)
            raster.save(root/'raster.pdf')
        _ocr(root/'raster.pdf',root/'ocr.pdf','always','eng','ocrmypdf')
        assert _validate_pdf(root/'ocr.pdf')==1
        with pymupdf.open(root/'ocr.pdf') as result:
            assert 'runtime' in result[0].get_text().lower()
    print(json.dumps({'runtime_check':'PASSED','raster_ocr':'PASSED','versions':versions}),flush=True)

if __name__=='__main__': main()
