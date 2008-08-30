#!/usr/bin/env python
# @author Stefano Borini 
import platform

def currentPlatform():
    """
    Returns the current platform as a string composed by system and machine eg. Linux-ia64, Darwin-i386 etc.
    If one of the two cannot be obtained, the result is Unknown for the system and unknown for the machine
    """
    (system, host, release, version, machine, processor) = platform.uname()
    if system == "":
        system="Unknown"
    if machine == "":
        machine = "unknown"

    return system+"-"+machine

def isCompatibleWith(platform):
    """
    Returns true if the current platform is compatible with the specified platform.

    @param platform : a platform string
    @return True if it is compatible, False otherwise
    """

    if platform == currentPlatform():
        return True
    if platform == "noarch":
        return True
    return False

