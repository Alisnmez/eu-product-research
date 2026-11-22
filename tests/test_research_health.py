import unittest,tempfile,json,datetime as dt
from pathlib import Path
from research_health import check
class HealthTests(unittest.TestCase):
 def test_empty_candidates_not_healthy(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   (p/"state.json").write_text(json.dumps({"last_run":"2026-11-23T00:00:00+00:00","runs":2}))
   (p/"opportunity_queue.json").write_text('{"candidates":[]}')
   result=check(d,dt.datetime(2026,11,23,1,tzinfo=dt.timezone.utc))
   self.assertIn("no_product_candidates",result["issues"])
 def test_stale(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   (p/"state.json").write_text('{"last_run":"2026-11-20T00:00:00+00:00"}')
   (p/"opportunity_queue.json").write_text('{"candidates":[{}]}')
   result=check(d,dt.datetime(2026,11,23,1,tzinfo=dt.timezone.utc))
   self.assertIn("research_stale_over_3_hours",result["issues"])
if __name__=="__main__":unittest.main()
