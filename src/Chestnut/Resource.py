#!/usr/bin/env python
# @author Stefano Borini
import PathType

class Resource:
    """
    Storage class for resources
    """
    def __init__(self):
        self.__path=None
        self.__path_type=None
        self.__platform=None
    def setPath(self, path):
        self.__path=path
    def setPathType(self, path_type):
        if not PathType.validPathType(path_type):
            raise Exception("Invalid path type")
        self.__path_type=path_type
    def setPlatform(self, platform):
        self.__platform=platform
    def platform(self):
        return self.__platform
    def path(self):
        return self.__path
    def pathType(self):
        return self.__path_type
    
