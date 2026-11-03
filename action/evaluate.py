"""Post-inference scoring with separately method-masked component judgments."""
import argparse,hashlib,json,random
from collections import Counter,defaultdict
from pathlib import Path
from workflow import ROOT,validate_direct
METHODS={'D1':'direct','D2':'revise','P2':'aggregate'}
LABELS=['supported','unsupported','indeterminate']
def read(p):return json.loads(p.read_text())
def write(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def ratio(a,b):return {'numerator':a,'denominator':b,'value':a/b if b else None}
def dataset(phase='test'):
 rows=read(ROOT/'data/private_split_plan.json')['entries'];gold=read(ROOT/'review/adjudicated_gold.json')['entries']
 selected=[r for r in rows if r['split']==phase]
 selection=ROOT/'dev_selection.json'
 if phase=='dev' and selection.exists():
  ids=set(read(selection)['record_ids']);selected=[r for r in selected if r['record_id'] in ids]
 return selected,gold

def load_prediction(rid,method,phase='test'):
 case=read(ROOT/'data/public_cases'/f'{rid}.json');p=ROOT/'raw'/f'{phase}_{rid}_{METHODS[method]}.json'
 try:pred=read(p)
 except (FileNotFoundError,json.JSONDecodeError):return {'decision':None,'issues':[],'summary':''},['missing_or_invalid_json']
 if not isinstance(pred,dict):return {'decision':None,'issues':[],'summary':''},['not_object']
 errors=validate_direct(case,pred)
 if method=='P2':errors+=pred.get('validation_errors',[]) if isinstance(pred.get('validation_errors',[]),list) else ['invalid_validation_errors']
 return pred,errors

def anon_id(rid,method):return 'c_'+hashlib.sha256(f'expanded-blind-v1:{rid}:{method}'.encode()).hexdigest()[:16]
def blind_pack(phase='test'):
 rows,gold=dataset(phase);pack=[];mapping={}
 for row in rows:
  rid=row['record_id'];case=read(ROOT/'data/public_cases'/f'{rid}.json')
  for method in METHODS:
   pred,errors=load_prediction(rid,method,phase);cid=anon_id(rid,method);mapping[cid]={'record_id':rid,'method':method}
   pack.append({'candidate_id':cid,'case':case,'gold':gold[rid],'candidate':{k:pred.get(k) for k in ['decision','issues','summary']},'schema_valid':not errors})
 pack.sort(key=lambda x:x['candidate_id']);write(ROOT/'review'/f'{phase}_semantic_blind_pack.json',pack);write(ROOT/'review'/f'{phase}_semantic_mapping_private.json',mapping)
 # Per-record packs preserve manageable reviewing units while method mapping stays separate.
 for rid in sorted({r['record_id'] for r in rows}):write(ROOT/'review'/f'{phase}_packets'/f'{rid}.json',[x for x in pack if x['case']['record_id']==rid])
 print('Candidates:',len(pack))

def validate_rating(rating,gold):
 if type(rating.get('summary_correct')) is not bool:raise ValueError('Missing summary correctness')
 if type(rating.get('extra_false_issue_count')) is not int or rating['extra_false_issue_count']<0:raise ValueError('Invalid extra issue count')
 units=rating.get('units');expected={x['unit_id'] for x in gold.get('issues',[])}
 if not isinstance(units,dict) or set(units)!=expected:raise ValueError('Exact gold unit ratings required')
 for u in units.values():
  if any(type(u.get(k)) is not bool for k in ['present','field_correct','requirement_correct','evidence_correct','exception_correct']):raise ValueError('All component judgments must be boolean')
 if not isinstance(rating.get('rationale'),str) or not rating['rationale'].strip():raise ValueError('Review rationale required')

def aggregate_rows(rows):
 n=len(rows);us=[r for r in rows if r['gold']=='unsupported'];ss=[r for r in rows if r['gold']=='supported'];ins=[r for r in rows if r['gold']=='indeterminate'];decidable=us+ss
 cm={g:{p:0 for p in LABELS+['invalid']} for g in LABELS}
 for r in rows:cm[r['gold']][r['prediction'] if r['valid'] else 'invalid']+=1
 out={'cases':n,'families':len({r['family_id'] for r in rows}),'confusion_matrix':cm,'decision_accuracy':ratio(sum(r['decision_correct'] for r in rows),n),'unsupported_recall':ratio(sum(r['decision_correct'] for r in us),len(us)),'supported_fpr':ratio(sum(r['prediction']=='unsupported' for r in ss),len(ss)),'indeterminate_recall':ratio(sum(r['decision_correct'] for r in ins),len(ins)),'unnecessary_abstention':ratio(sum(r['valid'] and r['prediction']=='indeterminate' for r in decidable),len(decidable)),'decision_coverage':ratio(sum(r['valid'] and r['prediction'] in LABELS[:2] for r in rows),n),'validity':ratio(sum(r['valid'] for r in rows),n),'full_diagnostic_joint':ratio(sum(r['joint_correct'] for r in rows),n),'unsupported_diagnostic_joint':ratio(sum(r['joint_correct'] for r in us),len(us)),'annotated_field_set_coverage':ratio(sum(r['annotated_fields_covered'] for r in us),len(us))}
 total=sum(r['unit_count'] for r in rows)
 for component in ['field','requirement','evidence','exception']:
  out[component+'_accuracy']=ratio(sum(r[component+'_correct_units'] for r in rows),total)
 out['diagnostic_omission']=ratio(sum(r['missing_units'] for r in rows),total)
 out['false_issue_candidates']=ratio(sum(r['extra_false_issue_count']>0 for r in rows),n)
 return out

def bootstrap(rows,key,seed=20261103,iterations=10000):
 families=sorted({r['family_id'] for r in rows});by={f:[r for r in rows if r['family_id']==f] for f in families};rng=random.Random(seed)
 if not families:return None
 # Resample whole families; average within-family accuracy gives equal family weight.
 means={f:sum(r[key] for r in rs)/len(rs) for f,rs in by.items()}
 vals=sorted(sum(means[rng.choice(families)] for _ in families)/len(families) for _ in range(iterations))
 return {'unit':'family','n_families':len(families),'iterations':iterations,'seed':seed,'estimate':sum(means.values())/len(means),'percentile_95':[vals[int(.025*iterations)],vals[min(iterations-1,int(.975*iterations))]]}

def edge_scores(rows,edges):
 by={r['record_id']:r for r in rows};out={}
 for kind in ['contrast','invariance']:
  es=[e for e in edges if e['kind']==kind and e['left'] in by and e['right'] in by]
  out[kind+'_both_correct']=ratio(sum(by[e['left']]['decision_correct'] and by[e['right']]['decision_correct'] for e in es),len(es))
  if kind=='invariance':out['invariance_prediction_retained']=ratio(sum(by[e['left']]['valid'] and by[e['right']]['valid'] and by[e['left']]['prediction']==by[e['right']]['prediction'] for e in es),len(es))
 return out

def score(phase='test'):
 if phase=='test':
  from harness import verify_freeze
  verify_freeze()
 rows,gold=dataset(phase);ratings=read(ROOT/'review'/f'{phase}_semantic_ratings.json')
 expected={anon_id(r['record_id'],m) for r in rows for m in METHODS}
 if set(ratings)!=expected:raise ValueError('Ratings must cover every candidate exactly')
 edgefile=ROOT/'data/comparison_edges.json';edges=read(edgefile)['edges'] if edgefile.exists() else []
 methods={}
 for method in METHODS:
  cr=[]
  for row in rows:
   rid=row['record_id'];g=gold[rid];rating=ratings[anon_id(rid,method)];validate_rating(rating,g);pred,errors=load_prediction(rid,method,phase)
   valid=not errors;correct=valid and pred.get('decision')==g['decision'];units=rating['units'];all_units=all(all(u[k] for k in ['present','field_correct','requirement_correct','evidence_correct','exception_correct']) for u in units.values())
   joint=correct and all_units and rating['extra_false_issue_count']==0 and rating['summary_correct']
   issues=pred.get('issues') if isinstance(pred.get('issues'),list) else []
   fields=sorted({x['field'] for x in issues if isinstance(x,dict) and isinstance(x.get('field'),str)})
   r={**row,'gold':g['decision'],'prediction':pred.get('decision'),'valid':valid,'validation_errors':errors,'decision_correct':correct,'joint_correct':joint,'annotated_fields_covered':correct and any(set(x).issubset(fields) for x in g.get('canonical_full_field_sets',[[]])),'unit_count':len(units),'missing_units':sum(not u['present'] for u in units.values()),'extra_false_issue_count':rating['extra_false_issue_count'],'review_rationale':rating['rationale'],'semantic_error_types':rating.get('error_types',[])}
   for c in ['field','requirement','evidence','exception']:r[c+'_correct_units']=sum(valid and u['present'] and u[c+'_correct'] for u in units.values())
   cr.append(r)
  families=sorted({r['family_id'] for r in cr});conditions=sorted({tag for r in cr for tag in r.get('condition_tags',[])});complexities=sorted({tag for r in cr for tag in r.get('complexity_tags',[])})
  methods[method]={'overall':aggregate_rows(cr),'by_family':{f:aggregate_rows([r for r in cr if r['family_id']==f]) for f in families},'by_condition':{t:aggregate_rows([r for r in cr if t in r.get('condition_tags',[])]) for t in conditions},'by_complexity':{t:aggregate_rows([r for r in cr if t in r.get('complexity_tags',[])]) for t in complexities},'edges':edge_scores(cr,edges),'by_edge_intervention':{t:edge_scores(cr,[e for e in edges if e.get('intervention_type')==t]) for t in sorted({e.get('intervention_type','unspecified') for e in edges})},'family_all_decisions_correct':ratio(sum(all(r['decision_correct'] for r in cr if r['family_id']==f) for f in families),len(families)),'family_bootstrap':{k:bootstrap(cr,k) for k in ['decision_correct','joint_correct']},'cases':cr}
 comparison={}
 by={m:{r['record_id']:r for r in d['cases']} for m,d in methods.items()}
 for a,b in [('D1','P2'),('D1','D2'),('D2','P2')]:
  comparison[a+'_vs_'+b]={}
  for metric in ['decision_correct','joint_correct']:
   comparison[a+'_vs_'+b][metric]={'a_only':[rid for rid in by[a] if by[a][rid][metric] and not by[b][rid][metric]],'b_only':[rid for rid in by[a] if by[b][rid][metric] and not by[a][rid][metric]]}
  paired=[]
  for r in methods[a]['cases']:paired.append({**r,'delta':int(by[b][r['record_id']]['joint_correct'])-int(r['joint_correct'])})
  comparison[a+'_vs_'+b]['joint_difference_b_minus_a']=bootstrap(paired,'delta')
 result={'version':'expanded-v1','scope':'LLM-authored and LLM-reviewed synthetic diagnostics; core annotated relations, not exhaustive policy coverage or actor error prevalence','phase':phase,'methods':methods,'comparisons':comparison,'correct_label_wrong_diagnosis':{m:[r['record_id'] for r in d['cases'] if r['decision_correct'] and not r['joint_correct']] for m,d in methods.items()}}
 log=ROOT/'execution_log.jsonl'
 if log.exists():
  events=[json.loads(x) for x in log.read_text().splitlines() if x.strip()];cost={}
  for ph in ['dev','test']:
   es=[e for e in events if e['phase']==ph];cost[ph]={'attempts':len(es),'successful_responses':sum(e['status']=='success' for e in es),'technical_failures':sum(e['status']=='technical_failure' for e in es),'retries':sum(e.get('attempt',0)>0 for e in es),'elapsed_seconds_sum':sum(e['elapsed_seconds'] for e in es),'tokens':None,'cost':None,'by_stage':dict(Counter(e['stage'] for e in es))}
  result['execution']=cost
 write(ROOT/f'{phase}_results.json',result)
 print(json.dumps({m:d['overall'] for m,d in methods.items()},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['blind-pack','score']);p.add_argument('--phase',choices=['dev','test'],default='test');a=p.parse_args()
 if a.command=='blind-pack':blind_pack(a.phase)
 else:score(a.phase)
