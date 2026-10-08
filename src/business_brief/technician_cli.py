from __future__ import annotations
import argparse, json
from .technician import TechnicianError, prepare_pdf

def main() -> int:
    p=argparse.ArgumentParser(prog="bb-technician")
    p.add_argument("source");p.add_argument("--workspace",default="./workspace")
    p.add_argument("--publication");p.add_argument("--date",dest="edition_date")
    p.add_argument("--variant",default="default");p.add_argument("--language")
    p.add_argument("--dpi",type=int,default=144);p.add_argument("--ocr",choices=["auto","always","never"],default="auto")
    p.add_argument("--ocr-language",default="eng");p.add_argument("--min-native-chars",type=int,default=30)
    p.add_argument("--max-pages-per-part",type=int,default=0)
    a=p.parse_args()
    try:
        b=prepare_pdf(a.source,workspace=a.workspace,publication=a.publication,edition_date=a.edition_date,edition_variant=a.variant,language=a.language,dpi=a.dpi,ocr_mode=a.ocr,ocr_languages=a.ocr_language,min_native_chars_per_page=a.min_native_chars,max_pages_per_part=a.max_pages_per_part)
        print(json.dumps(b.to_dict(),ensure_ascii=False,indent=2));return 0
    except TechnicianError as e:
        print(f"Technician error: {e}");return 2
if __name__=="__main__":raise SystemExit(main())
