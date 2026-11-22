import unittest
from opportunity_pipeline import process,normalize
class AssessmentIntegrationTests(unittest.TestCase):
 def test_unicode_family(self):
  self.assertEqual(normalize("Çocuk Çantası"),"çocuk çantası")
 def test_assessment_linked_not_invented(self):
  product={"product_family":"Çocuk Çantası","country":"LT","source_url":"https://example.org/item","observed_at":"2026-11-23"}
  assessment={"product_family":"ÇOCUK ÇANTASI","country":"LT","checks":{"demand.search_intent":{"status":"met","source_url":"https://example.org/evidence","observed_at":"2026-11-23"}}}
  result=process([product],[],[assessment])
  item=result["candidates"][0]
  self.assertEqual(item["criteria"]["criteria_verified"],1)
  self.assertFalse(item["criteria"]["eligible_for_winner"])
 def test_veto_passed_through(self):
  product={"product_family":"Example","country":"DE","source_url":"https://example.org/item","observed_at":"2026-11-23"}
  assessment={"product_family":"Example","country":"DE","hard_veto":{"unsafe_or_illegal":True}}
  result=process([product],[],[assessment])
  self.assertEqual(result["candidates"][0]["criteria"]["status"],"rejected")
if __name__=="__main__":unittest.main()
