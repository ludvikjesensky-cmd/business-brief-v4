"""Private, read-only Deep/Memory Control Tower; never executes runner operations."""
from __future__ import annotations

import base64
import hmac
import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def describe_selection(selection):
    """Derive guidance from exact selection evidence, never from COMPLETE alone."""
    requests = selection.get('requests', [])
    latest = {}
    for request in requests:  # SQL orders newest first
        latest.setdefault(request['operation'], request)
    if any(r['state'] in {'RUNNING', 'UNKNOWN'} for r in latest.values()):
        return 'Průběh nepotvrzený', 'Ověřit stav běhu; při přerušení použít původní request key.'
    if any(r['state'] != 'COMPLETE' or r.get('result_status') != 'PASS' for r in latest.values()):
        return 'Vyžaduje kontrolu', 'Prověřit poslední běh a opravit označené podklady.'
    if selection.get('review_articles', 0):
        return 'Články ke kontrole', 'Vyřešit kontrolu sestavených článků.'
    articles, indexed = selection.get('articles', 0), selection.get('indexed', 0)
    if articles and indexed == articles:
        search = latest.get('search', {})
        return 'Indexováno', ('Vyhodnotit relevanci výsledků; úspěšné volání není schválený retrieval benchmark.'
            if search.get('result_status') == 'PASS' else 'Provést a vyhodnotit kontrolní vyhledávání.')
    if articles:
        return 'Články uložené', 'Zkontrolovat plán Indexeru a explicitně spustit indexaci.'
    assembly = latest.get('assembler', {})
    if assembly.get('result_status') == 'PASS':
        return 'Plán sestavení prošel', 'Zkontrolovat výsledek plánu a explicitně povolit uložení článků.'
    return 'Výběr evidován', 'Ověřit accepted manifest a provést plán Assembleru.'


def snapshot():
    import psycopg
    from psycopg.rows import dict_row
    dsn = os.environ['BRIDGE_DATABASE_URL']
    with psycopg.connect(dsn, row_factory=dict_row, connect_timeout=10) as connection:
        connection.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
        connection.execute("SET LOCAL statement_timeout = '15s'")
        editions = connection.execute(Path(__file__).with_suffix('.sql').read_text()).fetchall()
    for edition in editions:
        # Raw private paths stay server-side.
        edition['prepared'] = bool(edition.pop('source_bundle_path', None))
        for selection in edition['selections']:
            selection['label'], selection['next_step'] = describe_selection(selection)
    return {'observed_at': datetime.now(timezone.utc).isoformat(), 'editions': editions,
            'limit': 100, 'read_only': True}


HTML = '''<!doctype html><html lang="cs"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Business Brief Control Tower</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0b1320;color:#e9edf3;font:16px system-ui}main{max-width:1200px;margin:auto;padding:32px 20px}header{display:flex;justify-content:space-between;gap:20px;align-items:center}h1{font:36px Georgia;margin:8px 0}h2{font:26px Georgia;margin:0 0 12px}h3{margin:12px 0}p{line-height:1.6}.muted,small{color:#9aabc0}.card{border:1px solid #2b3a50;border-radius:14px;padding:24px;margin:20px 0;background:#121e2f}.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:10px;margin:20px 0}.step{padding:14px;background:#1b2c43;border-radius:8px}.step b{display:block;margin-bottom:8px}.next{border-left:3px solid #e7b66d;padding:10px 16px;background:#202b38}.ok{color:#75d8a7}.warn{color:#efc881}button,select{background:#1b2c43;color:inherit;border:1px solid #52637a;padding:10px;border-radius:6px}details{margin-top:14px}summary{cursor:pointer}code{overflow-wrap:anywhere;font-size:12px}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:10px 5px;border-bottom:1px solid #2b3a50}.scroll{overflow:auto}#error{color:#ffb1a9}label{display:block;margin-top:20px}
</style></head><body><main><header><div><small>BUSINESS BRIEF · DEEP / MEMORY</small><h1>Průběh zpracování vydání</h1></div><button id="refresh">Obnovit</button></header>
<p class="muted">Od přípravy PDF po vyhledávání. Přehled uložených důkazů a dalšího kroku.</p><p id="stamp" class="muted"></p><p id="error" role="alert"></p><label>Vydání <select id="filter"><option value="all">Všechna</option></select></label><div id="app"></div>
<p class="muted">Pouze čtení · nejvýše 100 naposledy přijatých aktivních zdrojů. Technician se přes Chat zatím bezpečně spustit nedá. Fast Editorial má samostatný proces.</p>
<script>
const app=document.getElementById('app'),err=document.getElementById('error'),filter=document.getElementById('filter');let data;
const esc=v=>String(v??'—').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const date=v=>v?new Date(v).toLocaleString('cs-CZ',{timeZone:'Europe/Prague'}):'—';
const names={assembler:'Sestavení článků',indexer:'Indexace',search:'Vyhledávání'};
function render(){app.innerHTML=(data.editions||[]).filter(e=>filter.value==='all'||e.source_id===filter.value).map(e=>{
let h='<section class="card"><h2>'+esc(e.canonical_name)+' · '+esc(e.edition_date)+'</h2><small>'+esc(e.edition_variant)+' · stav zdroje '+esc(e.source_status)+'</small>';
if(['FAILED','BLOCKED','RETRY'].includes(e.technician_status)||['EDITION_COLLISION','IDENTITY_UNRESOLVED'].includes(e.source_status))h+='<p class="next warn">Příprava vyžaduje kontrolu operátora. Stav: '+esc(e.technician_status||e.source_status)+'</p>';
h+='<div class="steps"><div class="step"><b>1 · Příprava PDF</b>'+ (e.prepared?'Podklady uložené':'Příprava nepotvrzená')+'<br><small>'+esc(e.technician_status)+'</small>'+'</div><div class="step"><b>2 · Čtení stránek</b>'+esc(e.page_receipts)+' / '+esc(e.page_count)+' stran s v4 receipt</div><div class="step"><b>3 · Výběr podkladů</b>'+e.selections.length+' evidovaných výběrů</div></div>';
h+='<p class="muted">Počet stran vychází z potvrzených zápisů Bridge v4, včetně revisions. Nejde o nový readback Storage ani potvrzení úplnosti nebo právě běžící práce Chatu.</p>';
if(!e.selections.length)h+='<p class="next"><b>Co teď:</b> '+(e.prepared?'Pokračovat v Ingestoru, ověřit stránky a accepted manifest.':'Prověřit přípravu zdroje v Technicianu.')+'</p>';
h+=e.selections.map(s=>'<article><h3>'+esc(s.manifest_id)+' · <span class="ok">'+esc(s.label)+'</span></h3><div class="steps"><div class="step"><b>4 · Sestavení</b>'+esc(s.articles)+' uložených článků</div><div class="step"><b>5 · Indexace</b>'+esc(s.indexed)+' / '+esc(s.articles)+' článků<br>'+esc(s.chunks)+' textových úseků</div><div class="step"><b>6 · Vyhledávání</b>'+ (s.requests.some(r=>r.operation==='search'&&r.state==='COMPLETE'&&r.result_status==='PASS')?'Technické volání prošlo':'Bez úspěšného receipt')+'<br><small>Kvalita vyžaduje vlastní hodnocení.</small></div></div><p class="next"><b>Co teď:</b> '+esc(s.next_step)+'</p><details><summary>Historie běhů a přesná identita výběru</summary><p><code>source: '+esc(e.source_id)+'<br>manifest SHA: '+esc(s.manifest_sha256)+'</code></p><p class="muted">Nejvýše 50 posledních běhů tohoto výběru. COMPLETE znamená dokončené volání; PASS je technický výsledek. Běhy z CLI zde nemusí být.</p><div class="scroll"><table><thead><tr><th>Čas</th><th>Krok</th><th>Režim</th><th>Stav / výsledek</th></tr></thead><tbody>'+s.requests.map(r=>'<tr><td>'+esc(date(r.updated_at))+'</td><td>'+esc(names[r.operation]||r.operation)+'<br><code>'+esc(r.request_id)+'</code></td><td>'+esc(r.operation==='search'?'Dotaz':r.persist_requested==='true'?'Zápis vyžádán':r.persist_requested==='false'?'Plán bez zápisu':'Neznámý')+'</td><td>'+esc(r.state)+' / '+esc(r.result_status)+'<br><small>'+esc(JSON.stringify(r.counts||{}))+'</small></td></tr>').join('')+'</tbody></table></div></details></article>').join('');return h+'</section>';
}).join('')||'<p>Žádná vydání v tomto přehledu.</p>';}
async function refresh(){try{const r=await fetch('/api/dashboard',{cache:'no-store'});if(!r.ok)throw Error();data=await r.json();const chosen=filter.value;filter.innerHTML='<option value="all">Všechna</option>'+data.editions.map(e=>'<option value="'+esc(e.source_id)+'">'+esc(e.canonical_name)+' · '+esc(e.edition_date)+'</option>').join('');filter.value=chosen;if(!filter.value)filter.value='all';document.getElementById('stamp').textContent='Poslední načtení: '+date(data.observed_at);err.textContent='';render();}catch{err.textContent='Stav se nepodařilo načíst. Zobrazené údaje mohou být zastaralé; ověř přihlášení a připojení.';}}
filter.onchange=render;document.getElementById('refresh').onclick=refresh;refresh();setInterval(refresh,30000);
</script></main></body></html>'''


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, body, content_type='application/json; charset=utf-8', challenge=False):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        if challenge:
            self.send_header('WWW-Authenticate', 'Basic realm="Business Brief", charset="UTF-8"')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        user, password = os.getenv('DASHBOARD_USER'), os.getenv('DASHBOARD_PASSWORD')
        if user and password:
            expected = 'Basic ' + base64.b64encode(f'{user}:{password}'.encode()).decode()
            if not hmac.compare_digest(self.headers.get('Authorization', '').encode(), expected.encode()):
                return self.respond(401, b'{"error":"AUTH_REQUIRED"}', challenge=True)
        elif self.path == '/api/dashboard':
            return self.respond(503, b'{"error":"DASHBOARD_AUTH_NOT_CONFIGURED"}')
        if self.path == '/':
            return self.respond(200, HTML.encode(), 'text/html; charset=utf-8')
        if self.path != '/api/dashboard':
            return self.respond(404, b'{"error":"NOT_FOUND"}')
        try:
            body = json.dumps(snapshot(), ensure_ascii=False, default=str).encode()
        except Exception:
            # Never return DB exceptions, DSNs, upstream text or secrets.
            return self.respond(503, b'{"error":"SNAPSHOT_UNAVAILABLE"}')
        self.respond(200, body)


def main():
    ThreadingHTTPServer(('0.0.0.0', int(os.getenv('PORT', '8080'))), Handler).serve_forever()


if __name__ == '__main__':
    main()
