#!/usr/bin/env python
# @author Stefano Borini 

import os
import re
import stat

import collections 

import Platform
import PathType
import Utils
import DependencyType
import PackageResolver

class NotRunnableException(Exception): pass

def isRunnable(package, entry_point=None): # fold>>
    """
    @description checks runnability conditions.
    @description A package is runnable for a given entry point when the following conditions are met:
    @description  - there is an executable group with that entry point
    @description  - the executable exists for the current platform and is executable
    @description  - if an interpreter is declared, the interpreter can be found and is executable
    """

    if entry_point is None:
        entry_point = package.defaultExecutableGroupEntryPoint()
        # no default? then we know the answer
        if entry_point is None:
            return False
   
    if not _hasLocalRunnabilityRequisites(package, entry_point):
        return False

    return _isDepTreeRunnable(package, entry_point, [])
    # <<fold 
def run(package, arguments=None, environment=None): # fold>>
    """
    @description runs the platform specific default executable, or a compatible platform specific/aspecific code 
    @description under the same entry point.
    @description The function never returns. The executable runs with an execve call which
    @description replaces the current executable with the new executable. If you want to fork, you
    @description have to do it before calling run()
    """ 

    # FIXME : what happens if this is None
    default_entry_point = package.defaultExecutableGroupEntryPoint()
    runEntryPoint(package, default_entry_point, arguments, environment)
    # <<fold
def runEntryPoint(package, entry_point, arguments=None, environment=None): # fold>>
    """
    @description runs the platform specific executable with a given entry poin, or a compatible 
    @description platform specific/aspecific code under the same entry point.
    @description The function never returns. The executable runs with an execve call which
    @description replaces the current executable with the new executable. If you want to fork, you
    @description have to do it before calling run()
    """ 
    if not isRunnable(package, entry_point):
        raise NotRunnableException("Entry point "+entry_point+" is not runnable.")
  
    if arguments is None:
        arguments=[]
    if environment is None:
        environment = os.environ

    # add the environment variable containing the package base directory.
    # we use this and not os.setenv because os.setenv does not export to child processes.
    environment["PACKAGE_ROOT_DIR"]=package.rootDir()

    executable_group = package.manifest().executableGroup(entry_point)
    executable = executable_group.executable(Platform.currentPlatform())
    if executable is None:
        # try to see if there's an executable that can run on this platform
        for exe in executable_group.executableList():
            if Platform.isCompatibleWith(exe.platform()):
                executable = exe
                break
   
    executable_absolute_path = _computeExecutableAbsolutePath(package.rootDir(), executable.path(), executable.pathType(), executable.platform())

    interpreter = executable.interpreter()
    if interpreter is not None:
        interpreter_path=_which(interpreter)
        os.execve(interpreter_path, [interpreter_path, executable_absolute_path]+list(arguments), environment)
    else:
        os.execve(executable_absolute_path,[executable_absolute_path]+list(arguments), environment)

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
def _isExecutable(program_path): # fold>>
    """
    @description check if a program is executable.
    @param program_path : the path of the program
    @return True if executable. False if not executable/readable/existent
    """
    try:
        mode = os.stat(program_path)[stat.ST_MODE] 
    except:
        return False
    # it is a regular file or a link, and is executable?
    if not (
            (stat.S_ISREG(mode) or stat.S_ISLNK(mode)) and
            ( stat.S_IMODE(mode) & stat.S_IEXEC ) and
            ( stat.S_IMODE(mode) & stat.S_IREAD) 
        ):
        return False
    return True
    # <<fold
def _which(program_name): # fold>>
    """
    @description performs a search of program in the environment variable PATH
    @description like the which command does.
    @param program: the program name
    @return the program full path if found, otherwise None
    """

    try:
        path_list = os.getenv('PATH').split(os.pathsep)
    except:
        # path is not defined
        return None

    for dir in path_list:
        program_absolute_path = os.path.abspath(os.path.join(dir, program_name))
        if _isExecutable(program_absolute_path):
            return program_absolute_path
    return None
    # <<fold
def _hasLocalRunnabilityRequisites(package, entry_point): # fold>>
    """
    @description checks if a package has local runnability characteristics, meaning
    @description that everything is checked except the dependencies being satisfied.
    """
    # if we have no executables, it is quickly said
    if len(package.manifest().executableGroupList()) == 0: 
        return False
    
    if entry_point is None:
        entry_point = package.defaultExecutableGroupEntryPoint()
        # no default? then we know the answer
        if entry_point is None:
            return False

    executable_group = package.manifest().executableGroup(entry_point)
    if executable_group is None:
        return False
        
    # try with the executable for the current platform. If not found, try with something that is supported
    executable = executable_group.executable(Platform.currentPlatform())

    if executable is None:
        # try to see if there's an executable that can run on this platform
        for exe in executable_group.executableList():
            if Platform.isCompatibleWith(exe.platform()):
                executable = exe
                break

    # still none? we rest our case
    if executable is None:
        return False
   
    # check for the existence of the file as specified in the path
    executable_absolute_path = _computeExecutableAbsolutePath(package.rootDir(), executable.path(), executable.pathType(), executable.platform())
    if not os.path.exists(executable_absolute_path):
        return False

    # check if the executable is interpreted, and in this case, if the interpreter can be found and executed
    interpreter = executable.interpreter()
    if interpreter is not None:
        interpreter_path=_which(interpreter)
        if interpreter_path is None:
            return False
        if not _isExecutable(interpreter_path):
            return False
    else:
       # not interpreted, check the executability of the file itself 
        if not _isExecutable(executable_absolute_path):
            return False

    return True
    # <<fold
def _resolveDep(dependency): # fold>>
    name,version, entry_point = Utils.qualifiedNameComponents(dependency.dependency())
    
    resolver = PackageResolver.PackageResolver()
    dependency_package = resolver.find(name,version)

    return dependency_package
    # <<fold
def _isDepTreeRunnable(package, entry_point, visited_deps): # fold>>

    dependencies = _getDependencyList(package, entry_point)

    for dependency in dependencies:
        dep_name, dep_version, dep_entry_point = Utils.qualifiedNameComponents(dependency.dependency())
        for visited in visited_deps:
            visited_dep_name, visited_dep_version, visited_dep_entry_point = Utils.qualifiedNameComponents(visited.dependency())
            if dep_name == visited_dep_name and dep_version == visited_dep_version and dep_entry_point == visited_dep_entry_point:
                print "circular dep dropped: "+dep_name+dep_version+dep_entry_point
                dependencies.remove(dependency)

    if not _isDependencyListSatisfied(dependencies):
        return False
   
    visited_deps.extend(dependencies)

    runnable = True
    for dependency in dependencies:
        dependency_package = _resolveDep(dependency)
        dep_name, dep_version, dep_entry_point = Utils.qualifiedNameComponents(dependency.dependency())
        if not _isDepTreeRunnable(dependency_package, dep_entry_point, visited_deps):
            runnable = False
            break

    return runnable
    # <<fold 
def _isDependencyListSatisfied(dependencies): # fold>>
    for dependency in dependencies:
        dependency_package = _resolveDep(dependency)
        print dependency_package
     
        if dependency_package is None:
            return False
        dep_name, dep_version, dep_entry_point = Utils.qualifiedNameComponents(dependency.dependency())
        if not _hasLocalRunnabilityRequisites(dependency_package, dep_entry_point):
            return False
    return True
    # <<fold
def _getDependencyList(package, entry_point): # fold>>
    if len(package.manifest().executableGroupList()) == 0: 
        return []

    executable_group = package.manifest().executableGroup(entry_point)
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

