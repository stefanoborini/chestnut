#!/usr/bin/env python
# @author Stefano Borini 

class ResourceGroup:
    """
    Storage class for a resource group
    """
    def __init__(self): # fold>>
        self.__entry_point=None
        self.__resource_list=[]
        self.__description=None
        self.__deprecation_message = None
        # <<fold
    def setEntryPoint(self, entry_point): # fold>>
        self.__entry_point=entry_point
        # <<fold
    def entryPoint(self): # fold>>
        return self.__entry_point
        # <<fold
    def addResource(self, resource): # fold>>
        self.__resource_list.append(resource)
        # <<fold
    def resourceList(self): # fold>>
        return self.__resource_list
        # <<fold
    def resource(self, platform): # fold>>
        infolist = filter ( lambda x : x.platform() == platform, self.__resource_list)
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
    def setDeprecationMessage(self, message): # fold>>
        self.__deprecation_message = message
        # <<fold
    def deprecationMessage(self): # fold>>
        return self.__deprecation_message
        # <<fold
    def isDeprecated(self): # fold>>
        return self.__deprecation_message is not None
        # <<fold
