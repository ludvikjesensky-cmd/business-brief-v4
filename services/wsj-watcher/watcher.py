"""WSJ PoC. No guessed PDF paths, credentials, or direct POST replay."""
import datetime as dt
import fcntl
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import tempfile
import threading
import time
from zoneinfo import ZoneInfo

from pypdf import PdfReader

TZ = ZoneInfo('Europe/Prague')
DATA = Path(os.getenv('DATA_DIR', '/data'))
STATE = {'state': 'STARTING'}
MONTHS = ('JANUARY FEBRUARY MARCH APRIL MAY JUNE JULY AUGUST SEPTEMBER OCTOBER NOVEMBER DECEMBER').split()

class GateError(Exception):
    pass

def status(state, **facts):
    STATE.clear()
    STATE.update(state=state, time=dt.datetime.now(TZ).isoformat(), **facts)
    print(json.dumps(STATE), flush=True)

def parse_issue(label):
    m = re.search(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', label)
    return dt.date(int(m[3]), int(m[1]), int(m[2])) if m else None

def in_window(now):
    return dt.time(7, 50) <= now.time().replace(tzinfo=None) < dt.time(9)

def validate(pdf, issue, labels):
    raw = Path(pdf).read_bytes()
    if not raw.startswith(b'%PDF-'):
        raise GateError('NOT_PDF')
    reader = PdfReader(pdf, strict=True)
    if reader.is_encrypted:
        raise GateError('ENCRYPTED_PDF')
    if not labels or len(labels) != len(set(labels)) or len(reader.pages) != len(labels):
        raise GateError('PAGE_COUNT_MISMATCH')
    texts = []
    for page in reader.pages:
        # Decode each content stream; text presence is required for this WSJ PoC.
        page.get_contents().get_data()
        texts.append(page.extract_text() or '')
    if not all(t.strip() for t in texts):
        raise GateError('UNREADABLE_PAGE')
    date_pattern = rf'\b{MONTHS[issue.month-1]}\s+0?{issue.day}\s*,\s*{issue.year}\b'
    if not re.search(date_pattern, texts[0].upper()):
        raise GateError('WRONG_OR_UNVERIFIED_DATE')
    for label, text in zip(labels, texts):
        if not re.search(r'(?<![A-Z0-9])' + re.escape(label) + r'(?![A-Z0-9])', text.upper()):
            raise GateError('PAGE_LABEL_MISMATCH')
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
            'pages': len(texts), 'expected_page_labels': labels,
            'date_check': 'PASS', 'page_count_check': 'PASS',
            'ordered_label_presence_check': 'PASS', 'parse_check': 'PASS'}

def database(root):
    db = sqlite3.connect(root / 'outbox.sqlite3')
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, payload TEXT NOT NULL, acked INTEGER NOT NULL DEFAULT 0)')
    return db

def enqueue(db, manifest, directory):
    payload = {'type': 'WSJ_REFERENCE_READY', 'event_id': manifest['event_id'],
               'manifest_path': str(directory / 'manifest.json'),
               'pdf_path': str(directory / 'edition.pdf'), 'sha256': manifest['sha256']}
    with db:
        db.execute('INSERT OR IGNORE INTO events(id,payload) VALUES (?,?)',
                   (manifest['event_id'], json.dumps(payload)))

def recover(root, db):
    for path in (root / 'reference').glob('*/wsj/manifest.json'):
        manifest = json.loads(path.read_text())
        if hashlib.sha256((path.parent / 'edition.pdf').read_bytes()).hexdigest() != manifest['sha256']:
            raise GateError('REFERENCE_HASH_MISMATCH')
        enqueue(db, manifest, path.parent)

def publish(root, db, pdf, issue, labels, facts):
    directory = root / 'reference' / issue.isoformat() / 'wsj'
    if directory.exists():
        return False
    directory.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.reference-', dir=directory.parent))
    try:
        shutil.copyfile(pdf, stage / 'edition.pdf')
        manifest = dict(facts, issue_date=issue.isoformat(), edition='The Wall Street Journal',
                        acquired_at=dt.datetime.now(TZ).isoformat(),
                        transport='authenticated-browser-download',
                        event_id='wsj:' + issue.isoformat() + ':TheWallStreetJournal')
        (stage / 'manifest.json').write_text(json.dumps(manifest, indent=2))
        for path in stage.iterdir():
            with path.open('rb') as f:
                os.fsync(f.fileno())
        os.rename(stage, directory)
        fd = os.open(directory.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        enqueue(db, manifest, directory)
        return True
    finally:
        if stage.exists():
            shutil.rmtree(stage)

def find_reader(page):
    for _ in range(30):
        if any('sso.accounts.dowjones.com' in f.url for f in page.frames):
            raise GateError('AUTH_REQUIRED')
        for frame in page.frames:
            if frame.locator('#pullDownDate').count() and frame.locator('#hotspot1').count():
                return frame
        page.wait_for_timeout(1000)
    raise GateError('READER_NOT_READY_OR_AUTH_REQUIRED')

def snapshot(frame):
    return frame.evaluate('''() => {
      const date = document.querySelector('#pullDownDate');
      const edition = document.querySelector('#pullDownEdition');
      return {
        date: date?.selectedOptions[0]?.textContent?.trim(),
        dates: [...(date?.options || [])].map(o => ({text:o.textContent.trim(), value:o.value})),
        edition: edition?.selectedOptions[0]?.textContent?.trim(),
        labels: [...document.querySelectorAll('#pullDownPage option')].map(o => o.textContent.trim().replace(/^Page\\s+/, ''))
      };
    }''')

def acquire(context, root, db, issue):
    if (root / 'reference' / issue.isoformat() / 'wsj').exists():
        return 'ALREADY_READY'
    page = context.new_page()
    try:
        page.goto('https://ereader.wsj.net/', wait_until='domcontentloaded', timeout=60000)
        frame = find_reader(page)
        before = snapshot(frame)
        # No picking an old issue or assuming "latest" means today.
        candidate = next((o for o in before['dates'] if parse_issue(o['text']) == issue), None)
        if candidate is None:
            return 'NOT_YET_AVAILABLE'
        if parse_issue(before['date'] or '') != issue:
            frame.locator('#pullDownDate').select_option(candidate['value'])
            for _ in range(30):
                frame = find_reader(page)
                if parse_issue(snapshot(frame)['date'] or '') == issue:
                    break
                page.wait_for_timeout(1000)
            else:
                raise GateError('ISSUE_SELECTION_FAILED')
        before = snapshot(frame)
        if parse_issue(before['date'] or '') != issue:
            raise GateError('WRONG_READER_DATE')
        if not (before['edition'] or '').startswith('The Wall Street Journal ('):
            raise GateError('WRONG_EDITION')
        if not before['labels']:
            raise GateError('COMPLETENESS_UNVERIFIED')
        def dialog_handler(dialog):
            if dialog.type == 'confirm' and dialog.message.strip() == 'Are you sure you want to download this edition?':
                dialog.accept()
            else:
                dialog.dismiss()
        page.on('dialog', dialog_handler)
        status('DOWNLOADING', issue=issue.isoformat(), expected_pages=len(before['labels']))
        with page.expect_download(timeout=180000) as pending:
            frame.locator('#hotspot1').click()
        download = pending.value
        with tempfile.TemporaryDirectory(dir=root / 'tmp') as temp:
            pdf = Path(temp) / 'edition.pdf'
            download.save_as(pdf)
            after = snapshot(frame)
            if before != after:
                raise GateError('READER_CHANGED_DURING_DOWNLOAD')
            facts = validate(pdf, issue, before['labels'])
            publish(root, db, pdf, issue, before['labels'], facts)
        return 'REFERENCE_READY'
    finally:
        page.close()

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/health', '/status'):
            self.send_error(404)
            return
        body = json.dumps({'alive': True} if self.path == '/health' else STATE).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *args):
        pass

def main():
    from playwright.sync_api import sync_playwright
    os.umask(0o077)
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / 'tmp').mkdir(exist_ok=True)
    lock = (DATA / 'worker.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    db = database(DATA)
    recover(DATA, db)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 8081), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    mode = os.getenv('MODE', 'login')
    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(
            str(DATA / 'profile'), headless=False, accept_downloads=True,
            chromium_sandbox=True, viewport={'width': 1400, 'height': 950})
        try:
            if mode == 'login':
                page = context.new_page()
                page.goto('https://ereader.wsj.net/', wait_until='domcontentloaded')
                status('LOGIN_MODE', instruction='Sign in, select current issue, then redeploy with MODE=once')
                while True:
                    page.wait_for_timeout(1000)
            status('WAITING_FOR_WINDOW')
            failures = 0
            blocked_date = None
            while True:
                now = dt.datetime.now(TZ)
                if mode == 'once' or (mode == 'watch' and in_window(now)):
                    if blocked_date == now.date():
                        time.sleep(30)
                        continue
                    try:
                        state = acquire(context, DATA, db, now.date())
                        status(state, issue=now.date().isoformat(), pipeline='DURABLE_OUTBOX_ONLY')
                        failures = 0
                    except GateError as exc:
                        # Only our fixed reason codes are logged, never browser URLs/errors.
                        status(str(exc), issue=now.date().isoformat())
                        failures += 1
                        if 'AUTH_REQUIRED' in str(exc) or failures >= 3:
                            blocked_date = now.date()
                    except Exception:
                        status('BROWSER_OR_NETWORK_ERROR', issue=now.date().isoformat())
                        failures += 1
                        if failures >= 3:
                            blocked_date = now.date()
                    if mode == 'once':
                        # Leave status inspectable instead of a Railway restart/download loop.
                        blocked_date = now.date()
                        mode = 'paused'
                    time.sleep(min(120 * 2 ** failures, 900))
                else:
                    if mode != 'paused':
                        status('WAITING_FOR_WINDOW') if STATE.get('state') != 'WAITING_FOR_WINDOW' else None
                    time.sleep(30)
        finally:
            context.close()

if __name__ == '__main__':
    main()
