# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.insert(1,os.path.join(script_path, "../src"));
import unittest

from Chestnut import Platform

class TestPlatform(unittest.TestCase):
    def testCurrentPlatform(self):
        self.assertEqual(Platform.currentPlatform(), os.uname()[0]+"-"+os.uname()[4])

    def testIsCompatibleWith(self):
        self.assertEqual(Platform.isCompatibleWith(Platform.currentPlatform()), True)
        self.assertEqual(Platform.isCompatibleWith("Puppix-ia16"), False)
        


if __name__ == '__main__':
    unittest.main()
