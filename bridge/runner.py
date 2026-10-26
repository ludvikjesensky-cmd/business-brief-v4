"""Deep/Memory orchestration inside the existing Bridge trust boundary."""
import hashlib
import json
import os
import threading

SLOTS = threading.BoundedSemaphore(2)
from .validation import Failure, require, fields, uuid, sha, slug
from .selection import assembly_input

CONTRACT = 'deep-runner-v1'


def validate(body):
    require(type(body) is dict, 'INVALID_REQUEST', 400)
    operation = body.get('operation')
    require(operation in {'assembler', 'indexer', 'status', 'search', 'technician'}, 'INVALID_REQUEST', 400)
    extra = ' query limit' if operation == 'search' else ' persist' if operation in {'assembler', 'indexer'} else ''
    fields(body, 'contract_version operation source_id manifest_id manifest_sha' + extra)
    require(body['contract_version'] == CONTRACT, 'INVALID_REQUEST', 400)
    uuid(body['source_id']); slug(body['manifest_id']); sha(body['manifest_sha'])
    if 'persist' in body:
        require(type(body['persist']) is bool, 'INVALID_REQUEST', 400)
    if operation == 'search':
        require(type(body['query']) is str and 0 < len(body['query'].strip()) <= 2000, 'INVALID_REQUEST', 400)
        require(type(body['limit']) is int and 1 <= body['limit'] <= 20, 'INVALID_REQUEST', 400)
    return operation


class LocalAssemblyClient:
    def __init__(self, bridge, allowed):
        self.bridge, self.allowed = bridge, allowed

    def assembly_input(self, source_id, manifest_id, manifest_sha256):
        return assembly_input(self.bridge, source_id, manifest_id, manifest_sha256, self.allowed)


class Runner:
    def __init__(self, bridge):
        self.bridge = bridge

    def execute(self, body, principal, key):
        operation = validate(body)
        scopes = {'source:read', 'pipeline:read'}
        if operation in {'assembler', 'indexer'}:
            scopes.add('pipeline:run')
        if body.get('persist'):
            scopes.add('pipeline:persist')
            require(os.environ.get('BRIDGE_PIPELINE_PERSIST') == '1', 'PERSIST_DISABLED', 403)
        if operation == 'search':
            scopes.add('pipeline:search')  # Query embedding is billable even though retrieval is read-only.
        require(scopes.issubset(set(principal['scopes'])), 'FORBIDDEN', 403)
        sid = body['source_id']
        with self.bridge.db.connection() as c:
            self.bridge.db.authorize(c, sid, principal['publications'])
        if operation == 'technician':
            # Current queue drains ALL publications and has no source-scoped claim.
            raise Failure('TECHNICIAN_SOURCE_SCOPED_UNAVAILABLE', 409)
        # Revalidate the accepted exact selection on EVERY request, including replay/status.
        LocalAssemblyClient(self.bridge, principal['publications']).assembly_input(
            sid, body['manifest_id'], body['manifest_sha'])
        if operation == 'status':
            return 200, self.status(body, principal)
        uuid(key)
        digest = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        # A session advisory lock survives commits. Never use transaction pooling here.
        with self.bridge.db.connection() as c:
            locked = c.execute("select pg_try_advisory_lock(hashtextextended(%s, 937)) as ok", (sid,)).fetchone()['ok']
            require(locked, 'WRITE_IN_PROGRESS', 503)
            try:
                previous = c.execute('select * from bridge_private.pipeline_requests where principal_id=%s and request_id=%s', (principal['id'], key)).fetchone()
                if previous:
                    require(previous['request_sha256'] == digest, 'IDEMPOTENCY_CONFLICT', 409)
                    if previous['state'] == 'COMPLETE':
                        return 200, {**previous['result'], 'replayed': True}
                    # No executor currently holds the source lock. Queued duplicates
                    # recheck COMPLETE after acquiring it before runtime execution.
                else:
                    c.execute('insert into bridge_private.pipeline_requests (principal_id,request_id,request_sha256,source_id,manifest_id,manifest_sha256,operation,state) values (%s,%s,%s,%s,%s,%s,%s,\'RUNNING\')', (principal['id'], key, digest, sid, body['manifest_id'], body['manifest_sha'], operation))
                c.execute("update bridge_private.pipeline_requests set state='RUNNING', updated_at=now() where principal_id=%s and request_id=%s", (principal['id'], key))
                c.commit()
                require(SLOTS.acquire(blocking=False), 'WRITE_IN_PROGRESS', 503)
                # Executor opens its own session after this admission lock is released.
                try:
                    threading.Thread(target=self.worker_entry, args=(body, principal, key), daemon=True).start()
                except Exception:
                    SLOTS.release()
                    raise Failure('UPSTREAM_UNAVAILABLE', 503, persistence='UNKNOWN') from None
                return 202, {'status': 'ACCEPTED', 'request_id': key, 'selection': body, 'note': 'Poll status; timeout is not proof of failure.'}
            finally:
                c.execute('select pg_advisory_unlock(hashtextextended(%s, 937))', (sid,))

    def worker_entry(self, body, principal, key):
        try:
            self.worker(body, principal, key)
        finally:
            SLOTS.release()

    def worker(self, body, principal, key):
        from psycopg.types.json import Jsonb
        try:
            with self.bridge.db.connection() as c:
                # Admission holds this lock only briefly. Serialization covers all replicas.
                c.execute('select pg_advisory_lock(hashtextextended(%s, 937))', (body['source_id'],))
                try:
                    # Another identical executor may have completed while we waited.
                    row = c.execute('select state from bridge_private.pipeline_requests where principal_id=%s and request_id=%s', (principal['id'], key)).fetchone()
                    if row['state'] == 'COMPLETE':
                        return
                    c.commit()
                    # Recheck authorization and immutable selection after queueing.
                    LocalAssemblyClient(self.bridge, principal['publications']).assembly_input(body['source_id'], body['manifest_id'], body['manifest_sha'])
                    result = self.run(body, principal)
                    c.execute("update bridge_private.pipeline_requests set state='COMPLETE',result=%s, updated_at=now() where principal_id=%s and request_id=%s", (Jsonb(result), principal['id'], key))
                    c.commit()
                finally:
                    c.execute('select pg_advisory_unlock(hashtextextended(%s, 937))', (body['source_id'],))
        except Exception:
            # Never store/log upstream exceptions (they may contain credentials).
            try:
                with self.bridge.db.connection() as c:
                    c.execute("update bridge_private.pipeline_requests set state='UNKNOWN', updated_at=now() where principal_id=%s and request_id=%s and state!='COMPLETE'", (principal['id'], key))
            except Exception:
                pass  # Durable RUNNING remains uncertain, never success.

    def status(self, body, principal):
        with self.bridge.db.connection() as c:
            rows = c.execute('select request_id,operation,state,result,updated_at from bridge_private.pipeline_requests where principal_id=%s and source_id=%s and manifest_id=%s and manifest_sha256=%s order by updated_at desc limit 50', (principal['id'], body['source_id'], body['manifest_id'], body['manifest_sha'])).fetchall()
        return {'status': 'OBSERVED', 'requests': [{**r, 'request_id': str(r['request_id']), 'updated_at': r['updated_at'].isoformat()} for r in rows], 'note': 'RUNNING may be interrupted; retry the original request/key to reconcile. COMPLETE is an execution receipt, not editorial acceptance.'}

    def run(self, body, principal):
        from business_brief import assembler_runtime, indexer_runtime, index_search
        kwargs = dict(source_id=body['source_id'], manifest_id=body['manifest_id'], manifest_sha256=body['manifest_sha'])
        operation = body['operation']
        if operation == 'assembler':
            report = assembler_runtime.run(**kwargs, persist=body['persist'], bridge=LocalAssemblyClient(self.bridge, principal['publications']))
            status = 'BLOCKED' if report['counts']['blocked'] else 'NEEDS_REVIEW' if report['counts']['needs_review'] else 'PASS'
            # Do not send whole source text or arbitrary upstream diagnostics to Chat.
            result = {k: report[k] for k in ('counts', 'persistence')}
        elif operation == 'indexer':
            report = indexer_runtime.run(**kwargs, persist=body['persist'])
            status = 'BLOCKED' if not report['counts']['article_rows'] else 'NEEDS_REVIEW' if report['counts']['skipped'] else 'PASS'
            result = {k: report[k] for k in ('counts', 'profiles', 'persistence')}
        else:
            store = indexer_runtime.SupabaseIndexStore.from_env()
            rows = store.select_articles(**kwargs)
            identities = {(r['article_id'], r['artifact_sha256']) for r in rows}
            report = index_search.run(body['query'], 100)
            result = {ranking: [r for r in report[ranking] if (r.get('article_id'), r.get('article_record_sha256')) in identities][:body['limit']] for ranking in ('vector', 'lexical')}
            result['note'] = 'Separate calibration rankings; authorized exact-selection subset of global top 100. Recall may be incomplete.'
            status = 'PASS'
        return {'status': status, 'selection': kwargs, 'operation': operation, **result}
