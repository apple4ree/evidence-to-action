"""Reference/schema checks and label synthesis; semantic support stays a model judgment."""
FINAL_KEYS=['record_id','decision','first_source_events','transformation_events','reuse_events','scope_links','rationale','limitations']

def event_ids(case):return {x['event_id'] for x in case['history']}|set(case['target_action']['event_ids'])
def refs(value,ids):return isinstance(value,list) and all(isinstance(x,str) and x in ids for x in value)
def validate(case,obj,decision=True):
 if not isinstance(obj,dict):return ['not_object']
 ids=event_ids(case);err=[]
 if obj.get('record_id')!=case['record_id']:err.append('wrong_record_id')
 if decision and obj.get('decision') not in ['supported','unsupported','indeterminate']:err.append('invalid_decision')
 for k in ['first_source_events','transformation_events','reuse_events']:
  if not refs(obj.get(k),ids):err.append('invalid_'+k)
 links=obj.get('scope_links')
 if not isinstance(links,list):err.append('invalid_scope_links')
 else:
  for x in links:
   if not isinstance(x,dict) or not isinstance(x.get('from'),str) or not isinstance(x.get('to'),str) or x['from'] not in ids or x['to'] not in ids or x.get('judgment') not in ['preserved','unsupported_change','unresolved'] or x.get('dimension') not in ['source_type','entity','time','condition','coverage','correction','other'] or not isinstance(x.get('change'),str) or not x['change'].strip():err.append('invalid_scope_link')
 if not isinstance(obj.get('rationale'),str) or not obj['rationale'].strip():err.append('missing_rationale')
 if not isinstance(obj.get('limitations'),list) or any(not isinstance(x,str) for x in obj['limitations']):err.append('invalid_limitations')
 return err

def aggregate(case,obj):
 err=validate(case,obj,decision=False);ids=event_ids(case);checks=obj.get('checks',[]) if isinstance(obj,dict) else [];statuses=[];seen=set()
 if not isinstance(checks,list):err.append('invalid_checks');checks=[]
 for c in checks:
  if not isinstance(c,dict):err.append('invalid_check');continue
  rid=c.get('requirement_id')
  if not isinstance(rid,str) or not rid or rid in seen:err.append('invalid_requirement_id')
  else:seen.add(rid)
  if not refs(c.get('policy_events'),ids) or not refs(c.get('evidence_events'),ids):err.append('invalid_check_references')
  if not isinstance(c.get('requirement_text'),str) or not c['requirement_text'].strip() or not isinstance(c.get('rationale'),str) or not c['rationale'].strip():err.append('missing_check_text')
  if c.get('status') not in ['satisfied','excepted','violated','unresolved']:err.append('invalid_check_status')
  else:statuses.append(c['status'])
 coverage=obj.get('coverage') if isinstance(obj,dict) else None
 if coverage not in ['complete','incomplete','unknown']:err.append('invalid_coverage')
 decision='indeterminate'
 if not err:
  if 'violated' in statuses:decision='unsupported'
  elif statuses and 'unresolved' not in statuses and coverage=='complete':decision='supported'
 out={k:obj.get(k) for k in FINAL_KEYS if k!='decision'} if isinstance(obj,dict) else {}
 out['decision']=decision
 # shortcut: exact IDs validate existence, not entailment or actual actor visibility.
 return out,err
