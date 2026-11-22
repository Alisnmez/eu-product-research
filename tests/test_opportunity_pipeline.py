import unittest
from opportunity_pipeline import process
class OpportunityPipelineTests(unittest.TestCase):
 def test_dedup_and_no_invented_demand(self):
  p={"product_family":"Reusable Shoe Cover","country":"DE","source_url":"https://example.org/p1","observed_at":"2026-11-23"}
  r={"product_family":"Reusable Shoe Cover","country":"DE","review_id":"r1","source_url":"https://example.org/review","observed_at":"2026-11-23","text":"Broke after a week"}
  result=process([p,p],[r,r])
  self.assertEqual(result["unique_product_country_pairs"],1)
  self.assertEqual(result["candidates"][0]["distinct_review_count"],1)
  self.assertEqual(result["demand_verified"],0)
  self.assertEqual(result["candidates"][0]["criteria"]["score"],0)
 def test_reject_missing_source(self):
  result=process([{"product_family":"x","country":"DE"}],[])
  self.assertEqual(len(result["errors"]),1)
if __name__=="__main__":unittest.main()
