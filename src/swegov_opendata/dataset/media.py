import datetime
import typing as t

import pydantic

from swegov_opendata import shared


class Media(pydantic.BaseModel):
    dok_id: str
    url: str
    videofileurl: str
    audiofileurl: str | None
    downloadurl: str | None
    thumbnailurl: str | None
    debateurl: str
    debattsekunder: int
    debatt_rm: str | None
    debatt_typ: str | None
    dok_beteckning: str | None
    datum: datetime.datetime | None
    videostatus: int
    source: str
    inspelningstyp: str
    systemdatum: datetime.datetime

    model_config = pydantic.ConfigDict(extra="forbid")


class WebbMedia(pydantic.BaseModel):
    media: t.Annotated[list[Media], pydantic.BeforeValidator(shared.ensure_list)]

    model_config = pydantic.ConfigDict(extra="forbid")
