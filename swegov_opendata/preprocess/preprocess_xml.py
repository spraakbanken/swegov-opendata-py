"""Script for creating original/xml files for all rd-corpora."""

import re
import unicodedata
from datetime import datetime

from lxml import etree

from swegov_opendata.preprocess.preprocess_html import process_html

# Parsing large XML files:
# http://making-security-measurable.1364806.n2.nabble.com/Parsing-large-9-5mb-XML-files-with-lxml-td7580657.html


def preprocess_xml(xml_string, filename, *, testfile=False):  # noqa: C901
    """Extract meta data and html from f."""
    p = etree.XMLParser(huge_tree=True)
    tree = etree.fromstring(xml_string, p)  # noqa: S320

    # Create new element and build document
    docelem = etree.Element("dokument")
    textelem = etree.SubElement(docelem, "text")
    textelem.set("datatyp", "huvuddokument")

    dokbilaga = tree.find("dokbilaga")
    if dokbilaga and len(dokbilaga) > 0:
        for bilaga in dokbilaga:
            for child in bilaga:
                if child.tag.startswith("fil"):
                    textelem.set(child.tag, str(child.text))

    search_document = tree.find("dokument")
    if search_document is None:
        raise ValueError("Can't find <dokument> in file {filename}")

    # The html node contains the main text. Files without <html> may have other text nodes
    if search_document.find("html") is None:
        print(f"    WARNING: No html found in {filename}")

    for elem in search_document:
        # Process contents
        if elem.tag == "html":
            process_html(elem, textelem, filename, testfile=testfile)
        # Skip "text" element (if it exists, it contains the same text as <html>)
        elif elem.tag == "text":
            continue
        # Collect meta data from within "dokument"
        elif elem.text is not None:
            if elem.text.strip():
                if elem.tag in ["images"]:
                    continue
                # Assign document attrs to docelem and the rest to textelem
                elif elem.tag in [
                    "dok_id",
                    "dokumentstatus_url_xml",
                    "dokument_url_text",
                    "dokument_url_html",
                ]:
                    docelem.set(elem.tag, elem.text)
                else:
                    textelem.set(elem.tag, elem.text)

    # Collect more metadata (attributes outside of "dokument") and look for other text nodes
    intressenter = []
    interesting_textnodes = [
        "anforande > anf_text",
        "forslag > lydelse",
        "forslag > lydelse2",
        "uppgift > text",
        "utskottsforslag > votering_sammanfattning_html",
    ]
    for elem in tree.iter():
        # Skip dokument, html and text since they are already processed; ignore comments
        if elem.tag in ["dokument", "html", "text"] or type(elem) == etree._Comment:
            continue
        # Collect "intressent" metadata and process later
        elif elem.tag == "intressent":
            children = {c.tag: c.text for c in elem}
            name = children.get("namn", "")
            party = (children.get("partibet", "") or "").upper()
            if name and party:
                intressenter.append((name, party))
        # Collect all other relevant text nodes
        elif elem.text is not None and elem.text.strip():
            parent = next(elem.iterancestors())
            ancestorstring = parent.tag + " > " + elem.tag
            if ancestorstring in interesting_textnodes:
                textelem = etree.SubElement(docelem, "text")
                textelem.set("datatyp", parent.tag)
                process_html(elem, textelem, filename, testfile=testfile)
                # Metadata for new elements
                for child in list(parent):
                    if child != elem and child.text:
                        attrname = child.tag
                        if attrname.startswith("anf_"):
                            attrname = attrname[4:]
                        textelem.set(attrname, child.text.strip())

    # Check if docelem contains any text
    has_text = False
    for i in etree.ElementTextIterator(docelem):
        if len(i):
            has_text = True
            break
    if not has_text:
        return ""

    # Add "intressent" metadata as sets
    if intressenter:
        intressenter = set(intressenter)
        name_party = []
        name = []
        party = set()
        for n, p in intressenter:
            name_party.append(n + " (" + p + ")")
            name.append(n)
            party.add(p)
        textelem.set("intressent_namn_parti", "|" + "|".join(name_party) + "|")
        textelem.set("intressent_namn", "|" + "|".join(name) + "|")
        textelem.set("intressent_parti", "|" + "|".join(party) + "|")

    # Combine "datum" and "datumtid"
    if "datumtid" in docelem.attrib:
        docelem.set("datum", docelem.attrib["datumtid"])
        docelem.attrib.pop("datumtid", "")
    for textelem in docelem.iter("text"):
        textattrs = list(textelem.attrib.keys())
        if "datumtid" in textattrs:
            textelem.set("datum", textelem.attrib["datumtid"])
            textelem.attrib.pop("datumtid", "")
    # Remove invalid dates (year out of range)
    year = int(textelem.get("datum")[:4])
    this_year = int(datetime.today().strftime("%Y"))
    if (year < 1900) or (year > this_year):
        textelem.attrib.pop("datum")

    clean_element(textelem)
    # Return new XML
    tree = etree.ElementTree(docelem)
    return etree.tostring(tree, pretty_print=True, encoding="utf-8")


def clean_html(text):
    # Replace "special" spaces with ordinary spaces
    text = re.sub("[\u00A0\u2006 \n]+", " ", text)
    # Remove chars between 0-31 and 127-159, but keep 10 (line break).
    # TODO: does this have any effect?
    text = re.sub(
        r"&#("
        + "|".join(str(i) for i in [*range(10), *range(11, 32), *range(127, 160)])
        + ");",
        "",
        text,
    )
    chars = [chr(i) for i in [*range(10), *range(11, 32), *range(127, 160)]]
    text = text.translate({ord(c): None for c in chars})
    # Remove control and formatting chars
    text = "".join(c for c in text if unicodedata.category(c)[:2] != "Cc")
    text = "".join(c for c in text if unicodedata.category(c)[:2] != "Cf")

    # text = re.sub(u"\u2006", " ", text)
    # Remove long rows of underscores
    text = re.sub(r"__+", "", text)
    # Remove some more dirt
    text = re.sub("<\!\[if ! IE\]>", "", text)
    text = re.sub("<\!--\[if lte IE 7\]>", "", text)
    text = re.sub("<\!--\[if gte IE 8\]>", "", text)
    text = re.sub("<\!\[if \!vml\]>", "", text)
    text = re.sub("<\!\[if \!supportMisalignedColumns\]>", "", text)
    text = re.sub("<\!\[if \!supportLineBreakNewLine\]>", "", text)
    text = re.sub("<\!\[endif\]-->", "", text)
    text = re.sub("<\!\[endif\]>", "", text)
    text = re.sub("<\!\[if \!supportEmptyParas\]>", "", text)
    text = re.sub(r"<\/?NOBR>", "", text)
    text = re.sub("&nbsp;", "", text)
    # Replace br tags with line breaks
    text = re.sub(r"<(br|BR)( [^>]*)?\/?>", "\n", text)

    # Remove soft hyphens
    text = re.sub("\u00AD", "", text)

    return text.strip()


def clean_text(text: str) -> str:
    return clean_html(text)


def clean_element(elem) -> None:
    """Cleans an element."""
    for node in elem:
        node.text = clean_html(node.text)
        if node.tail is not None:
            node.tail = clean_html(node.tail)
