# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import ExecutableGroup
from Chestnut import Executable

class TestExecutableGroup(unittest.TestCase):
    def testInitialization(self):
        executable_group = ExecutableGroup.ExecutableGroup() 
        self.assertEqual(executable_group.__class__, ExecutableGroup.ExecutableGroup)
        self.assertEqual(executable_group.entryPoint(), None)
        self.assertEqual(executable_group.executableList(), [])
        self.assertEqual(executable_group.description(), None)

    def testEntryPoint(self):
        executable_group = ExecutableGroup.ExecutableGroup()
        executable_group.setEntryPoint("hello")
        self.assertEqual(executable_group.entryPoint(), "hello")

    def testExecutableList(self):
        executable_group = ExecutableGroup.ExecutableGroup()
        executable = Executable.Executable()
        executable_group.addExecutable(executable)
        self.assertEqual(len(executable_group.executableList()), 1)
        self.assertEqual(executable_group.executableList()[0], executable)

    def testDescription(self):
        executable_group = ExecutableGroup.ExecutableGroup()
        executable_group.setDescription("hello")
        self.assertEqual(executable_group.description(), "hello")


if __name__ == '__main__':
    unittest.main()
