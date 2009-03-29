# @author Stefano Borini 
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));

import unittest
from Chestnut import Executable
from Chestnut import PathType

class TestExecutable(unittest.TestCase):
    def testInitialization(self): # fold>>
        executable = Executable.Executable() 
        self.assertEqual(executable.__class__, Executable.Executable)
        self.assertEqual(executable.platform(), None)
        self.assertEqual(executable.path(), None)
        self.assertEqual(executable.pathType(), None)
        self.assertEqual(executable.interpreter(), None)
    # <<fold
    def testPlatform(self): # fold>>
        executable = Executable.Executable()
        executable.setPlatform("Linux-ia64")
        self.assertEqual(executable.platform(), "Linux-ia64")
    # <<fold
    def testPath(self): # fold>>
        executable = Executable.Executable()
        executable.setPath(os.path.join("foo","bar"))
        self.assertEqual(executable.path(), os.path.join("foo","bar"))
    # <<fold
    def testPathType(self): # fold>>
        executable = Executable.Executable()
        executable.setPathType(PathType.ABSOLUTE)
        self.assertEqual(executable.pathType(), PathType.ABSOLUTE)
    # <<fold
    def testWrongPathType(self): # fold>>
        executable = Executable.Executable()
        self.assertRaises(Exception, executable.setPathType, "frobniz")
    # <<fold 
    def testInterpreter(self): # fold>>
        executable = Executable.Executable()
        executable.setInterpreter("foo")
        self.assertEqual(executable.interpreter(), "foo")
    # <<fold


if __name__ == '__main__':
    unittest.main()
