"""Tests for restoration trust boundaries; no network or model calls."""
import json,tempfile,unittest
from pathlib import Path
import restore_inputs as restore
class RestoreTests(unittest.TestCase):
 def test_pointer_escapes(self):self.assertEqual(restore.pointer({'a/b':[{'~v':'x'}]},'/a~1b/0/~0v'),'x')
 def test_missing_and_corrupt_cache_rejected(self):
  original=restore.ROOT
  try:
   with tempfile.TemporaryDirectory() as d:
    root=Path(d);restore.ROOT=root
    spec=json.loads((original/'input_recipes.json').read_text())[0]
    (root/'input_recipes.json').write_text(json.dumps([spec]))
    cache=root/'cache'
    with self.assertRaises(FileNotFoundError):restore.restore(cache,True)
    (cache/spec['source_sha256']).write_bytes(b'corrupt')
    with self.assertRaisesRegex(ValueError,'Source hash mismatch'):restore.restore(cache,True)
    self.assertFalse((root/'public').exists())
  finally:restore.ROOT=original
if __name__=='__main__':unittest.main()
