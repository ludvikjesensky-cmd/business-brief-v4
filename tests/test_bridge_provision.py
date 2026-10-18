import copy
import httpx
import pytest
from bridge.core import Storage
from bridge.provision import configure_output,LIMIT
from test_bridge import assert_failure

@pytest.mark.parametrize('mode',['json-only','unrestricted','larger','new','public','bad-readback'])
def test_bucket_capability(mode):
    original={'public':mode=='public','allowed_mime_types':['application/json','text/plain'],'file_size_limit':5*1024*1024}
    if mode=='unrestricted':original.update(allowed_mime_types=None,file_size_limit=None)
    if mode=='larger':original.update(allowed_mime_types=['application/json','image/png'],file_size_limit=2*LIMIT)
    current=copy.deepcopy(original);calls=[]
    def handle(req):
        import json
        calls.append(req)
        if req.method=='GET':
            if mode=='new' and len(calls)==1:return httpx.Response(404)
            return httpx.Response(200,json=current)
        if mode!='bad-readback':current.update(json.loads(req.content))
        return httpx.Response(200,json={})
    s=Storage('https://example.test','secret');s.client=httpx.Client(transport=httpx.MockTransport(handle))
    if mode in ['public','bad-readback']:
        assert_failure('CONFIGURATION_MISSING',lambda:configure_output(s,'page-ingest'))
        return
    configure_output(s,'page-ingest')
    assert current['public'] is False
    if mode in ['unrestricted','larger']:assert current==original and all(r.method=='GET' for r in calls)
    else:
        assert 'image/png' in current['allowed_mime_types'] and current['file_size_limit']==LIMIT
        if mode=='json-only':assert 'text/plain' in current['allowed_mime_types']
