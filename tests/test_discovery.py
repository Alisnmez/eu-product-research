import unittest
from discovery import DOMAINS
class DiscoveryTests(unittest.TestCase):
 def test_breadth(self):self.assertGreaterEqual(len(DOMAINS),25)
 def test_unique_domains(self):self.assertEqual(len(DOMAINS),len({x[0] for x in DOMAINS}))
if __name__=="__main__":unittest.main()
