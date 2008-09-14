# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import Dependency
from Chestnut import DependencyType

class TestDependency(unittest.TestCase):
        
    def testInitialization(self): # fold>>
        script_path=sys.path[0]
        d = Dependency.Dependency(DependencyType.PACKAGED_EXECUTABLE, "foo-1.0.0")
        self.assertEqual(d.type(), DependencyType.PACKAGED_EXECUTABLE)
        self.assertEqual(d.dependency(), "foo-1.0.0")
        # <<fold

    def testInvalidType(self): # fold>>
        self.assertRaises(Exception, Dependency.Dependency, "invalidType", "foo-1.0.0")
        # <<fold

if __name__ == '__main__':
    unittest.main()
