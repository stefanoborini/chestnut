# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.insert(1,os.path.join(script_path, "../src"));
import unittest

from Chestnut import ExecutableGroup
from Chestnut import Executable

class TestExecutableGroup(unittest.TestCase):
    def testInitialization(self): # fold>>
        executable_group = ExecutableGroup.ExecutableGroup() 
        self.assertEqual(executable_group.__class__, ExecutableGroup.ExecutableGroup)
        self.assertEqual(executable_group.entryPoint(), None)
        self.assertEqual(executable_group.executableList(), [])
        self.assertEqual(executable_group.description(), None)
        # <<fold
    def testEntryPoint(self): # fold>>
        executable_group = ExecutableGroup.ExecutableGroup()
        executable_group.setEntryPoint("hello")
        self.assertEqual(executable_group.entryPoint(), "hello")
        # <<fold
    def testExecutableList(self): # fold>>
        executable_group = ExecutableGroup.ExecutableGroup()
        executable = Executable.Executable()
        executable_group.addExecutable(executable)
        self.assertEqual(len(executable_group.executableList()), 1)
        self.assertEqual(executable_group.executableList()[0], executable)
        # <<fold
    def testDescription(self): # fold>>
        executable_group = ExecutableGroup.ExecutableGroup()
        executable_group.setDescription("hello")
        self.assertEqual(executable_group.description(), "hello")
        # <<fold

if __name__ == '__main__':
    unittest.main()
