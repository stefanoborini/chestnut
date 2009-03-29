# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import Package
from Chestnut import PathType

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
    def testIsRunnable(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(package.isRunnable(), True)

        package_path=os.path.join(script_path,"notRunnablePackages","missingExecFlag-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(package.isRunnable(), False)
        self.assertEqual(package.isRunnable("secondary_entry"), False)

        package_path=os.path.join(script_path,"notRunnablePackages","unexistentExecutable-1.0.0.package")
        package = Package.Package(package_path)
        self.assertEqual(package.isRunnable(), False)
        self.assertEqual(package.isRunnable("secondary_entry"), False)
        # <<fold 
    def testNotRunnableException(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"notRunnablePackages","missingExecFlag-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertRaises(Package.NotRunnableException, package.run)
        self.assertRaises(Package.NotRunnableException, package.runEntryPoint, "secondary_entry")

        package_path=os.path.join(script_path,"notRunnablePackages","unexistentExecutable-1.0.0.package")
        package = Package.Package(package_path)
        self.assertRaises(Package.NotRunnableException, package.run)
        self.assertRaises(Package.NotRunnableException, package.runEntryPoint, "secondary_entry")
        # <<fold 
    def testRun(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)

        pid = os.fork()
        if pid == 0:
            package.run()
        
        pid, status = os.waitpid(pid,0)

        self.assertEqual(status, 0)
        # <<fold 
    def testRunEntryPoint(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)

        pid = os.fork()
        if pid == 0:
            package.runEntryPoint("package_relative_type")
        
        pid, status = os.waitpid(pid,0)

        self.assertEqual(status, 0)
        # <<fold
    def testDefaultExecutableEntryPoint(self): # fold>>
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
    def testSplitVersionedName(self): # fold>>
        self.assertEqual(Package._splitVersionedName("foo-1.0.0"), ("foo", ("1","0","0")))
        self.assertEqual(Package._splitVersionedName("foo-1.1.0"), ("foo", ("1","1","0")))
        self.assertEqual(Package._splitVersionedName("foo-1.1"), ("foo", ("1","1")))
        self.assertEqual(Package._splitVersionedName("foo-1"), ("foo", ("1",)))
        self.assertEqual(Package._splitVersionedName("foo"), ("foo", ()))
        self.assertEqual(Package._splitVersionedName("foo-a.b.c"), ("foo",("a","b","c")))

        self.assertEqual(Package._splitVersionedName("foo-"), None)
        self.assertEqual(Package._splitVersionedName("foo-1."), None)
        self.assertEqual(Package._splitVersionedName("foo-la-cvcvq.234.1"), None)
        self.assertEqual(Package._splitVersionedName("   "), None)
        self.assertEqual(Package._splitVersionedName("foo-a. .c"), None)
        self.assertEqual(Package._splitVersionedName("foo-a..c"), None)
        # <<fold
    def testWhich(self): # fold>>
        self.assertEqual(Package._which("ls"), os.path.join("/","bin","ls"))
        self.assertEqual(Package._which("wataa"), None)
        # <<fold
    def testIsExecutable(self): # fold>>
        self.assertEqual(Package._isExecutable(os.path.join("/","bin","ls")), True)
        self.assertEqual(Package._isExecutable(os.path.join("/","bin")), False)
        self.assertEqual(Package._isExecutable(os.path.join(script_path,"manifest.xml")), False)
        # <<fold

        
if __name__ == '__main__':
    unittest.main()
