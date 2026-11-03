"""Frozen, file-based native-session comparison; no hidden API calls."""
import argparse,hashlib,json,re,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
STAGES=['direct','revise','extract','relate']
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):
 p.parent.mkdir(exist_ok=True,parents=True)
 with p.open('x') as f:f.write(o if isinstance(o,str) else json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def verify():
 d=read(ROOT/'freeze_manifest.json')
 for name,h in d['files'].items():
  if sha(ROOT/name)!=h:raise ValueError('Frozen content changed: '+name)
 return d

def freeze():
 ids=read(ROOT/'case_ids.json');assert len(ids)==15 and len(set(ids))==15
 for cid in ids:assert (ROOT/'public'/f'{cid}.json').exists() and (ROOT/'gold'/f'{cid}.json').exists()
 files=list((ROOT/'public').glob('*.json'))+list((ROOT/'gold').glob('*.json'))+list((ROOT/'prompts').glob('*.txt'))+[ROOT/n for n in ['harness.py','protocol.md','scoring_spec.md','case_ids.json','config.json','gold_adjudication.json']]
 write(ROOT/'freeze_manifest.json',{'created_at':now(),'files':{str(p.relative_to(ROOT)):sha(p) for p in sorted(files)},'status':'pre-prediction freeze'})

def prepare(cid,stage):
 verify();assert cid in read(ROOT/'case_ids.json') and stage in STAGES
 text=(ROOT/'prompts/common.txt').read_text()+'\n'+(ROOT/'prompts'/f'{stage}.txt').read_text()+'\nPUBLIC INPUT\n'+(ROOT/'public'/f'{cid}.json').read_text()
 if stage in ['revise','relate']:
  prior='direct' if stage=='revise' else 'extract';text+='\nUNTRUSTED PRIOR OUTPUT\n'+(ROOT/'responses'/f'{cid}_{prior}.json').read_text()
 call=cid+'_'+stage;path=ROOT/'requests'/f'{call}.txt';write(path,text)
 meta={'call_id':call,'case_id':cid,'stage':stage,'prepared_at':now(),'request_sha256':sha(path),'model_alias':None,'immutable_model_id':None,'reasoning_effort':None,'api_cost':None,'token_usage':None,'status':'prepared'}
 write(ROOT/'calls'/f'{call}.json',meta)
 print(str(path.resolve()))

def parse(path):
 txt=path.read_text().strip()
 if txt.startswith('```'):txt=re.sub(r'^```(?:json)?\s*|\s*```$','',txt)
 return json.loads(txt)

def pointer(obj,p):
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
 return obj

def quoted_value(packet,loc):
 if loc.startswith('/'):
  v=pointer(packet,loc);return v if isinstance(v,str) else json.dumps(v,ensure_ascii=False)
 m=re.fullmatch(r'L(\d+)(?:-L?(\d+))?',loc)
 if not m:raise ValueError('Unknown locator')
 i,j=int(m[1]),int(m[2] or m[1]);inp=packet['input'];lines=inp['prior_record'].splitlines()+inp['target_action'].splitlines()
 if i<1 or j<i or j>len(lines):raise ValueError('Out-of-range lines')
 return '\n'.join(lines[i-1:j])

def validate(packet,obj,stage):
 errors=[]
 if not isinstance(obj,dict):return ['not an object']
 if stage=='extract':
  if not isinstance(obj.get('requirements'),list) or not obj['requirements']:errors.append('requirements missing')
  return errors
 if obj.get('decision') not in ['Supported','Unsupported','Indeterminate'] and stage!='relate':errors.append('decision invalid')
 issues=obj.get('issues')
 if not isinstance(issues,list) or not issues:return errors+['issues missing']
 if all(isinstance(r,dict) and r.get('relation')=='not_applicable' for r in issues):errors.append('no applicable focal relation')
 for n,r in enumerate(issues):
  if not isinstance(r,dict):errors.append(f'issue {n} not object');continue
  for k in ['field','requirement','relation','exception','rationale','evidence']:
   if k not in r:errors.append(f'issue {n} missing {k}')
  if r.get('relation') not in ['satisfied','violated','unresolved','not_applicable']:errors.append(f'issue {n} relation invalid')
  if not isinstance(r.get('evidence'),list):errors.append(f'issue {n} evidence invalid');continue
  for e in r['evidence']:
   try:
    value=quoted_value(packet,e['locator']);assert isinstance(e['quote'],str) and e['quote'] and e['quote'] in value
   except Exception:errors.append(f'issue {n} bad reference: {e.get("locator") if isinstance(e,dict) else e}')
 return errors

def aggregate(obj):
 statuses=[x['relation'] for x in obj['issues']]
 decision='Unsupported' if 'violated' in statuses else 'Indeterminate' if 'unresolved' in statuses else 'Supported'
 return {**obj,'decision':decision}

def collect(call):
 verify();meta=read(ROOT/'calls'/f'{call}.json');raw=ROOT/'responses'/f'{call}.json';packet=read(ROOT/'public'/f"{meta['case_id']}.json")
 try:
  obj=parse(raw);errors=validate(packet,obj,meta['stage']);parse_error=None
 except Exception as e:obj=None;errors=['parse failure'];parse_error=str(e)
 result={'call_id':call,'collected_at':now(),'response_sha256':sha(raw),'response_utf8_bytes':raw.stat().st_size,'format_reference_errors':errors,'parse_error':parse_error,'interval_seconds':(datetime.now(timezone.utc)-datetime.fromisoformat(meta['prepared_at'])).total_seconds(),'interval_definition':'preparation to collection, not pure model latency','token_usage':None,'model_alias':None,'immutable_model_id':None}
 write(ROOT/'validation'/f'{call}.json',result)
 if meta['stage']=='relate' and obj and not errors:write(ROOT/'predictions'/f"{meta['case_id']}_P2.json",aggregate(obj))
 elif meta['stage'] in ['direct','revise'] and obj:write(ROOT/'predictions'/f"{meta['case_id']}_{'D1' if meta['stage']=='direct' else 'D2'}.json",obj)
 print(json.dumps(result))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','verify','prepare','collect']);p.add_argument('case',nargs='?');p.add_argument('stage',nargs='?');a=p.parse_args()
 if a.command=='freeze':freeze()
 elif a.command=='verify':verify();print('Verified')
 elif a.command=='prepare':prepare(a.case,a.stage)
 else:collect(a.case)
