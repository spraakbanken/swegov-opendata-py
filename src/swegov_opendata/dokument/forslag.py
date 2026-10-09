import typing as t

import pydantic

from swegov_opendata import shared


class Forslag(pydantic.BaseModel):
    hangar_id: str | None = None
    nummer: int
    beteckning: str | None
    lydelse: t.Annotated[str, pydantic.BeforeValidator(shared.ensure_str)]
    lydelse2: str | None
    utskottet: str | None
    kammaren: str | None
    behandlas_i: str | None
    behandlas_i_punkt: str | None = None
    kammarbeslutstyp: str | None
    intressent: str | None = None
    avsnitt: str | None = None
    grundforfattning: str | None = None
    andringsforfattning: str | None = None

    model_config = pydantic.ConfigDict(extra="forbid")


class DokForslag(pydantic.BaseModel):
    forslag: t.Annotated[list[Forslag], pydantic.BeforeValidator(shared.ensure_list)]

    model_config = pydantic.ConfigDict(extra="forbid")


class MotForslag(pydantic.BaseModel):
    nummer: int
    rubrik: str | None = None
    forslag: str | None = None
    partier: str | None
    typ: str
    utskottsforslag_punkt: int
    id: str | None = None


class DokMotForslag(pydantic.BaseModel):
    motforslag: t.Annotated[list[MotForslag], pydantic.BeforeValidator(shared.ensure_list)]


class UtskottsForslag(pydantic.BaseModel):
    punkt: int
    rubrik: str | None
    forslag: str | None = None
    forslag_del2: str | None = None
    beteckning: str | None = None
    beslut: str | None = None
    beslutstyp: str | None = None
    motforslag_nummer: int
    motforslag_partier: str | None = None
    votering_id: str | None = None
    votering_sammanfattning_html: dict[str, t.Any] | None = None
    votering_ledamot_url_xml: str | None = None
    votering_url_xml: str | None = None
    rm: str
    bet: str
    vinnare: str | None = None
    voteringskrav: str | None = None
    beslutsregelkvot: str | None = None
    beslutsregelparagraf: str | None = None
    punkttyp: str | None = None


class DokUtskottsForslag(pydantic.BaseModel):
    utskottsforslag: t.Annotated[
        list[UtskottsForslag], pydantic.BeforeValidator(shared.ensure_list)
    ]
