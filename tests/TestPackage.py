# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import Package
from Chestnut import PathType
from Chestnut import Manifest
from Chestnut import Dependency

class TestPackage(unittest.TestCase):
        
    def testInitialization(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1/foo-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(package.__class__, Package.Package)
        # <<fold

    def testFailedInitialization(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"invalidPackages/different_extension-1.0.0.pack") 
        self.assertRaises(Package.InitializationException, Package.Package, package_path)

        package_path=os.path.join(script_path,"invalidPackages/invalid_name.package") 
        self.assertRaises(Package.InitializationException, Package.Package, package_path)

        package_path=os.path.join(script_path,"invalidPackages/invalid_version-1.0.package") 
        self.assertRaises(Package.InitializationException, Package.Package, package_path)

        package_path=os.path.join(script_path,"invalidPackages/invalid_version_2-1.1.0alpha.package") 
        self.assertRaises(Package.InitializationException, Package.Package, package_path)

        package_path=os.path.join(script_path,"invalidPackages/missing_manifest-1.0.0.package") 
        self.assertRaises(Package.InitializationException, Package.Package, package_path)

        package_path=os.path.join(script_path,"invalidPackages/no_extension-1.0.0") 
        self.assertRaises(Package.InitializationException, Package.Package, package_path)
        # <<fold
    def testDefaultExecutableGroupEntryPoint(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(package.defaultExecutableGroupEntryPoint(), "standard_type")
        # <<fold
    def testResourceAbsolutePath(self): # fold>>
        import platform
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)
        (system, host, release, version, machine, processor) = platform.uname()
        platform_string = system+"-"+machine
        self.assertEqual(package.resourceAbsolutePath("res_1"), os.path.join(package_path,"Bruble","something"))
        self.assertEqual(package.resourceAbsolutePath("res_2"), os.path.join(package_path,"Resources",platform_string,"something"))
        # <<fold
    def testExecutableAbsolutePath(self): # fold>>
        import platform
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)
        (system, host, release, version, machine, processor) = platform.uname()
        platform_string = system+"-"+machine
        self.assertEqual(package.executableAbsolutePath("standard_type"), os.path.join(package_path,"Executables",platform_string,"standard_type"))
        self.assertEqual(package.executableAbsolutePath("package_relative_type"), os.path.join(package_path,"FrobnizBaz","package_relative_"+platform_string))
        self.assertEqual(package.executableAbsolutePath("absolute_type"), "/bin/ls")
        # <<fold
    def testRootDir(self): # fold>>
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(package.rootDir(), package_path)
        # <<fold
    def testExecutableEntryPoints(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1/foo-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(len(package.executableEntryPoints()), 3)
       
        self.assertEqual("package_relative_type" in package.executableEntryPoints(), True )
        self.assertEqual("standard_type" in package.executableEntryPoints(), True)
        self.assertEqual("absolute_type" in package.executableEntryPoints(), True)
        # <<fold
    def testResourceEntryPoints(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1/foo-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual( len(package.resourceEntryPoints()), 2)
        self.assertEqual( "res_1" in package.resourceEntryPoints(), True)
        self.assertEqual( "res_2" in package.resourceEntryPoints(), True)
        # <<fold
    def testVersionedName(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1/foo-1.0.0.package") 
        package = Package.Package(package_path)

        self.assertEqual(package.versionedName(), "foo-1.0.0")
        # <<fold
    def testName(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1/foo-1.0.0.package") 
        package = Package.Package(package_path)

        self.assertEqual(package.name(), "foo")
        # <<fold
    def testVersion(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1/foo-1.0.0.package") 
        package = Package.Package(package_path)

        self.assertEqual(package.version(), ("1", "0", "0"))
        # <<fold
    def testManifest(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1/foo-1.0.0.package") 
        package = Package.Package(package_path)

        self.assertEqual(package.manifest().__class__, Manifest.Manifest)
        # <<fold
    def testDependencies(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1/foo-1.0.0.package") 
        package = Package.Package(package_path)

        deps = package.manifest().executableGroup("standard_type").executable("Linux-ia64").dependencies()
        self.assertEqual(deps.__class__, list)
        self.assertEqual(len(deps), 0)

        package_path=os.path.join(script_path,"testPackageDir1/withDependencies-1.0.0.package") 
        package = Package.Package(package_path)

        deps = package.manifest().executableGroup("default").executable("Linux-ia64").dependencies()
        self.assertEqual(deps.__class__, list)
        self.assertEqual(len(deps), 2)
        for dependency in deps:
            self.assertEqual(dependency.__class__, Dependency.Dependency)
    # <<fold

    def testComputeExecutableAbsolutePath(self): # fold>>
        self.assertEqual(Package._computeExecutableAbsolutePath("/foo/bar-1.0.0.package", "chu/fraz", PathType.PACKAGE_RELATIVE, "Linux-i386" ), 
                            os.path.join("/foo/bar-1.0.0.package","chu/fraz"))
        self.assertEqual(Package._computeExecutableAbsolutePath("/foo/bar-1.0.0.package", "chu/fraz", PathType.STANDARD, "Linux-i386" ), 
                            os.path.join("/foo/bar-1.0.0.package","Executables","Linux-i386","chu/fraz"))
        self.assertEqual(Package._computeExecutableAbsolutePath("/foo/bar-1.0.0.package", "chu/fraz", PathType.ABSOLUTE, "Linux-i386" ), 
                            os.path.join("chu/fraz"))
        # <<fold 
    def testComputeResourceAbsolutePath(self): # fold>>
        self.assertEqual(Package._computeResourceAbsolutePath("/foo/bar-1.0.0.package", "chu/fraz", PathType.PACKAGE_RELATIVE, "Linux-i386" ), 
                            os.path.join("/foo/bar-1.0.0.package","chu/fraz"))
        self.assertEqual(Package._computeResourceAbsolutePath("/foo/bar-1.0.0.package", "chu/fraz", PathType.STANDARD, "Linux-i386" ), 
                            os.path.join("/foo/bar-1.0.0.package","Resources","Linux-i386","chu/fraz"))
        self.assertEqual(Package._computeResourceAbsolutePath("/foo/bar-1.0.0.package", "chu/fraz", PathType.ABSOLUTE, "Linux-i386" ), 
                            os.path.join("chu/fraz"))
        # <<fold

        
if __name__ == '__main__':
    unittest.main()
