# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import Package
from Chestnut import PackageRunner
from Chestnut import PathType

class TestCnrun(unittest.TestCase):
        
    def testRun(self): # fold>>
        script_path=sys.path[0]
        package_path=os.path.join(script_path,"testPackageDir1","foo-1.0.0.package") 

        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1.0.0"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1.0"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo-1"), 0)
        self.assertEqual(os.system("PACKAGE_SEARCH_PATH=\""+os.path.join(script_path,"testPackageDir1")+"\" ../src/cnrun foo"), 0)
        # <<fold 

        
if __name__ == '__main__':
    unittest.main()
