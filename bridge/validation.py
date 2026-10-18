"""Strict wire validation for INGESTOR §19; dataclasses describe serialization only."""
import json
import math
import re
from datetime import date
from uuid import UUID

class Failure(Exception):
    def __init__(self, code, http=409, persistence='NOT_WRITTEN', path=''):
        self.code, self.http, self.persistence, self.path = code, http, persistence, path
        super().__init__(code)

def require(ok, code='PAGE_SCHEMA_INVALID', http=422, path=''):
    if not ok:
        raise Failure(code, http, path=path)

def strict_json(raw):
    def pairs(values):
        d = {}
        for k, v in values:
            if k in d: raise ValueError('duplicate')
            d[k] = v
        return d
    def constant(_): raise ValueError('constant')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, UnicodeError, RecursionError):
        raise Failure('INVALID_JSON', 400) from None

def fields(v, names):
    require(type(v) is dict and set(v) == set(names.split()))

def string(v, nonempty=False, nullable=False):
    require((nullable and v is None) or (type(v) is str and (not nonempty or bool(v.strip()))))
    if type(v) is str:
        try: v.encode('utf-8')
        except UnicodeError: raise Failure('PAGE_SCHEMA_INVALID', 422) from None

def strings(v):
    require(type(v) is list)
    for x in v: string(x)

def integer(v, low=1, high=9999):
    require(type(v) is int and low <= v <= high)

def uuid(v):
    try: require(type(v) is str and str(UUID(v)) == v)
    except (ValueError, TypeError, AttributeError): raise Failure('PAGE_SCHEMA_INVALID', 422) from None

def sha(v): require(type(v) is str and re.fullmatch('[0-9a-f]{64}', v) is not None)
def day(v):
    try: require(type(v) is str and len(v) == 10 and date.fromisoformat(v).isoformat() == v)
    except (ValueError, TypeError): raise Failure('PAGE_SCHEMA_INVALID', 422) from None

def slug(v): require(type(v) is str and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', v) is not None)

STATUSES = ['VERIFIED', 'VERIFIED_WITH_NOTES', 'NEEDS_REVIEW', 'BLOCKED']

def page_schema(p):
    fields(p, 'schema_version producer instruction_version source publication items page_status page_notes')
    generation = (p['schema_version'], p['producer'], p['instruction_version'])
    require(generation in [('page-ingest-v2', 'ingestor-v2.0-chat', '2.0'),
                           ('page-ingest-v3', 'ingestor-v2.1-chat', '2.1'),
                           ('page-ingest-v4', 'ingestor-v2.2-chat', '2.2')])
    legacy = p['schema_version'] == 'page-ingest-v2'
    fields(p['source'], 'source_id source_sha256'); uuid(p['source']['source_id']); sha(p['source']['source_sha256'])
    pub = p['publication']; fields(pub, 'publication_id canonical_name edition_date edition_variant page_no')
    slug(pub['publication_id']); string(pub['canonical_name'], True); day(pub['edition_date']); string(pub['edition_variant'], True); integer(pub['page_no'])
    strings(p['page_notes']); string(p['page_status']); require(p['page_status'] in STATUSES)
    require(type(p['items']) is list); seen = set(); asset_ids = set()
    for item in p['items']:
        fields(item, 'page_item_id item_type title subtitle kicker byline text_on_page relevance continuation verification' + (' perspective' if legacy else '') + (' assets' if p['schema_version'] == 'page-ingest-v4' else ''))
        string(item['page_item_id'], True); string(item['item_type'], True)
        require(item['page_item_id'] not in seen); seen.add(item['page_item_id'])
        for k in ['title', 'subtitle', 'kicker', 'byline', 'text_on_page']: string(item[k], nullable=True)
        r = item['relevance']; fields(r, 'state reason'); string(r['state']); require(r['state'] in ['relevant', 'irrelevant', 'uncertain']); string(r['reason'], True)
        if legacy:
            pe = item['perspective']; fields(pe, 'author_question framing central_argument distinctive_angle tensions_or_counterarguments open_questions observed_on_page interpreted_from_page unresolved_until_assembly')
            for k in ['author_question', 'framing', 'central_argument', 'distinctive_angle']: string(pe[k], nullable=True)
            for k in ['tensions_or_counterarguments', 'open_questions', 'observed_on_page', 'interpreted_from_page', 'unresolved_until_assembly']: strings(pe[k])
        if p['schema_version'] == 'page-ingest-v4':
            require(type(item['assets']) is list)
            for asset in item['assets']:
                asset_schema(asset, item, p, asset_ids)
        c = item['continuation']; fields(c, 'starts_here continued_from_previous_page continues_to_another_page continuation_marker continuation_target')
        for k in ['starts_here', 'continued_from_previous_page', 'continues_to_another_page']: require(type(c[k]) is bool)
        for k in ['continuation_marker', 'continuation_target']: string(c[k], nullable=True)
        v = item['verification']; fields(v, 'status visual_checked text_layer_checked title_verified byline_verified boundaries_verified reading_order_verified text_on_page_complete notes')
        string(v['status']); require(v['status'] in STATUSES); strings(v['notes'])
        for k in ['visual_checked', 'text_layer_checked', 'title_verified', 'boundaries_verified', 'reading_order_verified', 'text_on_page_complete']: require(type(v[k]) is bool)
        require(v['byline_verified'] is None or type(v['byline_verified']) is bool)

def verification(p):
    require(not any(a['verification']['status'] == 'BLOCKED' for i in p['items'] for a in i.get('assets', [])), 'PAGE_BLOCKED', 409)
    require(p['page_status'] != 'BLOCKED' and all(i['verification']['status'] != 'BLOCKED' for i in p['items']), 'PAGE_BLOCKED', 409)
    def check(ok): require(ok, 'PAGE_VERIFICATION_INVALID', 422)
    if p['page_status'] != 'VERIFIED': check(any(x.strip() for x in p['page_notes']))
    if not p['items']: check(any(x.strip() for x in p['page_notes']))
    for i in p['items']:
        v = i['verification']; status = v['status']
        for a in i.get('assets', []):
            av = a['verification']
            check(STATUSES.index(av['status']) <= STATUSES.index(status))
            if av['status'] != 'VERIFIED': check(any(n.strip() for n in av['notes']))
            if av['status'] in STATUSES[:2]:
                check(all(av[k] for k in ['visual_checked', 'ownership_verified', 'page_anchor_verified', 'text_anchor_verified']))
                check(a['text_anchor']['status'] == 'anchored')
            if a['text_anchor']['status'] == 'placement_needs_review':
                check(not av['text_anchor_verified'] and av['status'] == 'NEEDS_REVIEW')
        check(STATUSES.index(status) <= STATUSES.index(p['page_status']))
        if status != 'VERIFIED': check(any(x.strip() for x in v['notes']))
        if status in STATUSES[:2]:
            check(all(v[k] for k in ['visual_checked', 'text_layer_checked', 'boundaries_verified', 'reading_order_verified']))
            if i['title'] is not None: check(v['title_verified'])
            check(v['byline_verified'] is (True if i['byline'] is not None else None))
            if i['relevance']['state'] != 'irrelevant': check(v['text_on_page_complete'] and bool(i['text_on_page'] and i['text_on_page'].strip()))


GENERATION_DIRECTORIES = {
    'page-ingest-v2': 'ingestor-v2.0',
    'page-ingest-v3': 'ingestor-v2.1',
    'page-ingest-v4': 'ingestor-v2.2',
}


def generation_prefix(p):
    # Call page_schema first at transport boundaries; validate path components here too.
    pub = p['publication']; slug(pub['publication_id']); day(pub['edition_date'])
    sha(p['source']['source_sha256'])
    require(p['schema_version'] in GENERATION_DIRECTORIES)
    return f"page-ingest/{pub['publication_id']}/{pub['edition_date']}/{p['source']['source_sha256']}/{GENERATION_DIRECTORIES[p['schema_version']]}"


def asset_key(p, asset_id):
    require(p['schema_version'] == 'page-ingest-v4')
    slug(asset_id); integer(p['publication']['page_no'])
    return f"{generation_prefix(p)}/assets/page-{p['publication']['page_no']:04d}/{asset_id}.png"


def asset_schema(a, item, p, seen):
    fields(a, 'asset_id asset_type page_item_id page_no page_anchor text_anchor title caption artifact verification')
    slug(a['asset_id']); require(a['asset_id'] not in seen); seen.add(a['asset_id'])
    string(a['asset_type']); require(a['asset_type'] in ['chart', 'table', 'photo', 'infographic', 'illustration', 'other'])
    require(a['page_item_id'] == item['page_item_id']); integer(a['page_no'])
    require(a['page_no'] == p['publication']['page_no'])
    for k in ['title', 'caption']: string(a[k], nullable=True)
    pa = a['page_anchor']; fields(pa, 'bbox_norm bbox_px source_page_image_sha256')
    sha(pa['source_page_image_sha256'])
    b = pa['bbox_norm']
    require(type(b) is list and len(b) == 4)
    require(all(type(n) in (int, float) and 0 <= n <= 1 and math.isfinite(n) for n in b))
    require(b[0] < b[2] and b[1] < b[3])
    px = pa['bbox_px']
    if px is not None:
        require(type(px) is list and len(px) == 4)
        for n in px: integer(n, 0, 2147483647)
        require(px[0] < px[2] and px[1] < px[3])
    ta = a['text_anchor']; fields(ta, 'position paragraph_index anchor_text status')
    string(ta['position']); require(ta['position'] in ['before_paragraph', 'after_paragraph', 'inline_after_anchor'])
    string(ta['status']); require(ta['status'] in ['anchored', 'placement_needs_review'])
    string(ta['anchor_text'], nonempty=True, nullable=True)
    if ta['paragraph_index'] is not None: integer(ta['paragraph_index'], 0, 2147483647)
    if ta['status'] == 'anchored':
        require(type(ta['anchor_text']) is str and type(item['text_on_page']) is str)
        text = item['text_on_page']; anchor = ta['anchor_text']
        require(text.find(anchor) >= 0 and text.find(anchor) == text.rfind(anchor))
        paragraphs = text.split('\n\n')
        require(any(anchor in paragraph for paragraph in paragraphs))
        if ta['paragraph_index'] is not None:
            require(ta['paragraph_index'] < len(paragraphs))
            require(anchor in paragraphs[ta['paragraph_index']])
    ar = a['artifact']; fields(ar, 'bucket key media_type sha256 byte_size width height')
    string(ar['bucket'], True); require(ar['key'] == asset_key(p, a['asset_id']))
    require(ar['media_type'] == 'image/png'); sha(ar['sha256'])
    for k in ['byte_size', 'width', 'height']: integer(ar[k], 1, 2147483647)
    if px is not None: require(ar['width'] == px[2]-px[0] and ar['height'] == px[3]-px[1])
    v = a['verification']; fields(v, 'status visual_checked ownership_verified page_anchor_verified text_anchor_verified notes')
    string(v['status']); require(v['status'] in STATUSES); strings(v['notes'])
    for k in ['visual_checked', 'ownership_verified', 'page_anchor_verified', 'text_anchor_verified']:
        require(type(v[k]) is bool)
