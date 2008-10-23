# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import Package
from Chestnut import PackageRunner
from Chestnut import PathType
from Chestnut import Dependency
from Chestnut import DependencyType

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
    def testMissingDependencies(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"testPackageDir1","withUnresolvedDependencies-1.0.0.package") 
        package = Package.Package(package_path)
        os.environ["PACKAGE_SEARCH_PATH"]=""
        self.assertEqual(PackageRunner.isRunnable(package), False)

        os.environ["PACKAGE_SEARCH_PATH"]=dependenciesPath()
        self.assertEqual(PackageRunner.isRunnable(package), False)

        # <<fold 
    def testTryResolve(self): # fold>>
        script_path=sys.path[0]
        d = Dependency.Dependency(DependencyType.PACKAGED_EXECUTABLE, "DependencyPackage-1.2.0")

        self.assertEqual(PackageRunner._tryResolve(d), None)
        os.environ["PACKAGE_SEARCH_PATH"]=dependenciesPath()
        self.assertNotEqual(PackageRunner._tryResolve(d), None)

        # <<fold 
    def testHasLocalRunnabilityRequisites(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner._hasLocalRunnabilityRequisites(package, package.defaultExecutableGroupEntryPoint()), True)

        package_path=os.path.join(script_path,"notRunnablePackages","missingExecFlag-1.0.0.package") 
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner._hasLocalRunnabilityRequisites(package,"secondary_entry"), False)

        package_path=os.path.join(script_path,"notRunnablePackages","unexistentExecutable-1.0.0.package")
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner._hasLocalRunnabilityRequisites(package,"secondary_entry"), False)
        # <<fold 

# testing more complex dependency patterns
    def testComplexDepCase1_simpleDep_working(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"complexDependencyCases","working","simpleDependency","mainPackage-1.0.0.package") 
        os.environ["PACKAGE_SEARCH_PATH"]=os.path.join(script_path,"complexDependencyCases","working","simpleDependency")
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner.isRunnable(package), True)

        # <<fold 
    def testComplexDepCase1_doubleDep_working(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"complexDependencyCases","working","doubleDependency","mainPackage-1.0.0.package") 
        os.environ["PACKAGE_SEARCH_PATH"]=os.path.join(script_path,"complexDependencyCases","working","doubleDependency")
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner.isRunnable(package), True)

        # <<fold 
    def testComplexDepCase1_cascadeDep_working(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"complexDependencyCases","working","cascadeDependency","mainPackage-1.0.0.package") 
        os.environ["PACKAGE_SEARCH_PATH"]=os.path.join(script_path,"complexDependencyCases","working","cascadeDependency")
        package = Package.Package(package_path)
        self.assertEqual(PackageRunner.isRunnable(package), True)

        # <<fold 
    def testComplexDepCase1_circularDep_working(self): # fold>>
        script_path=sys.path[0]

        package_path=os.path.join(script_path,"complexDependencyCases","working","circularDependency","mainPackage-1.0.0.package") 
        os.environ["PACKAGE_SEARCH_PATH"]=os.path.join(script_path,"complexDependencyCases","working","circularDependency")
        package = Package.Package(package_path)
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
    def testComputeExecutableAbsolutePath(self):
        self.assertEqual(PackageRunner._computeExecutableAbsolutePath("/package/root","/stuff/path",PathType.ABSOLUTE,"Linux-ia64" ), "/stuff/path")
        self.assertEqual(PackageRunner._computeExecutableAbsolutePath("/package/root","stuff/path",PathType.STANDARD,"Linux-ia64" ), "/package/root/Executables/Linux-ia64/stuff/path")
        self.assertEqual(PackageRunner._computeExecutableAbsolutePath("/package/root","stuff/path",PathType.PACKAGE_RELATIVE,"Linux-ia64" ), "/package/root/stuff/path")
        # FIXME see bug #2190377


def dependenciesPath():
    script_path = sys.path[0]
    return os.path.join(script_path,"dependenciesDir")
        
if __name__ == '__main__':
    unittest.main()
