def attrib_startswith(elem, name: str, prefix: str) -> bool:
    return name in elem.attrib and elem.attrib[name].startswith(prefix)


def attrib_equals(elem, name: str, value: str) -> bool:
    return name in elem.attrib and elem.attrib[name] == value
