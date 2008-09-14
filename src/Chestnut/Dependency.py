#!/usr/bin/env python
# @author Stefano Borini

import DependencyType

class Dependency:
    def __init__(self, type, dependency):
        if not DependencyType.validDependencyType(type):
            raise Exception("invalid dependency type"+str(type))
        self.__type = type
        self.__dependency = dependency
    def type(self):
        return self.__type
    def dependency(self):
        return self.__dependency

