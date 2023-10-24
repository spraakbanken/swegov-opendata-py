def strip_tags(elem, tags_to_remove: list[str]) -> None:
    for child in elem:
        if child.tag in tags_to_remove:
            if child_text := collect_texts(child):
                elem.text = (
                    child_text if elem.text is None else f" {elem.text} {child_text} "
                )
            elem.remove(child)
        else:
            strip_tags(child, tags_to_remove)


def collect_texts(elem) -> str:
    result = elem.text or " "
    for child in elem:
        if child_text := collect_texts(child):
            result = f" {result} {child_text} "
    if tail := elem.tail:
        result = f"{result} {tail} "
    # print(f"collect_texts: {result=}")
    return result
