import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import workflow as w
import evaluate as e
import harness as h
C={'record_id':'c','policy':[{'id':'p','text':'Verify approval before sending.'}],'tool_documentation':[],'history':[{'event_id':'e','content':'employee exists'}],'target_action':{'arguments':{'recipient':'A'}},'capture_note':'complete'}
def relation(status='satisfied'):
 return {'record_id':'c','summary':'evidence state','checks':[{'requirement_id':'r','field':'recipient','requirement_text':'approval before send','policy_ids':['p'],'evidence_ids':['e'],'rationale':'complete capture','exception':{'applied':False,'policy_ids':[],'evidence_ids':[],'rationale':'none permitted'},'status':status,'origin':'extracted'}],'coverage':[{'field':'recipient','status':'checked'}]}
class Boundaries(unittest.TestCase):
 def test_absence_violation_and_unresolved(self):
  for state,label in [('satisfied','supported'),('violated','unsupported'),('unresolved','indeterminate')]:self.assertEqual(w.aggregate(C,relation(state))['decision'],label)
 def test_preserve_issue_details(self):
  out=w.aggregate(C,relation('violated'));self.assertEqual(out['issues'][0]['requirement_id'],'r');self.assertIn('exception',out['issues'][0]);self.assertEqual(w.validate_direct(C,out),[])
 def test_future_reference_invalid(self):
  r=relation('violated');r['checks'][0]['evidence_ids']=['future'];out=w.aggregate(C,r);self.assertFalse(out['valid']);self.assertEqual(out['decision'],'indeterminate')
 def test_missing_coverage_invalid(self):
  r=relation();r['coverage']=[];self.assertFalse(w.aggregate(C,r)['valid'])
 def test_violation_survives_unknown(self):
  r=relation('violated');r['checks'].append({**r['checks'][0],'requirement_id':'r2','status':'unresolved'});self.assertEqual(w.aggregate(C,r)['decision'],'unsupported')
 def test_exception_conflict_invalid(self):
  r=relation('violated');r['checks'][0]['exception']['applied']=True;self.assertFalse(w.aggregate(C,r)['valid'])
 def test_malformed_json_objects(self):
  for obj in [[],None,3]:self.assertFalse(w.aggregate(C,obj)['valid']);self.assertTrue(w.validate_direct(C,obj))
 def test_invalid_alert_is_false_positive(self):
  row={'record_id':'s','family_id':'f','gold':'supported','prediction':'unsupported','valid':False,'decision_correct':False,'joint_correct':False,'annotated_fields_covered':False,'unit_count':0,'missing_units':0,'extra_false_issue_count':1,**{k+'_correct_units':0 for k in ['field','requirement','evidence','exception']}}
  out=e.aggregate_rows([row]);self.assertEqual(out['supported_fpr']['value'],1);self.assertEqual(out['confusion_matrix']['supported']['invalid'],1)
 def test_edges_not_four_way_pair(self):
  rows=[{'record_id':'a','valid':True,'prediction':'supported','decision_correct':True},{'record_id':'b','valid':True,'prediction':'supported','decision_correct':False},{'record_id':'c','valid':True,'prediction':'supported','decision_correct':True}]
  out=e.edge_scores(rows,[{'left':'a','right':'b','kind':'contrast'},{'left':'a','right':'c','kind':'invariance'}]);self.assertEqual(out['contrast_both_correct']['value'],0);self.assertEqual(out['invariance_both_correct']['value'],1)
 def test_family_bootstrap_unit(self):
  rows=[{'family_id':'a','ok':True}]*4+[{'family_id':'b','ok':False}]
  out=e.bootstrap(rows,'ok',iterations=100);self.assertEqual(out['estimate'],.5);self.assertEqual(out['n_families'],2)
 def test_semantic_units_exact(self):
  with self.assertRaises(ValueError):e.validate_rating({'summary_correct':True,'extra_false_issue_count':0,'units':{},'rationale':'x'},{'issues':[{'unit_id':'u'}]})
 def test_public_allowlist_and_capture(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'data/public_cases').mkdir(parents=True);(root/'prompts').mkdir()
   (root/'data/private_split_plan.json').write_text(json.dumps({'entries':[{'record_id':'c','split':'dev'}]}));(root/'data/public_cases/c.json').write_text(json.dumps({**C,'gold':'SECRET','family_id':'private'}));(root/'prompts/common.txt').write_text('common');(root/'prompts/direct.txt').write_text('direct');(root/'run_config.json').write_text('{"model":null,"settings":{}}')
   with patch.object(h,'ROOT',root):h.prepare('c','direct','dev')
   text=(root/'calls/dev_c_direct.txt').read_text();self.assertIn('capture_note',text);self.assertNotIn('SECRET',text);self.assertNotIn('family_id',text)
 def test_no_semantic_retry(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'data').mkdir();(root/'data/private_split_plan.json').write_text(json.dumps({'entries':[{'record_id':'c','split':'dev'}]}));(root/'execution_log.jsonl').write_text('{"call_id":"dev_c_direct","status":"success"}\n')
   with patch.object(h,'ROOT',root),self.assertRaises(ValueError):h.prepare('c','direct','dev',attempt=1)
 def test_empty_denominator(self):self.assertIsNone(e.ratio(0,0)['value'])
if __name__=='__main__':unittest.main()
