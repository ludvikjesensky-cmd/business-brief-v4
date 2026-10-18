"""Immutable full page revisions and explicit edition selection. No latest fallback."""
import copy
import re
import psycopg
from datetime import datetime
from uuid import uuid5, NAMESPACE_URL

from .validation import (fields, require, slug, sha, uuid, integer, string,
                         page_schema, verification, generation_prefix,
                         GENERATION_DIRECTORIES, strict_json, Failure)
from .assets import verify_crop, MAX_BYTES

REVISION = 'page-revision-v1'
MANIFEST = 'edition-selection-v1'

# Exact immutable artifacts with independently established content defects.
# Additions require a reviewed release; a technical usable flag cannot clear them.
BLOCKED_SHA256 = frozenset({
    'f135489008902816526cd4d2b73710e18e4833931f8adcae47af5ab793741e97',
    'd8672242e2cf88e51518c824c4ffceefbcfd524eb07a50d33a6611e2af4531ef',
})


def timestamp(value):
    string(value, True)
    try:
        t = datetime.fromisoformat(value.replace('Z', '+00:00'))
        require(t.utcoffset() is not None)
    except ValueError:
        raise Failure('PAGE_SCHEMA_INVALID', 422) from None


def revision_schema(revision, *, submission=False):
    fields(revision, 'schema_version revision_id supersedes reason created_by created_at crop_previews page')
    require(revision['schema_version'] == REVISION)
    slug(revision['revision_id'])
    fields(revision['supersedes'], 'key sha256')
    sha(revision['supersedes']['sha256'])
    for k in ('reason', 'created_by'): string(revision[k], True)
    timestamp(revision['created_at'])
    p = revision['page']
    require(type(p) is dict and p.get('schema_version') == 'page-ingest-v4')
    page_schema(p, submission=submission, revision_id=revision['revision_id'])
    expected = f"{generation_prefix(p)}/page-{p['publication']['page_no']:04d}.json"
    require(revision['supersedes']['key'] == expected, 'SUPERSEDES_MISMATCH', 409)
    previews = revision['crop_previews']; require(type(previews) is list)
    assets = [a for i in p['items'] for a in i['assets']]
    require(all(type(x) is dict for x in previews), 'CROP_PREVIEW_REQUIRED', 422)
    require(len(previews) == len(assets), 'CROP_PREVIEW_REQUIRED', 422)
    require(len({x.get('asset_id') for x in previews if type(x) is dict}) == len(assets), 'CROP_PREVIEW_REQUIRED', 422)
    for a in assets:
        preview = next((x for x in previews if x.get('asset_id') == a['asset_id']), None)
        require(preview is not None, 'CROP_PREVIEW_REQUIRED', 422)
        fields(preview, 'asset_id sha256 inspected_by inspected_at')
        sha(preview['sha256']); string(preview['inspected_by'], True); timestamp(preview['inspected_at'])
        if a['artifact'] is not None:
            require(preview['sha256'] == a['artifact']['sha256'], 'CROP_PREVIEW_MISMATCH', 409)


def verify_supersedes(bridge, page, revision):
    from .core import digest
    raw = bridge.storage.download(bridge.output_bucket, revision['supersedes']['key'])
    require(digest(raw) == revision['supersedes']['sha256'], 'SUPERSEDES_MISMATCH', 409)
    old = strict_json(raw); page_schema(old)
    require(old['source'] == page['source'] and old['publication'] == page['publication'], 'SUPERSEDES_MISMATCH', 409)


def prefix(identity):
    return f"page-ingest/{identity['publication_id']}/{identity['edition_date']}/{identity['source_sha256']}"


def artifact_key(identity, no, generation, revision_id=None):
    require(generation in GENERATION_DIRECTORIES.values(), 'INVALID_REQUEST', 400)
    integer(no)
    root = f"{prefix(identity)}/{generation}"
    if revision_id is not None:
        slug(revision_id)
        return f"{root}/revisions/page-{no:04d}/{revision_id}/page.json"
    return f"{root}/page-{no:04d}.json"


def read_artifact(bridge, row, ident, no, generation, revision_id=None):
    from .core import digest, jcs, stamp
    require(1 <= no <= ident['page_count'], 'PAGE_NOT_FOUND', 404)
    key = artifact_key(ident, no, generation, revision_id)
    raw = bridge.storage.download_bounded(bridge.output_bucket, key, 5*1024*1024)
    document = strict_json(raw)
    if revision_id is not None:
        revision_schema(document)
        require(document['revision_id'] == revision_id, 'IDENTITY_MISMATCH', 409)
        p = document['page']; verify_supersedes(bridge, p, document)
    else:
        p = document; page_schema(p)
    require(raw == jcs(document), 'ARTIFACT_HASH_MISMATCH', 409)
    require(p['source'] == {'source_id':ident['source_id'], 'source_sha256':ident['source_sha256']} and
            all(p['publication'][k] == ident[k] for k in ('publication_id','canonical_name','edition_date','edition_variant')) and
            p['publication']['page_no'] == no and GENERATION_DIRECTORIES[p['schema_version']] == generation,
            'IDENTITY_MISMATCH', 409)
    verification(p)
    assets = []
    for i in p['items']:
        for a in i.get('assets', []):
            ar = a['artifact']
            require(ar['bucket'] == bridge.output_bucket, 'IDENTITY_MISMATCH', 409)
            data = bridge.storage.download_bounded(bridge.output_bucket, ar['key'], MAX_BYTES)
            verify_crop(data, ar)
            assets.append({'asset_id':a['asset_id'], **ar, 'verification':'VERIFIED'})
    blocked = digest(raw) in BLOCKED_SHA256
    return {'source':ident, 'page_no':no, 'generation':generation, 'schema_version':p['schema_version'],
            'kind':'revision' if revision_id else 'canonical', 'revision_id':revision_id,
            'key':key, 'sha256':digest(raw), 'byte_size':len(raw), 'page_status':p['page_status'],
            'usable_for_assembly':p['page_status'] in ('VERIFIED','VERIFIED_WITH_NOTES') and not blocked,
            'blocked_known_defect':blocked, 'page':p, 'assets':assets,
            'verification':{'status':'VERIFIED','verified_at':stamp(), 'receipt_id':digest(raw)},
            **({'revision':{k:v for k,v in document.items() if k != 'page'}} if revision_id else {})}


def get_artifact(bridge, sid, no, generation, revision_id, allowed):
    with bridge.db.connection() as c:
        r = bridge.db.row(c, sid, allowed); _, h = bridge.bundle(r)
        ident = bridge.identity(r, h)
        result = read_artifact(bridge, r, ident, no, generation, revision_id)
        require(bridge.bundle(r)[1] == h, 'SOURCE_CHANGED', 409)
        return result


def list_artifacts(bridge, sid, allowed):
    # Enumerate Storage, not claims: pending writes are never an authoritative index.
    with bridge.db.connection() as c:
        r = bridge.db.row(c, sid, allowed); _, h = bridge.bundle(r)
        ident = bridge.identity(r, h); results = []
        for generation in GENERATION_DIRECTORIES.values():
            root = f"{prefix(ident)}/{generation}"
            for entry in bridge.storage.list(bridge.output_bucket, root):
                name = entry['name']
                match = re.fullmatch(r'page-([0-9]{4})\.json', name)
                if match:
                    results.append({'page_no':int(match[1]), 'generation':generation, 'revision_id':None,
                                    'key':f'{root}/{name}', 'kind':'canonical'})
            for page in bridge.storage.list(bridge.output_bucket, root+'/revisions'):
                match = re.fullmatch(r'page-([0-9]{4})', page['name'])
                if not match: continue
                for rev in bridge.storage.list(bridge.output_bucket, root+'/revisions/'+page['name']):
                    slug(rev['name'])
                    results.append({'page_no':int(match[1]), 'generation':generation, 'revision_id':rev['name'],
                                    'key':artifact_key(ident,int(match[1]),generation,rev['name']), 'kind':'revision'})
        require(bridge.bundle(r)[1] == h, 'SOURCE_CHANGED', 409)
        return {'source':ident, 'artifacts':results, 'verification':'INDEX_ONLY_USE_READBACK'}


def manifest_schema(m):
    fields(m, 'schema_version manifest_id source created_by created_at status pages')
    require(m['schema_version'] == MANIFEST)
    slug(m['manifest_id']); string(m['created_by'], True); timestamp(m['created_at'])
    require(m['status'] in ('DRAFT','ACCEPTED_FOR_ASSEMBLY'))
    require(type(m['source']) is dict and type(m['pages']) is list)
    require(all(type(p) is dict for p in m['pages']))
    integer(m['source'].get('page_count'))
    require(sorted(p.get('page_no',0) for p in m['pages']) == list(range(1,m['source']['page_count']+1)), 'MANIFEST_INCOMPLETE', 422)
    for p in m['pages']:
        fields(p, 'page_no generation schema_version kind revision_id key sha256 page_status usable_for_assembly evidence selection_reason')
        integer(p['page_no']); sha(p['sha256']); string(p['selection_reason'],nullable=True)
        require(p['kind'] in ('canonical','revision'))
        require((p['revision_id'] is not None) == (p['kind'] == 'revision'))
        require(p['key'] == artifact_key(m['source'],p['page_no'],p['generation'],p['revision_id']), 'SELECTION_MISMATCH', 409)
        require(p['schema_version'] in GENERATION_DIRECTORIES and GENERATION_DIRECTORIES[p['schema_version']] == p['generation'])
        require(type(p['usable_for_assembly']) is bool)
        require(p['page_status'] in ('VERIFIED','VERIFIED_WITH_NOTES','NEEDS_REVIEW','BLOCKED'))
        fields(p['evidence'], 'receipt_id verified_at'); sha(p['evidence']['receipt_id']); timestamp(p['evidence']['verified_at'])
        require(p['evidence']['receipt_id'] == p['sha256'], 'SELECTION_MISMATCH', 409)


def verify_selection(bridge, row, ident, m, *, assembly=False):
    manifest_schema(m)
    require(m['source'] == ident, 'IDENTITY_MISMATCH', 409)
    if assembly: require(m['status'] == 'ACCEPTED_FOR_ASSEMBLY', 'MANIFEST_NOT_ACCEPTED', 409)
    selected = []
    for p in m['pages']:
        a = read_artifact(bridge,row,ident,p['page_no'],p['generation'],p['revision_id'])
        require(all(p[k] == a[k] for k in ('key','sha256','schema_version','kind','page_status','usable_for_assembly')), 'SELECTION_MISMATCH', 409)
        if assembly or m['status'] == 'ACCEPTED_FOR_ASSEMBLY':
            require(a['usable_for_assembly'] and not a['blocked_known_defect'], 'SELECTION_BLOCKED', 409)
        selected.append(a)
    return selected


def persist_manifest(bridge, m, key, principal, allowed):
    """Same session + durable source fence as page writes; validation repeats after commit."""
    from .core import digest, jcs
    manifest_schema(m); m=copy.deepcopy(m)
    sid=m['source']['source_id']; target=f"{prefix(m['source'])}/edition-selection/{m['manifest_id']}.json"
    raw=jcs(m); rh=digest(raw)
    def eligible(c):
        r=bridge.db.row(c,sid,allowed); _,h=bridge.bundle(r); ident=bridge.identity(r,h)
        verify_selection(bridge,r,ident,m)
        return r
    with bridge.db.connection() as c:
        c.execute('select pg_advisory_lock(hashtextextended(%s,0))',(target,))
        try:
            r=eligible(c)
            # Reserve target across principals as well as binding original request.
            claims=[(principal,key),('@edition-selection-v1',str(uuid5(NAMESPACE_URL,target)))]
            for owner,claim in claims:
                c.execute('''insert into bridge_private.bindings(principal,idempotency_key,request_sha256,target_key,source_id,edition_id,blob_id,publication_id)
                values(%s,%s,%s,%s,%s,%s,%s,%s) on conflict(principal,idempotency_key) do nothing''',
                (owner,claim,rh,target,r['id'],r['edition_id'],r['blob_id'],r['publication_uuid']))
                old=c.execute('select request_sha256,target_key from bridge_private.bindings where principal=%s and idempotency_key=%s for update',(owner,claim)).fetchone()
                require(old['request_sha256']==rh and old['target_key']==target,'IDEMPOTENCY_CONFLICT',409)
                c.execute("update bridge_private.bindings set state='PENDING' where principal=%s and idempotency_key=%s",(owner,claim))
            c.commit(); eligible(c)
            try:
                created=bridge.storage.create(bridge.output_bucket,target,raw)
                stored=bridge.storage.download(bridge.output_bucket,target)
                require(stored==raw,'MANIFEST_CONFLICT',409)
                eligible(c)
            except Failure as e:
                raise Failure(e.code,e.http,'UNKNOWN') from None
            for owner,claim in claims:
                c.execute("update bridge_private.bindings set state='VERIFIED',artifact_sha256=%s where principal=%s and idempotency_key=%s",(rh,owner,claim))
            c.commit()
            return (201 if created else 200),{'status':'STORED','key':target,'sha256':rh,'byte_size':len(raw),'manifest':m,'verification':'VERIFIED'}
        except psycopg.Error:
            raise Failure('PERSISTENCE_UNVERIFIED',503,'UNKNOWN') from None
        finally:
            if not c.closed:
                try:
                    c.rollback(); c.execute('select pg_advisory_unlock(hashtextextended(%s,0))',(target,)); c.commit()
                except psycopg.Error: pass


def assembly_input(bridge, sid, manifest_id, expected_sha256, allowed):
    """Only entry for future Assembler. No directory scan, discovery or fallback."""
    from .core import digest
    slug(manifest_id); sha(expected_sha256)
    with bridge.db.connection() as c:
        r=bridge.db.row(c,sid,allowed); _,h=bridge.bundle(r); ident=bridge.identity(r,h)
        raw=bridge.storage.download(bridge.output_bucket,f'{prefix(ident)}/edition-selection/{manifest_id}.json')
        require(digest(raw)==expected_sha256,'ARTIFACT_HASH_MISMATCH',409)
        m=strict_json(raw); require(m.get('manifest_id')==manifest_id,'IDENTITY_MISMATCH',409)
        pages=verify_selection(bridge,r,ident,m,assembly=True)
        require(bridge.bundle(r)[1]==h,'SOURCE_CHANGED',409)
        return {'manifest':m,'sha256':expected_sha256,'pages':pages}
