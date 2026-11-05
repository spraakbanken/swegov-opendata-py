import datetime as dt

import pydantic


class Votering(pydantic.BaseModel):
    rm: str
    beteckning: str
    hangar_id: int
    votering_id: str
    punkt: int
    namn: str
    intressent_id: str
    parti: str
    valkrets: str | None
    valkretsnummer: int
    iort: str | None
    rost: str
    avser: str
    votering: str
    banknummer: int
    fornamn: str
    efternamn: str
    kon: str
    fodd: int
    datum: dt.datetime | None

    model_config = pydantic.ConfigDict(extra="forbid")


class DokVotering(pydantic.BaseModel):
    votering: list[Votering]


class DokVoteringPage(pydantic.BaseModel):
    dokvotering: DokVotering | None
