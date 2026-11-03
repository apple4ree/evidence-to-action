import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import workflow as w
import harness as h
C={'record_id':'x','history':[{'event_id':'L1','text':'policy'},{'event_id':'L2','text':'observation'}],'target_action':{'event_ids':['L3'],'text':'act'}}
def pred():return {'record_id':'x','first_source_events':['L2'],'transformation_events':[],'reuse_events':['L3'],'scope_links':[{'from':'L2','to':'L3','dimension':'source_type','change':'preserved','judgment':'preserved'}],'rationale':'visible evidence','limitations':[]}
def rel(status='satisfied'):
 return {**pred(),'checks':[{'requirement_id':'r1','requirement_text':'required','policy_events':['L1'],'evidence_events':['L2'],'status':status,'rationale':'checked'}],'coverage':'complete'}
class Tests(unittest.TestCase):
 def test_synthesis_boundaries(self):
  for s,d in [('satisfied','supported'),('excepted','supported'),('violated','unsupported'),('unresolved','indeterminate')]:self.assertEqual(w.aggregate(C,rel(s))[0]['decision'],d)
 def test_partial_and_conflicting_requirements(self):
  r=rel();r['coverage']='incomplete';self.assertEqual(w.aggregate(C,r)[0]['decision'],'indeterminate');r['checks'].append({**r['checks'][0],'requirement_id':'r2','status':'violated'});self.assertEqual(w.aggregate(C,r)[0]['decision'],'unsupported')
 def test_no_future_or_fabricated_references(self):
  r=rel('violated');r['checks'][0]['evidence_events']=['L4'];out,err=w.aggregate(C,r);self.assertTrue(err);self.assertEqual(out['decision'],'indeterminate');r=pred();r['decision']='supported';r['scope_links'][0]['to']='missing';self.assertTrue(w.validate(C,r))
 def test_empty_and_malformed(self):
  for r in [None,[],{}, {**rel(),'checks':[]}]:self.assertEqual(w.aggregate(C,r)[0]['decision'],'indeterminate')
 def test_common_final_schema(self):
  out,err=w.aggregate(C,rel());self.assertEqual(set(out),set(w.FINAL_KEYS));self.assertEqual(w.validate(C,out),[])
 def test_no_response_retry_only(self):
  with tempfile.TemporaryDirectory() as t,patch.object(h,'ROOT',Path(t)):
   p=Path(t);(p/'calls').mkdir();meta={'call_id':'x_direct','record_id':'x','stage':'direct','created_utc':h.now()};(p/'calls/x_direct.json').write_text(json.dumps(meta));r=p/'response.txt';r.write_text('wrong answer')
   with self.assertRaises(ValueError):h.save('x_direct',str(r),'technical_failure')
if __name__=='__main__':unittest.main()
