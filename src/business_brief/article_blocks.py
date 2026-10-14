"""Human-directed article extraction: source IDs, explicit order, audited typography.

No model calls, semantic inference, production worker or Visual Page Map dependency.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import time
import unicodedata
from pathlib import Path

VERSION = 'article-blocks-v1'

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':')).encode()).hexdigest()

def save(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)

def load(path):
    return json.loads(Path(path).read_text())

def prepare(pdf_path, page_no, output, width=600):
    import fitz
    start = time.perf_counter(); source = Path(pdf_path); output = Path(output)
    if page_no < 1 or not 128 <= width <= 2400:
        raise ValueError('Invalid page or image width')
    with fitz.open(source) as doc:
        if page_no > len(doc): raise ValueError('Page outside PDF')
        page = doc[page_no - 1]
        if page.rotation: raise ValueError('Rotated PDF requires an explicit normalized derivative')
        lines = []; groups = []
        for block in page.get_text('dict')['blocks']:
            if block['type'] != 0: continue
            ids = []
            for line in block['lines']:
                text = ''.join(s['text'] for s in line['spans']).strip()
                if not text: continue
                identity = f'L{len(lines)+1:04d}'; ids.append(identity)
                lines.append({'id': identity, 'text': text,
                    'bbox': [round(float(v), 3) for v in line['bbox']],
                    'group': f'G{len(groups)+1:03d}'})
            if ids: groups.append({'id': f'G{len(groups)+1:03d}', 'ids': ids})
        payload = {'version': VERSION, 'pdf_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'page_no': page_no, 'page_count': len(doc), 'width': page.rect.width,
            'height': page.rect.height, 'lines': lines, 'native_groups': groups}
        payload['page_digest'] = digest(payload)
        output.mkdir(parents=True, exist_ok=True)
        save(output/'blocks.json', payload)
        page.get_pixmap(matrix=fitz.Matrix(width/page.rect.width, width/page.rect.width),
            alpha=False, annots=False).save(str(output/'page.png'))
    lookup = {line['id']: line for line in lines}
    inventory = []
    for group in groups:
        inventory.append(f"\n{group['id']} ({', '.join(group['ids'])})")
        inventory.extend(f"{i} {lookup[i]['bbox']} {lookup[i]['text']}" for i in group['ids'])
    (output/'blocks.txt').write_text('\n'.join(inventory)+'\n')
    save(output/'plan-template.json', {'version': VERSION, 'page_digest': payload['page_digest'],
        'articles': [], 'excluded': [], 'hyphenation': {}})
    return {'page': page_no, 'lines': len(lines), 'groups': len(groups),
            'seconds': round(time.perf_counter()-start, 4)}

def assemble(data, plan):
    original = {k: v for k, v in data.items() if k != 'page_digest'}
    if data['version'] != VERSION or digest(original) != data['page_digest']:
        raise ValueError('Source block integrity mismatch')
    if plan.get('version') != VERSION or plan.get('page_digest') != data['page_digest']:
        raise ValueError('Plan belongs to a different source/page')
    if not plan.get('articles'): raise ValueError('Plan contains no articles')
    by_id = {x['id']: x for x in data['lines']}
    if len(by_id) != len(data['lines']): raise ValueError('Duplicate source IDs')
    used = {}; warnings = []; joins = plan.get('hyphenation', {}); consumed_joins = set()
    no_space = set(plan.get("no_space_after", [])); consumed_no_space = set()
    evidence = []; articles = []; article_ids = set()
    def take(ids, owner):
        for i in ids:
            if i not in by_id: raise ValueError(f'Unknown source ID: {i}')
            if i in used: raise ValueError(f'Duplicate ownership: {i}')
            used[i] = owner
        return [by_id[i]['text'] for i in ids]
    def text(ids, owner):
        parts = take(ids, owner)
        result = ''
        for n, part in enumerate(parts):
            if n:
                left = parts[n-1]
                if ids[n-1] in no_space:
                    if len(left) != 1 or not left.isalpha() or not part[0].islower():
                        raise ValueError('No-space decision must join a drop cap to its word')
                    consumed_no_space.add(ids[n-1]); result += part; continue
                if left.endswith('-') and part and part[0].isalnum():
                    action = joins.get(ids[n-1])
                    if action not in ('remove', 'keep'):
                        warnings.append({'kind':'unreviewed_hyphen','left_id':ids[n-1],
                                         'right_id':ids[n]})
                        result += '\n' + part; continue
                    consumed_joins.add(ids[n-1])
                    if action == 'remove': result = result[:-1]
                    result += part; continue
                result += ' '
            result += part
        # No paraphrasing: compare all source characters, ignoring whitespace and reviewed hyphens.
        canonical = lambda t: re.sub(r'[\s-]', '', t)
        if canonical(result) != canonical(''.join(parts)):
            raise ValueError('Typography changed source content')
        return result
    for a in plan['articles']:
        aid = a['id']
        if not aid or aid in article_ids: raise ValueError('Duplicate/empty article ID')
        article_ids.add(aid)
        title = text(a['title_ids'], aid+':title')
        if 'title_text' in a:
            if re.sub(r'\s', '', a['title_text']) != re.sub(r'\s', '', title):
                raise ValueError('Title typography changes source characters')
            title = a['title_text']
        intro = text(a.get('intro_ids', []), aid+':intro')
        take(a.get('byline_ids', []), aid+':byline')
        paragraphs = [text(ids, aid+':body') for ids in a['paragraphs']]
        if not title or not paragraphs or any(not p for p in paragraphs):
            raise ValueError('Empty title/body/paragraph')
        articles.append({'title':title, 'text':'\n\n'.join(x for x in [intro]+paragraphs if x)})
        evidence.append({'article_id':aid,'title_ids':a['title_ids'],
            'intro_ids':a.get('intro_ids',[]),'byline_ids':a.get('byline_ids',[]),
            'paragraph_ids':a['paragraphs'], 'relevance':a.get('relevance'),
            'continuation':a.get('continuation')})
    for exclusion in plan['excluded']:
        if not exclusion['reason'].strip(): raise ValueError('Exclusion requires a reason')
        take(exclusion['ids'], 'excluded:'+exclusion['reason'])
    if no_space != consumed_no_space: raise ValueError('Unused no-space decision')
    if set(joins) != consumed_joins: raise ValueError('Unused/invalid hyphenation decision')
    missing = [i for i in by_id if i not in used]
    if missing: warnings.append({'kind':'unassigned_ids','ids':missing})
    duplicates = []
    by_text = {}
    for line in data['lines']:
        if len(line['text']) >= 8:
            for other in by_text.get(line['text'], []):
                if max(abs(x-y) for x,y in zip(line['bbox'],other['bbox'])) <= .25:
                    duplicates.append([other['id'],line['id']]); break
            by_text.setdefault(line['text'],[]).append(line)
    damaged = [line['id'] for line in data['lines'] if '\ufffd' in line['text'] or any(unicodedata.category(c) == 'Cc' and c not in '\n\r\t' for c in line['text'])]
    if damaged: warnings.append({'kind':'source_text_quality','ids':damaged})
    if duplicates: warnings.append({'kind':'coincident_source_duplicates','pairs':duplicates})
    return articles, {'version':VERSION,'page_digest':data['page_digest'],
        'pdf_sha256':data['pdf_sha256'],'page_no':data['page_no'],'plan_digest':digest(plan),
        'source_lines':len(by_id),'accounted_lines':len(used),'article_lines':sum(not o.startswith('excluded:') for o in used.values()),'excluded_lines':sum(o.startswith('excluded:') for o in used.values()),'unassigned_ids':missing,
        'needs_review':bool(warnings),'semantic_validation':'controller_authored_not_independently_verified','warnings':warnings,'articles':evidence,
        'scope':'Selected page fragments only; source characters preserved, semantic order is controller-authored.'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('prepare'); q.add_argument('--pdf',required=True); q.add_argument('--page',type=int,required=True); q.add_argument('--output',required=True); q.add_argument('--width',type=int,default=600)
    q=sub.add_parser('assemble'); q.add_argument('--blocks',required=True); q.add_argument('--plan',required=True); q.add_argument('--output',required=True)
    args=p.parse_args(argv)
    try:
        if args.command=='prepare': print(json.dumps(prepare(args.pdf,args.page,args.output,args.width))); return 0
        start=time.perf_counter(); articles,audit=assemble(load(args.blocks),load(args.plan))
        out=Path(args.output);save(out/'articles.json',articles);save(out/'audit.json',audit)
        print(json.dumps({'articles':len(articles),'needs_review':audit['needs_review'],
            'seconds':round(time.perf_counter()-start,4)}));return 0
    except (ValueError,KeyError,TypeError,OSError) as exc: p.error(str(exc))

if __name__=='__main__': main()
