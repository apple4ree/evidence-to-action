"""Compare a submitted review with frozen annotations, without replacing gold."""
import hashlib,json
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
E=ROOT.parent
def read(p):return json.loads(p.read_text())
def analyze():
 submission=read(ROOT/'submission_original.json');ids=read(E/'case_ids.json')
 assert submission['packet']=='eta-real-trace-human-15-v2'
 assert submission['record_ids']==ids and set(submission['answers'])==set(ids)
 for cid in ids:
  assert submission['public_input_hashes'][cid]==hashlib.sha256((E/'public'/f'{cid}.json').read_bytes()).hexdigest(),cid
  a=submission['answers'][cid]
  assert a['complete'] and a['decision'] in ['supported','unsupported','indeterminate'],cid
  assert all(isinstance(a[k],str) and a[k].strip() for k in ['requirement','requirement_source','evidence_source','reason']),cid
 rows=[]
 for cid in ids:
  gold=read(E/'gold'/f'{cid}.json');a=submission['answers'][cid]
  rows.append({'case_id':cid,'frozen_label':gold['decision'],'submitted_label':a['decision'],'matches':gold['decision']==a['decision'],'submitted_reason':a['reason']})
 method_matches={}
 for m in ['D1','D2','P2']:
  method_matches[m]={'matches':sum(read(E/'predictions'/f'{c}_{m}.json')['decision'].lower()==submission['answers'][c]['decision'] for c in ids),'total':len(ids),'interpretation':'Agreement with unadjudicated submitted labels; not a replacement primary performance score.'}
 result={'status':'single human review confirmed; three label disagreements unadjudicated; no gold changes', 'input_hash_matches':len(ids),'complete_answers':len(ids),'reference_label_agreement':{'matches':sum(r['matches'] for r in rows),'total':len(rows)},'submitted_label_distribution':dict(Counter(a['decision'] for a in submission['answers'].values())),'label_confusion':dict(Counter(r['frozen_label']+' -> '+r['submitted_label'] for r in rows)),'disagreements':[r for r in rows if not r['matches']],'methods_against_submitted_labels':method_matches,'provenance':{'declared_review_type':submission.get('review_type'),'confirmed_review_process':read(ROOT/'review_provenance.json')['interpretation'],'revision_events':len(submission.get('revisions',[])),'familiar_count':sum(a.get('familiar',False) for a in submission['answers'].values()),'export_timestamp':submission.get('exported_at'),'duration_inferred':False,'note':'Metadata alone does not establish unaided human authorship or blinding; no first-submission revision events were included.'},'submission_sha256':hashlib.sha256((ROOT/'submission_original.json').read_bytes()).hexdigest()}
 (ROOT/'comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 assert result['reference_label_agreement']=={'matches':12,'total':15}
 assert {r['case_id'] for r in result['disagreements']}=={'MAST-R06','AHN04','AHN08'}
 print(json.dumps({k:result[k] for k in ['input_hash_matches','complete_answers','reference_label_agreement','submitted_label_distribution','methods_against_submitted_labels']},ensure_ascii=False))
if __name__=='__main__':analyze()
