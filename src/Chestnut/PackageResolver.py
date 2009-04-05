#!/usr/bin/env python
# @author Stefano Borini
import Package

import os

class PackageResolver:
    """
    @description Class dealing with the lookup of the packages in the special paths contained in the environment
    @description PACKAGE_SEARCH_PATH. 
    """
    def __init__(self): # fold>>
        package_search_path = os.getenv("PACKAGE_SEARCH_PATH")
        if package_search_path is None:
            self.__search_path_list = []
        else:
            self.__search_path_list = package_search_path.split(os.pathsep) 
        # <<fold
    def find(self, name, version): # fold>>
        """
        @description Performs a lookup of the package in the directories specified by PACKAGE_SEARCH_PATH.
        @return a Package object if found, otherwise None.
        @param name : the name of the package to search
        @param version : a tuple containing the parts of the version
        """

        try:
            numeric_version=tuple(map(int, version))
        except:
            raise Exception("Non numeric version entries currently unsupported")

        packages_filter_name = filter (lambda x: x.name() == name, self.allPackages())

        longest_tuple_len = len(numeric_version)
        for package in packages_filter_name:
            longest_tuple_len = max(len(package.version()), longest_tuple_len) 

        numeric_version = numeric_version + (0,)*(len(numeric_version)-longest_tuple_len)

        # we add a priority count because we don't want to loose the ordering precedence
        # imposed by the PACKAGE_SEARCH_PATH, rearranging accidentally packages with the same versioned name.
        # we add it negative, so when we sort and reverse the list, the first packages encountered
        # will have a higher value (lower in absolute value) and kept first in the list, so we can
        # just pick the first element of the filtered list and be sure it's the one we want.
        #
        # Implementation detail: we are using python 2.3, so we don't have key parameter in sort().
        decorated_list = [ ( tuple(map(int, package.version()))+(0,)*(len(package.version())-longest_tuple_len), 
                            -count,
                            package) for count, package in enumerate(packages_filter_name) ]
        decorated_list.sort()
        decorated_list.reverse()

        chosen=decorated_list[:]
        for pos in xrange(len(numeric_version)):
            chosen = filter(lambda decorated_element : decorated_element[0][pos] == numeric_version[pos], chosen)

        if len(chosen) == 0:
            return None
        else:
            return chosen[0][2]

        # <<fold
    def allPackages(self): # fold>>
        """
        @description scouts the PACKAGE_SEARCH_PATH and produces a list of all available (and sane) packages absolute paths.
        @return a list of absolute paths to packages, in the order they are found
        """
       
        returned_list = []
        # get all the packages found in PACKAGE_SEARCH_PATH
        for path_entry in self.__search_path_list:
            try:
                dir_list=os.listdir(path_entry)
            except:
                dir_list=[]
            for package_dir_name in dir_list:
                if os.path.splitext(package_dir_name)[1] != os.extsep+'package':
                    continue
                try:
                    package = Package.Package(os.path.join(path_entry,package_dir_name))
                except:
                    # failed to initialize the package (missing/corrupted manifest, for example)
                    continue
                returned_list.append(package)
        
        return returned_list
        # <<fold 
