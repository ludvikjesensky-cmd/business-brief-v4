import datetime as dt
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, DictionaryObject
from watcher import GateError, validate, publish, database, recover, in_window, parse_issue, TZ

ISSUE = dt.date(2026, 10, 8)

def fixture(path, pages=('A1', 'B1'), date='OCTOBER 8, 2026'):
    writer = PdfWriter()
    font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                            NameObject('/Subtype'): NameObject('/Type1'),
                            NameObject('/BaseFont'): NameObject('/Helvetica')})
    font_ref = writer._add_object(font)
    for label in pages:
        page = writer.add_blank_page(width=500, height=700)
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'):font_ref})})
        stream = DecodedStreamObject()
        stream.set_data(f'BT /F1 12 Tf 20 650 Td ({date} {label}) Tj ET'.encode())
        page[NameObject('/Contents')] = writer._add_object(stream)
    writer.write(path)

class Gates(unittest.TestCase):
    def test_invalid_inputs_do_not_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / 'input.pdf'
            pdf.write_text('<html>Sign in</html>')
            with self.assertRaisesRegex(GateError, 'NOT_PDF'):
                validate(pdf, ISSUE, ['A1', 'B1'])
            fixture(pdf, pages=['A1'])
            with self.assertRaisesRegex(GateError, 'PAGE_COUNT_MISMATCH'):
                validate(pdf, ISSUE, ['A1', 'B1'])
            fixture(pdf, date='OCTOBER 7, 2026')
            with self.assertRaisesRegex(GateError, 'WRONG_OR_UNVERIFIED_DATE'):
                validate(pdf, ISSUE, ['A1', 'B1'])
            fixture(pdf, pages=['B1', 'A1'])
            with self.assertRaisesRegex(GateError, 'PAGE_LABEL_MISMATCH'):
                validate(pdf, ISSUE, ['A1', 'B1'])

    def test_publish_restart_and_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pdf = root / 'input.pdf'
            fixture(pdf)
            facts = validate(pdf, ISSUE, ['A1', 'B1'])
            db = database(root)
            self.assertTrue(publish(root, db, pdf, ISSUE, ['A1', 'B1'], facts))
            self.assertFalse(publish(root, db, pdf, ISSUE, ['A1', 'B1'], facts))
            # Simulate crash after atomic reference rename but before outbox insert.
            with db:
                db.execute('DELETE FROM events')
            recover(root, db)
            recover(root, db)
            self.assertEqual(db.execute('SELECT count(*) FROM events').fetchone()[0], 1)
            db.close()

    def test_prague_window_in_winter_and_summer(self):
        for month in (1, 7):
            self.assertFalse(in_window(dt.datetime(2026, month, 8, 7, 49, tzinfo=TZ)))
            self.assertTrue(in_window(dt.datetime(2026, month, 8, 7, 50, tzinfo=TZ)))
            self.assertFalse(in_window(dt.datetime(2026, month, 8, 9, 0, tzinfo=TZ)))
        self.assertEqual(parse_issue('Th 10/08/2026'), ISSUE)

if __name__ == '__main__':
    unittest.main()
