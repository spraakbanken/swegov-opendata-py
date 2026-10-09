import datetime
import typing as t

import pydantic

from swegov_opendata import shared


class Anforande(pydantic.BaseModel):
    anf_beteckning: str | None
    anf_datum: datetime.datetime
    anf_hangar_id: t.Annotated[int | None, pydantic.BeforeValidator(shared.ensure_int_opt)]
    anf_id: str | None = None
    anf_klockslag: str | None
    anf_nummer: str
    anf_rm: str | None
    anf_sekunder: int
    anf_text: str | None = None
    anf_typ: str | None
    anf_video_id: str
    datumtid: datetime.datetime
    debatt_id: str | None = None
    debatt_titel: str | None = None
    debatt_typ: str | None = None
    dok_beteckning: str | None = None
    dok_id: str | None = None
    dok_intressent: str | None = None
    intressent_id: str | None = None
    kon: str | None = None
    parent_id: str | None = None
    parti: str | None = None
    startpos: int | None = None
    systemdatum: datetime.datetime | None = None
    talare: str | None
    talare_kort: str | None = None
    tumnagel: t.Annotated[list[str] | None, pydantic.BeforeValidator(shared.ensure_list_opt)] = (
        None
    )
    tumnagel_mini: str | None = None
    tumnagel_liten: str | None = None
    tumnagel_medium: str | None = None
    tumnagel_stor: str | None = None
    video_id: str | None
    video_url: str
    videostatus: int | None = None
    voteringspunkt: str | None = None

    model_config = pydantic.ConfigDict(extra="forbid")


class Debatt(pydantic.BaseModel):
    anforande: t.Annotated[list[Anforande], pydantic.BeforeValidator(shared.ensure_list)]

    model_config = pydantic.ConfigDict(extra="forbid")
