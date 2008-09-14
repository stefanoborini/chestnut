#!/usr/bin/env python
# @author Stefano Borini
PACKAGED_EXECUTABLE="PACKAGED_EXECUTABLE"
PACKAGED_RESOURCE="PACKAGED_RESOURCE"

def validDependencyType(dependency_type):
    return dependency_type in (PACKAGED_EXECUTABLE, PACKAGED_RESOURCE)

    
