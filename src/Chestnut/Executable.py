#!/usr/bin/env python
# @author Stefano Borini 
import PathType

class Executable:
    """
    Storage class for a platform dependent executable
    """
    def __init__(self):
        self.__platform=None
        self.__path=None
        self.__path_type=None
        self.__interpreter=None
    def setPath(self, path):
        self.__path=path
    def setPathType(self, path_type):
        if not PathType.validPathType(path_type):
            raise Exception("Invalid path type")
        self.__path_type=path_type
    def setPlatform(self, platform):
        self.__platform=platform
    def setInterpreter(self, interpreter):
        self.__interpreter=interpreter
    def platform(self):
        return self.__platform
    def path(self):
        return self.__path
    def pathType(self):
        return self.__path_type
    def interpreter(self):
        return self.__interpreter