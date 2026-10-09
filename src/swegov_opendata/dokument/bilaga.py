import enum
import typing as t

import pydantic

from swegov_opendata import shared


class FilTyp(str, enum.Enum):
    Doc = "doc"
    Docx = "docx"
    Htm = "htm"
    Pdf = "pdf"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def _missing_(cls, value) -> t.Self:
        for member in cls:
            if member.value == value.lower():
                return member
        raise ValueError("Unknown value '{value}'")


class Bilaga(pydantic.BaseModel):
    dok_id: str
    titel: str | None = None
    subtitel: str | None
    filnamn: str
    filstorlek: str
    filtyp: FilTyp
    fil_url: pydantic.HttpUrl

    model_config = pydantic.ConfigDict(extra="forbid")


class DokBilaga(pydantic.BaseModel):
    bilaga: t.Annotated[list[Bilaga], pydantic.BeforeValidator(shared.ensure_list)]

    model_config = pydantic.ConfigDict(extra="forbid")
