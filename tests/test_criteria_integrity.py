import unittest
from criteria import GROUPS,assess
class CriteriaIntegrityTests(unittest.TestCase):
 def test_failed_is_not_verified(self):
  checks={"demand.search_intent":{"status":"not_met","source_url":"https://example.org","observed_at":"2026-11-23"}}
  r=assess(checks)
  self.assertEqual(r["criteria_verified"],0)
  self.assertEqual(r["criteria_failed"],1)
  self.assertEqual(r["criteria_unknown"],59)
  self.assertFalse(r["eligible_for_winner"])
 def test_complete_evidence_required(self):
  checks={g+"."+name:{"status":"met","source_url":"https://example.org/evidence","observed_at":"2026-11-23"} for g,names in GROUPS.items() for name in names}
  r=assess(checks)
  self.assertEqual(r["criteria_verified"],60)
  self.assertEqual(r["score"],100)
  self.assertTrue(r["eligible_for_winner"])
 def test_veto_blocks_even_perfect_score(self):
  checks={g+"."+name:{"status":"met","source_url":"https://example.org/evidence","observed_at":"2026-11-23"} for g,names in GROUPS.items() for name in names}
  r=assess(checks,{"unsafe_or_illegal":True})
  self.assertEqual(r["score"],0)
  self.assertFalse(r["eligible_for_winner"])
if __name__=="__main__":unittest.main()
