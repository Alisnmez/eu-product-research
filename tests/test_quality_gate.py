import unittest
from quality_gate import validate_record,audit
from evaluation import Evidence,evaluate,unit_economics
class QualityGateTests(unittest.TestCase):
 def test_reject_missing_evidence(self):
  self.assertIn("product_family",validate_record({"source_url":"https://example.com","observed_at":"2026-11-23"}))
 def test_unknown_never_scores(self):
  r=evaluate({"demand":{"proof":Evidence(True)}} ,{})
  self.assertEqual(r["score"],0)
  self.assertEqual(r["status"],"needs_validation")
 def test_negative_contribution(self):
  self.assertFalse(unit_economics(20,.2,15,4,2,1)["viable_before_ads"])
 def test_missing_dataset(self):
  self.assertEqual(audit("/tmp/does-not-exist-research.jsonl")["valid_evidence_records"],0)
if __name__=="__main__":unittest.main()
