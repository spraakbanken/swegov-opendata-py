import typing as t

import pydantic


class Uppgift(pydantic.BaseModel):
    dok_id: str | None = None
    kod: str
    namn: str
    systemdatum: str | None = None
    text: str | None


class DokUppgift(pydantic.BaseModel):
    uppgift: list[Uppgift]

    @pydantic.field_validator("uppgift", mode="before")
    @classmethod
    def ensure_list(cls, value: t.Any) -> t.Any:
        def _create_uppgift_from_dict(v: t.Any) -> Uppgift:
            if isinstance(v, Uppgift):
                return v
            return Uppgift.model_validate(v)

        if not isinstance(value, list):
            return [_create_uppgift_from_dict(value)]
        return [_create_uppgift_from_dict(v) for v in value]
