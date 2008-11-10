#!/usr/bin/env python
# @author Stefano Borini
from xml.dom import minidom

import Executable
import ExecutableGroup
import Resource
import ResourceGroup
import PathType
import Dependency
import DependencyType

class Manifest:
    def __init__(self, path): # fold>>
        """
        @description Initializes the manifest out of a given file path
        @param path the manifest file path
        """
        self.__path = path
        self.__all_groups = {}
        self.__default_executable_group_entry_point = None

        manifest_doc = minidom.parse(path)
        
        # handmade parsing and validation. no other choice at the time being :/
        root = manifest_doc.documentElement

        version = _parseVersion(root)
        if version not in _supportedVersions():
            raise ParseException("Unsupported manifest version")

        contents_node = _getContentsNode(root)



        executable_group_nodelist = _getExecutableGroupNodelist(contents_node)
        for node in executable_group_nodelist:
            executable_group = _parseExecutableGroupNode(node)

            if self.__all_groups.has_key(executable_group.entryPoint()):
                raise ParseException("Duplicated entry point "+executable_group.entryPoint())

            self.__all_groups[executable_group.entryPoint()] = executable_group
            
        resource_group_nodelist = _getResourceGroupNodelist(contents_node)
        for node in resource_group_nodelist:
            resource_group = _parseResourceGroupNode(node)

            if self.__all_groups.has_key(resource_group.entryPoint()):
                raise ParseException("Duplicated entry point "+resource_group.entryPoint()) 

            self.__all_groups[resource_group.entryPoint()] = resource_group
       
        package_meta_node = _getPackageMetaNode(root)

        if package_meta_node is not None:
            self.__default_executable_group_entry_point = _parseDefaultExecutableGroupEntryPoint(package_meta_node)
            if self.__default_executable_group_entry_point is not None:
                if len(self.__default_executable_group_entry_point) == 0:
                    raise ParseException("Empty default executable group entry point")

                # check if the entry point is actually defined by some executable group.
                # we prefer this explicit test instead of relying on executableGroup() because we are
                # in the __init__ and so it's better not to rely on non-initialization methods during initialization
                if not (
                    self.__all_groups.has_key(self.__default_executable_group_entry_point) and 
                    isinstance(self.__all_groups[self.__default_executable_group_entry_point], ExecutableGroup.ExecutableGroup)
                    ):
                    raise ParseException("Default executable group entry point does not reference any currently defined executable group")

            self.__package_description = _parsePackageDescription(package_meta_node)

        else:
            self.__default_executable_group_entry_point = None
            self.__package_description = None

        # <<fold
    def defaultExecutableGroupEntryPoint(self): # fold>>
        """
        @return the default executable group entry point as defined in the manifest, or None if not defined
        """
        return self.__default_executable_group_entry_point
        # <<fold
    def executable(self, entry_point, platform): # fold>>
        """
        @description produces the executable for a given entry point and platform entries
        @param entry_point: the entry point string
        @param platform: the platform string
        @return an Executable object, or None if not found
        """
        group = self.executableGroup(entry_point)
        if group is None: 
            return None

        executable_list = filter ( lambda x : x.platform() == platform, group.executableList())
        if len(executable_list) > 0:
            executable = executable_list[0]
        else:
            executable = None
        return executable

        # <<fold
    def resource(self, entry_point, platform): # fold>>
        """
        @description produces the resource for a given entry point and platform entries
        @param entry_point: the entry point string
        @param platform: the platform string
        @return a Resource object, or None if not found
        """
        group = self.resourceGroup(entry_point)

        if group is None:
            return None

        resource_list = filter ( lambda x : x.platform() == platform, group.resourceList())
        if len(resource_list) > 0:
            resource = resource_list[0]
        else:
            resource = None
        return resource
        # <<fold
    def executableGroupList(self): # fold>>
        """
        @description produces a list of all the executable groups contained into the manifest
        @return a list
        """
        return [x[1] for x in self.__all_groups.items() if isinstance(x[1],ExecutableGroup.ExecutableGroup)]
        # <<fold
    def resourceGroupList(self): # fold>>
        """
        @description produces a list of all the resource groups contained into the manifest
        @return a list
        """
        return [x[1] for x in self.__all_groups.items() if isinstance(x[1],ResourceGroup.ResourceGroup)]
        # <<fold
    def executableGroup(self, entry_point): # fold>>
        """
        @description produces the executable group for a given entry point, or None if not found
        @param entry_point: an entry point string
        @return An ExecutableGroup object, or None if not found
        """
        if self.__all_groups.has_key(entry_point) and isinstance(self.__all_groups[entry_point], ExecutableGroup.ExecutableGroup):
            return self.__all_groups[entry_point]
        return None
        # <<fold
    def resourceGroup(self, entry_point): # fold>>
        """
        @description produces the resource group for a given entry point, or None if not found
        @param entry_point : an entry point string
        @return A ResourceGroup object, or None if not found
        """
        if self.__all_groups.has_key(entry_point) and isinstance(self.__all_groups[entry_point], ResourceGroup.ResourceGroup):
            return self.__all_groups[entry_point]
        return None
        # <<fold 
    def packageDescription(self): # fold>>
        """
        @return the package description if provided in the manifest, otherwise None
        """
        return self.__package_description
        # <<fold

class ParseException(Exception): pass

def _supportedVersions():
    return ["1.0.0"]

# helper methods for parsing 
def _parseExecutableGroupNode(executable_group_node): # fold>>
    """
    @description performs parsing of the ExecutableGroup xml subtree.
    @param node : the ExecutableGroup node
    @returns an ExecutableGroup object
    """

    # getting the entry point
    entry_point = executable_group_node.getAttribute("entryPoint")
    if len(entry_point) == 0:
        raise Exception("Empty entry point specification found")

    # create the executable group
    executable_group = ExecutableGroup.ExecutableGroup()
    executable_group.setEntryPoint(entry_point)
    
    description = executable_group_node.getAttribute("description")
    if len(description) == 0:
        description = None

    executable_group.setDescription(description)

    # get each executable and add it to the group
    executable_nodelist=executable_group_node.getElementsByTagName("Executable")

    for executable_node in executable_nodelist:
        executable = _parseExecutableNode(executable_node)
        executable_group.addExecutable(executable)

    return executable_group
# <<fold
def _parseExecutableNode(executable_node): # fold>>
    
    platform=_getPlatform(executable_node)
    path_type, path = _getPathInfo(executable_node)
    interpreter = _getInterpreter(executable_node)

    dependency_nodelist=executable_node.getElementsByTagName("Dependencies")
    if len(dependency_nodelist) > 1:
        raise ParseException("Too many dependency root nodes for executable")

    dependencies=[]
    if len(dependency_nodelist) == 1:
        dependencies = _parseDependencies(dependency_nodelist[0])

    executable = Executable.Executable()
    executable.setPath(path)
    executable.setPathType(path_type)
    executable.setInterpreter(interpreter)
    executable.setPlatform(platform)

    for dependency in dependencies:
        executable.addDependency(dependency)

    return executable
# <<fold
def _parseResourceGroupNode(resource_group_node): # fold>>
    """
    """

    # getting the entry_point
    entry_point = resource_group_node.getAttribute("entryPoint")
    if len(entry_point) == 0:
        raise Exception("Empty entry point specification found")

    resource_group = ResourceGroup.ResourceGroup()
    resource_group.setEntryPoint(entry_point)

    description = resource_group_node.getAttribute("description")
    if len(description) == 0:
        description = None

    resource_group.setDescription(description)

    resource_nodelist = resource_group_node.getElementsByTagName("Resource")
    for resource_node in resource_nodelist:
        resource = _parseResourceNode(resource_node)
        resource_group.addResource(resource)

    return resource_group
# <<fold
def _parseResourceNode(resource_node): # fold>>
    """
    @description parses a resource xml node. returns a Resource object.
    @param resource_node : a resource node
    @return a Resource object
    """
    
    platform = _getPlatform(resource_node)
    path_type, path = _getPathInfo(resource_node)

    resource = Resource.Resource()
    resource.setPath(path)
    resource.setPathType(path_type)
    resource.setPlatform(platform)

    return resource
# <<fold
def _parseDefaultExecutableGroupEntryPoint(elem): # fold>>
    default_execgroup_entry_nodelist = elem.getElementsByTagName("DefaultExecutableGroupEntryPoint")
    if len(default_execgroup_entry_nodelist) > 1:
        raise ParseException("Too many DefaultExecutableGroupEntryPoint entries")
    if len(default_execgroup_entry_nodelist) == 1:
        return default_execgroup_entry_nodelist[0].childNodes[0].nodeValue
    return None
    # <<fold
def _parsePackageDescription(elem): # fold>>
    package_description_nodelist = elem.getElementsByTagName("Description")
    if len(package_description_nodelist) > 1:
        raise ParseException("Too many package description entries in meta section")
    if len(package_description_nodelist) == 1:
        return package_description_nodelist[0].childNodes[0].nodeValue
    return None
    # <<fold
def _parseVersion(node): # fold>>
    return node.getAttribute("version")
    # <<fold
def _parseDependencies(node): # fold>>
    dep_list = []
    depends_on_nodelist = node.getElementsByTagName("DependsOn")
    for dependency in depends_on_nodelist:
        type_string = dependency.getAttribute("type")
        if type_string == "packaged_executable":
            type = DependencyType.PACKAGED_EXECUTABLE
        else:
            raise Exception("Empty or invalid dependency type specification for executable")
        dep = dependency.childNodes[0].nodeValue
        dep_list.append( Dependency.Dependency(type, dep) )

    return dep_list
    # <<fold 
def _getContentsNode(elem): # fold>>
    contents_nodelist = elem.getElementsByTagName("Contents")
    if len(contents_nodelist) == 0:
        raise ParseException("No Contents entry")
    if len(contents_nodelist) > 1:
        raise ParseException("Too many Contents entries")
    return contents_nodelist[0]
    # <<fold
def _getExecutableGroupNodelist(elem): # fold>>
    return elem.getElementsByTagName("ExecutableGroup")
    # <<fold
def _getResourceGroupNodelist(elem): # fold>>
    return elem.getElementsByTagName("ResourceGroup")
# <<fold

def _getPackageMetaNode(elem): # fold>>
    meta_nodelist=elem.getElementsByTagName("Meta")
    if len(meta_nodelist) > 1:
        raise ParseException("Too many package meta sections")
    if len(meta_nodelist) == 0:
        return None
    return meta_nodelist[0]
    # <<fold

def _getPlatform(elem): # fold>>
    platform_nodelist = elem.getElementsByTagName("Platform")

    if len(platform_nodelist) == 0:
        raise Exception("No platform specifications")
    if len(platform_nodelist) > 1:
        raise Exception("Too many platform specifications")

    platform=platform_nodelist[0].childNodes[0].nodeValue
    return platform
# <<fold
def _getPathInfo(elem): # fold>>
    path_nodelist=elem.getElementsByTagName("Path")
    if len(path_nodelist) == 0:
        raise ParseException("No path specifications")
    if len(path_nodelist) > 1:
        raise ParseException("Too many path specifications")
    
    path=path_nodelist[0].childNodes[0].nodeValue
    if len(path) == 0:
        raise ParseException("Empty relative_path specification")

    path_type_string = path_nodelist[0].getAttribute("type")

    if path_type_string == "absolute":
        path_type = PathType.ABSOLUTE
    elif path_type_string == "package_relative":
        path_type = PathType.PACKAGE_RELATIVE
    elif path_type_string == "standard":
        path_type = PathType.STANDARD
    else:
        raise ParseException("Empty or invalid path type specification")

    return (path_type, path)
# <<fold
def _getInterpreter(elem): # fold>>
    interpreter_nodelist=elem.getElementsByTagName("Interpreter")
    if len(interpreter_nodelist) > 1:
        raise ParseException("Too many interpreter specifications for executable")
    
    interpreter=None
    if len(interpreter_nodelist) != 0:
        interpreter=interpreter_nodelist[0].childNodes[0].nodeValue
        if len(interpreter) == 0:
            raise ParseException("Empty interpreter specification for executable")
    return interpreter
# <<fold
