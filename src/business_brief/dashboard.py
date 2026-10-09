from __future__ import annotations
import json,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from supabase import create_client

def client():
    return create_client(os.environ["SUPABASE_URL"],os.environ["SUPABASE_SECRET_KEY"])
def snapshot():
    db=client()
    today=db.table("dashboard_today").select("*").execute().data or []
    metrics=db.table("dashboard_metrics_30d").select("*").execute().data or []
    events=db.table("pipeline_events").select("*").order("occurred_at",desc=True).limit(200).execute().data or []
    jobs=db.table("dashboard_technician_jobs").select("*").order("created_at",desc=True).limit(100).execute().data or []
    queue=db.table("technician_inbox_queue").select("*").order("created_at",desc=True).limit(100).execute().data or []
    ingestor=db.table("ingestor_jobs").select("*").order("created_at",desc=True).limit(100).execute().data or []
    today=[x for x in today if x.get("edition_status")!="SUPERSEDED"]
    blocked=any(x.get("status") in {"BLOCKED","RETRY"} for x in queue) or any((x.get("job_status") in {"FAILED","BLOCKED"} or x.get("source_status") in {"EDITION_COLLISION","IDENTITY_UNRESOLVED"}) for x in today)
    running=any(x.get("status")=="PROCESSING" for x in queue) or any(x.get("job_status")=="PROCESSING" for x in today)
    blocked=blocked or any(x.get("status") in {"BLOCKED","RETRY"} for x in ingestor)
    running=running or any(x.get("status")=="PROCESSING" for x in ingestor)
    health="BLOCKED" if blocked else "RUNNING" if running else "HEALTHY"
    return {"health":health,"today":today,"metrics_30d":metrics[0] if metrics else {},"events":events,"jobs":jobs,"queue":queue,"ingestor_jobs":ingestor}

HTML="""<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><meta http-equiv=refresh content=15><title>Business Brief Control Tower</title><style>
body{font-family:ui-sans-serif,system-ui;background:#08111f;color:#eaf0f7;margin:0}main{max-width:1400px;margin:auto;padding:28px}.top{display:flex;justify-content:space-between;align-items:end}.muted{color:#8fa2b8}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.card{background:#101c2d;border:1px solid #22344b;border-radius:14px;padding:18px;margin-top:16px}.ok{color:#57d68d}.warn{color:#ffd166}.bad{color:#ff6b6b}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:9px;border-bottom:1px solid #22344b;text-align:left}code{font-size:12px}.log{max-height:480px;overflow:auto}.pill{padding:5px 9px;border-radius:20px;background:#1b2a40}h1,h2{margin:.2em 0}</style></head><body><main><div class=top><div><div class=muted>BUSINESS BRIEF v4</div><h1>Control Tower</h1></div><div id=health></div></div><div id=app></div><script>
fetch('/api/dashboard').then(r=>r.json()).then(d=>{const esc=v=>typeof v==='string'?v.replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c])):v; for(const key of ['today','events','queue','ingestor_jobs']) d[key]=(d[key]||[]).map(row=>Object.fromEntries(Object.entries(row).map(([k,v])=>[k,esc(v)]))); let cls=d.health==='HEALTHY'?'ok':d.health==='BLOCKED'?'bad':'warn';health.innerHTML='<b class="'+cls+'">● '+d.health+'</b>';
let m=d.metrics_30d||{};let h='<div class=grid>'+[['Dnešní vydání',d.today.length],['Úspěšné 30 dní',m.successful||0],['Chyby',m.failed||0],['Kolize',m.collisions||0],['Retry',m.retries||0],['Medián',m.median_seconds?Math.round(m.median_seconds)+' s':'—']].map(x=>'<div class=card><div class=muted>'+x[0]+'</div><h2>'+x[1]+'</h2></div>').join('')+'</div>';
h+='<div class=card><h2>Dnešní pipeline</h2><table><tr><th>Titul</th><th>Vydání</th><th>Source</th><th>Job</th><th>Stran</th><th>Attempt</th></tr>'+d.today.map(x=>'<tr><td>'+x.canonical_name+'</td><td>'+x.edition_date+' · '+x.edition_variant+'</td><td>'+x.source_status+'</td><td>'+x.job_status+'</td><td>'+(x.page_count||'—')+'</td><td>'+(x.attempt||'—')+'</td></tr>').join('')+'</table></div>';
h+='<div class=card><h2>Inbox queue</h2><table><tr><th>Soubor</th><th>Stav</th><th>Pokus</th><th>Chyba</th></tr>'+d.queue.map(x=>'<tr><td>'+x.object_key+'</td><td>'+x.status+'</td><td>'+x.attempt+'</td><td>'+(x.last_error||'')+'</td></tr>').join('')+'</table></div>';
h+='<div class=card><h2>Ingestor</h2><table><tr><th>Source</th><th>Stav</th><th>Stran</th><th>Bloků</th><th>Pokus</th><th>Chyba</th></tr>'+d.ingestor_jobs.map(x=>'<tr><td><code>'+x.source_id+'</code></td><td>'+x.status+'</td><td>'+((x.metrics||{}).page_count||'—')+'</td><td>'+((x.metrics||{}).block_count||'—')+'</td><td>'+x.attempt+'</td><td>'+(x.last_error||'')+'</td></tr>').join('')+'</table></div>';
h+='<div class="card log"><h2>Event log</h2><table><tr><th>Čas</th><th>Komponenta</th><th>Stage</th><th>Event</th><th>Stav</th><th>ms</th><th>Zpráva</th></tr>'+d.events.map(x=>'<tr><td>'+new Date(x.occurred_at).toLocaleTimeString()+'</td><td>'+x.component+'</td><td>'+(x.stage||'')+'</td><td>'+x.event+'</td><td>'+(x.status||x.severity)+'</td><td>'+(x.duration_ms||'')+'</td><td>'+(x.message||'')+'</td></tr>').join('')+'</table></div>';app.innerHTML=h;});</script></main></body></html>"""
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/api/dashboard":
            body=json.dumps(snapshot(),ensure_ascii=False).encode();ctype="application/json"
        else: body=HTML.encode();ctype="text/html; charset=utf-8"
        self.send_response(200);self.send_header("Content-Type",ctype);self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body)
def main():
    ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8080"))),Handler).serve_forever()
if __name__=="__main__": main()
