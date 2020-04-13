import unittest
import sys

class Test_TestTatort(unittest.TestCase):
    def test_alwaysTrue(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    sys.path.insert(0, "C:/")
    
    import tatort
    unittest.main()