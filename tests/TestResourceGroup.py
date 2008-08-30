# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import ResourceGroup
from Chestnut import Resource

class TestResourceGroup(unittest.TestCase):
    def testInitialization(self):
        resource_group = ResourceGroup.ResourceGroup() 
        self.assertEqual(resource_group.__class__, ResourceGroup.ResourceGroup)
        self.assertEqual(resource_group.entryPoint(), None)
        self.assertEqual(resource_group.resourceList(), [])
        self.assertEqual(resource_group.description(), None)

    def testEntryPoint(self):
        resource_group = ResourceGroup.ResourceGroup()
        resource_group.setEntryPoint("hello")
        self.assertEqual(resource_group.entryPoint(), "hello")

    def testResourceList(self):
        resource_group = ResourceGroup.ResourceGroup()
        resource = Resource.Resource()
        resource_group.addResource(resource)
        self.assertEqual(len(resource_group.resourceList()), 1)
        self.assertEqual(resource_group.resourceList()[0], resource)

    def testDescription(self):
        resource_group = ResourceGroup.ResourceGroup()
        resource_group.setDescription("hello")
        self.assertEqual(resource_group.description(), "hello")


if __name__ == '__main__':
    unittest.main()
