#!/usr/bin/env python
# @author Stefano Borini
PACKAGED_EXECUTABLE="PACKAGED_EXECUTABLE"
PACKAGED_RESOURCE="PACKAGED_RESOURCE"

def validDependencyType(path_type):
    return path_type in (PACKAGED_EXECUTABLE, PACKAGED_RESOURCE)

    
