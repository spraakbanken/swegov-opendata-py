import datetime
import typing as t

import pydantic

from swegov_opendata import shared


class Uppgift(pydantic.BaseModel):
    systemdatum: datetime.datetime | None = None
    dok_id: str | None = None
    kod: str
    namn: str
    text: str | None

    model_config = pydantic.ConfigDict(extra="forbid")


class DokUppgift(pydantic.BaseModel):
    uppgift: t.Annotated[list[Uppgift], pydantic.BeforeValidator(shared.ensure_list)]

    model_config = pydantic.ConfigDict(extra="forbid")
