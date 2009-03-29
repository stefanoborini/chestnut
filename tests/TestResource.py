# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.insert(1,os.path.join(script_path, "../src"));

import unittest

from Chestnut import Resource
from Chestnut import PathType

class TestResource(unittest.TestCase):
    def testInitialization(self):
        resource = Resource.Resource() 
        self.assertEqual(resource.__class__, Resource.Resource)
        self.assertEqual(resource.path(), None)
        self.assertEqual(resource.pathType(), None)
        self.assertEqual(resource.platform(), None)

    def testPlatform(self):
        resource = Resource.Resource()
        resource.setPlatform("Linux-ia64")
        self.assertEqual(resource.platform(), "Linux-ia64")

    def testPath(self):
        resource = Resource.Resource()
        resource.setPath(os.path.join("foo","bar"))
        self.assertEqual(resource.path(), os.path.join("foo","bar"))

    def testPathType(self):
        resource = Resource.Resource()
        resource.setPathType(PathType.ABSOLUTE)
        self.assertEqual(resource.pathType(), PathType.ABSOLUTE)

    def testWrongPathType(self):
        resource = Resource.Resource()
        self.assertRaises(Exception, resource.setPathType, "frobniz")
        

if __name__ == '__main__':
    unittest.main()
