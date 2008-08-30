#!/usr/bin/env python
# @author Stefano Borini

class ExecutableGroup:
    """
    Storage class for a group of executables
    """
    def __init__(self):
        self.__entry_point=None
        self.__executable_list=[]
        self.__description = None
    def setEntryPoint(self, entry_point):
        self.__entry_point=entry_point
    def entryPoint(self):
        return self.__entry_point
    def addExecutable(self, executable):
        self.__executable_list.append(executable)
    def executableList(self):
        return self.__executable_list
    def executable(self, platform):
        infolist = filter ( lambda x : x.platform() == platform, self.__executable_list)
        if len(infolist) > 0:
            return infolist[0]
        return None
    def setDescription(self, description):
        self.__description = description
    def description(self):
        return self.__description

