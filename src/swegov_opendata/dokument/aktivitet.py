import datetime
import typing as t

import pydantic

from swegov_opendata import shared


class Aktivitet(pydantic.BaseModel):
    datum: datetime.datetime
    hangar_id: str | None = None
    kod: str
    namn: str
    status: str | None
    ordning: str
    process: str | None

    model_config = pydantic.ConfigDict(extra="forbid")


class DokAktivitet(pydantic.BaseModel):
    aktivitet: t.Annotated[list[Aktivitet], pydantic.BeforeValidator(shared.ensure_list)]

    model_config = pydantic.ConfigDict(extra="forbid")
