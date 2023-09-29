"""Script for creating original/xml files for all rd-corpora."""

import xml.sax.saxutils

from lxml import etree, html

from swegov_opendata.serialization import write_xml


def process_html(elem, textelem, filename, *, testfile=False):  # noqa: C901
    """Process the actual text content of the document."""

    contents = xml.sax.saxutils.unescape(elem.text)
    if not isinstance(contents, str):
        contents = contents.decode("UTF-8")

    # cleaned_content = clean_html(contents)
    cleaned_content = contents
    if not cleaned_content:
        return False

    # print(cleaned_content)
    # print("\n-----\n")
    contents = "<text>" + cleaned_content + "</text>"
    contentsxml = html.fromstring(
        contents, parser=etree.HTMLParser(remove_comments=True, remove_pis=True)
    )

    # Remove some attributes and tags
    etree.strip_attributes(
        contentsxml,
        [
            "style",
            "class",
            "cellpadding",
            "cellspacing",
            "colspan",
            "images" ".",
            "align",
            "valign",
            "name",
            "rowspan",
        ],
    )
    etree.strip_elements(
        contentsxml,
        [
            "style",
            "STYLE",
            "meta",
            "META",
            "ingenbild",
            "INGENBILD",
            "script",
            "SCRIPT",
        ],
    )

    # Check text length
    orig_text_length = 0
    for i in etree.ElementTextIterator(contentsxml):
        orig_text_length += len(i)
    if not orig_text_length:
        return False

    if testfile:
        write_xml(etree.tostring(contentsxml, encoding="utf-8"), "test_orig.xml")

    # Remove tags but keep contents
    strip_tags(
        contentsxml,
        [
            "table",
            "thead",
            "tbody",
            "form",
            "caption",
            "a",
            "link",
            "span",
            "em",
            "strong",
            "sub",
            "sup",
            "b",
            "i",
            "u",
            "nobr",
            "ul",
            "ol",
            "colgroup",
            "col",
            "tt",
            "dir",
            "del",
            "ins",
            "s",
            "label",
            "pre",
            "spanstyle",
            "metricconverterproductid",
            "spanclass",
            "bstyle",
            "istyle",
            "brclear",
            "brstyle",
            "comment",
            "img",
            "hr",
            "fontsize",
            "aname",
            "metricconverter",
            "astyle",
            "personname",
            "spanlang",
            "date",
            "font",
            "fontcolor",
            "ahref",
            "textovervagande",
            "rubrikavvikandemening",
        ],
    )

    # Replace divs with more meaningful tags
    for element in list(contentsxml.iter("div")):
        if "id" in element.attrib:
            if element.attrib["id"].startswith("page_"):
                element.tag = "page"
                element.attrib["id"] = element.attrib["id"][5:]
                continue

    # Replace some tags with p
    for element in list(
        contentsxml.iter(
            "title", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "td", "th"
        )
    ):
        element.tag = "p"

    # Remove nested pages (but keep contents)
    for outer_page_elem in contentsxml.xpath("//page[.//page]"):
        outer_page_elem.tag = "kasta"

    # Remove attributes from p and remove nested ps (but keep contents)
    for outer_p_elem in contentsxml.xpath("//p[.//p]"):
        outer_p_elem.tag = "kasta"
    for p_elem in contentsxml.xpath("//p"):
        for attr in p_elem.attrib:
            p_elem.attrib.pop(attr)

    # Decompose anything that's not "text", "page" or "p"
    allowed_tags = {"kasta", "div", "text", "page", "p"}
    forbidden_tags = set()
    for element in contentsxml.iter():
        if element.tag not in allowed_tags:
            forbidden_tags.add(element.tag)
            element.tag = "kasta"
    etree.strip_tags(contentsxml, ["kasta", "div"])
    if forbidden_tags:
        print(f"    Removed forbidden tags from {filename}: {forbidden_tags}")

    # Check text length to see that nothing was lost
    text_length = 0
    for i in etree.ElementTextIterator(contentsxml):
        text_length += len(i)
    if text_length != orig_text_length:
        diff = orig_text_length - text_length
        # if diff > 100:
        print(f"    Contents were lost in {filename} ({diff} chars missing)")
    if not text_length:
        return False

    # Remove unnecessary whitespace
    for element in contentsxml.iter():
        if element.tail is not None:
            element.tail = (
                trimmed_tail if (trimmed_tail := element.tail.strip()) else None
            )
        if element.text is not None:
            element.text = (
                trimmed_text if (trimmed_text := element.text.strip()) else None
            )
    # Remove empty tags
    for element in contentsxml.xpath(".//*[not(node())]"):
        element.getparent().remove(element)

    # # Check for nested tags
    # if contentsxml.xpath("//*/p/*/p"):
    #     print(f"    WARNING: Found nested element 'p'")
    #     etree.dump(contentsxml.xpath("//*/p/*/p")[0])

    # Attach to parent
    if len(contentsxml) == 0:
        textelem.text = contentsxml.text
    for element in contentsxml:
        textelem.append(element)
    return True


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
