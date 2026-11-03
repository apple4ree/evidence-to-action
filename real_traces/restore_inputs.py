"""Restore exact evaluation packets from revision-pinned upstream source bytes."""
import argparse,copy,hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def digest(b):return hashlib.sha256(b).hexdigest()
def pointer(o,p):
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');o=o[int(k)] if isinstance(o,list) else o[k]
 return o
def restore(cache,offline=False):
 cache.mkdir(exist_ok=True,parents=True);recipes=json.loads((ROOT/'input_recipes.json').read_text())
 for spec in recipes:
  cached=cache/spec['source_sha256']
  if cached.exists():raw=cached.read_bytes()
  elif offline:raise FileNotFoundError('Missing cached source: '+str(cached))
  else:
   url=spec['source_url'].replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/',1)
   with urllib.request.urlopen(url,timeout=60) as response:raw=response.read()
  if digest(raw)!=spec['source_sha256']:raise ValueError('Source hash mismatch: '+spec['case_id'])
  if spec.get('source_git_blob_sha') and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=spec['source_git_blob_sha']:raise ValueError('Git blob hash mismatch')
  if not cached.exists():cached.write_bytes(raw)
  packet=copy.deepcopy(spec['template']);inp=packet['input']
  if 'line_start' in spec:
   lines=raw.decode().splitlines();inp['prior_record']='\n'.join(lines[:spec['line_start']-1]);inp['target_action']='\n'.join(lines[spec['line_start']-1:spec['line_end']])
  else:
   original=json.loads(raw);inp['history']=original[spec['history_key']][:spec['history_count']];inp['target_action']=pointer(original,spec['target_pointer'])
   if 'question_count' in spec:inp['task']=original['question'][:spec['question_count']]
  encoded=(json.dumps(packet,ensure_ascii=False,indent=2)+'\n').encode()
  if digest(encoded)!=spec['public_sha256']:raise ValueError('Reconstructed packet differs: '+spec['case_id'])
  path=ROOT/'public'/f"{spec['case_id']}.json";path.parent.mkdir(exist_ok=True)
  if path.exists() and path.read_bytes()!=encoded:raise ValueError('Existing input differs; refusing overwrite: '+str(path))
  path.write_bytes(encoded)
 # Restore archived requests, not fresh inference. Prior responses are the saved
 # original outputs; a new run must use its own first-stage responses.
 hashes=json.loads((ROOT/'request_hashes.json').read_text())
 for name,expected in hashes.items():
  cid,stage=name[:-4].rsplit('_',1)
  text=(ROOT/'prompts/common.txt').read_text()+'\n'+(ROOT/'prompts'/f'{stage}.txt').read_text()+'\nPUBLIC INPUT\n'+(ROOT/'public'/f'{cid}.json').read_text()
  if stage in ['revise','relate']:
   prior='direct' if stage=='revise' else 'extract';text+='\nUNTRUSTED PRIOR OUTPUT\n'+(ROOT/'responses'/f'{cid}_{prior}.json').read_text()
  if digest(text.encode())!=expected:raise ValueError('Request differs: '+name)
  path=ROOT/'requests'/name;path.parent.mkdir(exist_ok=True)
  if path.exists() and path.read_text()!=text:raise ValueError('Existing request differs: '+name)
  path.write_text(text)
 print(f'Restored {len(recipes)} exact inputs and {len(hashes)} archived requests')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,default=ROOT/'source_cache');p.add_argument('--offline',action='store_true');a=p.parse_args();restore(a.cache,a.offline)
