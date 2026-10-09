import pydantic


class Votering(pydantic.BaseModel):
    rm: str
    beteckning: str
    hangar_id: str
    votering_id: str
    punkt: str
    namn: str
    intressent_id: str
    parti: str
    valkrets: str | None
    valkretsnummer: str
    iort: str | None
    rost: str
    avser: str
    votering: str
    banknummer: str
    fornamn: str
    efternamn: str
    kon: str
    fodd: str
    datum: str | None

    model_config = pydantic.ConfigDict(extra="forbid")


class DokVotering(pydantic.BaseModel):
    votering: list[Votering]


class DokVoteringPage(pydantic.BaseModel):
    dokvotering: DokVotering | None
