#!/usr/bin/env python
# @author Stefano Borini

import DependencyType

class Dependency:
    def __init__(self, type, dependency): # fold>>
        if not DependencyType.validDependencyType(type):
            raise Exception("Invalid dependency type "+str(type))
        self.__type = type
        self.__dependency = dependency
        # <<fold
    def type(self): # fold>>
        return self.__type
        # <<fold
    def dependency(self): # fold>>
        return self.__dependency
        # <<fold
