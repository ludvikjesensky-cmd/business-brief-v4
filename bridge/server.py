"""Small HTTP service. No worker imports, model calls, or editorial processing."""
import hmac
import json
import os
import re
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl
from uuid import uuid4
from .core import Bridge, Database, Storage, CONTRACT
from .validation import Failure, require, uuid, sha, fields, page_schema, strict_json

MAX_BODY=5*1024*1024
RETRYABLE={'RATE_LIMITED','UPSTREAM_UNAVAILABLE','WRITE_IN_PROGRESS','PERSISTENCE_UNVERIFIED'}

class Application:
    def __init__(self,bridge,principals): self.bridge,self.principals=bridge,principals
    def auth(self,header,write):
        principal=None
        if header and header.startswith('Bearer '):
            token=header[7:]
            for p in self.principals:
                if hmac.compare_digest(token.encode('utf-8'),p['token'].encode('utf-8')): principal=p
        if not principal: raise Failure('UNAUTHENTICATED',401)
        scopes={'source:read','page:write'} if write else {'source:read'}
        require(scopes.issubset(set(principal['scopes'])),'FORBIDDEN',403)
        return principal
    def dispatch(self,method,path,headers,read):
        p=self.auth(headers.get('Authorization'),method=='POST')
        url=urlsplit(path); args=parse_qsl(url.query,keep_blank_values=True)
        allowed=p['publications']
        if url.path in ('/health','/ready'):
            require(method=='GET' and not args,'INVALID_REQUEST',400)
            if url.path=='/ready':
                with self.bridge.db.connection() as c:
                    c.execute('select 1 from bridge_private.bindings limit 1')
                self.bridge.storage.private(self.bridge.source_bucket); self.bridge.storage.private(self.bridge.output_bucket)
            return 200,{'status':'READY'}
        if method=='GET':
            require(headers.get('Content-Length','0')=='0' and not headers.get('Transfer-Encoding'),'INVALID_REQUEST',400)
            if url.path=='/ingestor-v2/source/current':
                require(len(args)==1 and args[0][0]=='publication','INVALID_REQUEST',400)
                return 200,self.bridge.current(args[0][1],allowed)
            match=re.fullmatch('/ingestor-v2/source/([^/]+)/page/([^/]+)',url.path)
            require(bool(match) and not args,'INVALID_REQUEST',400)
            sid,no=match.groups()
            try: uuid(sid)
            except Failure: raise Failure('INVALID_REQUEST',400) from None
            require(bool(re.fullmatch('[1-9][0-9]{0,3}',no)),'INVALID_REQUEST',400)
            return 200,self.bridge.page(sid,int(no),allowed)
        require(method=='POST' and url.path=='/ingestor-v2/page' and not args,'INVALID_REQUEST',400)
        require(headers.get('Content-Type','').lower()=='application/json' and headers.get('Content-Encoding','identity')=='identity','UNSUPPORTED_MEDIA_TYPE',415)
        require(not headers.get('Transfer-Encoding'),'INVALID_REQUEST',400)
        try: length=int(headers.get('Content-Length',''))
        except ValueError: raise Failure('INVALID_REQUEST',400) from None
        require(0<=length<=MAX_BODY,'PAYLOAD_TOO_LARGE',413)
        key=headers.get('Idempotency-Key')
        try: uuid(key)
        except Failure: raise Failure('INVALID_REQUEST',400) from None
        raw=read(length); require(len(raw)==length,'INVALID_JSON',400)
        body=strict_json(raw)
        # Conceal unauthorized resources before detailed body validation whenever selectable.
        if type(body) is dict and type(body.get('page')) is dict:
            page=body['page']; pub=page.get('publication'); src=page.get('source')
            if type(pub) is dict and type(pub.get('publication_id')) is str and pub['publication_id'] not in allowed: raise Failure('SOURCE_NOT_FOUND',404)
            if type(src) is dict and type(src.get('source_id')) is str:
                try: uuid(src['source_id'])
                except Failure: pass
                else:
                    with self.bridge.db.connection() as c: self.bridge.db.authorize(c,src['source_id'],allowed)
        fields(body,'contract_version source_bundle_sha256 page')
        require(body['contract_version']==CONTRACT,'INVALID_REQUEST',400); sha(body['source_bundle_sha256']); page_schema(body['page'])
        return self.bridge.post(body,key,p['id'],allowed)

class Handler(BaseHTTPRequestHandler):
    app=None
    protocol_version='HTTP/1.1'
    def setup(self):
        super().setup(); self.connection.settimeout(35)
    def log_message(self,*args): pass  # Never log paths, credentials, signed capabilities or payloads.
    def handle_request(self):
        rid=str(uuid4()); self.close_connection=True
        try:
            # Railway terminates TLS; direct cleartext public traffic is rejected.
            require(self.headers.get('X-Forwarded-Proto')=='https','INVALID_REQUEST',400)
            for name in ['Authorization','Content-Length','Content-Type','Idempotency-Key','X-Forwarded-Proto']:
                require(len(self.headers.get_all(name,[]))<=1,'INVALID_REQUEST',400)
            code,body=self.app.dispatch(self.command,self.path,self.headers,self.rfile.read)
        except Failure as e:
            code=e.http; body={'status':'BLOCKED','error':{'code':e.code,'message':e.code,'retryable':e.code in RETRYABLE,'persistence':e.persistence,'details':[]}}
        except Exception:
            code=500; body={'status':'BLOCKED','error':{'code':'INTERNAL_ERROR','message':'Internal error','retryable':False,'persistence':'UNKNOWN' if self.command=='POST' else 'NOT_WRITTEN','details':[]}}
        body={'contract_version':CONTRACT,'request_id':rid,**body}
        data=json.dumps(body,ensure_ascii=False,separators=(',',':')).encode()
        self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.send_header('X-Request-ID',rid); self.send_header('Content-Length',str(len(data))); self.send_header('Connection','close')
        if code==503 and body.get('error',{}).get('retryable'): self.send_header('Retry-After','5')
        self.end_headers(); self.wfile.write(data)
    do_GET=handle_request
    do_POST=handle_request
    do_PUT=handle_request
    do_DELETE=handle_request

def main():
    names=['BRIDGE_DATABASE_URL','SUPABASE_URL','SUPABASE_SECRET_KEY','BRIDGE_SOURCE_BUCKET','BRIDGE_PAGE_INGEST_BUCKET','BRIDGE_PRINCIPALS']
    if not all(os.environ.get(k) for k in names): raise SystemExit('CONFIGURATION_MISSING')
    principals=strict_json(os.environ['BRIDGE_PRINCIPALS'].encode())
    require(type(principals) is list and bool(principals),'CONFIGURATION_MISSING',503)
    for p in principals:
        require(set(p)=={'id','token','scopes','publications'} and type(p['token']) is str and len(p['token'])>=43 and bool(p['publications']),'CONFIGURATION_MISSING',503)
    db=Database(os.environ['BRIDGE_DATABASE_URL'],str(Path(__file__).with_name('supabase-ca.crt')))
    storage=Storage(os.environ['SUPABASE_URL'],os.environ['SUPABASE_SECRET_KEY'])
    Handler.app=Application(Bridge(db,storage,os.environ['BRIDGE_SOURCE_BUCKET'],os.environ['BRIDGE_PAGE_INGEST_BUCKET']),principals)
    ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8080'))),Handler).serve_forever()
if __name__=='__main__': main()
