# @author Stefano Borini 
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));

import unittest
from Chestnut import Executable
from Chestnut import PathType
from Chestnut import DependencyType

class TestExecutable(unittest.TestCase):
    def testInitialization(self):
        executable = Executable.Executable() 
        self.assertEqual(executable.__class__, Executable.Executable)
        self.assertEqual(executable.platform(), None)
        self.assertEqual(executable.path(), None)
        self.assertEqual(executable.pathType(), None)
        self.assertEqual(executable.interpreter(), None)

    def testPlatform(self):
        executable = Executable.Executable()
        executable.setPlatform("Linux-ia64")
        self.assertEqual(executable.platform(), "Linux-ia64")

    def testPath(self):
        executable = Executable.Executable()
        executable.setPath(os.path.join("foo","bar"))
        self.assertEqual(executable.path(), os.path.join("foo","bar"))

    def testPathType(self):
        executable = Executable.Executable()
        executable.setPathType(PathType.ABSOLUTE)
        self.assertEqual(executable.pathType(), PathType.ABSOLUTE)

    def testWrongPathType(self):
        executable = Executable.Executable()
        self.assertRaises(Exception, executable.setPathType, "frobniz")
        
    def testInterpreter(self):
        executable = Executable.Executable()
        executable.setInterpreter("foo")
        self.assertEqual(executable.interpreter(), "foo")

    def testDependencies(self):
        executable = Executable.Executable()
        executable.addDependency(DependencyType.PACKAGED_EXECUTABLE, "foo-1.2/bar")
        executable.addDependency(DependencyType.PACKAGED_RESOURCE, "foo-1.2/baz")
       
        self.assertEqual(len(executable.getDependencies()), 2)


if __name__ == '__main__':
    unittest.main()
