import typing as t

import pydantic

from swegov_opendata import shared


class Intressent(pydantic.BaseModel):
    roll: str | None
    namn: str | None
    partibet: str | None
    intressent_id: str | None
    ordning: str

    model_config = pydantic.ConfigDict(extra="forbid")


class DokIntressent(pydantic.BaseModel):
    intressent: t.Annotated[list[Intressent], pydantic.BeforeValidator(shared.ensure_list)]
