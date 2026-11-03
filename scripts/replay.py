"""Re-score frozen predictions. No model calls or new semantic judgments."""
import argparse, hashlib, json, subprocess, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--output',type=Path,default=ROOT/'runs/replay')
a=p.parse_args();out=a.output.resolve()
if out.exists():raise SystemExit('Refusing to overwrite: '+str(out))
archive=ROOT/'data/expanded_frozen.zip'
expected=json.loads((ROOT/'data/archive_manifest.json').read_text())['sha256']
if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:raise SystemExit('Archive hash mismatch')
with zipfile.ZipFile(archive) as z:
 for entry in z.infolist():
  dest=(out/entry.filename).resolve()
  if not dest.is_relative_to(out):raise SystemExit('Unsafe archive path')
 out.mkdir(parents=True)
 z.extractall(out)
subprocess.run([sys.executable,'harness.py','verify'],cwd=out,check=True)
subprocess.run([sys.executable,'-m','unittest','discover','-p','test_*.py'],cwd=out,check=True)
with (out/'scoring_stdout.json').open('w') as log:
 subprocess.run([sys.executable,'evaluate.py','score'],cwd=out,stdout=log,check=True)
actual=json.loads((out/'test_results.json').read_text())
original=json.loads((ROOT/'results/expanded_original.json').read_text())
for key in ['methods','comparisons','correct_label_wrong_diagnosis']:
 if actual[key]!=original[key]:raise SystemExit('Replayed results differ: '+key)
for method,data in actual['methods'].items():
 print(method,json.dumps(data['overall'],ensure_ascii=False))
print('PASS: frozen scoring reproduced. Model inference and semantic annotation were not rerun.')
