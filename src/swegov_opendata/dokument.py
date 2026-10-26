import datetime
import typing as t

import pydantic

from swegov_opendata import validators
from swegov_opendata.value_objects.avdelning import Avdelningar
from swegov_opendata.value_objects.dokument_typ import DokumentTyp


class Dokument(pydantic.BaseModel):
    avdelningar: Avdelningar | None = None
    beteckning: str | None
    datum: t.Annotated[
        datetime.date | None,
        pydantic.BeforeValidator(validators.split_space_take_first),
        pydantic.BeforeValidator(validators.ensure_none_if_empty),
    ]
    debattnamn: str | None = None
    dok_id: str
    doktyp: t.Annotated[
        str, pydantic.BeforeValidator(validators.ensure_str_if_list_take_first)
    ] = ""
    dokument_url_html: pydantic.HttpUrl | None = None
    dokument_url_text: pydantic.HttpUrl | None = None
    dokumentstatus_url_xml: pydantic.HttpUrl | None = None
    dokumentnamn: str | None = None
    hangar_id: str
    html: str | None = None
    htmlformat: str | None = None
    images: str | None = None
    metadata: str | None = None
    mottagare: str | None = None
    nummer: str | None
    organ: str | None
    pretext: str | None = None
    publicerad: t.Annotated[
        datetime.datetime | None, pydantic.BeforeValidator(validators.ensure_none_if_empty)
    ]
    relaterat_id: str | None = None
    rm: str | None
    rubriker: str | None = None
    slutnummer: str | None
    source: str | None = None
    sourceid: str | None = None
    status: str | None
    subtitel: str | None
    subtyp: str | None
    systemdatum: t.Annotated[
        datetime.datetime | None,
        pydantic.BeforeValidator(validators.split_space_take_first),
        pydantic.BeforeValidator(validators.ensure_none_if_empty),
    ]
    tempbeteckning: str | None
    text: str | None = None
    titel: str | None
    typ: t.Annotated[
        DokumentTyp | None, pydantic.BeforeValidator(validators.ensure_none_if_empty)
    ]
    typrubrik: str | None = None
    utskottsforslag_url_xml: str | None = None

    model_config = pydantic.ConfigDict(extra="forbid")
