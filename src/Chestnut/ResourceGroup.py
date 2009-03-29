#!/usr/bin/env python
# @author Stefano Borini 

class ResourceGroup:
    """
    Storage class for a resource group
    """
    def __init__(self):
        self.__entry_point=None
        self.__resource_list=[]
        self.__description=None
    def setEntryPoint(self, entry_point):
        self.__entry_point=entry_point
    def entryPoint(self):
        return self.__entry_point
    def addResource(self, resource):
        self.__resource_list.append(resource)
    def resourceList(self):
        return self.__resource_list
    def resource(self, platform):
        infolist = filter ( lambda x : x.platform() == platform, self.__resource_list)
        if len(infolist) > 0:
            return infolist[0]
        return None
    def setDescription(self, description):
        self.__description = description
    def description(self):
        return self.__description
