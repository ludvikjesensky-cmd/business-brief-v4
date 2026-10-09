from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import tempfile
import threading

from .events import EventLogger
from .fast_editorial import (VERSION, PAGE_PROMPT, ISSUE_PROMPT, PAGE_SCHEMA, ISSUE_SCHEMA,
    EditorialError, ResponsesProvider, neutral_page, validate_page, freeze_issue)
from .ingestor_worker import archive_key
from .storage import SupabaseArchive


def encoded(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()


def checked_download(bucket, key, digest):
    payload = bucket.download(archive_key(key))
    if hashlib.sha256(payload).hexdigest() != digest:
        raise EditorialError("Input artifact SHA mismatch")
    return payload


def process(archive, source_id, provider, concurrency=4):
    db = archive.client
    log = EventLogger(db, component="FAST_EDITORIAL")
    tasks = db.rpc("claim_fast_editorial", {"p_source_id":source_id,"p_version":VERSION,"p_model":provider.model}).execute().data or []
    if not tasks:
        return {"source_id":source_id,"status":"NO_CLAIM"}
    task = tasks[0]
    auth = {"p_job_id":task["id"],"p_lease_token":task["lease_token"]}
    stop = threading.Event()
    def heartbeat():
        while not stop.wait(60):
            try:
                db.rpc("heartbeat_fast_editorial",auth).execute()
            except Exception:
                log.emit("EDITORIAL_HEARTBEAT_FAILED",severity="WARNING",source_id=source_id)
    thread = threading.Thread(target=heartbeat,daemon=True)
    thread.start()
    log.emit("EDITORIAL_STARTED",source_id=source_id,metadata={"model":provider.model,"version":VERSION})
    try:
        source = db.table("sources").select("*").eq("id",source_id).single().execute().data
        ingested = db.table("ingestor_jobs").select("*").eq("source_id",source_id).eq("status","DONE").order("created_at",desc=True).limit(1).execute().data[0]
        bucket = db.storage.from_(archive.archive)
        physical = json.loads(checked_download(bucket, ingested["physical_map_path"], ingested["physical_map_sha256"]))
        manifest_key = archive_key(source["source_bundle_path"])
        manifest = json.loads(bucket.download(manifest_key))
        if physical["source_id"] != source_id or physical["source_sha256"] != manifest["source_sha256"]:
            raise EditorialError("Physical Map source identity mismatch")
        if len(physical["pages"]) != source["page_count"] or manifest["page_count"] != source["page_count"]:
            raise EditorialError("Incomplete source page count")
        images = {p["page_no"]:p for p in manifest["page_images"]}
        if sorted(images) != list(range(1,source["page_count"]+1)):
            raise EditorialError("Incomplete image sequence")
        cached = {row["page_no"]:row for row in db.table("fast_editorial_pages").select("*").eq("job_id",task["id"]).execute().data or []}
        results = {}
        audits = {}
        def discover(page):
            number = page["page_no"]
            image = images[number]
            fingerprint = hashlib.sha256(encoded({"physical_map":ingested["physical_map_sha256"],
                "image":image["sha256"],"version":VERSION,"model":provider.model,
                "prompt":PAGE_PROMPT,"schema":PAGE_SCHEMA})).hexdigest()
            prior = cached.get(number)
            if prior and prior["input_sha256"]==fingerprint:
                validate_page(prior["response"]["result"], page)
                return number, prior["response"]
            key = archive_key(image["path"],manifest_key.rsplit("/",1)[0]+"/")
            raster = checked_download(bucket,key,image["sha256"])
            response = provider.generate(PAGE_PROMPT,neutral_page(page),PAGE_SCHEMA,image=raster)
            validate_page(response["result"], page)
            db.rpc("save_fast_editorial_page",{**auth,"p_page_no":number,"p_input_sha256":fingerprint,"p_response":response}).execute()
            log.emit("EDITORIAL_PAGE_SAVED",source_id=source_id,metadata={"page_no":number,"items":len(response["result"]["items"]),"usage":response.get("usage",{})})
            return number,response
        with ThreadPoolExecutor(max_workers=max(1,min(concurrency,4))) as pool:
            futures = [pool.submit(discover,page) for page in physical["pages"]]
            try:
                for future in as_completed(futures):
                    number, response = future.result()
                    results[number] = response["result"]
                    audits[number] = {k:v for k,v in response.items() if k!="result"}
            except Exception:
                for future in futures:
                    future.cancel()
                raise
        fragments = [{"fragment_id":f"p{n:04d}:{item['local_id']}","page_no":n,**item}
                     for n in sorted(results) for item in results[n]["items"]]
        synthesis = provider.generate(ISSUE_PROMPT,{"fragments":fragments},ISSUE_SCHEMA)
        issue = freeze_issue(source_id,physical["source_sha256"],physical["pages"],results,synthesis["result"])
        issue["provenance"] = {"physical_map_sha256":ingested["physical_map_sha256"],
            "manifest_path":manifest_key,"model":provider.model,"page_calls":audits,
            "issue_call":{k:v for k,v in synthesis.items() if k!="result"}}
        digest = hashlib.sha256(encoded(issue)).hexdigest()
        prefix = f"fast-editorial/{source_id}/{task['id']}/sha256-{digest}"
        with tempfile.TemporaryDirectory(prefix="bbv4-editorial-") as temp:
            local = Path(temp)/"issue-map.json"
            local.write_bytes(encoded(issue))
            archive.upload_file(local,prefix+"/issue-map.json","application/json")
            markdown = Path(temp)/"issue-map.md"
            markdown.write_text(render_markdown(issue))
            archive.upload_file(markdown,prefix+"/issue-map.md","text/markdown")
        db.rpc("finalize_fast_editorial",{**auth,"p_path":prefix+"/issue-map.json","p_sha256":digest,"p_map":issue}).execute()
        log.emit("EDITORIAL_FROZEN",source_id=source_id,status="FROZEN",metadata={"items":len(issue["items"]),"pages":len(results),"path":prefix+"/issue-map.md"})
        return {"source_id":source_id,"status":"FROZEN","pages":len(results),"items":len(issue["items"]),"artifact":prefix+"/issue-map.md"}
    except Exception as exc:
        db.rpc("fail_fast_editorial",{**auth,"p_error":str(exc)}).execute()
        log.emit("EDITORIAL_FAILED",source_id=source_id,status="FAILED",severity="ERROR",message=str(exc))
        raise
    finally:
        stop.set()
        thread.join()


def render_markdown(issue):
    lines = ["# Předběžná redakční mapa vydání", "", "Provisional — před Selective Deep Read a verifikací.","",issue["edition_note_cs"],""]
    for item in issue["items"]:
        lines += [f"## {item['provisional_id']} · {item['priority'].upper()} · {item['headline_original'] or '(pokračování bez titulku)'}",
                  "",f"Strany: {', '.join(map(str,item['page_refs']))}","",item["summary_cs"],"",
                  "Pohled autora: "+item["author_angle_cs"],"Nová informace: "+item["new_information_cs"],
                  "Význam události: "+item["importance_reason_cs"],"Hodnota četby: "+item["reading_value_reason_cs"],
                  "Deep Read: "+item["deep_read_reason_cs"],"Nejistoty: "+"; ".join(item["uncertainties"]),""]
    lines += ["## Poznámky k průchodu stran",""]
    for page in issue["page_observations"]:
        lines.append(f"- Strana {page['page_no']}: {page['page_note_cs']}")
    return "\n".join(lines)+"\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id",required=True)
    parser.add_argument("--concurrency",type=int,default=4)
    args = parser.parse_args()
    print(json.dumps(process(SupabaseArchive.from_env(),args.source_id,ResponsesProvider(),args.concurrency),ensure_ascii=False))


if __name__=="__main__":
    main()
