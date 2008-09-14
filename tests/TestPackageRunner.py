# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import Package
from Chestnut import PackageRunner
from Chestnut import PathType

class TestPackageRunner(unittest.TestCase):
        
    def testIsRunnable(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner.isRunnable(package), True)

        package_path=os.path.join(script_path,"notRunnablePackages","missingExecFlag-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner.isRunnable(package), False)
        self.assertEqual(PackageRunner.isRunnable(package,"secondary_entry"), False)

        package_path=os.path.join(script_path,"notRunnablePackages","unexistentExecutable-1.0.0.package")
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner.isRunnable(package), False)
        self.assertEqual(PackageRunner.isRunnable(package,"secondary_entry"), False)
        # <<fold 
    def testNotRunnableException(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"notRunnablePackages","missingExecFlag-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertRaises(PackageRunner.NotRunnableException, PackageRunner.run, package)
        self.assertRaises(PackageRunner.NotRunnableException, PackageRunner.runEntryPoint, package, "secondary_entry")

        package_path=os.path.join(script_path,"notRunnablePackages","unexistentExecutable-1.0.0.package")
        package = Package.Package(package_path)
        self.assertRaises(PackageRunner.NotRunnableException, PackageRunner.run, package)
        self.assertRaises(PackageRunner.NotRunnableException, PackageRunner.runEntryPoint, package, "secondary_entry")
        # <<fold 
    def testRun(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)

        pid = os.fork()
        if pid == 0:
            PackageRunner.run(package)
        
        pid, status = os.waitpid(pid,0)

        self.assertEqual(status, 0)
        # <<fold 
    def testRunEntryPoint(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)

        pid = os.fork()
        if pid == 0:
            PackageRunner.runEntryPoint(package,"package_relative_type")
        
        pid, status = os.waitpid(pid,0)

        self.assertEqual(status, 0)
        # <<fold
    def testIsRunnableForDependency(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"testPackageDir1","withDependencies-1.0.0.package") 
        package = Package.Package(package_path)
        os.environ["PACKAGE_SEARCH_PATH"]=""
        self.assertEqual(PackageRunner.isRunnable(package), False)

        os.environ["PACKAGE_SEARCH_PATH"]=dependenciesPath()
        self.assertEqual(PackageRunner.isRunnable(package), True)

        # <<fold 

    def testWhich(self): # fold>>
        self.assertEqual(PackageRunner._which("ls"), os.path.join("/","bin","ls"))
        self.assertEqual(PackageRunner._which("wataa"), None)
        # <<fold
    def testIsExecutable(self): # fold>>
        self.assertEqual(PackageRunner._isExecutable(os.path.join("/","bin","ls")), True)
        self.assertEqual(PackageRunner._isExecutable(os.path.join("/","bin")), False)
        self.assertEqual(PackageRunner._isExecutable(os.path.join(script_path,"manifest.xml")), False)
        # <<fold

def dependenciesPath():
    script_path = sys.path[0]
    return os.path.join(script_path,"dependenciesDir")
        
if __name__ == '__main__':
    unittest.main()
