"""Scope correction must retain the remaining rubric and its failure behavior."""
import json
import tempfile
import unittest
from pathlib import Path
from evaluate import evaluate, ROOT, read

V2 = ROOT / 'corrections/scope_v2'

class ScopeCorrectionTests(unittest.TestCase):
    def test_only_two_components_removed(self):
        old_ratings = read(ROOT / 'semantic_ratings.json')
        new_ratings = read(V2 / 'semantic_ratings.json')
        for cid, removed in [('AHN08', 'normal_value'), ('AHN09', 'file_link')]:
            old, new = read(ROOT / 'gold' / (cid + '.json')), read(V2 / 'gold' / (cid + '.json'))
            self.assertEqual(new['decision'], old['decision'])
            self.assertEqual(new['semantic_components'], [c for c in old['semantic_components'] if c['id'] != removed])
            for method in ('D1', 'D2', 'P2'):
                key = cid + '_' + method
                self.assertEqual(new_ratings[key]['components'], {k: v for k, v in old_ratings[key]['components'].items() if k != removed})
        for key in old_ratings:
            if not key.startswith(('AHN08_', 'AHN09_')):
                self.assertEqual(old_ratings[key], new_ratings[key])

    def test_remaining_failure_still_fails_joint(self):
        ratings = read(V2 / 'semantic_ratings.json')
        ratings['AHN08_D1']['components']['location_gap'] = 'fail'
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / 'ratings.json').write_text(json.dumps(ratings))
            evaluate(out_dir=folder / 'results', gold_overrides=V2 / 'gold', semantic_path=folder / 'ratings.json')
            rows = read(folder / 'results/per_case.json')
            row = next(r for r in rows if r['case_id'] == 'AHN08' and r['method'] == 'D1')
            self.assertTrue(row['decision_correct'])
            self.assertFalse(row['joint_correct'])

if __name__ == '__main__':
    unittest.main()
