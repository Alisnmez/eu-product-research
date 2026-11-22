"""Offline integration test: no external API or credentials required."""
import json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import openfoodfacts_source as source

class CatalogueSmokeTest(unittest.TestCase):
 def test_pipeline_writes_actual_schema_without_network(self):
  payload={"products":[{"code":"5901234123457","product_name":"Example oat snack","brands":"Example","countries_tags":["en:poland"],"categories_tags":["en:snacks"]}]}
  with tempfile.TemporaryDirectory() as tmp:
   previous=os.getcwd()
   try:
    os.chdir(tmp)
    with patch.object(source,"fetch",return_value=payload),patch.object(source.time,"sleep",return_value=None):
     source.main()
    status=json.loads(Path("data/openfoodfacts_status.json").read_text())
    rows=[json.loads(line) for line in Path("data/openfoodfacts_catalogue.jsonl").read_text().splitlines()]
    self.assertEqual(status["new"],1)
    self.assertEqual(status["total"],1)
    self.assertEqual(status["errors"],[])
    self.assertEqual(rows[0]["barcode"],"5901234123457")
    self.assertFalse(rows[0]["sales_verified"])
    with patch.object(source,"fetch",return_value=payload),patch.object(source.time,"sleep",return_value=None):
     source.main()
    status=json.loads(Path("data/openfoodfacts_status.json").read_text())
    self.assertEqual(status["new"],0)
    self.assertEqual(status["total"],1)
   finally:os.chdir(previous)
if __name__=="__main__":unittest.main()
