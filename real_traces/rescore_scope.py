"""Replay the post-hoc scope correction without altering frozen gold or predictions."""
import hashlib
import json
from pathlib import Path
from evaluate import evaluate, ROOT, read


def main():
    version = ROOT / 'corrections/scope_v2'
    original = read(version / 'original_hashes.json')
    def verify_originals():
        for name, expected in original.items():
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    verify_originals()
    before = read(ROOT / 'results/summary.json')
    # Replay v1 through the same evaluator to check compatibility before applying v2.
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        assert evaluate(out_dir=temp) == before, 'Original results did not reproduce'
    after = evaluate(out_dir=version / 'results', gold_overrides=version / 'gold',
                     semantic_path=version / 'semantic_ratings.json')
    original_rows = {(x['case_id'], x['method']): x for x in read(ROOT / 'results/per_case.json')}
    changed = []
    for row in read(version / 'results/per_case.json'):
        old = original_rows[(row['case_id'], row['method'])]
        delta = {k: [old[k], row[k]] for k in row if row[k] != old[k]}
        if delta:
            assert row['case_id'] in ('AHN08', 'AHN09'), row
            assert set(delta) == {'semantic_components_pass', 'joint_correct'}, delta
            changed.append({'case_id': row['case_id'], 'method': row['method'], 'changes': delta})
    assert len(changed) == 6
    for method in before:
        for key in before[method]:
            if key != 'joint_diagnostic_accuracy':
                assert before[method][key] == after[method][key], (method, key)
    verify_originals()
    report = {'type': 'post-evaluation scope correction using unchanged saved predictions',
              'new_inference': False, 'human_disagreements_adjudicated': False,
              'before': before, 'after': after, 'changed_rows': changed,
              'original_hashes_verified': len(original)}
    (version / 'impact.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({m: {'decision': after[m]['decision_accuracy'],
                         'joint_before': before[m]['joint_diagnostic_accuracy'],
                         'joint_after': after[m]['joint_diagnostic_accuracy']} for m in after}, indent=2))

if __name__ == '__main__':
    main()
