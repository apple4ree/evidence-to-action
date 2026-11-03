import unittest
from harness import aggregate,quoted_value,validate
class ContractTests(unittest.TestCase):
 def test_composition_priority(self):
  for states,want in [(['violated','unresolved'],'Unsupported'),(['satisfied','unresolved'],'Indeterminate'),(['satisfied','not_applicable'],'Supported')]:
   self.assertEqual(aggregate({'issues':[{'relation':s} for s in states]})['decision'],want)
 def test_quote_boundaries(self):
  p={'input':{'prior_record':'a\nb','target_action':'c'}}
  self.assertEqual(quoted_value(p,'L2-L3'),'b\nc')
  with self.assertRaises(ValueError):quoted_value(p,'L4')
  self.assertEqual(quoted_value({'input':{'history':[{'content':'yes'}]}},'/input/history/0/content'),'yes')
 def test_reference_error_not_semantic_retry(self):
  obj={'decision':'Supported','issues':[{'field':'x','requirement':'x','relation':'satisfied','exception':{},'rationale':'x','evidence':[{'locator':'L1','quote':'invented'}]}]}
  self.assertTrue(validate({'input':{'prior_record':'actual','target_action':'target'}},obj,'direct'))
if __name__=='__main__':unittest.main()
