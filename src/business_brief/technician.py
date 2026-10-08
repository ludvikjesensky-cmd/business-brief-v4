from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, unicodedata
from datetime import datetime, timezone
from pathlib import Path
import fitz
from .contracts import OcrInfo, PageImage, PublicationIdentity, SourceBundle, SourcePart

TECHNICIAN_VERSION = "technician-v4.1"
MONTHS = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12,
"januar":1,"februar":2,"marz":3,"maerz":3,"april":4,"mai":5,"juni":6,"juli":7,"august":8,"september":9,"oktober":10,"november":11,"dezember":12}

class TechnicianError(RuntimeError): pass
class IdentityUnresolved(TechnicianError): pass

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def slugify(s: str) -> str:
    s=unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+","-",s).strip("-") or "unknown-publication"

def _validate_pdf(path: Path) -> int:
    try: doc=fitz.open(path)
    except Exception as e: raise TechnicianError(f"Cannot open PDF: {e}") from e
    try:
        if doc.page_count<1: raise TechnicianError("PDF has no pages")
        for p in doc:
            if p.rect.width<=0 or p.rect.height<=0: raise TechnicianError(f"Invalid page geometry: {p.number+1}")
        return doc.page_count
    finally: doc.close()

def _probe(path: Path):
    doc=fitz.open(path)
    try:
        meta={k:(v or "").strip() for k,v in (doc.metadata or {}).items()}
        first=doc[0].get_text("text").strip()
        counts=[len("".join(p.get_text("text").split())) for p in doc]
        return meta,first,counts
    finally: doc.close()

def _parse_date(text: str) -> str|None:
    m=re.search(r"\b(20\d{2})[-/.](0?[1-9]|1[0-2])[-/.](0?[1-9]|[12]\d|3[01])\b",text)
    if m:
        y,mo,d=map(int,m.groups()); return f"{y:04d}-{mo:02d}-{d:02d}"
    m=re.search(r"\b(0?[1-9]|[12]\d|3[01])[./](0?[1-9]|1[0-2])[./](20\d{2})\b",text)
    if m:
        d,mo,y=map(int,m.groups()); return f"{y:04d}-{mo:02d}-{d:02d}"
    t=unicodedata.normalize("NFKD",text).encode("ascii","ignore").decode().lower()
    m=re.search(r"\b(0?[1-9]|[12]\d|3[01])\s+([a-z]+)\s+(20\d{2})\b",t)
    if m and m.group(2) in MONTHS:
        d,mo,y=m.groups(); return f"{int(y):04d}-{MONTHS[mo]:02d}-{int(d):02d}"
    m=re.search(r"\b([a-z]+)\s+(0?[1-9]|[12]\d|3[01]),?\s+(20\d{2})\b",t)
    if m and m.group(1) in MONTHS:
        mo,d,y=m.groups(); return f"{int(y):04d}-{MONTHS[mo]:02d}-{int(d):02d}"
    return None

KNOWN_PUBLICATIONS = (
    ("the-wall-street-journal", "The Wall Street Journal", (r"\bthe\s+wall\s+street\s+journal\b", r"\bwall\s+street\s+journal\b", r"\bwsj\b")),
    ("financial-times", "Financial Times", (r"\bfinancial\s+times\b",)),
    ("handelsblatt", "Handelsblatt", (r"\bhandelsblatt\b",)),
)

def _known_publication(text: str):
    normalized=re.sub(r"\s+"," ",text).strip().lower()
    for publication_id,canonical_name,patterns in KNOWN_PUBLICATIONS:
        if any(re.search(pattern,normalized,re.I) for pattern in patterns):
            return publication_id,canonical_name
    return None

def _identity_ocr(path: Path) -> str:
    """OCR only the first page for edition identity; no editorial interpretation."""
    executable=shutil.which("tesseract")
    if not executable: return ""
    doc=fitz.open(path)
    try:
        pix=doc[0].get_pixmap(matrix=fitz.Matrix(2.5,2.5),alpha=False)
        import tempfile
        with tempfile.TemporaryDirectory(prefix="bb-identity-") as td:
            image=Path(td)/"first.png"; pix.save(image)
            run=subprocess.run([executable,str(image),"stdout","-l","eng+deu","--psm","3"],capture_output=True,text=True,timeout=90)
            if run.returncode:
                run=subprocess.run([executable,str(image),"stdout","-l","eng","--psm","3"],capture_output=True,text=True,timeout=90)
            return run.stdout if run.returncode==0 else ""
    finally: doc.close()

def identify_pdf(path: Path, publication=None, edition_date=None, edition_variant="default", language=None) -> PublicationIdentity:
    meta,first,_=_probe(path); evidence=[]
    # Filename is transport metadata only. Never use it as identity evidence.
    corpus="\n".join([meta.get("title",""),meta.get("subject",""),first[:12000]])
    date=edition_date or _parse_date(corpus)\n    if not date or (not publication and not _known_publication(corpus) and not meta.get("title")):\n        first_page_ocr=_identity_ocr(path)\n        if first_page_ocr:\n            corpus += "\\n" + first_page_ocr\n            evidence.append("first_page_ocr=tesseract")\n            date=edition_date or _parse_date(corpus)
    if edition_date: evidence.append(f"trusted_intake.edition_date={edition_date}")
    if not date: raise IdentityUnresolved("Could not establish edition date from document content")

    if publication:
        candidate=publication.strip()
        if not candidate or slugify(candidate)=="unknown-publication":
            raise IdentityUnresolved("Trusted publication identity is empty or unresolved")
        evidence.append(f"trusted_intake.publication={candidate}")
        return PublicationIdentity(slugify(candidate),candidate,date,edition_variant or "default",language,1.0,tuple(evidence))

    known=_known_publication(corpus)
    if known:
        publication_id,canonical_name=known
        evidence.append(f"publication_pattern={canonical_name}")
        return PublicationIdentity(publication_id,canonical_name,date,edition_variant or "default",language,.95,tuple(evidence))

    title=(meta.get("title") or "").strip()
    if title and 2<=len(title)<=100 and slugify(title)!="unknown-publication":
        evidence.append(f"pdf_metadata.title={title}")
        return PublicationIdentity(slugify(title),title,date,edition_variant or "default",language,.80,tuple(evidence))
    raise IdentityUnresolved("Could not establish publication identity with sufficient confidence")

def _ocr(src:Path,dst:Path,mode:str,languages:str,binary:str):
    exe=shutil.which(binary)
    if not exe: raise TechnicianError(f"OCR required but {binary!r} is not installed")
    dst.parent.mkdir(parents=True,exist_ok=True)
    cmd=[exe,"--deskew","--rotate-pages","--output-type","pdf","-l",languages,"--force-ocr" if mode=="always" else "--skip-text",str(src),str(dst)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: raise TechnicianError("OCR failed: "+(r.stderr.strip() or r.stdout.strip()))

def _render(src:Path,out:Path,dpi:int):
    out.mkdir(parents=True,exist_ok=True); doc=fitz.open(src); result=[]; matrix=fitz.Matrix(dpi/72,dpi/72)
    try:
        for i,p in enumerate(doc,1):
            target=out/f"page-{i:04d}.png"; pix=p.get_pixmap(matrix=matrix,alpha=False); pix.save(target)
            result.append(PageImage(i,str(target),pix.width,pix.height,sha256_file(target)))
    finally: doc.close()
    return tuple(result)

def _split(src:Path,out:Path,max_pages:int):
    if max_pages<=0:return ()
    doc=fitz.open(src)
    try:
        if max_pages>=doc.page_count:return ()
        out.mkdir(parents=True,exist_ok=True); result=[]
        for n,start in enumerate(range(0,doc.page_count,max_pages),1):
            end=min(doc.page_count-1,start+max_pages-1); target=out/f"part-{n:04d}-p{start+1:04d}-p{end+1:04d}.pdf"; d=fitz.open()
            try:d.insert_pdf(doc,from_page=start,to_page=end);d.save(target)
            finally:d.close()
            result.append(SourcePart(n,start+1,end+1,str(target),sha256_file(target),target.stat().st_size))
        return tuple(result)
    finally:doc.close()

def prepare_pdf(source_pdf,*,workspace,publication=None,edition_date=None,edition_variant="default",language=None,dpi=144,ocr_mode="auto",ocr_languages="eng",min_native_chars_per_page=30,max_pages_per_part=0,ocrmypdf_binary="ocrmypdf",received_at=None):
    if ocr_mode not in {"auto","always","never"}:raise TechnicianError("Invalid OCR mode")
    source=Path(source_pdf).expanduser().resolve()
    if not source.is_file():raise TechnicianError(f"Source does not exist: {source}")
    page_count=_validate_pdf(source); digest=sha256_file(source)
    identity=identify_pdf(source,publication,edition_date,edition_variant,language)
    root=Path(workspace).expanduser().resolve(); final=root/"sources"/digest/TECHNICIAN_VERSION; manifest=final/"manifest.json"
    if manifest.exists():return bundle_from_manifest(json.loads(manifest.read_text(encoding="utf-8")))
    staging=root/".staging"/f"{digest}-{os.getpid()}"; shutil.rmtree(staging,ignore_errors=True); staging.mkdir(parents=True)
    try:
        original=staging/"original.pdf"; shutil.copyfile(source,original)
        if sha256_file(original)!=digest:raise TechnicianError("Immutable copy hash mismatch")
        _,_,counts=_probe(original); needs=tuple(i for i,c in enumerate(counts,1) if c<min_native_chars_per_page)
        required=ocr_mode=="always" or (ocr_mode=="auto" and bool(needs)); prepared=original; performed=False; engine=None
        if required:
            prepared=staging/"prepared"/"ocr.pdf"; _ocr(original,prepared,ocr_mode,ocr_languages,ocrmypdf_binary); performed=True;engine="ocrmypdf"
            if _validate_pdf(prepared)!=page_count:raise TechnicianError("OCR derivative page count mismatch")
        pages=_render(original,staging/"pages",dpi)
        if len(pages)!=page_count:raise TechnicianError("Rendered page count mismatch")
        parts=_split(prepared,staging/"parts",max_pages_per_part)
        ocr=OcrInfo(ocr_mode,required,performed,engine,ocr_languages if required else None,needs,str(prepared),sha256_file(prepared))
        bundle=SourceBundle(f"sha256:{digest}",digest,identity,source.name,source.stat().st_size,page_count,str(original),str(prepared),pages,ocr,parts,received_at or datetime.now(timezone.utc).isoformat(),TECHNICIAN_VERSION)
        (staging/"manifest.json").write_text(json.dumps(bundle.to_dict(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        final.parent.mkdir(parents=True,exist_ok=True)
        if final.exists():shutil.rmtree(staging)
        else:os.replace(staging,final)
        data=json.loads((final/"manifest.json").read_text(encoding="utf-8"))
        def canon(p):return str(final/Path(p).relative_to(staging))
        data["original_path"]=canon(data["original_path"]);data["prepared_pdf_path"]=canon(data["prepared_pdf_path"]);data["ocr"]["prepared_pdf_path"]=canon(data["ocr"]["prepared_pdf_path"])
        for p in data["page_images"]:p["path"]=canon(p["path"])
        for p in data["parts"]:p["path"]=canon(p["path"])
        tmp=final/".manifest.tmp";tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");os.replace(tmp,final/"manifest.json")
        return bundle_from_manifest(data)
    except Exception:
        shutil.rmtree(staging,ignore_errors=True);raise

def bundle_from_manifest(d):
    i=d["identity"]; identity=PublicationIdentity(i["publication_id"],i["canonical_name"],i["edition_date"],i["edition_variant"],i.get("language"),float(i["confidence"]),tuple(i.get("evidence",[])))
    o=d["ocr"]; ocr=OcrInfo(o["mode"],o["required"],o["performed"],o.get("engine"),o.get("languages"),tuple(o.get("pages_requiring_ocr",[])),o["prepared_pdf_path"],o["prepared_sha256"])
    return SourceBundle(d["source_id"],d["source_sha256"],identity,d["original_filename"],d["byte_size"],d["page_count"],d["original_path"],d["prepared_pdf_path"],tuple(PageImage(**p) for p in d["page_images"]),ocr,tuple(SourcePart(**p) for p in d.get("parts",[])),d["received_at"],d["technician_version"],d.get("schema_version","source-bundle-v4"),d.get("status","READY_FOR_INGESTOR"))
