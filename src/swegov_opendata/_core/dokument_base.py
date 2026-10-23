import datetime
import typing as t

import pydantic

from swegov_opendata import validators
from swegov_opendata.value_objects.dokument_typ import DokumentTyp


class DokumentBase(pydantic.BaseModel):
    beteckning: str | None
    datum: t.Annotated[
        datetime.date | None,
        pydantic.BeforeValidator(validators.split_space_take_first),
        pydantic.BeforeValidator(validators.ensure_none_if_empty),
    ]
    debattnamn: str | None = None
    dok_id: str
    dokumentnamn: str | None = None
    hangar_id: str
    html: str | None = None
    images: str | None = None
    metadata: str | None = None
    nummer: str | None
    organ: str | None
    pretext: str | None = None
    publicerad: t.Annotated[
        datetime.datetime | None, pydantic.BeforeValidator(validators.ensure_none_if_empty)
    ]
    rm: str | None
    rubriker: str | None = None
    slutnummer: str | None
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
