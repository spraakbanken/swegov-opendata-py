import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum
from xml.etree.ElementTree import Element

from pydantic import HttpUrl


class DataFormat(str, Enum):
    json = "json"
    csv = "csv"
    csvt = "csvt"
    html = "html"
    sql = "sql"
    text = "text"
    xml = "xml"


@dataclass
class Dataset:
    format: DataFormat
    url: HttpUrl
    uppdaterad: str

    @classmethod
    def from_elem(cls, elem: Element) -> "Dataset":
        if elem.tag != "dataset":
            raise RuntimeError(f"Expected <dataset>, found <{elem.tag}>")
        format_ = None
        url = None
        uppdaterad = None
        for child in elem:
            if child.tag == "format":
                format_ = DataFormat(child.text)
            elif child.tag == "url":
                url = child.text
            elif child.tag == "uppdaterad":
                uppdaterad = child.text

        if format_ is None:
            raise RuntimeError("Dataset is missing 'format'")
        if url is None:
            raise RuntimeError("Dataset is missing 'url'")
        if uppdaterad is None:
            raise RuntimeError("Dataset is missing 'uppdaterad'")
        return cls(format=format_, url=HttpUrl(url), uppdaterad=uppdaterad)


@dataclass
class DatasetLista:
    datasets: list[Dataset]

    @classmethod
    def from_xml(cls, xml: str) -> "DatasetLista":
        root = ET.fromstring(xml)
        if root.tag != "datasetlista":
            raise RuntimeError(f"Expected <datasetlista>, found <{root.tag}>")
        datasets = [Dataset.from_elem(child) for child in root]
        return cls(datasets=datasets)
