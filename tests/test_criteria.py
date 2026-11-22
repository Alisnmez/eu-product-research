import unittest
from criteria import GROUPS,assess
class CriteriaTests(unittest.TestCase):
 def test_exactly_sixty(self):self.assertEqual(sum(map(len,GROUPS.values())),60)
 def test_missing_is_unknown(self):
  r=assess({})
  self.assertEqual(len(r["unknown"]),60)
  self.assertEqual(r["score"],0)
 def test_no_source_no_credit(self):
  r=assess({"demand.search_intent":{"status":"met"}})
  self.assertEqual(r["score"],0)
 def test_veto(self):
  r=assess({},{"unsafe_or_illegal":True})
  self.assertEqual(r["status"],"rejected")
if __name__=="__main__":unittest.main()
