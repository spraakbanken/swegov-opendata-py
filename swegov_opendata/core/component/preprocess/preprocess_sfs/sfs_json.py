import json
import sys
from typing import Optional, Tuple, Union

from lxml import etree, html

from swegov_opendata.lxml_extension import attrib_equals, attrib_startswith
from swegov_opendata.lxml_extension.cleaning import clean_element
from swegov_opendata.lxml_extension.printing import elem_open_as_str, print_tree
from swegov_opendata.serialization import write_xml


def preprocess_json(source: str) -> bytes:
    dokumentstatus = json.loads(source)
    dokumentstatus = dokumentstatus["dokumentstatus"]
    dokument = dokumentstatus["dokument"]
    dokuppgift = dokumentstatus["dokuppgift"]

    docelem = etree.Element("dokument")
    docelem.set("dok_id", dokument["dok_id"])
    textelem = etree.SubElement(docelem, "text")
    textelem.set("datatyp", "huvuddokument")
    for key in [
        "hangar_id",
        "rm",
        "beteckning",
        "dokumentnamn",
        "typ",
        "subtyp",
        "organ",
        "nummer",
        "slutnummer",
        "titel",
        "status",
        "publicerad",
        "systemdatum",
        "datum",
    ]:
        textelem.set(key, dokument[key].replace("\r\n", " "))
    for key in [
        "tempbeteckning",
        "subtitel",
    ]:
        if value := dokument.get(key):
            textelem.set(key, value)
    for dokuppg in dokuppgift["uppgift"]:
        if dokuppg["kod"] == "upphnr":
            textelem.set("upphnr", dokuppg["text"])
        if dokuppg["kod"] == "upphavd":
            upphavd_at, _remaining = dokuppg["text"].split(" ", 1)
            textelem.set("upphavd", upphavd_at)

    process_sfs_html(dokument["html"], textelem, filename="unknown")

    clean_element(textelem)
    # Return new XML
    tree = etree.ElementTree(docelem)
    return etree.tostring(tree, pretty_print=True, encoding="utf-8")


def process_sfs_html(  # noqa: C901
    contents: str,
    textelem,
    filename: str,
    *,
    testfile=False,
):
    """Process the actual text content of the document."""
    contents = contents.replace('"', '"')
    contents = contents.replace("\r\n", " ")
    contentsxml = build_elem(contents)
    # print(etree.tostring(contentsxml), file=sys.stderr)

    if contentsxml[0].tag == "div" and attrib_equals(contentsxml[0], "class", "dok"):
        convert_div_dok(contentsxml[0], textelem)
    else:
        convert_sfs_standard(contentsxml, textelem, filename, testfile=testfile)


def convert_sfs_standard(contentsxml, textelem, filename, *, testfile: bool = False):
    extract_metadata(contentsxml, textelem)
    for element in contentsxml:
        if (
            element.tag == "div"
            and "class" in element.attrib
            and element.attrib["class"] == "sfstoc"
        ):
            print("removed <div class='sfstoc'>")
            # print_tree(element)
            contentsxml.remove(element)
            # print_tree(contentsxml)

            break

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
    # print_tree(contentsxml)

    # Check text length
    orig_text_length = 0
    for i in etree.ElementTextIterator(contentsxml):
        orig_text_length += len(i)
    if not orig_text_length:
        return False

    if testfile:
        write_xml(etree.tostring(contentsxml, encoding="utf-8"), "test_orig.xml")

    # Remove tags but keep contents
    # strip_tags(
    #     contentsxml,
    #     [
    #         "table",
    #         "thead",
    #         "tbody",
    #         "form",
    #         "caption",
    #         "a",
    #         "link",
    #         "span",
    #         "em",
    #         "strong",
    #         "sub",
    #         "sup",
    #         "b",
    #         "i",
    #         "u",
    #         "nobr",
    #         "ul",
    #         "ol",
    #         "colgroup",
    #         "col",
    #         "tt",
    #         "dir",
    #         "del",
    #         "ins",
    #         "s",
    #         "label",
    #         "pre",
    #         "spanstyle",
    #         "metricconverterproductid",
    #         "spanclass",
    #         "bstyle",
    #         "istyle",
    #         "brclear",
    #         "brstyle",
    #         "comment",
    #         "img",
    #         "hr",
    #         "fontsize",
    #         "aname",
    #         "metricconverter",
    #         "astyle",
    #         "personname",
    #         "spanlang",
    #         "date",
    #         "font",
    #         "fontcolor",
    #         "ahref",
    #         "textovervagande",
    #         "rubrikavvikandemening",
    #     ],
    # )
    # print_tree(contentsxml)

    # Replace divs with more meaningful tags
    page_nr = 1
    for element in contentsxml.iter("div"):
        print(elem_open_as_str(element))
        # print_tree(element)
        if attrib_startswith(element, "id", "page_"):
            element.tag = "page"
            element.attrib["id"] = element.attrib["id"][5:]
            continue
        if attrib_equals(element, "class", "pageWrap"):
            raise RuntimeError("found pageWrap")
            element.tag = "page"
            element.attrib["id"] = str(page_nr)
            page_nr += 1
            continue
        prev = None
        prev_text = None
        for child in element:
            # print("=== before ===")
            # print_tree(child)
            if prev is not None and child.tag == "br":
                prev.append(child)
                # print("=== after ===")
                # print_tree(prev)
                continue
            if prev_text:
                child.text = merge_text(prev_text, child.text)
                prev_text = None
            if child.tag == "h3" and child.attrib.get("name") == "overgang":
                prev_text = child.tail
                child.tail = None
                # print("=== after tail ===")
                # print(f"{prev_text=}")
                # print_tree(child)

            to_paragraph(child)
            # print("=== after ===")
            # print_tree(child)
            prev = child

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
    # print("=== whole tree ===")
    # print_tree(contentsxml)
    # # Replace some tags with p
    # for element in list(
    #     contentsxml.iter(
    #         "title", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "td", "th"
    #     )
    # ):
    #     element.tag = "p"

    # # Remove nested pages (but keep contents)
    # for outer_page_elem in contentsxml.xpath("//page[.//page]"):
    #     outer_page_elem.tag = "kasta"

    # # Remove attributes from p and remove nested ps (but keep contents)
    # for outer_p_elem in contentsxml.xpath("//p[.//p]"):
    #     outer_p_elem.tag = "kasta"
    # for p_elem in contentsxml.xpath("//p"):
    #     for attr in p_elem.attrib:
    #         p_elem.attrib.pop(attr)

    # # Decompose anything that's not "text", "page" or "p"
    # allowed_tags = {"kasta", "div", "text", "page", "p"}
    # forbidden_tags = set()
    # for element in contentsxml.iter():
    #     if element.tag not in allowed_tags:
    #         forbidden_tags.add(element.tag)
    #         element.tag = "kasta"
    # etree.strip_tags(contentsxml, ["kasta", "div"])
    # if forbidden_tags:
    #     print(f"    Removed forbidden tags from {filename}: {forbidden_tags}")

    # # Check text length to see that nothing was lost
    # text_length = 0
    # for i in etree.ElementTextIterator(contentsxml):
    #     text_length += len(i)
    # if text_length != orig_text_length:
    #     diff = orig_text_length - text_length
    #     # if diff > 100:
    #     print(f"    Contents were lost in {filename} ({diff} chars missing)")
    # if not text_length:
    #     return False

    # # Remove unnecessary whitespace
    # for element in contentsxml.iter():
    #     if element.tail is not None:
    #         element.tail = (
    #             trimmed_tail if (trimmed_tail := element.tail.strip()) else None
    #         )
    #     if element.text is not None:
    #         element.text = (
    #             trimmed_text if (trimmed_text := element.text.strip()) else None
    #         )
    # # Remove empty tags
    # for element in contentsxml.xpath(".//*[not(node())]"):
    #     element.getparent().remove(element)

    # # Check for nested tags
    # if contentsxml.xpath("//*/p/*/p"):
    #     print(f"    WARNING: Found nested element 'p'")
    #     etree.dump(contentsxml.xpath("//*/p/*/p")[0])

    # Attach to parent
    if len(contentsxml) == 0:
        textelem.text = contentsxml.text
    for element in contentsxml.iter("div"):
        for child in element:
            if not is_empty(child):
                textelem.append(child)
    # print("=== whole tree ===")
    # print_tree(textelem)
    return True


def is_empty(elem) -> bool:
    num_empty_children = sum(is_empty(child) for child in elem)

    return elem.text is None and elem.tail is None and len(elem) == num_empty_children


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


def build_elem(contents: str) -> etree._Element:
    if not isinstance(contents, str):
        contents = contents.decode("UTF-8")

    # print(cleaned_content)
    # print("\n-----\n")
    contents = f"<text>{contents}</text>"
    return html.fromstring(
        contents, parser=etree.HTMLParser(remove_comments=True, remove_pis=True)
    )


def extract_metadata(contentsxml, textelem) -> None:
    metadata_key = ""
    for child in contentsxml:
        if child.tag == "b" and child.text in ["Ändringsregister", "Källa"]:
            metadata_key = child.text

        if metadata_key and child.tag == "a":
            value = child.attrib["href"]
            textelem.set(metadata_key.lower(), value)
            metadata_key = ""


def to_paragraph(elem) -> None:
    # print("=== to_paragraph ===")
    elem.tag = "p"
    for child in elem:
        # print("=== to_paragraph ===")
        # print_tree(child)
        elem.text = merge_text(elem.text, child.text)
        elem.text = merge_text(elem.text, child.tail)
        elem.remove(child)

    elem.text = merge_text(elem.text, elem.tail)
    elem.tail = None


def merge_text(t1: Optional[str], t2: Optional[str]) -> Optional[str]:
    if t1 is None:
        return None if t2 is None else t2
    return t1 if t2 is None else f"{t1} {t2}"


def convert_div_dok(contentsxml: etree._Element, textelem: etree._Element) -> None:
    print(f">>> convert_div_dok {elem_open_as_str(contentsxml)}")
    page_nr = 1
    for element in contentsxml:
        if element.tag == "style":
            continue
        if element.tag == "div" and attrib_equals(element, "class", "pageWrap"):
            page = div_dok_extract_page(element)
            page.attrib["id"] = str(page_nr)
            page_nr += 1
            print(f"=== convert_div_dok {elem_open_as_str(page)}")
            textelem.append(page)
    print(f"<<< convert_div_dok {elem_open_as_str(contentsxml)}")


def div_dok_extract_page(elem: etree._Element) -> etree._Element:
    print(f">>> div_dok_extract_page {elem_open_as_str(elem)}")
    page = etree.Element("page")

    if elem[0].tag == "div" and attrib_equals(elem[0], "class", "sida"):
        elem = elem[0]
    # elem = elem[0]
    for child in elem:
        paragraphs = div_dok_extract_paragraphs(child)
        for paragraph in paragraphs:
            print_tree(paragraph)
            page.append(paragraph)
    print(f"{len(elem)=}")
    print(f"{len(page)=}")
    print(
        f"<<< div_dok_extract_page {elem_open_as_str(elem)}: {elem_open_as_str(page)}"
    )
    return page


def div_dok_extract_paragraphs(elem: etree._Element) -> list[etree._Element]:
    print(f">>> div_dok_extract_paragraphs {elem_open_as_str(elem)}")
    print_tree(elem)
    paragraphs = []
    if elem.tag == "div":
        if len(elem) == 0:
            print(
                f"=== div_dok_extract_paragraphs {elem_open_as_str(elem)}: no children"
            )
            return paragraphs
        for i, child in enumerate(elem):
            print(
                f"=== div_dok_extract_paragraphs {elem_open_as_str(elem)} === child {i}: {elem_open_as_str(child)}"
            )
            # print_tree(child)
            child_p = extract_paragraph_recursive(child)
            print_tree(child_p)
            paragraphs.append(child_p)
    elif elem.tag == "p":
        print(f"=== div_dok_extract_paragraphs {elem_open_as_str(elem)} === ")
        elem_p = extract_paragraph_recursive(elem)
        print_tree(elem_p)
        paragraphs.append(elem_p)
        # div_dok_extract_paragraph(elem, paragraphs)
    print(
        f"<<< div_dok_extract_paragraphs {elem_open_as_str(elem)}: {[elem_open_as_str(p) for p in paragraphs]}"
    )
    return paragraphs


def div_dok_extract_paragraph(elem, paragraphs):
    print(f"div_dok_extract_paragraph {elem_open_as_str(elem)}")
    paragraph = etree.Element("p")
    paragraph.text = elem.text
    prev = paragraph
    for child in elem:
        print_tree(child)
        for text_or_elem in div_dok_extract_text_br_and_tail(child):
            if isinstance(text_or_elem, str):
                prev.text = merge_text(prev.text, text_or_elem)
            else:
                paragraph.append(text_or_elem)
                prev = text_or_elem
        # prev.text = merge_text(prev.text, child.text)
        # if child.tag == "br":
        #     print("found <br>")
        #     prev = etree.SubElement(paragraph, "br")
        # else:
        #     prev.tail = merge_text(prev.tail, child.tail)
    prev.tail = merge_text(prev.tail, elem.tail)
    paragraphs.append(paragraph)


def div_dok_extract_text_and_br(paragraph: etree._Element, elem: etree._Element):
    print(f"div_dok_extract_text_and_br {elem_open_as_str(elem)}")
    if len(elem) == 0:
        paragraph.text = merge_text(paragraph.text, elem.text)
    else:
        for child in elem:
            pass


def div_dok_extract_text_br_and_tail(
    elem: etree._Element,
) -> list[Union[str, etree._Element]]:
    print(f"div_dok_extract_text_br_and_tail {elem_open_as_str(elem)}")
    result = []
    prev_text = elem.text
    prev_tail = None
    for child in elem:
        if child.tag == "br":
            result.append(prev_text)
            prev_text = None
            result.append(etree.Element("br"))
        else:
            prev_text = merge_text(prev_text, child.text)
            prev_text = merge_text(prev_text, child.tail)
        print(f"{result=}")

    prev_text = merge_text(prev_text, elem.tail)
    if prev_text is not None:
        result.append(prev_text)
    print(f"{result=}")

    return result


def extract_paragraph_recursive(elem: etree._Element) -> etree._Element:
    print(f">>> extract_paragraph_recursive {elem_open_as_str(elem)}")
    if elem.tag == "table":
        return etree.Element("table", attrib={"class": "removed"})
    tag = "br" if elem.tag == "br" else "p"
    parapraph = etree.Element(tag)
    parapraph.text = elem.text
    parapraph.tail = elem.tail
    prev = parapraph
    for child in elem:
        child_p = extract_paragraph_recursive(child)
        if child_p.tag == "br":
            parapraph.append(child_p)
            prev = child_p
        elif child_p.tag == "p":
            print("=== paragraph")
            print_tree(parapraph)
            print("=== child_p")
            print_tree(child_p)
            print("=== ")
            if len(parapraph) == 0:
                prev.text = merge_text(prev.text, child_p.text)
            else:
                prev.tail = merge_text(prev.tail, child_p.text)
            parapraph.extend(child_p)
            prev = parapraph[-1] if len(parapraph) > 0 else prev

    print(
        f"<<< extract_paragraph_recursive {elem_open_as_str(elem)}: {elem_open_as_str(parapraph)}"
    )
    return parapraph
