import datetime
import enum
import logging
import typing as t
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from xml.etree.ElementTree import Element

import pydantic

from swegov_opendata import constants

logger = logging.getLogger(__name__)


class DataFormat(enum.StrEnum):
    json = "json"
    csv = "csv"
    csvt = "csvt"
    html = "html"
    sql = "sql"
    text = "text"
    xml = "xml"


def ensure_full_url(value: t.Any) -> str:
    if isinstance(value, str):
        return urljoin(constants.BASE_URL, value)
    raise ValueError(f"Expected <str>, got '<{type(value)}>' (value={value})")


class Dataset(pydantic.BaseModel):
    namn: str
    typ: str
    samling: str
    rm: str
    filnamn: str
    storlek: int
    format: DataFormat
    filformat: str
    uppdaterad: datetime.datetime
    url: t.Annotated[pydantic.HttpUrl, pydantic.BeforeValidator(ensure_full_url)]
    description: str | None
    beskrivning: str | None
    upplysning: str | None

    model_config = pydantic.ConfigDict(extra="forbid")

    @classmethod
    def from_elem(cls, elem: Element) -> t.Self:
        if elem.tag != "dataset":
            raise ValueError(f"Expected <dataset>, found <{elem.tag}>")
        kwargs: dict[str, bytes | str | int | None] = {child.tag: child.text for child in elem}

        return cls(**kwargs)  # ty: ignore[invalid-argument-type]

    @classmethod
    def from_xml(cls, xml: str) -> t.Self:
        root = ET.fromstring(xml)

        try:
            return cls.from_elem(root)
        except Exception:
            logger.exception("Failed to create Dataset from source", extra={"source": xml})
            raise


class DatasetLista(pydantic.BaseModel):
    datasets: list[Dataset]

    @classmethod
    def from_xml(cls, xml: str) -> t.Self:
        root = ET.fromstring(xml)
        if root.tag != "datasetlista":
            logger.error("Expected <datasetlista>, found <%s>", root.tag, extra={"source": xml})
            raise ValueError(f"Expected <datasetlista>, found <{root.tag}>")
        try:
            datasets = [Dataset.from_elem(child) for child in root]
        except (pydantic.ValidationError, ValueError):
            logger.exception("Failed to create Dataset from source", extra={"source": xml})
            raise
        return cls(datasets=datasets)
