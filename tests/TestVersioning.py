# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import Versioning

class TestVersioning(unittest.TestCase):
    def testCorrectVersioningHierarchy(self):
        self.assertEqual(Versioning.compareVersion("1.0", "1.1"), -1)
        self.assertEqual(Versioning.compareVersion("1.0", "1.0.1"), -1)
        self.assertEqual(Versioning.compareVersion("1.0.1", "1.0"), -1)
        self.assertEqual(Versioning.compareVersion("1.0beta", "1.0"), -1)
        self.assertEqual(Versioning.compareVersion("1.0", "1.1"), -1)
        self.assertEqual(Versioning.compareVersion("1.0", "1.1"), -1)
        self.assertEqual(Versioning.compareVersion("1.0", "1.1"), -1)
        


if __name__ == '__main__':
    unittest.main()
