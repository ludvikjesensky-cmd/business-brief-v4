from __future__ import annotations
import json, os, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .events import EventLogger
from .storage import SupabaseArchive
from .technician import IdentityUnresolved
from .technician_worker import process_inbox_object

_lock=threading.Lock()

def drain_inbox():
    if not _lock.acquire(blocking=False): return {"status":"ALREADY_RUNNING"}
    try:
        archive=SupabaseArchive.from_env(); keys=archive.list_inbox(); results=[]
        for key in keys:
            try: results.append({"object_key":key,**process_inbox_object(key)})
            except IdentityUnresolved as exc:
                EventLogger(archive.client).emit("IDENTITY_UNRESOLVED",stage="T05",severity="ERROR",status="IDENTITY_UNRESOLVED",message=str(exc),metadata={"object_key":key})
                results.append({"object_key":key,"status":"IDENTITY_UNRESOLVED","error":str(exc)})
            except Exception as exc:
                EventLogger(archive.client).emit("TECHNICIAN_FAILED",stage="T24",severity="ERROR",status="FAILED",message=str(exc),metadata={"object_key":key})
                results.append({"object_key":key,"status":"FAILED","error":str(exc)})
        return {"status":"DRAINED","count":len(keys),"results":results}
    finally: _lock.release()

class Handler(BaseHTTPRequestHandler):
    def _json(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(status)
        self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        self._json(200,{"ok":True}) if self.path=="/health" else self._json(404,{"error":"not found"})
    def do_POST(self):
        if self.path!="/wake": return self._json(404,{"error":"not found"})
        token=os.environ.get("TECHNICIAN_WAKE_TOKEN")
        if not token or self.headers.get("X-Technician-Token")!=token: return self._json(401,{"error":"unauthorized"})
        threading.Thread(target=drain_inbox,daemon=True).start(); self._json(202,{"accepted":True})
    def log_message(self,format,*args): pass

def main():
    ThreadingHTTPServer(("0.0.0.0",int(os.environ.get("PORT","8080"))),Handler).serve_forever()

if __name__=="__main__": main()
