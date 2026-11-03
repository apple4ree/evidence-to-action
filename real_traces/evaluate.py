"""Re-score saved predictions and separately saved blinded semantic ratings."""
import json,csv,random,statistics
from pathlib import Path
from collections import Counter,defaultdict
from harness import ROOT,read,verify
METHODS={'D1':['direct'],'D2':['direct','revise'],'P2':['extract','relate']}
def ratio(n,d):return {'correct':n,'total':d,'rate':n/d if d else None}
def evaluate():
 verify();ids=read(ROOT/'case_ids.json');rows=[];semantic={}
 if (ROOT/'semantic_ratings.json').exists():semantic=read(ROOT/'semantic_ratings.json')
 for cid in ids:
  gold=read(ROOT/'gold'/f'{cid}.json');g=gold['decision'].lower()
  for method,stages in METHODS.items():
   pf=ROOT/'predictions'/f'{cid}_{method}.json';obj=read(pf) if pf.exists() else {};pred=str(obj.get('decision','missing')).lower()
   errors=[]
   for stage in stages:
    f=ROOT/'validation'/f'{cid}_{stage}.json'
    errors.extend(read(f)['format_reference_errors'] if f.exists() else ['missing stage'])
   s=semantic.get(cid+'_'+method);component=None if s is None else all(v=='pass' for v in s['components'].values())
   joint=None if s is None else (pred==g and component and s['evidence_semantically_correct'] and not s['contradiction'] and not errors)
   runtimes=[]
   for stage in stages:
    f=ROOT/'runtime'/f'{cid}_{stage}.json'
    if f.exists():runtimes.append(read(f))
   durations=[r.get('native_task_duration_ms') for r in runtimes];known=len(runtimes)==len(stages) and all(x is not None for x in durations)
   usages=[r.get('session_total_token_usage') for r in runtimes];usageknown=len(runtimes)==len(stages) and all(x is not None for x in usages)
   rows.append({'case_id':cid,'group_id':gold['group_id'],'method':method,'gold':g,'prediction':pred,'decision_correct':pred==g,'reference_format_valid':not errors,'reference_format_errors':errors,'semantic_components_pass':component,'joint_correct':joint,'active_session_seconds':sum(durations)/1000 if known else None,'input_tokens':sum(u.get('input_tokens',0) for u in usages) if usageknown else None,'output_tokens':sum(u.get('output_tokens',0) for u in usages) if usageknown else None,'sessions_observed':len(runtimes),'raw_output_bytes':sum((ROOT/'responses'/f'{cid}_{s}.json').stat().st_size for s in stages if (ROOT/'responses'/f'{cid}_{s}.json').exists())})
 results={}
 for method in METHODS:
  rs=[r for r in rows if r['method']==method];u=[r for r in rs if r['gold']=='unsupported'];s=[r for r in rs if r['gold']=='supported'];i=[r for r in rs if r['gold']=='indeterminate'];decided=[r for r in rs if r['prediction'] in ['supported','unsupported']];rated=[r for r in rs if r['joint_correct'] is not None]
  groups=defaultdict(list)
  for r in rs:groups[r['group_id']].append(int(r['decision_correct']))
  means=[statistics.mean(x) for x in groups.values()];rng=random.Random(20261103);boot=sorted(statistics.mean(rng.choices(means,k=len(means))) for _ in range(2000))
  times=[r['active_session_seconds'] for r in rs if r['active_session_seconds'] is not None]
  results[method]={'decision_accuracy':ratio(sum(r['decision_correct'] for r in rs),len(rs)),'confusion_matrix':dict(Counter(r['gold']+' -> '+r['prediction'] for r in rs)),'unsupported_recall':ratio(sum(r['prediction']=='unsupported' for r in u),len(u)),'supported_false_positive_rate':ratio(sum(r['prediction']=='unsupported' for r in s),len(s)),'indeterminate_accuracy':ratio(sum(r['prediction']=='indeterminate' for r in i),len(i)),'unnecessary_abstention':ratio(sum(r['prediction']=='indeterminate' for r in u+s),len(u+s)),'decision_coverage':ratio(len(decided),len(rs)),'joint_diagnostic_accuracy':ratio(sum(r['joint_correct'] for r in rated),len(rated)),'semantic_unrated':len(rs)-len(rated),'valid_reference_format':ratio(sum(r['reference_format_valid'] for r in rs),len(rs)),'group_macro_accuracy':statistics.mean(means),'group_bootstrap_95_interval':[boot[49],boot[1949]],'group_count':len(means),'mean_active_session_seconds':statistics.mean(times) if times else None,'time_cases_observed':len(times),'input_tokens':sum(r['input_tokens'] for r in rs) if all(r['input_tokens'] is not None for r in rs) else None,'output_tokens':sum(r['output_tokens'] for r in rs) if all(r['output_tokens'] is not None for r in rs) else None,'raw_output_bytes':sum(r['raw_output_bytes'] for r in rs)}
 out=ROOT/'results';out.mkdir(exist_ok=True);(out/'per_case.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(out/'summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 with (out/'per_case.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 return results
if __name__=='__main__':print(json.dumps(evaluate(),ensure_ascii=False,indent=2))
