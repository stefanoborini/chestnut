#!/usr/bin/env python
# @author Stefano Borini
ABSOLUTE="ABSOLUTE"
PACKAGE_RELATIVE="PACKAGE_RELATIVE"
STANDARD="STANDARD"

def validPathType(path_type):
    return path_type in (ABSOLUTE, PACKAGE_RELATIVE, STANDARD)

    
