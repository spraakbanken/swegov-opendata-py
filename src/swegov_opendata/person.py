import datetime as dt
import typing as t

import pydantic

from swegov_opendata import validators


class Uppdrag(pydantic.BaseModel):
    organ_kod: str
    sortering: t.Annotated[int | None, pydantic.BeforeValidator(validators.ensure_none_if_empty)]
    organ_sortering: int
    uppgift_en: str
    uppgift: str
    tom: t.Annotated[dt.date | None, pydantic.BeforeValidator(validators.ensure_none_if_empty)]
    from_: dt.date = pydantic.Field(alias="from")
    typ: str
    status: str
    ordningsnummer: int
    roll_kod_en: str
    roll_kod: str

    model_config = pydantic.ConfigDict(extra="forbid")


class PersonUppdrag(pydantic.BaseModel):
    uppdrag: list[Uppdrag]

    model_config = pydantic.ConfigDict(extra="forbid")


class Uppgift(pydantic.BaseModel):
    typ: str
    uppgift: str
    kod: str

    model_config = pydantic.ConfigDict(extra="forbid")


class PersonUppgift(pydantic.BaseModel):
    uppgift: list[Uppgift]

    model_config = pydantic.ConfigDict(extra="forbid")
