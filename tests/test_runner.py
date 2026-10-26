from contextlib import contextmanager
from types import SimpleNamespace
from uuid import uuid4
import pytest
from bridge.runner import Runner, validate, CONTRACT
from bridge.server import Application
from bridge.validation import Failure

SID = str(uuid4())
KEY = str(uuid4())
BODY = dict(contract_version=CONTRACT, operation='assembler', source_id=SID,
            manifest_id='accepted-r1', manifest_sha='a'*64, persist=False)
P = dict(id='chat', token='x'*43, scopes=['source:read','pipeline:read','pipeline:run'], publications=['wsj'])

@pytest.mark.parametrize('change', [dict(source_id='../x'),dict(manifest_sha='A'*64),dict(manifest_id='../x'),dict(persist='false'),dict(secret='x'),dict(operation='shell'),dict(contract_version='x')])
def test_validation(change):
    with pytest.raises(Failure): validate({**BODY, **change})

@pytest.mark.parametrize('operation', ['assembler','indexer','status','search','technician'])
def test_contract(operation):
    body={k:v for k,v in BODY.items() if k!='persist'}
    body['operation']=operation
    if operation in {'assembler','indexer'}: body['persist']=False
    if operation=='search': body.update(query='bank rates',limit=5)
    assert validate(body)==operation

class DB:
    @contextmanager
    def connection(self): yield self
    def authorize(self,c,sid,allowed):
        if 'wsj' not in allowed: raise Failure('SOURCE_NOT_FOUND',404)

@pytest.mark.parametrize('scopes', [[], ['source:read'], ['source:read','pipeline:read']])
def test_scopes(scopes):
    with pytest.raises(Failure,match='FORBIDDEN'):
        Runner(SimpleNamespace(db=DB())).execute(BODY,{**P,'scopes':scopes},KEY)

def test_persist_disabled(monkeypatch):
    monkeypatch.delenv('BRIDGE_PIPELINE_PERSIST',raising=False)
    with pytest.raises(Failure,match='PERSIST_DISABLED'):
        Runner(SimpleNamespace(db=DB())).execute({**BODY,'persist':True},P,KEY)

def test_publication_concealment():
    with pytest.raises(Failure,match='SOURCE_NOT_FOUND'):
        Runner(SimpleNamespace(db=DB())).execute(BODY,{**P,'publications':['ft']},KEY)

def test_technician_not_global_drain():
    body={k:v for k,v in BODY.items() if k!='persist'}
    body['operation']='technician'
    with pytest.raises(Failure,match='TECHNICIAN_SOURCE_SCOPED_UNAVAILABLE'):
        Runner(SimpleNamespace(db=DB())).execute(body,P,KEY)

def test_http_disabled(monkeypatch):
    monkeypatch.delenv('BRIDGE_PIPELINE_ENABLED',raising=False)
    app=Application(None,[P])
    with pytest.raises(Failure,match='RUNNER_DISABLED'):
        app.dispatch('POST','/deep-runner/v1/tool',{'Authorization':'Bearer '+P['token']},lambda n:b'')

def test_http_runner_does_not_require_page_write(monkeypatch):
    import json
    monkeypatch.setenv('BRIDGE_PIPELINE_ENABLED','1')
    monkeypatch.setattr(Runner,'execute',lambda self,b,p,k:(202,{'status':'ACCEPTED'}))
    raw=json.dumps(BODY).encode()
    assert Application(None,[P]).dispatch('POST','/deep-runner/v1/tool',{'Authorization':'Bearer '+P['token'],'Content-Type':'application/json','Content-Length':str(len(raw))},lambda n:raw)[0]==202

def test_search_selection_filter(monkeypatch):
    from business_brief import index_search,indexer_runtime
    monkeypatch.setattr(indexer_runtime.SupabaseIndexStore,'from_env',lambda:SimpleNamespace(select_articles=lambda **kw:[{'article_id':'allowed','artifact_sha256':'a'*64}]))
    good={'article_id':'allowed','article_record_sha256':'a'*64}
    monkeypatch.setattr(index_search,'run',lambda *a:{'vector':[{'article_id':'secret','article_record_sha256':'b'*64},good], 'lexical':[]})
    result=Runner(None).run({**BODY,'operation':'search','query':'bank','limit':5},P)
    assert result['vector']==[good]
    assert 'secret' not in str(result)

class Cursor:
    def __init__(self,row=None,rows=None): self.row,self.rows=row,rows
    def fetchone(self): return self.row
    def fetchall(self): return self.rows or []

class Ledger(DB):
    def __init__(self): self.rows={}; self.locked=True
    def commit(self): pass
    def execute(self,sql,args=()):
        if 'pg_try_advisory_lock' in sql: return Cursor({'ok':self.locked})
        if sql.startswith('select state'): return Cursor(self.rows[args])
        if sql.startswith('select *'): return Cursor(self.rows.get(args))
        if sql.startswith('insert into'):
            pid,key,digest,sid,mid,msha,op=args
            self.rows[pid,key]=dict(request_sha256=digest,state='RUNNING',result=None)
        if "set state='COMPLETE'" in sql:
            result,pid,key=args
            self.rows[pid,key].update(state='COMPLETE',result=result.obj)
        if "set state='UNKNOWN'" in sql:
            self.rows[args].update(state='UNKNOWN')
        return Cursor()

@pytest.fixture
def ledger_runner(monkeypatch):
    from bridge import runner
    monkeypatch.setattr(runner.LocalAssemblyClient,'assembly_input',lambda *a:{})
    # Execute worker immediately under a test DB; production uses a separate session/thread.
    class Thread:
        def __init__(self,target,args,**kw): self.target,self.args=target,args
        def start(self): self.target(*self.args)
    monkeypatch.setattr(runner.threading,'Thread',Thread)
    db=Ledger(); r=Runner(SimpleNamespace(db=db))
    monkeypatch.setattr(r,'run',lambda *a:{'status':'PASS','counts':{'eligible':1}})
    return r,db

def test_durable_accept_complete_replay_and_conflict(ledger_runner):
    r,db=ledger_runner
    assert r.execute(BODY,P,KEY)[0]==202
    assert db.rows[P['id'],KEY]['state']=='COMPLETE'
    code,result=r.execute(BODY,P,KEY)
    assert code==200 and result['replayed'] and result['status']=='PASS'
    with pytest.raises(Failure,match='IDEMPOTENCY_CONFLICT'):
        r.execute({**BODY,'manifest_sha':'b'*64},P,KEY)

def test_runtime_failure_is_uncertain_and_redacted(ledger_runner,monkeypatch):
    r,db=ledger_runner
    def fail(*a): raise RuntimeError('secret-token')
    monkeypatch.setattr(r,'run',fail)
    assert r.execute(BODY,P,KEY)[0]==202
    assert db.rows[P['id'],KEY]['state']=='UNKNOWN'
    assert 'secret-token' not in str(db.rows)
    monkeypatch.setattr(r,'run',lambda *a:{'status':'PASS'})
    assert r.execute(BODY,P,KEY)[0]==202
    assert db.rows[P['id'],KEY]['state']=='COMPLETE'

def test_source_busy(ledger_runner):
    r,db=ledger_runner; db.locked=False
    with pytest.raises(Failure,match='WRITE_IN_PROGRESS'): r.execute(BODY,P,KEY)
    assert not db.rows

def test_chat_adapter_defaults_and_no_secret_errors():
    from bridge.chat_tools import ChatTools, tool_definitions
    args={k:BODY[k] for k in ('source_id','manifest_id','manifest_sha')}
    captured=[]
    def transport(path,body,headers):
        captured.append((path,body,headers))
        raise RuntimeError('Bearer SUPER_SECRET')
    result=ChatTools(transport).call('run_assembler',args)
    assert captured[0][1]['persist'] is False
    assert result['request_id']==captured[0][2]['Idempotency-Key']
    assert result['status']=='UNKNOWN' and 'SUPER_SECRET' not in str(result)
    assert len(tool_definitions())==5

def test_standalone_entrypoint_fails_closed():
    from business_brief.runner_runtime import main
    with pytest.raises(SystemExit,match='Standalone runner superseded'): main()
