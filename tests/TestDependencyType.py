# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import DependencyType

class TestDependencyType(unittest.TestCase):
        
    def testValidDependencyType(self): # fold>>
        script_path=sys.path[0]
        self.assertEqual(DependencyType.validDependencyType(DependencyType.PACKAGED_EXECUTABLE), True)
        self.assertEqual(DependencyType.validDependencyType(DependencyType.PACKAGED_RESOURCE), True)
        self.assertEqual(DependencyType.validDependencyType("foo"), False)
        # <<fold

if __name__ == '__main__':
    unittest.main()
