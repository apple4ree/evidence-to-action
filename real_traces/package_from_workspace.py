"""Refresh public artifacts from the local research workspace, without changing it."""
import json,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=ROOT.parents[2]
SOURCE=WORK/'research_2026_11/underspecification_proposal/real_trace_benchmark'
EXPERIMENT=SOURCE/'experiment'
def read(p):return json.loads(p.read_text())
def put(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def publishable(p):
 rel=p.relative_to(ROOT)
 return p.is_file() and p.name!='publish_batch_paths.json' and not set(rel.parts)&{'__pycache__','public','requests','source_cache'} and rel.as_posix() not in {'review/cases.js','review/review.html','review/build_check.json'}
def main():
 recipes=[]
 for cid in read(EXPERIMENT/'case_ids.json'):
  public=read(EXPERIMENT/'public'/f'{cid}.json');private=read(SOURCE/'private'/f'{cid}.json');inp=public['input'];original=WORK/private['source']['local_path'];raw=original.read_bytes();assert hashlib.sha256(raw).hexdigest()==public['source']['sha256']
  spec={'case_id':cid,'source_url':public['source']['url'],'source_sha256':public['source']['sha256'],'source_git_blob_sha':private['source'].get('git_blob_sha'),'public_sha256':sha(EXPERIMENT/'public'/f'{cid}.json'),'template':public}
  if 'prior_record' in inp:
   spec['line_start']=inp['target_locator']['line_start'];spec['line_end']=inp['target_locator']['line_end'];inp['prior_record']=None
  else:
   data=json.loads(raw);spec['history_key']='history';spec['history_count']=len(inp['history']);assert data['history'][:spec['history_count']]==inp['history'];inp['history']=None
   spec['target_pointer']=inp['target_locator']['json_pointer']
   if 'task' in inp:
    spec['question_count']=len(inp['task']);assert data['question'][:spec['question_count']]==inp['task'];inp['task']=None
  inp['target_action']=None;recipes.append(spec)
 put(ROOT/'input_recipes.json',recipes)
 # Frozen files are copied byte-for-byte. Source trace bodies and prepared requests
 # are restored from pinned upstream files, rather than rehosted wholesale.
 names=['harness.py','evaluate.py','test_harness.py','case_ids.json','config.json','freeze_manifest.json','protocol.md','scoring_spec.md','gold_adjudication.json','scoring_implementation_manifest.json','technical_retries.json','semantic_ratings.json']
 for name in names:
  src=EXPERIMENT/name
  if src.exists():shutil.copyfile(src,ROOT/name)
 for dirname in ['prompts','gold','calls','responses','validation','predictions','results']:
  src=EXPERIMENT/dirname
  if src.exists():
   for p in src.glob('*'):
    if p.is_file():(ROOT/dirname).mkdir(exist_ok=True);shutil.copyfile(p,ROOT/dirname/p.name)
 for p in (EXPERIMENT/'runtime').glob('*.json'):
  obj=read(p)
  if 'native_task_duration_ms' not in obj:continue
  # Keep measured metrics and delivery flags; omit local session identifiers,
  # filesystem paths and tool-call argument bodies from the public export.
  keep=['single_task_completion','exact_invocation_verified','child_user_invocation_match','invocation_source','prepared_input_delivery','truncation_output_indices','model_aliases','reasoning_efforts','immutable_model_id','cost','native_task_duration_ms','time_to_first_token_ms','session_total_token_usage','unique_response_usage_records','response_usage_sum','tool_call_count','raw_response_sha256','note']
  out={k:obj[k] for k in keep if k in obj};out['suspicious_access_call_count']=len(obj.get('suspicious_access_calls',[]));out['export_note']='Runtime metrics subset; original local audit preserved in research workspace.';put(ROOT/'runtime'/p.name,out)
 put(ROOT/'request_hashes.json',{p.name:sha(p) for p in (EXPERIMENT/'requests').glob('*.txt')})
 put(ROOT/'publish_files.json',sorted(set([str(p.relative_to(ROOT.parent)) for p in ROOT.rglob('*') if publishable(p)]+['real_traces/publish_files.json','real_traces/export_manifest.json'])))
 put(ROOT/'export_manifest.json',{'source_freeze_sha256':sha(EXPERIMENT/'freeze_manifest.json'),'public_inputs':'reconstruct using restore_inputs.py','files':{str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*')) if publishable(p) and p.name!='export_manifest.json'}})
 print('Exported',len(recipes),'input recipes;',len(list((ROOT/'responses').glob('*.json'))),'raw responses')
if __name__=='__main__':main()
