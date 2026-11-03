"""Prepare isolated native sessions and preserve responses; no model API client."""
import argparse,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from workflow import aggregate,validate
ROOT=Path(__file__).resolve().parent
STAGES=['direct','revise','extract','relate']
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def write_new(p,text):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:f.write(text)
def json_new(p,obj):write_new(p,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def verify():
 d=read(ROOT/'freeze_manifest.json');bad=[n for n,h in d['sha256'].items() if not (ROOT/n).is_file() or sha(ROOT/n)!=h]
 if bad:raise ValueError('Frozen changes: '+str(bad))
 return d

def freeze():
 if list((ROOT/'calls').glob('*.json')):raise ValueError('Calls already prepared')
 entries=read(ROOT/'split.json')['entries'];ids=[x['record_id'] for x in entries]
 if len(set(ids))!=len(ids):raise ValueError('Duplicate record IDs')
 for rid in ids:
  c=read(ROOT/'public'/f'{rid}.json');events=[e['event_id'] for e in c['history']]+c['target_action']['event_ids']
  if len(events)!=len(set(events)):raise ValueError('Duplicate events or target in history')
 files=list(ROOT.glob('*.py'))+[ROOT/'split.json',ROOT/'protocol.md',ROOT/'scoring_spec.md']+list((ROOT/'prompts').glob('*.txt'))+list((ROOT/'public').glob('*.json'))+list((ROOT/'gold').glob('*.json'))
 if not list((ROOT/'gold').glob('*.json')):raise ValueError('Root must finalize gold before freeze')
 json_new(ROOT/'freeze_manifest.json',{'version':'provenance-comparison-v1','created_utc':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(files)}})

def records():return [json.loads(x) for x in (ROOT/'execution_log.jsonl').read_text().splitlines()] if (ROOT/'execution_log.jsonl').exists() else []
def prepare(rid,stage,attempt=0):
 verify()
 if stage not in STAGES or rid not in {x['record_id'] for x in read(ROOT/'split.json')['entries']}:raise ValueError('Invalid stage or case')
 if attempt not in [0,1]:raise ValueError('One technical retry at most')
 base=f'{rid}_{stage}';cid=base+(f'_retry{attempt}' if attempt else '')
 if attempt and not any(x['call_id']==base and x['status']=='technical_failure' for x in records()):raise ValueError('Retry requires no-response technical failure')
 case=read(ROOT/'public'/f'{rid}.json');allowed=['record_id','task','source','capture','history','target_action'];case={k:case[k] for k in allowed if k in case}
 txt=(ROOT/'prompts/common.txt').read_text()+'\n'+(ROOT/'prompts'/f'{stage}.txt').read_text()+'\nPUBLIC RECORD\n'+json.dumps(case,ensure_ascii=False,indent=2)
 if stage in ['revise','relate']:
  prior='direct' if stage=='revise' else 'extract';txt+='\nUNTRUSTED PREVIOUS STAGE OUTPUT\n'+(ROOT/'raw'/f'{rid}_{prior}.txt').read_text()
 path=ROOT/'calls'/f'{cid}.txt';write_new(path,txt+'\n')
 message=f'Read ONLY {path.resolve()} and follow its instructions. Do not inspect other files, source labels, gold, external sources, or other cases. Use functions.exec with tools.exec_command to cat this exact file, setting max_output_tokens=50000. Read the entire returned file including all history and any prior-stage output; do not substitute selective snippets. If output is truncated, read every omitted range before answering. Use tools only for reading this file; do not write files. Return requested JSON in final.'
 json_new(ROOT/'calls'/f'{cid}.json',{'call_id':cid,'record_id':rid,'stage':stage,'attempt':attempt,'created_utc':now(),'task_sha256':sha(path),'invocation_message':message,'model_alias':None,'immutable_model_version':None,'settings':None})
 print(message)

def save(cid,response,status,task_id=None):
 meta=read(ROOT/'calls'/f'{cid}.json')
 if any(r['call_id']==cid for r in records()):raise ValueError('Already saved')
 raw=Path(response).read_text() if response else ''
 if status=='success' and not raw:raise ValueError('Response required')
 if status=='technical_failure' and raw:raise ValueError('Content/semantic failures cannot be retried')
 write_new(ROOT/'responses'/f'{cid}.txt',raw)
 row={**meta,'completed_utc':now(),'status':status,'runtime_task_id':task_id,'response_sha256':sha(ROOT/'responses'/f'{cid}.txt'),'tokens':None,'cost':None,'elapsed_seconds':(datetime.now(timezone.utc)-datetime.fromisoformat(meta['created_utc'])).total_seconds(),'latency_scope':'preparation to storage; includes orchestration'}
 if status=='success':
  stem=f"{meta['record_id']}_{meta['stage']}";write_new(ROOT/'raw'/f'{stem}.txt',raw)
  try:obj=json.loads(raw);json_new(ROOT/'raw'/f'{stem}.json',obj);row['json_valid']=True
  except json.JSONDecodeError:obj={};row['json_valid']=False
  case=read(ROOT/'public'/f"{meta['record_id']}.json")
  if meta['stage']=='relate':
   out,errors=aggregate(case,obj);json_new(ROOT/'raw'/f"{meta['record_id']}_aggregate.json",out);json_new(ROOT/'raw'/f"{meta['record_id']}_aggregate_validation.json",{'errors':errors,'valid':not errors})
  elif meta['stage'] in ['direct','revise']:row['validation_errors']=validate(case,obj)
 with (ROOT/'execution_log.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 print(json.dumps({'call_id':cid,'status':status,'json_valid':row.get('json_valid')}))
def replay():
 count=0
 for f in (ROOT/'raw').glob('*_relate.json'):
  rid=f.name[:-12];out,errors=aggregate(read(ROOT/'public'/f'{rid}.json'),read(f));assert out==read(ROOT/'raw'/f'{rid}_aggregate.json');assert errors==read(ROOT/'raw'/f'{rid}_aggregate_validation.json')['errors'];count+=1
 print('Replayed',count)
if __name__=='__main__':
 p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
 for n in ['freeze','verify','replay']:s.add_parser(n)
 a=s.add_parser('prepare');a.add_argument('record_id');a.add_argument('stage',choices=STAGES);a.add_argument('--attempt',type=int,default=0)
 a=s.add_parser('save');a.add_argument('call_id');a.add_argument('--response');a.add_argument('--status',choices=['success','technical_failure'],required=True);a.add_argument('--task-id')
 a=p.parse_args()
 if a.cmd=='freeze':freeze()
 elif a.cmd=='verify':verify();print('Verified')
 elif a.cmd=='replay':replay()
 elif a.cmd=='prepare':prepare(a.record_id,a.stage,a.attempt)
 else:save(a.call_id,a.response,a.status,a.task_id)
