import unittest
from review_analysis import analyze
class ReviewTests(unittest.TestCase):
 def test_dedup_and_evidence(self):
  r={"review_id":"a1","product_family":"sample","text":"Broke after a week; too small","source_url":"https://example.com/review/1","observed_at":"2026-11-23","country":"DE","verified_buyer":True}
  result=analyze([r,r])
  self.assertEqual(result["accepted_reviews"],1)
  self.assertEqual(len(result["issue_clusters"]),2)
  self.assertFalse(result["issue_clusters"][0]["sales_verified"])
 def test_reject_unattributed(self):
  self.assertEqual(analyze([{"text":"broken"}])["rejected_records"],1)
if __name__=="__main__":unittest.main()
