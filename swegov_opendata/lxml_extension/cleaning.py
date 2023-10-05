import re
import unicodedata
from typing import Optional


def clean_html(text):
    # Replace "special" spaces with ordinary spaces
    text = re.sub("[\u00A0\u2006 \r\n]+", " ", text)
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
    text = re.sub("<![if ! IE]>", "", text)
    text = re.sub("<!--\[if lte IE 7\]>", "", text)
    text = re.sub("<!--\[if gte IE 8\]>", "", text)
    text = re.sub("<!\[if \!vml\]>", "", text)
    text = re.sub("<!\[if \!supportMisalignedColumns\]>", "", text)
    text = re.sub("<!\[if \!supportLineBreakNewLine\]>", "", text)
    text = re.sub("<!\[endif\]-->", "", text)
    text = re.sub("<!\[endif\]>", "", text)
    text = re.sub("<!\[if \!supportEmptyParas\]>", "", text)
    text = re.sub(r"<\/?NOBR>", "", text)
    text = re.sub("&nbsp;", "", text)
    # Replace br tags with line breaks
    text = re.sub(r"<(br|BR)( [^>]*)?\/?>", "\n", text)

    # Remove soft hyphens
    text = re.sub("\u00AD", "", text)

    return text.strip()


def clean_text(text: str) -> str:
    return clean_html(text)


def clean_text_opt(text: Optional[str]) -> Optional[str]:
    return None if text is None else clean_html(text)


def clean_element(elem) -> None:
    """Cleans an element."""
    for node in elem:
        if node.text is not None:
            node.text = clean_text(node.text)
        if node.tail is not None:
            node.tail = clean_text(node.tail)
        clean_element(node)
