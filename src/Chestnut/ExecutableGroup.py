#!/usr/bin/env python
# @author Stefano Borini

class ExecutableGroup:
    """
    Storage class for a group of executables
    """
    def __init__(self): # fold>>
        self.__entry_point=None
        self.__executable_list=[]
        self.__description = None
        # <<fold
    def setEntryPoint(self, entry_point): # fold>>
        self.__entry_point=entry_point
        # <<fold
    def entryPoint(self): # fold>>
        return self.__entry_point
        # <<fold
    def addExecutable(self, executable): # fold>>
        self.__executable_list.append(executable)
        # <<fold
    def executableList(self): # fold>>
        return self.__executable_list
        # <<fold
    def executable(self, platform): # fold>>
        infolist = filter ( lambda x : x.platform() == platform, self.__executable_list)
        if len(infolist) > 0:
            return infolist[0]
        return None
        # <<fold
    def setDescription(self, description): # fold>>
        self.__description = description
        # <<fold
    def description(self): # fold>>
        return self.__description
        # <<fold

