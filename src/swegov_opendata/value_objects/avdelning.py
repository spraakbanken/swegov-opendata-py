import pydantic


class Avdelning(pydantic.BaseModel):
    text: str


class Avdelningar(pydantic.BaseModel):
    avdelning: list[str]
