import typing as t

import pydantic


class Forslag(pydantic.BaseModel):
    hangar_id: str | None = None
    nummer: str
    beteckning: str | None
    lydelse: str = ""
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

    @pydantic.field_validator("lydelse", mode="before")
    @classmethod
    def ensure_str(cls, value: t.Any) -> t.Any:
        if value is None:
            return ""
        return value


class DokForslag(pydantic.BaseModel):
    forslag: list[Forslag]

    @pydantic.field_validator("forslag", mode="before")
    @classmethod
    def ensure_list(cls, value: t.Any) -> t.Any:
        def _create_from_dict(v: t.Any) -> Forslag:
            if isinstance(v, Forslag):
                return v
            return Forslag.model_validate(v)

        if not isinstance(value, list):
            return [_create_from_dict(value)]
        return [_create_from_dict(v) for v in value]
