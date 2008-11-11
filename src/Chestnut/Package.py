#!/usr/bin/env python
# @author Stefano Borini 
import Manifest
import Platform
import PathType
import Utils

import os
import re
import stat

class InitializationException(Exception): pass

class Package:
    def __init__(self, path): # fold>>
        self.__package_root_dir=os.path.abspath(path)
        
        package_dir_name=os.path.basename(self.__package_root_dir)
       
        versioned_name, extension = os.path.splitext(package_dir_name) 
        if extension != os.extsep+'package':
            raise InitializationException("Invalid package extension "+extension)
        
        try: 
            name, version, entry_point = Utils.qualifiedNameComponents(versioned_name)
        except:
            raise InitializationException("Invalid name for package ", versioned_name)

        if len(version) != 3:
            raise InitializationException("Invalid name for package ", versioned_name)
            
        # for now we want all of them numeric
        try:
            for v in version:
                int(v)
        except:
            raise InitializationException("Invalid name for package ", versioned_name)

        manifest_path = os.path.join(self.__package_root_dir, "manifest.xml")
        try:
            self.__manifest = Manifest.Manifest(manifest_path)
        except IOError, e:
            raise InitializationException("Unable to open manifest. "+str(e))
        except Manifest.ParseException, e:
            raise InitializationException("Invalid manifest. "+str(e))
        
        # <<fold
    def defaultExecutableGroupEntryPoint(self): # fold>>
        """
        @description returns the default entry point string
        """
        return self.__manifest.defaultExecutableGroupEntryPoint()
        # <<fold
    def resourceAbsolutePath(self, entry_point): # fold>>
        platform = Platform.currentPlatform()

        group = self.__manifest.resourceGroup(entry_point)

        if group is None:
            return None

        resource = group.resource(platform)

        if resource is not None:
            return _computeResourceAbsolutePath(self.rootDir(), resource.path(), resource.pathType(), platform)

        # look for something compatible
        for resource in group.resourceList():
            if Platform.isCompatibleWith(resource.platform()):
                return _computeResourceAbsolutePath(self.rootDir(), resource.path(), resource.pathType(), resource.platform())

        return None
        # <<fold
    def executableAbsolutePath(self, entry_point): # fold>>
        platform = Platform.currentPlatform()
        
        group = self.__manifest.executableGroup(entry_point)

        if group is None:
            return None

        executable = group.executable(platform)

        if executable is not None:
            return _computeExecutableAbsolutePath(self.rootDir(), executable.path(), executable.pathType(), platform)

        # look for something compatible
        for executable in group.executableList():
            if Platform.isCompatibleWith(executable.platform()):
                return _computeExecutableAbsolutePath(self.rootDir(), executable.path(), executable.pathType(), executable.platform())

        return None
        # <<fold
    def resourceDescription(self, entry_point): # fold>>
        group = self.__manifest.resourceGroup(entry_point)

        if group is None:
            return None

        return group.description()
        # <<fold
    def executableDescription(self, entry_point): # fold>>
        
        group = self.__manifest.executableGroup(entry_point)

        if group is None:
            return None

        return group.description()

        # <<fold
    def executableInterpreter(self, entry_point): # fold>>
        
        group = self.__manifest.executableGroup(entry_point)

        if group is None:
            return None

        executable = group.executable(Platform.currentPlatform())

        if executable is None:
            return None

        # try to see if there's an executable that can run on this platform
        for exe in group.executableList():
            if Platform.isCompatibleWith(executable.platform()):
                executable = exe
                break

        # still none? we rest our case
        if executable is None:
            return False
   
        return executable.interpreter()
        # <<fold
    def manifest(self): # fold>>
        return self.__manifest
    # <<fold
    def dependencyList(self, entry_point): # fold>>
        if len(self.__manifest.executableGroupList()) == 0: 
            return []
    
        if entry_point is None:
            entry_point = self.defaultExecutableGroupEntryPoint()
            # no default? then we know the answer
            if entry_point is None:
                return False
    
        executable_group = self.__manifest.executableGroup(entry_point)
        if executable_group is None:
            return []
            
        executable = executable_group.executable(Platform.currentPlatform())
    
        if executable is None:
            # try to see if there's an executable that can run on this platform
            for exe in executable_group.executableList():
                if Platform.isCompatibleWith(exe.platform()):
                    executable = exe
                    break
    
        # still none? we rest our case
        if executable is None:
            return []
    
        return executable.dependencies()
        # <<fold

    def rootDir(self): # fold>>
        """
        @description returns the root directory of the package, as absolute path.
        @return a string with the package root directory absolute path
        """
        return self.__package_root_dir
        # <<fold
    def executableEntryPoints(self): # fold>>
        """
        returns a list of strings of all the executable entry points as marked 
        in the manifest
        """
        # we don't have sets in python 2.3, so I use a dict to make a unique list
        entry_points = {}
        for group in self.__manifest.executableGroupList():
            entry_points[group.entryPoint()] = "dummy"
        
        return entry_points.keys()
        # <<fold
    def resourceEntryPoints(self): # fold>>
        """
        returns a list of strings of all the resource entry points as marked 
        in the manifest
        """
        # we don't have sets in python 2.3, so I use a dict to make a unique list
        entry_points = {}
        for group in self.__manifest.resourceGroupList():
            entry_points[group.entryPoint()] = "dummy"
        
        return entry_points.keys()
        # <<fold
    def versionedName(self): # fold>>
        return os.path.splitext(os.path.basename(self.rootDir()))[0]
        # <<fold
    def name(self): # fold>>
        return Utils.qualifiedNameComponents(self.versionedName())[0]
        # <<fold
    def version(self): # fold>>
        return Utils.qualifiedNameComponents(self.versionedName())[1]
        # <<fold
    def description(self): # fold>>
        return self.__manifest.packageDescription()
        # <<fold

def _computeResourceAbsolutePath(package_root_dir, path, path_type, platform): # fold>>
    """
    @description returns the resource absolute path according to the package root dir, the path
    @description of the resource as specified in the manifest, the path type and the platform
    @param package_root_dir : the package root
    @param path : the resource path as from the manifest
    @param path_type: the path type enumeration, as derived from the manifest
    @param platform: the platform string
    @return a string with the path, or None if unable to compute this value
    """
    if path_type == PathType.ABSOLUTE:
        return path
    elif path_type == PathType.STANDARD:
        return os.path.join(package_root_dir, "Resources",platform,path)
    elif path_type == PathType.PACKAGE_RELATIVE:
        return os.path.join(package_root_dir, path)
    
    return None
    # <<fold
def _computeExecutableAbsolutePath(package_root_dir, path, path_type, platform): # fold>>
    """
    @description returns the executable absolute path according to the package root dir, the path
    @description of the resource as specified in the manifest, the path type and the platform
    @param package_root_dir : the package root
    @param path : the executable path as from the manifest
    @param path_type: the path type enumeration, as derived from the manifest
    @param platform: the platform string
    @return a string with the path, or None if unable to compute this value
    """
    if path_type == PathType.ABSOLUTE:
        return path
    elif path_type == PathType.STANDARD:
        return os.path.join(package_root_dir, "Executables",platform,path)
    elif path_type == PathType.PACKAGE_RELATIVE:
        return os.path.join(package_root_dir, path)
    
    return None
    # <<fold 
