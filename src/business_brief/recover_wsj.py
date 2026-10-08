"""One-time recovery of the incorrectly identified v4.0 acceptance source."""
from pathlib import Path
import hashlib
from .storage import SupabaseArchive, StorageError
from .database import TechnicianRepository

DIGEST='4f971090776ba6991c1e1f6d82fc5bb7ccd4e95e749e4a3f625f239506095af2'
FILENAME='wallstreetjournal_20261008_TheWallStreetJournal.pdf'

def main():
    archive=SupabaseArchive.from_env()
    repo=TechnicianRepository(archive.client)
    blob=repo.blob_by_sha(DIGEST)
    if not blob:
        raise StorageError('Recovery requires the existing immutable WSJ blob')
    current=repo.source_for_blob(blob['id'])
    if current and current['status']=='READY_FOR_INGESTOR':
        print('WSJ recovery already completed')
        return
    data=archive.client.storage.from_(archive.archive).download(blob['immutable_original_path'])
    if hashlib.sha256(data).hexdigest()!=DIGEST:
        raise StorageError('Recovery original SHA-256 mismatch')
    if FILENAME in archive.list_inbox():
        existing=archive.client.storage.from_(archive.inbox).download(FILENAME)
        if hashlib.sha256(existing).hexdigest()!=DIGEST:
            raise StorageError('Recovery inbox object differs from archived original')
    else:
        archive.client.storage.from_(archive.inbox).upload(FILENAME,data,{'content-type':'application/pdf','upsert':'false'})
    print('WSJ original restored to Inbox; SHA-256 verified')

if __name__=='__main__': main()
