# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.insert(1,os.path.join(script_path, "../src"));
import unittest

from Chestnut import Package
from Chestnut import PackageResolver

class TestPackageResolver(unittest.TestCase):
    def setUp(self):
        os.environ["PACKAGE_SEARCH_PATH"]=searchPath()

    def testInitialization(self):
        resolver = PackageResolver.PackageResolver()
        self.assertEqual(resolver.__class__, PackageResolver.PackageResolver)

    def testFindUnfindable(self):
        resolver = PackageResolver.PackageResolver()

        self.assertEqual(resolver.find("frobniz",("1","0","42")), None)

    def testFindFindable(self):
        os.environ["PACKAGE_SEARCH_PATH"]=versionSearchPath()

        resolver = PackageResolver.PackageResolver()
        package = resolver.find("foo",("1","0","0"))
        
        self.assertNotEqual(package, None)
        self.assertEqual(package.__class__, Package.Package)

    def testVersionPriority(self):
        os.environ["PACKAGE_SEARCH_PATH"]=versionSearchPath()

        resolver=PackageResolver.PackageResolver()

        self.assertEqual( "versionPackageDir1/foo-1.0.0.package" in resolver.find("foo",("1","0","0")).rootDir(), True )
        self.assertEqual( "versionPackageDir1/foo-1.0.1.package" in resolver.find("foo",("1","0","1")).rootDir(), True )
        self.assertEqual( "versionPackageDir1/foo-1.0.2.package" in resolver.find("foo",("1","0")).rootDir(), True )
        self.assertEqual( "versionPackageDir2/foo-1.1.2.package" in resolver.find("foo",("1","1")).rootDir(), True )
        self.assertEqual( "versionPackageDir2/foo-1.1.2.package" in resolver.find("foo",("1","1","2")).rootDir(), True )
        self.assertEqual( "versionPackageDir2/foo-1.2.4.package" in resolver.find("foo",("1","2")).rootDir(), True )
        self.assertEqual( "versionPackageDir1/foo-2.0.0.package" in resolver.find("foo",("2",)).rootDir(), True )
        self.assertEqual( "versionPackageDir1/foo-3.0.1.package" in resolver.find("foo",("3",)).rootDir(), True )
        self.assertEqual( "versionPackageDir1/foo-3.0.1.package" in resolver.find("foo",("3","0")).rootDir(), True ) # sure ?
        self.assertEqual( "versionPackageDir1/foo-3.0.1.package" in resolver.find("foo",()).rootDir(), True )

    

def searchPath():
    script_path = sys.path[0]
    return os.path.join(script_path,"unexistentPackageDir") \
                +os.pathsep \
                +os.path.join(script_path,"testPackageDir1") \
                +os.pathsep \
                +os.path.join(script_path,"testPackageDir2") 
               
def versionSearchPath():
    script_path = sys.path[0]
    return os.path.join(script_path,"versionPackageDir1") \
                +os.pathsep \
                +os.path.join(script_path,"versionPackageDir2")

if __name__ == '__main__':
    unittest.main()
