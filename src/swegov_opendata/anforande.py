import datetime as dt

import pydantic


class Anforande(pydantic.BaseModel):
    dok_hangar_id: int
    dok_id: str
    dok_titel: str
    dok_rm: str
    dok_nummer: int
    dok_datum: dt.datetime
    avsnittsrubrik: str
    underrubrik: str | None = None
    kammaraktivitet: str | None
    anforande_id: str
    anforande_nummer: int
    talare: str
    parti: str | None
    anforandetext: str
    intressent_id: str
    rel_dok_id: str | None
    replik: bool
    systemdatum: dt.datetime

    model_config = pydantic.ConfigDict(extra="forbid")


class AnforandePage(pydantic.BaseModel):
    anforande: Anforande
