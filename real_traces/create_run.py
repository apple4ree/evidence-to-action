"""Create a separate, empty prediction run using the fixed public evaluation inputs."""
import argparse,shutil
from pathlib import Path
from harness import ROOT,verify,read

def create(destination):
 verify()
 destination=destination.resolve()
 if destination.exists():raise FileExistsError('Choose a new directory; existing runs are never overwritten')
 destination.mkdir(parents=True)
 for name in read(ROOT/'freeze_manifest.json')['files']:
  target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
 for name in ['freeze_manifest.json','evaluate.py','test_harness.py']:
  shutil.copyfile(ROOT/name,destination/name)
 (destination/'NEW_RUN.md').write_text('New inference workspace. Gold is evaluation-only: predictors read only requests/*.txt. No original predictions or semantic scores were copied. Record your own model ID, settings, request/response and usage.\n')
 print(destination)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('destination',type=Path);a=p.parse_args();create(a.destination)
