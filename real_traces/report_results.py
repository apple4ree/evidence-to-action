"""Descriptive breakdowns of the frozen real-trace comparison."""
import json
from collections import defaultdict,Counter
from pathlib import Path
from evaluate import evaluate,ratio
R=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def main():
 summary=evaluate();rows=load(R/'results/per_case.json');ratings=load(R/'semantic_ratings.json')
 sources=defaultdict(list);groups=defaultdict(list);components={};pairs={}
 for row in rows:
  cid=row['case_id'];dataset=load(R/'public'/f'{cid}.json')['dataset']
  sources[(dataset,row['method'])].append(row);groups[(row['group_id'],row['method'])].append(row)
 for m in summary:
  values=[v for k,r in ratings.items() if k.endswith('_'+m) for v in r['components'].values()]
  rs=[r for r in rows if r['method']==m]
  components[m]={'semantic_components':dict(Counter(values)),'semantic_denominator':len(values),'evidence_correct':ratio(sum(r['evidence_semantically_correct'] for k,r in ratings.items() if k.endswith('_'+m)),len(rs)),'missed_components':[{'case_id':k.rsplit('_',1)[0],'component':c,'rating':v} for k,r in ratings.items() if k.endswith('_'+m) for c,v in r['components'].items() if v!='pass']}
 for a,b in [('D1','P2'),('D1','D2')]:
  ar={r['case_id']:r for r in rows if r['method']==a};br={r['case_id']:r for r in rows if r['method']==b}
  pairs[a+'_vs_'+b]={metric:{'first_only':[c for c in ar if ar[c][metric] and not br[c][metric]],'second_only':[c for c in ar if br[c][metric] and not ar[c][metric]],'both_correct':[c for c in ar if ar[c][metric] and br[c][metric]],'both_incorrect':[c for c in ar if not ar[c][metric] and not br[c][metric]]} for metric in ['decision_correct','joint_correct']}
 def aggregate(collection):return [{'group':g,'method':m,'decision':ratio(sum(r['decision_correct'] for r in rs),len(rs)),'joint':ratio(sum(r['joint_correct'] for r in rs),len(rs))} for (g,m),rs in collection.items()]
 runtimes=[load(p) for p in (R/'runtime').glob('*.json')]
 out={'by_source':aggregate(sources),'by_original_run':aggregate(groups),'components':components,'paired_comparisons':pairs,'runtime_audit':{'completed_stages':len(runtimes),'full_prepared_text_observed':sum(r['prepared_input_delivery']=='exact_text_observed' for r in runtimes),'valid_output_references':sum(not load(p)['format_reference_errors'] for p in (R/'validation').glob('*.json')),'model_aliases':sorted({a for r in runtimes for a in r['model_aliases']}),'reasoning_efforts':sorted({a for r in runtimes for a in r['reasoning_efforts']}),'technical_retries':load(R/'technical_retries.json')},'sampling':'content-selected exploratory sample, no prevalence estimate','rating':'method-name-blinded separate-context LLM ratings, no human ratings','scope_caveat':'AHN08 normal_value and AHN09 file_link omissions are scored by frozen criteria; breadth relative to focal relation requires human review. No post-hoc score relaxation.'}
 (R/'results/breakdowns.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 assert len(rows)==45 and len(ratings)==45 and len(runtimes)==60
 assert all(sum(summary[m]['confusion_matrix'].values())==15 for m in summary)
 print({m:{'decision':s['decision_accuracy'],'joint':s['joint_diagnostic_accuracy'],'components':components[m]['semantic_components']} for m,s in summary.items()})
if __name__=='__main__':main()
