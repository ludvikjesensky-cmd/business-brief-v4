"""Read-only technical acceptance, exactly page 1; never submits Page JSON."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import httpx

BASE='https://ingestor-access-bridge-production.up.railway.app'
def main():
    credential_file,output=sys.argv[1:]
    token=json.loads(Path(credential_file).read_text())['read_token']
    client=httpx.Client(timeout=90,follow_redirects=False)
    headers={'Authorization':'Bearer '+token}
    def get(path):
        r=client.get(BASE+path,headers=headers)
        assert r.status_code==200, f'HTTP {r.status_code}; '+r.json().get('error',{}).get('code','UNKNOWN')
        d=r.json();assert r.headers['X-Request-ID']==d['request_id'];assert r.headers['Cache-Control']=='no-store'
        return d
    assert client.get(BASE+'/health').status_code==401
    health=get('/health');ready=get('/ready')
    current=get('/ingestor-v2/source/current?publication=the-wall-street-journal')
    source=current['source'];page=get('/ingestor-v2/source/'+source['source_id']+'/page/1')
    assert page['source']==source and page['page_no']==1
    artifacts={'manifest':page['manifest'],'page_image':page['page_image']['artifact'],'prepared_evidence':page['prepared_evidence']['artifact'],'original_pdf':page['original_pdf']}
    result={};manifest=None
    for label,a in artifacts.items():
        expiry=datetime.fromisoformat(a['expires_at'].replace('Z','+00:00'));assert expiry>datetime.now(timezone.utc)
        assert a['url'].startswith('https://')
        r=client.get(a['url']);assert r.status_code==200, 'artifact download failed: '+label
        data=r.content;h=hashlib.sha256(data).hexdigest();assert h==a['sha256'] and len(data)==a['byte_size']
        if label=='manifest':manifest=json.loads(data)
        if label in ('prepared_evidence','original_pdf'):assert data.startswith(b'%PDF-')
        if label=='page_image':assert data.startswith(b'\x89PNG\r\n\x1a\n')
        result[label]={k:a[k] for k in ('bucket','storage_key','sha256','byte_size','media_type')}
    assert manifest['source_id']=='sha256:'+source['source_sha256']
    assert manifest['source_sha256']==source['source_sha256']
    assert source['source_id']!=manifest['source_id']
    assert result['manifest']['sha256']==source['source_bundle_sha256']
    assert result['original_pdf']['sha256']==source['source_sha256']
    assert page['prepared_evidence']['pdf_page_no']==1
    assert page['prepared_evidence']['ocr']['prepared_pdf_path']==result['prepared_evidence']['storage_key']
    report={'status':'PASS','checked_at':datetime.now(timezone.utc).isoformat(),'service':BASE,'health':health['status'],'readiness':ready['status'],'source':source,'page_no':1,'artifacts':result,'uuid_sha_manifest_mapping':'PASS','client_download_hashes':'PASS','unauthenticated_access':401,'production_post_requests':0,'semantic_ingestion':False,'page_json_saved':False,'transport':'authenticated Codex HTTPS client; ChatGPT connector not provisioned'}
    Path(output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('ACCEPTANCE_FAILED '+type(e).__name__+(' '+str(e) if isinstance(e,AssertionError) else ''),file=sys.stderr);sys.exit(1)
