def qualifiedNameComponents(qualified_name): # fold>>
    """
    @description parses a qualified name and returns the components
    @param versioned_name: a string in the format name[-major[.minor[.patch_level[etc..]]]][/entry_point]
    @return A tuple with four elements (name, major, minor, patch_level) with missing values set to None
    @return If the versioned_name string does not comply with the format, it returns None.
    """

    if len(qualified_name.strip()) == 0:
        return None

    if "/" in qualified_name:
        versioned_name, entry_point = qualified_name.split("/", 1)
        if len(entry_point.strip()) == 0 or len(versioned_name.strip()) == 0:
            return None
    else:
        versioned_name = qualified_name
        entry_point = None

    l = versioned_name.split("-")

    if len(l) == 1:
        package_name = l[0]
        version_string = None
    elif len(l) == 2:
        package_name, version_string = l
    else:
        return None
        
    if version_string is not None:
        version_tuple = tuple(version_string.split("."))
    else:
        version_tuple = tuple()
    
    for entry in version_tuple:
        if len(entry.strip()) == 0:
            return None

    return (package_name, version_tuple, entry_point)

    # <<fold

