import datetime as dt
import unittest
from evidence_registry import validate,compile_assessments
class EvidenceRegistryTests(unittest.TestCase):
 def sample(self,**kw):
  r={"product_family":"Example","country":"DE","criterion":"demand.search_intent","status":"met","source_url":"https://example.org/report","observed_at":"2026-11-23T00:00:00+00:00","evidence_type":"public_report","evidence_note":"Observed search demand in report"}
  r.update(kw);return r
 def test_valid(self):
  self.assertEqual(validate(self.sample(),dt.datetime(2026,11,24,tzinfo=dt.timezone.utc)),[])
 def test_missing_explanation(self):
  self.assertIn("missing_positive_evidence_explanation",validate(self.sample(evidence_note="")))
 def test_conflict_downgrade(self):
  a=self.sample()
  b=self.sample(status="not_met")
  out,rejected=compile_assessments([a,b])
  self.assertFalse(rejected)
  self.assertEqual(out[0]["checks"]["demand.search_intent"]["status"],"unknown")
 def test_invalid_criterion(self):
  self.assertIn("unknown_criterion",validate(self.sample(criterion="invented")))
if __name__=="__main__":unittest.main()
