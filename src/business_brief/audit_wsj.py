"""Verify the acceptance bundle in Storage and optionally probe a duplicate upload."""
import argparse, hashlib, json
from pathlib import PurePosixPath
from .database import TechnicianRepository
from .storage import SupabaseArchive, StorageError
from .events import EventLogger
from .recover_wsj import DIGEST, FILENAME

def audit(probe=False):
    archive=SupabaseArchive.from_env(); repo=TechnicianRepository(archive.client)
    blob=repo.blob_by_sha(DIGEST); source=repo.source_for_blob(blob['id']) if blob else None
    if not source or source['status']!='READY_FOR_INGESTOR': raise StorageError('No current READY WSJ source to audit')
    manifest_path=source['source_bundle_path']; prefix=manifest_path.rsplit('/',1)[0]
    data=json.loads(archive.client.storage.from_(archive.archive).download(manifest_path))
    assert data['original_filename']==FILENAME
    assert data['identity']['publication_id']=='the-wall-street-journal'
    assert data['identity']['edition_date']=='2026-10-08'
    assert data['source_sha256']==DIGEST
    assert data['page_count']==32
    artifacts={data['original_path']:DIGEST,data['prepared_pdf_path']:data['ocr']['prepared_sha256']}
    artifacts.update({p['path']:p['sha256'] for p in data['page_images']+data['parts']})
    original=None
    for path,digest in artifacts.items():
        assert not PurePosixPath(path).is_absolute() and '..' not in PurePosixPath(path).parts
        assert path.startswith(prefix+'/')
        payload=archive.client.storage.from_(archive.archive).download(path)
        assert hashlib.sha256(payload).hexdigest()==digest, path
        if path==data['original_path']: original=payload
    summary={'source_id':source['id'],'manifest_path':manifest_path,'original_filename':data['original_filename'],'identity':data['identity'],'page_count':data['page_count'],'verified_artifacts':len(artifacts),'ocr':data['ocr']['performed'],'sha256':DIGEST}
    EventLogger(archive.client).emit('ARCHIVE_VERIFIED',stage='T22',status='OK',source_id=source['id'],metadata=summary)
    print(json.dumps(summary),flush=True)
    if probe:
        if FILENAME in archive.list_inbox(): raise StorageError('Duplicate probe requires an empty WSJ Inbox slot')
        archive.client.storage.from_(archive.inbox).upload(FILENAME,original,{'content-type':'application/pdf','upsert':'false'})
        EventLogger(archive.client).emit('WAKE_PROBE_UPLOADED',status='OK',source_id=source['id'],metadata={'object_key':FILENAME,'sha256':DIGEST})
        print('Duplicate probe uploaded; only the Storage trigger may wake the idle worker',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--probe',action='store_true');args=parser.parse_args();audit(args.probe)
