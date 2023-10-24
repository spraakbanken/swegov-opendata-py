def print_tree(elem, level=0, *, verbose: bool = False):
    padding = " " * level
    attribs = " ".join(f'{name}="{value}"' for (name, value) in elem.attrib.items())
    elem_open = f"<{elem.tag} {attribs}>" if attribs else f"<{elem.tag}>"
    if verbose:
        elem_text = f"'{elem.text}'" if elem.text else "None"
    else:
        elem_text = elem.text or ""
    print(f"{padding}{elem_open}{elem_text}")
    for child in elem:
        print_tree(child, level + 1, verbose=verbose)
    if verbose:
        elem_tail = f"'{elem.tail}'" if elem.tail else "None"
    else:
        elem_tail = elem.tail or ""
    print(f"{padding}</{elem.tag}>{elem_tail}")


def elem_open_as_str(elem) -> str:
    attribs = " ".join(f'{name}="{value}"' for (name, value) in elem.attrib.items())

    return f"<{elem.tag} {attribs}>" if attribs else f"<{elem.tag}>"


def debug_tree(elem, level=0) -> str:
    padding = " " * level
    attribs = " ".join(f'{name}="{value}"' for (name, value) in elem.attrib.items())
    output = f"{padding}<{elem.tag} {attribs}>{elem.text}"
    for child in elem:
        child_output = debug_tree(child, level + 1)
        output += f"\n{child_output}"
    output += f"{padding}</{elem.tag}>{elem.tail}"
    return output
