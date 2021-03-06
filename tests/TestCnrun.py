# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.insert(1,os.path.join(script_path, "../src"));
import unittest

class TestCnrun(unittest.TestCase):
        
    def testRun(self): # fold>>
        script_path=sys.path[0]

        self.assertEqual(os.system("CN_PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1.0.0"), 0)
        self.assertEqual(os.system("CN_PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1.0"), 0)
        self.assertEqual(os.system("CN_PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1"), 0)
        self.assertEqual(os.system("CN_PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo"), 0)
        self.assertEqual(os.system("CN_PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun /bin/ls"), 0)
        self.assertEqual(os.system("CN_PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun ls"), 0)
        self.assertNotEqual(os.system("CN_PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun shouldNotBeFound"), 0)
        self.assertEqual(os.system("CN_PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun executableTestDir/foo"), 0)
        # <<fold 
    def testRunWithPackageSearchPath(self): # fold>>
        script_path=sys.path[0]

        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1.0.0"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1.0"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun /bin/ls"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun ls"), 0)
        self.assertNotEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun shouldNotBeFound"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun executableTestDir/foo"), 0)
        # <<fold 
    def testExportedVars(self): # fold>>
        script_path=sys.path[0]

        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun exportedVars-1.0.0"), 0)
        # <<fold 

        
if __name__ == '__main__':
    unittest.main()
