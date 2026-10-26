import base64
import os
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from business_brief import dashboard

class ProcessTests(unittest.TestCase):
    def selection(self, **kwargs):
        return {**dict(articles=21,indexed=21,review_articles=0,requests=[]), **kwargs}

    def test_indexed_is_not_benchmark_pass(self):
        label, step = dashboard.describe_selection(self.selection())
        self.assertEqual(label,'Indexováno')
        self.assertIn('vyhodnotit',step)

    def test_plan_is_not_persistence(self):
        s=self.selection(articles=0,indexed=0,requests=[dict(operation='assembler',state='COMPLETE',result_status='PASS')])
        self.assertEqual(dashboard.describe_selection(s)[0],'Plán sestavení prošel')

    def test_uncertain_review_missing_results_not_complete(self):
        for state,result in [('RUNNING',None),('UNKNOWN',None),('COMPLETE','NEEDS_REVIEW'),('COMPLETE','BLOCKED'),('COMPLETE',None),('FAILED',None)]:
            s=self.selection(requests=[dict(operation='indexer',state=state,result_status=result)])
            self.assertNotEqual(dashboard.describe_selection(s)[0],'Indexováno')

    def test_latest_result_per_operation(self):
        s=self.selection(requests=[dict(operation='indexer',state='COMPLETE',result_status='PASS'),dict(operation='indexer',state='FAILED',result_status=None)])
        self.assertEqual(dashboard.describe_selection(s)[0],'Indexováno')

    def test_partial_index_and_review(self):
        self.assertEqual(dashboard.describe_selection(self.selection(indexed=20))[0],'Články uložené')
        self.assertEqual(dashboard.describe_selection(self.selection(review_articles=1))[0],'Články ke kontrole')

    def test_auth_redaction_routes_and_missing_configuration(self):
        with patch.dict(os.environ,{'DASHBOARD_USER':'owner','DASHBOARD_PASSWORD':'test-only'}):
            server=dashboard.ThreadingHTTPServer(('127.0.0.1',0),dashboard.Handler)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            base=f'http://127.0.0.1:{server.server_port}'
            auth='Basic '+base64.b64encode(b'owner:test-only').decode()
            def call(path='/api/dashboard',authenticated=True):
                return urlopen(Request(base+path,headers={'Authorization':auth} if authenticated else {}))
            try:
                with self.assertRaises(HTTPError) as error:call(authenticated=False)
                self.assertEqual(error.exception.code,401)
                with patch.object(dashboard,'snapshot',return_value={'editions':[]}):
                    with call() as response:
                        self.assertEqual(response.read(),b'{"editions": []}')
                        self.assertEqual(response.headers['Cache-Control'],'no-store')
                with patch.object(dashboard,'snapshot',side_effect=RuntimeError('secret-dsn')):
                    with self.assertRaises(HTTPError) as error:call()
                    self.assertNotIn(b'secret',error.exception.read())
                with self.assertRaises(HTTPError) as error:call('/missing')
                self.assertEqual(error.exception.code,404)
                with patch.dict(os.environ,{'DASHBOARD_USER':'','DASHBOARD_PASSWORD':''}):
                    with self.assertRaises(HTTPError) as error:call()
                    self.assertEqual(error.exception.code,503)
            finally:server.shutdown();server.server_close();thread.join()
