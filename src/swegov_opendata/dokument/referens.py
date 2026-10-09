import typing as t

import pydantic

from swegov_opendata import shared


class Referens(pydantic.BaseModel):
    hangar_id: str | None = None
    referenstyp: str | None
    uppgift: str | None
    ref_dok_id: str
    ref_dok_typ: str
    ref_dok_rm: str | None
    ref_dok_bet: str | None
    ref_dok_titel: str | None = pydantic.Field(default="")
    ref_dok_subtitel: str | None
    ref_dok_subtyp: str | None = None
    ref_dok_dokumentnamn: str | None = None


class DokReferens(pydantic.BaseModel):
    referens: t.Annotated[list[Referens], pydantic.BeforeValidator(shared.ensure_list)]
