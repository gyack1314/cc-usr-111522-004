import tempfile,unittest,json
from pathlib import Path
from temporal.storage import SegmentStore

class Base(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name);self.store=SegmentStore(self.path/'store')
        sample=json.loads((Path(__file__).resolve().parents[1]/'data/sample.json').read_text(encoding='utf-8'))
        for name,rows in sample.items():self.store.write_segment(name,rows)
    def tearDown(self):self.tmp.cleanup()

class StorageTests(Base):
    def test_roundtrip(self):
        rows=[{'row_id':str(i),'v':i} for i in range(5)];self.store.write_segment('roundtrip',rows)
        self.assertEqual(list(self.store.scan('roundtrip')),rows);self.assertEqual(len(self.store.pages_read),3)
    def test_projection_keeps_missing(self):
        self.store.write_segment('project',[{'row_id':'a','v':None},{'row_id':'b'}]);self.assertEqual(list(self.store.scan('project',['v'])),[{'v':None},{}])
    def test_segment_immutable(self):
        self.store.write_segment('fixed',[{'row_id':'a'}]);self.assertRaises(ValueError,self.store.write_segment,'fixed',[])
    def test_page_corruption(self):
        self.store.write_segment('damaged',[{'row_id':'a'}]);meta=self.store.manifest('damaged')['pages'][0];(self.store.root/meta['file']).write_bytes(b'[]')
        self.assertRaises(ValueError,list,self.store.scan('damaged'))
    def test_duplicate_row_identity(self):self.assertRaises(ValueError,self.store.write_segment,'duplicate',[{'row_id':'a'}]*2)
    def test_fingerprint_and_no_projection_scan_skip(self):
        self.store.write_segment('identity',[{'row_id':'a','v':2}]);first=self.store.fingerprint('identity');self.assertEqual(len(first),64)
        list(self.store.scan('identity',['row_id']));self.assertGreater(self.store.bytes_read,0)

from temporal.model import Period
from temporal.operations import clip,snapshot_at,overlap_pairs
class DomainTests(Base):
    def test_half_open(self):self.assertIsNone(Period(0,5).intersection(Period(5,8)))
    def test_snapshot(self):self.assertEqual({r['row_id'] for r in snapshot_at(self.store,'enrollment',5)},{'s2','s3'})
    def test_multiplicity(self):self.assertEqual(next(r for r in overlap_pairs(self.store,'enrollment','teaching') if r['left']=='s1')['multiplicity'],6)
    def test_clip(self):self.assertTrue(all(4<=r['start']<r['end']<=6 for r in clip(self.store,'enrollment',4,6)))
