# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../src"));
import unittest

from Chestnut import Utils

class TestUtils(unittest.TestCase):
    def testQualifiedNameComponents(self): # fold>>
        self.assertEqual(Utils.qualifiedNameComponents("foo-1.0.0.0"), ("foo", ("1","0","0","0"), None))
        self.assertEqual(Utils.qualifiedNameComponents("foo-1.0.0"), ("foo", ("1","0","0"), None))
        self.assertEqual(Utils.qualifiedNameComponents("foo-1.1.0"), ("foo", ("1","1","0"), None))
        self.assertEqual(Utils.qualifiedNameComponents("foo-1.1.0/hello"), ("foo", ("1","1","0"), "hello"))
        self.assertEqual(Utils.qualifiedNameComponents("foo-1.1"), ("foo", ("1","1"), None))
        self.assertEqual(Utils.qualifiedNameComponents("foo-1"), ("foo", ("1",), None))
        self.assertEqual(Utils.qualifiedNameComponents("foo-1/bar"), ("foo", ("1",), "bar"))
        self.assertEqual(Utils.qualifiedNameComponents("foo"), ("foo", (), None))
        self.assertEqual(Utils.qualifiedNameComponents("foo/bar"), ("foo", (), "bar"))
        self.assertEqual(Utils.qualifiedNameComponents("foo-a.b.c"), ("foo",("a","b","c"), None))

        self.assertEqual(Utils.qualifiedNameComponents("foo-"), None)
        self.assertEqual(Utils.qualifiedNameComponents("foo-1."), None)
        self.assertEqual(Utils.qualifiedNameComponents("foo-la-cvcvq.234.1"), None)
        self.assertEqual(Utils.qualifiedNameComponents("   "), None)
        self.assertEqual(Utils.qualifiedNameComponents("foo-a. .c"), None)
        self.assertEqual(Utils.qualifiedNameComponents("foo-a..c"), None)
        self.assertEqual(Utils.qualifiedNameComponents("foo-1.0.0/"), None)
        # <<fold

        
if __name__ == '__main__':
    unittest.main()
