"""Public-only call preparation and append-only runtime capture; never invokes models."""
import argparse, hashlib, json, random
from datetime import datetime, timezone
from pathlib import Path
from workflow import ROOT, aggregate

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def write_new(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f: f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def verify_freeze():
    f=read(ROOT/'freeze_manifest.json')
    bad=[p for p,h in f['sha256'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    if bad: raise ValueError('Frozen dependencies changed: '+str(bad))
    return f

def freeze():
    if list((ROOT/'calls').glob('test_*.json')):raise ValueError('Cannot freeze after test call preparation')
    rows=read(ROOT/'data/private_split_plan.json')['entries']
    gold=read(ROOT/'review/adjudicated_gold.json')['entries']
    ids=[x['record_id'] for x in rows]
    if len(ids)!=len(set(ids)) or set(ids)!=set(gold):raise ValueError('ID/gold coverage mismatch')
    dev={x['family_id'] for x in rows if x['split']=='dev'};test={x['family_id'] for x in rows if x['split']=='test'}
    if dev&test:raise ValueError('Family leakage')
    for rid in ids:
        case=read(ROOT/'data/public_cases'/f'{rid}.json')
        forbidden={'decision','gold','family_id','variant','variant_type','condition_tags','complexity_tags','split'}
        if forbidden&set(case):raise ValueError('Private metadata in public case '+rid)
        es=[e['event_id'] for e in case['history']]
        if len(es)!=len(set(es)):raise ValueError('Duplicate event ID')
    test_ids=[x['record_id'] for x in rows if x['split']=='test'];random.Random(20261103).shuffle(test_ids)
    write_new(ROOT/'test_schedule.json',{'seed':20261103,'record_ids':test_ids,'stage_orders':{rid: ['direct','revise','extract','relate'] if i%2==0 else ['extract','relate','direct','revise'] for i,rid in enumerate(test_ids)}})
    files=[p for directory in ['data','prompts','review'] for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in str(p)]
    files += list(ROOT.glob('*.py'))+list(ROOT.glob('*.csv'))+[ROOT/'run_config.json',ROOT/'protocol.md',ROOT/'test_schedule.json',ROOT/'scoring_spec.md',ROOT/'development_changes.md',ROOT/'dev_validation.json',ROOT/'rigor_design_review.md']
    if (ROOT/'dev_selection.json').exists():files.append(ROOT/'dev_selection.json')
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(files))}
    write_new(ROOT/'freeze_manifest.json',{'version':'expanded-v1','created_utc':now(),'sha256':hashes,'dev_families':len(dev),'test_families':len(test),'test_cases':len(test_ids)})
    print('Frozen',len(hashes),'files;',len(test_ids),'test cases')

def prepare(rid,stage,phase,previous=None,attempt=0):
    rows=read(ROOT/'data/private_split_plan.json')['entries']
    if not any(x['record_id']==rid and x['split']==phase for x in rows):raise ValueError('ID not in requested split')
    if phase=='dev' and (ROOT/'dev_selection.json').exists() and rid not in read(ROOT/'dev_selection.json')['record_ids']:raise ValueError('Not in predetermined dev subset')
    if phase=='test':
        verify_freeze()
        if rid not in read(ROOT/'test_schedule.json')['record_ids']:raise ValueError('Not a test ID')
    if attempt not in [0,1]:raise ValueError('At most one technical retry')
    stem=f'{phase}_{rid}_{stage}';call_id=stem+(f'_retry{attempt}' if attempt else '')
    if attempt:
        records=[json.loads(x) for x in (ROOT/'execution_log.jsonl').read_text().splitlines()]
        prior=[x for x in records if x['call_id']==stem]
        if not prior or prior[-1]['status']!='technical_failure':raise ValueError('Only technical failures may retry')
    case=read(ROOT/'data/public_cases'/f'{rid}.json')
    # Deliberate allowlist: tags, labels, family metadata cannot enter detector input.
    allowed=['record_id','policy','tool_documentation','history','target_action','capture']
    public={k:case[k] for k in allowed if k in case}
    # Original cases may use capture_provenance; preserve that public scope statement.
    for k in ['capture_provenance','capture_scope','capture_note','context']:
        if k in case:public[k]=case[k]
    text=(ROOT/'prompts/common.txt').read_text()+'\n'+(ROOT/'prompts'/f'{stage}.txt').read_text()+'\nRAW CASE\n'+json.dumps(public,ensure_ascii=False,indent=2)
    if stage in ['revise','relate']:
        expected=ROOT/'raw'/f"{phase}_{rid}_{'direct' if stage=='revise' else 'extract'}.txt"
        if previous and Path(previous).resolve()!=expected.resolve():raise ValueError('Wrong preceding output')
        text+='\nUNTRUSTED PREVIOUS STAGE OUTPUT\n'+expected.read_text()
    elif previous:raise ValueError('Unexpected preceding output')
    path=ROOT/'calls'/f'{call_id}.txt';path.parent.mkdir(exist_ok=True)
    with path.open('x') as f:f.write(text+'\n')
    message=f'Read ONLY {path.resolve()} and follow its instructions. Do not inspect other files, private labels, other cases, or external sources. Use a tool only to read this file; do not write files. Return requested JSON in final. This is one isolated prediction.'
    cfg=read(ROOT/'run_config.json')
    write_new(ROOT/'calls'/f'{call_id}.json',{'call_id':call_id,'record_id':rid,'stage':stage,'phase':phase,'attempt':attempt,'created_utc':now(),'task_sha256':sha(path),'invocation_message':message,'model':cfg['model'],'settings':cfg['settings']})
    print(message)

def save(call_id,response,status,task_id=None):
    meta=read(ROOT/'calls'/f'{call_id}.json');raw=Path(response).read_text() if response else ''
    if status=='success' and not response:raise ValueError('Response required')
    target=ROOT/'responses'/f'{call_id}.txt';target.parent.mkdir(exist_ok=True)
    with target.open('x') as f:f.write(raw)
    record={**meta,'completed_utc':now(),'status':status,'runtime_task_id':task_id,'response_sha256':sha(target),'tokens':None,'cost':None,'exact_model_version':None,'latency_definition':'preparation to response storage, includes orchestration','elapsed_seconds':(datetime.now(timezone.utc)-datetime.fromisoformat(meta['created_utc'])).total_seconds()}
    if status=='success':
        stem=f"{meta['phase']}_{meta['record_id']}_{meta['stage']}";dest=ROOT/'raw';dest.mkdir(exist_ok=True)
        with (dest/f'{stem}.txt').open('x') as f:f.write(raw)
        try:
            parsed=json.loads(raw);write_new(dest/f'{stem}.json',parsed);record['json_valid']=True
        except json.JSONDecodeError:record['json_valid']=False
        if meta['stage']=='relate':
            case=read(ROOT/'data/public_cases'/f"{meta['record_id']}.json")
            try:relation=json.loads(raw)
            except json.JSONDecodeError:relation={}
            write_new(dest/f"{meta['phase']}_{meta['record_id']}_aggregate.json",aggregate(case,relation))
    with (ROOT/'execution_log.jsonl').open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
    print(json.dumps({'call_id':call_id,'status':status,'json_valid':record.get('json_valid')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('freeze');sub.add_parser('verify')
    a=sub.add_parser('prepare');a.add_argument('record_id');a.add_argument('stage',choices=['direct','revise','extract','relate']);a.add_argument('--phase',required=True,choices=['dev','test']);a.add_argument('--previous');a.add_argument('--attempt',type=int,default=0)
    a=sub.add_parser('save');a.add_argument('call_id');a.add_argument('--response');a.add_argument('--status',required=True,choices=['success','technical_failure']);a.add_argument('--task-id')
    a=p.parse_args()
    if a.cmd=='freeze':freeze()
    elif a.cmd=='verify':verify_freeze();print('Verified')
    elif a.cmd=='prepare':prepare(a.record_id,a.stage,a.phase,a.previous,a.attempt)
    else:save(a.call_id,a.response,a.status,a.task_id)
