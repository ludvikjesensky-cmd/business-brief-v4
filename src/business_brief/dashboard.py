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
@import url('https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&family=Source+Sans+3:wght@400;500;600;700&display=swap');
:root{color-scheme:light;--paper:#f5f1e8;--surface:#eeeae0;--ink:#20251f;--muted:#64685f;--red:#a33123;--rule:#cdcbbf;--serif:'Newsreader',Georgia,'Times New Roman',serif;--sans:'Source Sans 3',Arial,Helvetica,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px var(--sans);-webkit-font-smoothing:antialiased}main{max-width:1240px;margin:auto;padding:0 56px 44px}header{display:flex;justify-content:space-between;gap:24px;align-items:center;padding:28px 0;border-bottom:1px solid var(--ink)}.brand{font-family:var(--serif);font-size:32px;font-weight:700;letter-spacing:-1.2px;line-height:1}.brand span{color:var(--red)}.header-meta{text-align:right;font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:var(--muted)}.intro{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:end;gap:24px;padding:38px 0 28px;border-bottom:1px solid var(--rule)}.eyebrow{font-size:11px;letter-spacing:1.6px;text-transform:uppercase;color:var(--red);font-weight:600}h1,h2,h3,p{margin:0}h1,h2,h3{font-family:var(--serif)}h1{font-size:clamp(40px,5vw,66px);line-height:1.04;letter-spacing:-2px;font-weight:500;margin:14px 0 12px}h2{font-size:clamp(29px,3vw,40px);line-height:1.1;letter-spacing:-1px;font-weight:600;margin:0 0 8px}h3{font-size:25px;line-height:1.2;letter-spacing:-.4px;font-weight:600;margin:20px 0 0;overflow-wrap:anywhere}p{line-height:1.55}.muted,small{color:var(--muted)}.intro p{max-width:650px}.controls{display:flex;justify-content:space-between;align-items:end;gap:16px;padding:22px 0 8px}.controls label{font-size:11px;letter-spacing:1.3px;text-transform:uppercase;font-weight:600;color:var(--muted)}.controls select{display:block;margin-top:7px}.stamp{font-size:13px;color:var(--muted)}.card{border-top:1px solid var(--ink);padding:26px 0 32px;margin:22px 0 0}.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin:22px 0}.step{padding:20px 22px 20px 0;line-height:1.45;min-width:0}.step+.step{border-left:1px solid var(--rule);padding-left:22px}.step b{display:block;margin-bottom:8px;font-size:11px;letter-spacing:1.1px;text-transform:uppercase;font-weight:700;color:var(--red)}.step small{font-size:13px}.card>p.muted{font-size:13px;max-width:900px}.next{border-left:3px solid var(--red);padding:14px 18px;background:#ebe6da;margin:18px 0}.next b{color:var(--red)}.ok{color:#46644b}.warn,#error{color:#a33123}button,select{font:600 14px var(--sans);color:var(--ink);background:transparent;border:1px solid var(--ink);padding:10px 14px;border-radius:0;cursor:pointer}button{background:var(--ink);color:var(--paper);min-width:110px}button:hover{background:var(--red);border-color:var(--red)}select{min-width:240px;max-width:100%}button:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--red);outline-offset:3px}details{margin-top:18px;border-top:1px solid var(--rule);padding-top:16px}summary{cursor:pointer;font-weight:600}details p{margin:12px 0}details .muted{font-size:13px}code{overflow-wrap:anywhere;font-size:12px}.scroll{overflow:auto}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:12px 8px 12px 0;border-bottom:1px solid var(--rule);vertical-align:top}th{font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--muted)}#error{font-weight:600;margin-top:12px}.footer{border-top:1px solid var(--rule);margin-top:36px;padding-top:20px;font-size:13px;line-height:1.6}.footer strong{font-family:var(--serif);font-size:21px;color:var(--ink)}
/* Compact operational overview while keeping the editorial typography. */
header{padding:18px 0}.brand{font-size:28px}.intro{padding:22px 0 18px}h1{font-size:clamp(34px,4vw,48px);margin:7px 0}h2{font-size:28px;line-height:1.1;margin-bottom:4px}h3{font-size:19px;margin:10px 0 0}.controls{padding:14px 0 4px}.card{padding:14px 0 16px;margin:10px 0 0}.steps{margin:10px 0}.step{padding:8px 12px 8px 0;line-height:1.25;font-size:14px}.step+.step{padding-left:12px}.step b{margin-bottom:3px;font-size:10px}.step small{font-size:12px}.next{padding:7px 12px;margin:8px 0;font-size:14px;line-height:1.35}details{margin-top:8px;padding-top:7px;font-size:14px}.footer{margin-top:20px;padding-top:12px}
@media(max-width:800px){main{padding:0 24px 34px}.intro{padding-top:30px}.steps{grid-template-columns:repeat(3,minmax(0,1fr))}.step,.step+.step{padding:8px 8px 8px 0}.step+.step{border-left:1px solid var(--rule);padding-left:8px}.card{padding-top:14px}.controls{align-items:start;flex-direction:column}.stamp{order:2}}
@media(max-width:480px){main{padding:0 18px 30px}.brand{font-size:27px}.header-meta{font-size:9px;letter-spacing:.7px}.intro{grid-template-columns:1fr;gap:18px}h1{font-size:34px;letter-spacing:-1px}h2{font-size:25px}h3{font-size:19px}.intro button{justify-self:start}.controls,select{width:100%}.steps{grid-template-columns:1fr}.step,.step+.step{padding:6px 0;border-left:0}.step+.step{border-top:1px solid var(--rule)}.next{padding:7px 10px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style></head><body><main><header><div class="brand">Business Brief<span>.</span></div><div class="header-meta">Deep / Memory<br>Provozní přehled</div></header>
<div class="intro"><div><div class="eyebrow">Přehled zpracování</div><h1>Deep Read Processing</h1><p class="muted">Sleduj cestu vydání od přípravy PDF po vyhledávání. Přehled ukazuje uložené podklady a další krok.</p></div><button id="refresh">Obnovit přehled ↻</button></div>
<div class="controls"><label>Vybrat vydání <select id="filter"><option value="all">Všechna vydání</option></select></label><p id="stamp" class="stamp"></p></div><p id="error" role="alert"></p><div id="app"></div>
<footer class="footer muted"><strong>Business Brief<span style="color:var(--red)">.</span></strong><p>Pouze čtení · nejvýše 100 naposledy přijatých aktivních zdrojů. Technician se přes Chat zatím bezpečně spustit nedá. Fast Editorial má samostatný proces.</p></footer>
<script>
const app=document.getElementById('app'),err=document.getElementById('error'),filter=document.getElementById('filter');let data;
const esc=v=>String(v??'—').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const date=v=>v?new Date(v).toLocaleString('cs-CZ',{timeZone:'Europe/Prague'}):'—';
const names={assembler:'Sestavení článků',indexer:'Indexace',search:'Vyhledávání'};
function render(){app.innerHTML=(data.editions||[]).filter(e=>filter.value==='all'||e.source_id===filter.value).map(e=>{
let h='<section class="card"><h2>'+esc(e.canonical_name)+' · '+esc(e.edition_date)+'</h2><small>'+esc(e.edition_variant)+' · stav zdroje '+esc(e.source_status)+'</small>';
if(['FAILED','BLOCKED','RETRY'].includes(e.technician_status)||['EDITION_COLLISION','IDENTITY_UNRESOLVED'].includes(e.source_status))h+='<p class="next warn">Příprava vyžaduje kontrolu operátora. Stav: '+esc(e.technician_status||e.source_status)+'</p>';
h+='<div class="steps"><div class="step"><b>1 · TECHNICIAN</b>'+ (e.prepared?'Podklady uložené':'Příprava nepotvrzená')+'<br><small>'+esc(e.technician_status)+'</small>'+'</div><div class="step"><b>2 · INGESTOR</b>'+esc(e.page_receipts)+' / '+esc(e.page_count)+' stran s v4 receipt</div><div class="step"><b>3 · SELECTION</b>'+e.selections.length+' evidovaných výběrů</div></div>';
h+='<p class="muted">Počet stran vychází z potvrzených zápisů Bridge v4, včetně revisions. Nejde o nový readback Storage ani potvrzení úplnosti nebo právě běžící práce Chatu.</p>';
if(!e.selections.length)h+='<p class="next"><b>Co teď:</b> '+(e.prepared?'Pokračovat v Ingestoru, ověřit stránky a accepted manifest.':'Prověřit přípravu zdroje v Technicianu.')+'</p>';
h+=e.selections.map(s=>'<article><h3>'+esc(s.manifest_id)+' · <span class="'+(s.label==='Indexováno'?'ok':'warn')+'">'+esc(s.label)+'</span></h3><div class="steps"><div class="step"><b>4 · ASSEMBLER</b>'+esc(s.articles)+' uložených článků</div><div class="step"><b>5 · INDEXER</b>'+esc(s.indexed)+' / '+esc(s.articles)+' článků<br>'+esc(s.chunks)+' textových úseků</div><div class="step"><b>6 · RETRIEVAL</b>'+ (s.requests.some(r=>r.operation==='search'&&r.state==='COMPLETE'&&r.result_status==='PASS')?'Technické volání prošlo':'Bez úspěšného receipt')+'<br><small>Kvalita vyžaduje vlastní hodnocení.</small></div></div><p class="next"><b>Co teď:</b> '+esc(s.next_step)+'</p><details><summary>Historie běhů a přesná identita výběru</summary><p><code>source: '+esc(e.source_id)+'<br>manifest SHA: '+esc(s.manifest_sha256)+'</code></p><p class="muted">Nejvýše 50 posledních běhů tohoto výběru. COMPLETE znamená dokončené volání; PASS je technický výsledek. Běhy z CLI zde nemusí být.</p><div class="scroll"><table><thead><tr><th>Čas</th><th>Krok</th><th>Režim</th><th>Stav / výsledek</th></tr></thead><tbody>'+s.requests.map(r=>'<tr><td>'+esc(date(r.updated_at))+'</td><td>'+esc(names[r.operation]||r.operation)+'<br><code>'+esc(r.request_id)+'</code></td><td>'+esc(r.operation==='search'?'Dotaz':r.persist_requested==='true'?'Zápis vyžádán':r.persist_requested==='false'?'Plán bez zápisu':'Neznámý')+'</td><td>'+esc(r.state)+' / '+esc(r.result_status)+'<br><small>'+esc(JSON.stringify(r.counts||{}))+'</small></td></tr>').join('')+'</tbody></table></div></details></article>').join('');return h+'</section>';
}).join('')||'<p>Žádná vydání v tomto přehledu.</p>';}
async function refresh(){try{const r=await fetch('/api/dashboard',{cache:'no-store'});if(!r.ok)throw Error();data=await r.json();const chosen=filter.value;filter.innerHTML='<option value="all">Všechna vydání</option>'+data.editions.map(e=>'<option value="'+esc(e.source_id)+'">'+esc(e.canonical_name)+' · '+esc(e.edition_date)+'</option>').join('');filter.value=chosen;if(!filter.value)filter.value='all';document.getElementById('stamp').textContent='Poslední načtení: '+date(data.observed_at);err.textContent='';render();}catch{err.textContent='Stav se nepodařilo načíst. Zobrazené údaje mohou být zastaralé; ověř přihlášení a připojení.';}}
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
