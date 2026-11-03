"""Export existing scored results, preserving raw denominators and overlapping strata."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
METRICS=['decision_accuracy','unsupported_recall','supported_fpr','indeterminate_recall','unnecessary_abstention','decision_coverage','field_accuracy','requirement_accuracy','evidence_accuracy','exception_accuracy','diagnostic_omission','full_diagnostic_joint']
def export(result):
    out=ROOT/'tables';out.mkdir(exist_ok=True)
    for filename,group in [('overall','overall'),('conditions','by_condition'),('complexities','by_complexity'),('families','by_family')]:
        rows=[]
        for method,data in result['methods'].items():
            strata={'all':data[group]} if group=='overall' else data[group]
            for stratum,scores in strata.items():
                for metric in METRICS:
                    rows.append({'method':method,'stratum':stratum,'cases':scores['cases'],'families':scores['families'],'metric':metric,**scores[metric]})
        with (out/(filename+'.csv')).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['method','stratum','cases','families','metric','numerator','denominator','value']);writer.writeheader();writer.writerows(rows)
    (out/'comparisons.json').write_text(json.dumps(result['comparisons'],ensure_ascii=False,indent=2)+'\n')
    print('Exported overall, overlapping condition/complexity, family tables and paired comparisons.')
if __name__=='__main__':export(json.loads((ROOT/'test_results.json').read_text()))
