"""Opt-in, non-editorial DB fence checks. All claim/state changes roll back."""
import os
from pathlib import Path
from uuid import uuid4
import psycopg
from .core import Database

def main():
    db=Database(os.environ['BRIDGE_DATABASE_URL'],str(Path(__file__).with_name('supabase-ca.crt')))
    with db.connection() as c:
        # Pin exactly one existing READY source for read-only lock checks.
        r=db.current(c,'the-wall-street-journal',['the-wall-street-journal'])
        for phase in ('storage-write','storage-readback'):
            with db.connection() as other:
                try:
                    other.execute('select id from public.sources where id=%s for update nowait',(r['id'],))
                except psycopg.errors.LockNotAvailable: other.rollback()
                else: raise RuntimeError('row fence missing')
            print('BRIDGE_DB_ROW_FENCE_PASS phase='+phase,flush=True)
        # Uncommitted synthetic binding and attempted identity updates; no source changes survive.
        principal='selftest-'+str(uuid4());key=uuid4()
        c.execute('''insert into bridge_private.bindings(principal,idempotency_key,request_sha256,target_key,source_id,edition_id,blob_id,publication_id)
          values(%s,%s,%s,%s,%s,%s,%s,%s)''',(principal,key,'0'*64,'selftest/'+str(key),r['id'],r['edition_id'],r['blob_id'],r['publication_uuid']))
        for query,args in [
            ("update public.sources set status='SELFTEST' where id=%s",(r['id'],)),
            ("update public.editions set active_source_id=null where id=%s",(r['edition_id'],)),
            ("update public.source_blobs set sha256=%s where id=%s",('0'*64,r['blob_id'])),
            ("update public.publications set canonical_name='SELFTEST' where id=%s",(r['publication_uuid'],))]:
            blocked=False
            try:
                with c.transaction(): c.execute(query,args)
            except psycopg.errors.ObjectNotInPrerequisiteState: blocked=True
            assert blocked,'durable pending fence missing'
        c.rollback()
    print('BRIDGE_DB_PENDING_GUARDS_PASS source,edition,blob,publication; all mutations rolled back',flush=True)
if __name__=='__main__':main()
