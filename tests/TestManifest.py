# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.insert(1,os.path.join(script_path, "../src"));

import unittest
from xml.dom import minidom

from Chestnut import Manifest
from Chestnut import ResourceGroup
from Chestnut import Resource
from Chestnut import ExecutableGroup
from Chestnut import Executable


class TestManifest(unittest.TestCase):
    def testInitialization(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.__class__, Manifest.Manifest)
        # <<fold
    def testInvalidManifestNoContents(self): # fold>>
        self.assertRaises( Manifest.ParseException, Manifest.Manifest, os.path.join(script_path,"invalidManifests","no_contents.xml"))
        # <<fold
    def testInvalidManifestTooManyContents(self): # fold>>
        self.assertRaises( Manifest.ParseException, Manifest.Manifest, os.path.join(script_path,"invalidManifests","many_contents.xml"))
        # <<fold
    def testInvalidManifestTooManyMeta(self): # fold>>
        self.assertRaises( Manifest.ParseException, Manifest.Manifest, os.path.join(script_path,"invalidManifests","many_meta.xml"))
        # <<fold
    def testInvalidManifestMissingDefaultEntryPoint(self): # fold>>
        self.assertRaises( Manifest.ParseException, Manifest.Manifest, os.path.join(script_path,"invalidManifests","unexistent_default.xml"))
        # <<fold
    def testInvalidManifestNonUniqueEntryPoints(self): # fold>>
        self.assertRaises( Manifest.ParseException, Manifest.Manifest, os.path.join(script_path,"invalidManifests","non_unique_entry_points.xml"))
        # <<fold
    def testInvalidManifestUnexistentDefaultEntryPoint(self): # fold>>
        self.assertRaises( Manifest.ParseException, Manifest.Manifest, os.path.join(script_path,"invalidManifests","unexistent_default.xml"))
        # <<fold
    def testInvalidManifestUnsupportedVersion(self): # fold>>
        self.assertRaises( Manifest.ParseException, Manifest.Manifest, os.path.join(script_path,"invalidManifests","unsupported_version.xml"))
        # <<fold
    def testDefaultExecutableGroupEntryPoint(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.defaultExecutableGroupEntryPoint(), "hello")
        # <<fold
    def testMetaSectionWithNoDefaultExecGroup(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest_only_description_in_meta.xml"))
        self.assertEqual(manifest.__class__, Manifest.Manifest)
        self.assertEqual(manifest.defaultExecutableGroupEntryPoint(), None)
        # <<fold
    def testExecutableGroupList(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(len(manifest.executableGroupList()), 3)
        # <<fold
    def testResourceGroupList(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(len(manifest.resourceGroupList()), 2)
        # <<fold
    def testExecutableGroup(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.executableGroup("eles").__class__, ExecutableGroup.ExecutableGroup)
        self.assertEqual(manifest.executableGroup("frobniz"), None)
        # <<fold
    def testExecutableGroupDescription(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.executableGroup("eles").description(), "ls executable")
        self.assertEqual(manifest.executableGroup("hello").description(), None)
        # <<fold
    def testResourceGroup(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.resourceGroup("res_2").__class__, ResourceGroup.ResourceGroup)
        self.assertEqual(manifest.resourceGroup("frobniz"), None)
        # <<fold
    def testResourceGroupDescription(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.resourceGroup("res_2").description(), "resource 2")
        self.assertEqual(manifest.resourceGroup("res_1").description(), None)
        # <<fold
    def testExecutable(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.executable("eles", "Darwin-i386").__class__, Executable.Executable)
        self.assertEqual(manifest.executable("eles", "NCC-1701"), None)
        self.assertEqual(manifest.executable("frobniz", "NCC-1701"), None)
        # <<fold
    def testResource(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.resource("res_2","Linux-ia64").__class__, Resource.Resource)
        self.assertEqual(manifest.resource("res_2","NCC-1701"), None)
        self.assertEqual(manifest.resource("frobniz","NCC-1701"), None)
        # <<fold
    def testPackageDescription(self):
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest.xml"))
        self.assertEqual(manifest.packageDescription(), "a cool manifest for a cool package")
        # <<fold
    def testEmptyPackageDescription(self): # fold>>
        manifest = Manifest.Manifest(os.path.join(script_path,"validManifests","manifest_no_package_description.xml"))
        self.assertEqual(manifest.packageDescription(), None)
            # <<fold 
    def testParseExecutableGroupNode(self): # fold>>
        manifest_doc = minidom.parse(os.path.join(script_path,"validManifests","manifest.xml"))
        
        root = manifest_doc.documentElement

        exe_group_nodelist = root.getElementsByTagName("ExecutableGroup")

        exe_group = Manifest._parseExecutableGroupNode(exe_group_nodelist[0])
        self.assertEqual(exe_group.__class__, ExecutableGroup.ExecutableGroup)
        self.assertEqual(exe_group.entryPoint(), "hello")
        self.assertEqual(len(exe_group.executableList()), 3)

        exe_group = Manifest._parseExecutableGroupNode(exe_group_nodelist[1])
        self.assertEqual(exe_group.__class__, ExecutableGroup.ExecutableGroup)
        self.assertEqual(exe_group.entryPoint(), "a_name")
        self.assertEqual(len(exe_group.executableList()), 1)

        exe_group = Manifest._parseExecutableGroupNode(exe_group_nodelist[2])
        self.assertEqual(exe_group.__class__, ExecutableGroup.ExecutableGroup)
        self.assertEqual(exe_group.entryPoint(), "eles")
        self.assertEqual(len(exe_group.executableList()), 2)

    def testParseResourceGroupNode(self):
        manifest_doc = minidom.parse(os.path.join(script_path,"validManifests","manifest.xml"))
        
        root = manifest_doc.documentElement

        res_group_nodelist = root.getElementsByTagName("ResourceGroup")

        res_group = Manifest._parseResourceGroupNode(res_group_nodelist[0])
        self.assertEqual(res_group.__class__, ResourceGroup.ResourceGroup)
        self.assertEqual(res_group.entryPoint(), "res_1")
        self.assertEqual(len(res_group.resourceList()), 2)

        res_group = Manifest._parseResourceGroupNode(res_group_nodelist[1])
        self.assertEqual(res_group.__class__, ResourceGroup.ResourceGroup)
        self.assertEqual(res_group.entryPoint(), "res_2")
        self.assertEqual(len(res_group.resourceList()), 1)

if __name__ == '__main__':
    unittest.main()
