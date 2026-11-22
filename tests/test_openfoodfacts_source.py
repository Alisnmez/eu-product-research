import unittest
from openfoodfacts_source import extract
class RealCatalogueTests(unittest.TestCase):
 def test_real_catalogue_schema_never_claims_sales(self):
  payload={"products":[{"code":"1234567890123","product_name":"Sample soap","brands":"Sample Brand","categories_tags":["en:soaps"]},{"code":"", "product_name":"bad"}]}
  rows=extract(payload,"2026-11-23T00:00:00+00:00")
  self.assertEqual(len(rows),1)
  self.assertEqual(rows[0]["barcode"],"1234567890123")
  self.assertFalse(rows[0]["sales_verified"])
  self.assertFalse(rows[0]["demand_verified"])
  self.assertEqual(rows[0]["license"],"ODbL")
if __name__=="__main__":unittest.main()
