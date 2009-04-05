#!/usr/bin/env python
# @author Stefano Borini 
import PathType

class Executable:
    """
    Storage class for a platform dependent executable
    """
    def __init__(self): # fold>>
        self.__platform=None
        self.__path=None
        self.__path_type=None
        self.__interpreter=None

        # <<fold
    def setPath(self, path): # fold>>
        self.__path=path
        # <<fold
    def setPathType(self, path_type): # fold>>
        if not PathType.validPathType(path_type):
            raise Exception("Invalid path type")
        self.__path_type=path_type
        # <<fold
    def setPlatform(self, platform): # fold>>
        self.__platform=platform
        # <<fold
    def setInterpreter(self, interpreter): # fold>>
        self.__interpreter=interpreter
        # <<fold
    def platform(self): # fold>>
        return self.__platform
        # <<fold
    def path(self): # fold>>
        return self.__path
        # <<fold
    def pathType(self): # fold>>
        return self.__path_type
        # <<fold
    def interpreter(self): # fold>>
        return self.__interpreter
        # <<fold
