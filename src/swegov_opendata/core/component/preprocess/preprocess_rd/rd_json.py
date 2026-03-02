import typing as t
from collections.abc import Iterable

import trafilatura
from json_arrays import jsonlib
from lxml import etree
from orjson import JSONDecodeError
from structlog import BoundLogger
from trafilatura.settings import Document

from swegov_opendata.core.component.formatting import LazyStr
from swegov_opendata.core.component.swegov_opendata.dokument.forslag import DokForslag
from swegov_opendata.core.component.swegov_opendata.dokument.intressent import (
    DokIntressent,
)
from swegov_opendata.core.component.swegov_opendata.dokument.uppgift import DokUppgift


def extract_elem(raw_text: str) -> etree.Element | None:
    document = trafilatura.extract_with_metadata(
        raw_text, output_format="xml", include_formatting=True, favor_recall=True
    )
    # logger.warning("\ndocument=%s", _to_string(document))
    return etree.fromstring(document.text) if document is not None else None


class ExtractFromJsonError(Exception):
    """Error when extracting text from JSON."""


def preprocess_json(
    data: bytes, metadata: dict[str, t.Any], logger: BoundLogger
) -> bytes | None:
    log = logger.bind(name=__name__)
    log.debug("preprocess_json")
    filecontents = data.decode("utf-8-sig")
    try:
        dokumentstatus_page = jsonlib.loads(filecontents)
    except JSONDecodeError as exc:
        log.error(
            "failed to decode JSON from '%s' in the zipfile '%s'",
            extra={"filecontents": filecontents},
        )
        raise ExtractFromJsonError("failed to decode JSON") from exc
    dokumentstatus = dokumentstatus_page["dokumentstatus"]
    # logger.debug("dokumentstatus=%s", dokumentstatus)
    dokument = dokumentstatus["dokument"]

    docelem = etree.Element("dokument")
    docelem.set("dok_id", dokument["dok_id"])
    for attr in ("dokument_url_text", "dokument_url_html", "dokumentstatus_url_xml"):
        if value := dokument[attr]:
            docelem.set(attr, value)
    html = dokument.get("html")
    if html is None:
        log.warning("The 'html' field is empty")
    # logger.debug(
    #     "html[..]=%s", html[115000:160000], extra={"zippath": zippath.filename, "path": path}
    # )
    elem = extract_elem(html)
    if elem is None:
        return None
    fingerprint = elem.get("fingerprint")
    # print(f"{etree.tostring(elem)=}")
    # print(f"{len(elem)=}")
    for child in elem:
        if child.tag == "main":
            textelem = child
        else:
            log.debug("child=%s", LazyStr(lambda x: str(etree.tostring(x)), child))
    # textelem = elem[0]
    textelem.tag = "text"
    # print(f"{etree.tostring(textelem)=}")
    textelem.set("fingerprint", fingerprint or "")
    textelem.set("datatyp", "huvuddokument")
    for attr in (
        "hangar_id",
        "rm",
        "dokumentnamn",
        "typ",
        "nummer",
        "slutnummer",
        "title",
        "beteckning",
        "subtyp",
        "organ",
        "status",
    ):
        value = dokument.get(attr) or ""
        value = value.replace("\r\n", " ")
        textelem.set(attr, value)
    for attr in (
        "publicerad",
        "datum",
    ):
        value = dokument.get(attr) or ""
        value = value.split(" ")[0]
        textelem.set(attr, value)
    textelem.set("systemdatum", dokument.get("systemdatum") or "")
    if upplysning := metadata.get("upplysning"):
        textelem.set("upplysning", _serialize_upplysning(upplysning))

    if dokintressent_raw := dokumentstatus.get("dokintressent"):
        log.debug("dokintressent=%s", dokintressent_raw)
        dokintressent = DokIntressent.model_validate(dokintressent_raw)
        intressenter = set(dokintressent.intressent)
        name_party = set()
        name = set()
        party = set()
        intressent_id = set()
        roles = set()
        name_party_intressent_id_role = []

        for dok_int in intressenter:
            name.add(dok_int.namn)
            party.add(dok_int.partibet or "")
            name_party.add(f"{dok_int.namn} ({dok_int.partibet or ''})")
            intressent_id.add(dok_int.intressent_id or "")
            roles.add(dok_int.roll)
            name_party_intressent_id_role.append(
                "{namn} ({partibet}), {intressent_id}, {roll}".format(
                    namn=dok_int.namn,
                    partibet=dok_int.partibet or "",
                    intressent_id=dok_int.intressent_id,
                    roll=dok_int.roll,
                )
            )
            textelem.set("intressent_namn_parti", format_multi_value(sorted(name_party)))
            textelem.set("intressent_namn", format_multi_value(sorted(name)))
            textelem.set("intressent_parti", format_multi_value(sorted(party)))
            textelem.set("intressent_id", format_multi_value(sorted(intressent_id)))
            textelem.set(
                "intressent_namn_parti_id_roll",
                format_multi_value(sorted(name_party_intressent_id_role)),
            )
    docelem.append(textelem)
    if debatt := dokumentstatus.get("debatt"):
        log.error("debatt=%s", debatt)
        raise NotImplementedError("handle debatt")
    if dokforslag_raw := dokumentstatus.get("dokforslag"):
        log.debug("dokforslag=%s", dokforslag_raw)
        dokforslag = DokForslag.model_validate(dokforslag_raw)
        for forslag in dokforslag.forslag:
            textelem = etree.Element("text")
            textelem.set("datatyp", "förslag")
            textelem.set("nummer", forslag.nummer)
            for attr, value in (
                ("hangar_id", forslag.hangar_id),
                ("beteckning", forslag.beteckning),
                ("utskottet", forslag.utskottet),
                ("kammaren", forslag.kammaren),
                ("behandlas_i", forslag.behandlas_i),
                ("behandlas_i_punkt", forslag.behandlas_i_punkt),
                ("kammarbeslutstyp", forslag.kammarbeslutstyp),
                ("intressent", forslag.intressent),
                ("avsnitt", forslag.avsnitt),
                ("grundforfattning", forslag.grundforfattning),
                ("andringsforfattning", forslag.andringsforfattning),
            ):
                textelem.set(attr, value or "")

            elem = extract_elem(forslag.lydelse)
            if elem is None:
                textelem.text = forslag.lydelse
            else:
                textelem.append(elem)
            docelem.append(textelem)
        # raise NotImplementedError("handle dokforslag")

    if dokuppgift_raw := dokumentstatus.get("dokuppgift"):
        log.debug("dokuppgift=%s", dokuppgift_raw)
        dokuppgift = DokUppgift.model_validate(dokuppgift_raw)
        for uppgift in dokuppgift.uppgift:
            textelem = etree.Element("text")
            textelem.set("datatyp", "uppgift")
            for attr, value in (
                ("kod", uppgift.kod),
                ("namn", uppgift.namn),
                ("dok_id", uppgift.dok_id or ""),
            ):
                textelem.set(attr, value.strip())

            textelem.set("systemdatum", uppgift.systemdatum or "")
            if text := uppgift.text:
                elem = extract_elem(text)
                if elem is None:
                    textelem.text = text
                else:
                    textelem.append(elem)
            docelem.append(textelem)

    if dokutskottsforslag := dokumentstatus.get("dokutskottsforslag"):
        log.error("dokutskottsforslag=%s", dokutskottsforslag)
        raise NotImplementedError("handle dokutskottsforslag")

    if dokmotforslag := dokumentstatus.get("dokmotforslag"):
        log.error("dokmotforslag=%s", dokmotforslag)
        raise NotImplementedError("handle dokmotforslag")

    # print(f"{etree.tostring(docelem)=}")
    return etree.tostring(docelem, pretty_print=True, encoding="utf-8")


def _serialize_upplysning(d: dict) -> str:
    # print(f"{d=}")
    res = f"{d['upplysning']}"
    res += ",".join(d["year_comment"]["year_comments"])
    # print(f"{res=}")
    return res


def _to_string(document: Document | None) -> str:
    if document is None:
        return "None"
    fields = ",\n\t".join(f"{field}={getattr(document, field)}" for field in document.__slots__)
    # return f"Document({fields})"
    return f"Document(\n\tbody={etree.tostring(document.body, encoding='utf-8')},\n\tcommentsbody={etree.tostring(document.commentsbody)},\n\t{fields})"  # noqa: E501


def format_multi_value(it: Iterable) -> str:
    res = "|".join(it)
    # print(f"{res=}")
    if len(res) == 0:
        return "|"
    return f"|{res}|"
