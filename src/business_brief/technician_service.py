from __future__ import annotations
import json, logging, os, threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .events import EventLogger
from .storage import SupabaseArchive
from .technician import IdentityUnresolved, TECHNICIAN_VERSION
from .technician_worker import process_inbox_object

_lock = threading.Lock()

def drain_inbox():
    if not _lock.acquire(blocking=False):
        return {"status": "ALREADY_RUNNING"}
    try:
        archive = SupabaseArchive.from_env()
        db = archive.client
        db.rpc("reconcile_technician_inbox", {}).execute()
        results = []
        while True:
            rows = db.rpc("claim_technician_inbox", {}).execute().data or []
            if not rows:
                break
            task = rows[0]
            stop = threading.Event()
            def heartbeat():
                while not stop.wait(60):
                    try:
                        until = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
                        db.table("technician_inbox_queue").update({"lease_until":until}).eq("id",task["id"]).eq("lease_token",task["lease_token"]).execute()
                    except Exception:
                        logging.exception("Queue heartbeat failed")
            thread = threading.Thread(target=heartbeat, daemon=True)
            thread.start()
            try:
                result = process_inbox_object(task["object_key"], object_version=task["object_version"])
                state = "DONE" if result["status"] in {"READY_FOR_INGESTOR", "DUPLICATE_SOURCE"} else "BLOCKED"
                error = None
            except Exception as exc:
                state = "BLOCKED" if isinstance(exc, IdentityUnresolved) else "RETRY"
                error = str(exc)
                result = {"status": "IDENTITY_UNRESOLVED" if isinstance(exc, IdentityUnresolved) else "FAILED", "error":error}
                EventLogger(db).emit(result["status"],stage="T24",severity="ERROR",status=result["status"],message=error,metadata={"object_key":task["object_key"],"queue_id":task["id"]})
            finally:
                stop.set()
                thread.join()
            db.table("technician_inbox_queue").update({"status":state,"last_error":error,"lease_until":None,"available_at":(datetime.now(timezone.utc)+timedelta(minutes=min(60,5*task["attempt"]))).isoformat()}).eq("id",task["id"]).eq("lease_token",task["lease_token"]).execute()
            results.append({"object_key":task["object_key"],**result})
        logging.info("Queue drained: %s",json.dumps(results))
        return {"status":"DRAINED","results":results}
    finally:
        _lock.release()

class Handler(BaseHTTPRequestHandler):
    def _json(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(status)
        self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        self._json(200,{"ok":True,"technician_version":TECHNICIAN_VERSION}) if self.path=="/health" else self._json(404,{"error":"not found"})
    def do_POST(self):
        if self.path!="/wake": return self._json(404,{"error":"not found"})
        token=os.environ.get("TECHNICIAN_WAKE_TOKEN")
        if not token or self.headers.get("X-Technician-Token")!=token: return self._json(401,{"error":"unauthorized"})
        threading.Thread(target=drain_inbox,daemon=True).start(); self._json(202,{"accepted":True})
    def log_message(self,format,*args): pass

def main():
    logging.basicConfig(level=logging.INFO)
    threading.Thread(target=drain_inbox,daemon=True).start()
    ThreadingHTTPServer(("0.0.0.0",int(os.environ.get("PORT","8080"))),Handler).serve_forever()

if __name__=="__main__": main()
