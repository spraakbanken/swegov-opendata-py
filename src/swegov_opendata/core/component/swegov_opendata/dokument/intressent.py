import typing as t

import pydantic


class Intressent(pydantic.BaseModel, frozen=True):
    roll: str
    namn: str
    partibet: str | None
    ordning: str
    intressent_id: str | None


class DokIntressent(pydantic.BaseModel):
    intressent: list[Intressent]

    @pydantic.field_validator("intressent", mode="before")
    @classmethod
    def ensure_list(cls, value: t.Any) -> t.Any:
        def _create_from_dict(v: t.Any) -> Intressent:
            if isinstance(v, Intressent):
                return v
            return Intressent.model_validate(v)

        if not isinstance(value, list):
            return [_create_from_dict(value)]
        return [_create_from_dict(v) for v in value]
