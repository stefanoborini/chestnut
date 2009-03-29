# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.insert(1,os.path.join(script_path, "../src"));
import unittest

from Chestnut import PathType

class TestPathType(unittest.TestCase):
        
    def testValidPathType(self): # fold>>
        script_path=sys.path[0]
        self.assertEqual(PathType.validPathType(PathType.ABSOLUTE), True)
        self.assertEqual(PathType.validPathType(PathType.PACKAGE_RELATIVE), True)
        self.assertEqual(PathType.validPathType(PathType.STANDARD), True)
        self.assertEqual(PathType.validPathType("foo"), False)
        # <<fold

if __name__ == '__main__':
    unittest.main()
