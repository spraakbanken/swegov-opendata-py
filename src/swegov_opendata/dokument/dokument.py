import datetime
import logging
import typing as t

import pydantic

from swegov_opendata.value_objects.avdelning import Avdelningar
from swegov_opendata.value_objects.dokument_typ import DokumentTyp

logger = logging.getLogger(__name__)


def split_space_take_first(value: t.Any) -> t.Any:
    if isinstance(value, str):
        return "" if not value else value.split()[0]
    return value


def ensure_none_if_empty(value: t.Any) -> t.Any:
    if isinstance(value, str):
        return None if value == "" else value
    return value


def ensure_string(value: t.Any) -> t.Any:
    def _ensure_str(v: t.Any) -> str:
        return v if isinstance(v, str) else str(v)

    if isinstance(value, list):
        if len(value) == 0:
            return ""
        return _ensure_str(value[0])
    return _ensure_str(value)


class Dokument(pydantic.BaseModel):
    avdelningar: Avdelningar
    beteckning: str | None
    datum: t.Annotated[
        datetime.date | None,
        pydantic.BeforeValidator(split_space_take_first),
        pydantic.BeforeValidator(ensure_none_if_empty),
    ]
    debattnamn: str | None = None
    dok_id: str
    # doktyp: t.Annotated[str, pydantic.BeforeValidator(ensure_string)]
    # dokument_url_html: pydantic.HttpUrl
    # dokument_url_text: pydantic.HttpUrl
    dokumentnamn: str | None = None
    # dokumentstatus_url_xml: pydantic.HttpUrl
    hangar_id: str
    html: str | None = None
    # htmlformat: str | None
    images: str | None = None
    metadata: str | None = None
    # mottagare: str | None
    nummer: str | None
    organ: str | None
    pretext: str | None = None
    publicerad: t.Annotated[
        datetime.datetime | None, pydantic.BeforeValidator(ensure_none_if_empty)
    ]
    # relaterat_id: str | None
    rm: str | None
    rubriker: str | None = None
    slutnummer: str | None
    # source: str | None
    # sourceid: str | None
    status: str | None
    subtitel: str | None
    subtyp: str | None
    # systemdatum: datetime.datetime
    systemdatum: t.Annotated[
        datetime.datetime | None,
        pydantic.BeforeValidator(split_space_take_first),
        pydantic.BeforeValidator(ensure_none_if_empty),
    ]
    tempbeteckning: str | None
    text: str | None = None
    titel: str | None
    typ: t.Annotated[DokumentTyp | None, pydantic.BeforeValidator(ensure_none_if_empty)]
    typrubrik: str | None = None
    utskottsforslag_url_xml: str | None = None

    model_config = pydantic.ConfigDict(extra="forbid")

    def get_rm(self) -> str:
        return self.rm or "missing"

    def get_typ_short_name(self) -> str:
        return self.typ.short_name() if self.typ else "missing"

    def get_typ_long_name(self) -> str:
        return self.typ.long_name() if self.typ else "missing"
