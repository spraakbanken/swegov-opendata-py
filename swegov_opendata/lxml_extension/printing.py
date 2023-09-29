def print_tree(elem, level=0):
    padding = " " * level
    attribs = " ".join(f'{name}="{value}"' for (name, value) in elem.attrib.items())
    elem_open = f"<{elem.tag} {attribs}>" if attribs else f"<{elem.tag}>"
    print(f"{padding}{elem_open}{elem.text or ''}")
    for child in elem:
        print_tree(child, level + 1)
    print(f"{padding}</{elem.tag}>{elem.tail or ''}")


def debug_tree(elem, level=0) -> str:
    padding = " " * level
    attribs = " ".join(f'{name}="{value}"' for (name, value) in elem.attrib.items())
    output = f"{padding}<{elem.tag} {attribs}>{elem.text}"
    for child in elem:
        child_output = debug_tree(child, level + 1)
        output += f"\n{child_output}"
    output += f"{padding}</{elem.tag}>{elem.tail}"
    return output
