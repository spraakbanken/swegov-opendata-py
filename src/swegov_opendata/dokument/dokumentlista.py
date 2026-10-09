import datetime
import typing as t

import pydantic

from swegov_opendata import shared
from swegov_opendata.dokument.dokument import DokumentTyp


class Fil(pydantic.BaseModel):
    typ: str
    namn: str
    storlek: int
    url: str

    model_config = pydantic.ConfigDict(extra="forbid")


class FilBilaga(pydantic.BaseModel):
    fil: t.Annotated[list[Fil] | None, pydantic.BeforeValidator(shared.ensure_list_opt)]

    model_config = pydantic.ConfigDict(extra="forbid")


class SokData(pydantic.BaseModel):
    titel: str
    undertitel: str
    soktyp: str | None
    statusrad: str
    brodsmula: str | None
    parti_kod: str | None
    parti_namn: str | None
    parti_website_url: str | None
    parti_website_namn: str | None
    parti_epost: str | None
    parti_telefon: str | None
    parti_telefontider: str | None
    parti_logotyp_img_id: str | None
    parti_logotyp_img_url: str | None
    parti_logotyp_img_alt: str | None
    parti_mandat: str | None
    kalenderprio: str | None

    model_config = pydantic.ConfigDict(extra="forbid")


class DokumentListaDokument(pydantic.BaseModel):
    ardometyp: str | None
    audio: str | None
    avdelning: str
    avdelningar: shared.Avdelningar | None
    beredningsdag: str | None
    beslutad: str | None
    beslutsdag: str | None
    beteckning: str | None
    database: str
    datum: datetime.date
    debatt: str | None
    debattdag: str | None
    debattgrupp: str | None
    debattnamn: str
    debattsekunder: str | None
    dok_id: str
    dokintressent: str | None
    doktyp: str
    dokument_url_html: str
    dokument_url_text: str
    dokumentformat: str | None
    dokumentnamn: str
    domain: str
    filbilaga: FilBilaga | None
    id: str
    inlamnad: str | None
    justeringsdag: str | None
    kall_id: str | None
    kalla: str | None
    klockslag: str | None
    lang: str | None
    motionstid: str | None
    notis: str | None
    notisrubrik: str
    nummer: str | None
    organ: str | None
    plats: str | None
    # TODO this field can contain date (2018-03-07) and datetime (2016-02-11 15:28:15)
    publicerad: str
    rddata: str | None
    rdrest: str | None
    relaterat_id: str | None
    relurl: str | None
    reservationer: str | None
    rm: str
    score: str
    slutdatum: str | None
    sokdata: SokData
    status: str | None
    struktur: str | None
    subtyp: str
    summary: str | None
    systemdatum: datetime.datetime
    tempbeteckning: str | None
    tilldelat: str | None
    titel: str
    traff: int
    typ: DokumentTyp
    undertitel: str | None
    url: str | None
    video: str | None

    model_config = pydantic.ConfigDict(extra="forbid")

    def get_rm(self) -> str:
        return self.rm or "missing"

    def get_typ_short_name(self) -> str:
        return self.typ.short_name() if self.typ else "missing"

    def get_typ_long_name(self) -> str:
        return self.typ.long_name() if self.typ else "missing"


class DokumentLista(pydantic.BaseModel):
    d_dt: str = pydantic.Field(alias="@dDt")
    d_pre: str = pydantic.Field(alias="@dPre")
    d_r: str = pydantic.Field(alias="@dR")
    d_sol: str = pydantic.Field(alias="@dSol")
    datum: datetime.datetime = pydantic.Field(alias="@datum")
    ms: str = pydantic.Field(alias="@ms")
    nasta_sida: str | None = pydantic.Field(alias="@nasta_sida")
    q: str = pydantic.Field(alias="@q")
    sida: int = pydantic.Field(alias="@sida")
    sidor: int = pydantic.Field(alias="@sidor")
    traff_fran: int = pydantic.Field(alias="@traff_fran")
    traff_till: int = pydantic.Field(alias="@traff_till")
    traffar: int = pydantic.Field(alias="@traffar")
    varning: str | None = pydantic.Field(None, alias="@varning")
    version: str = pydantic.Field(alias="@version")
    facettlista: str | None
    dokument: list[DokumentListaDokument]

    model_config = pydantic.ConfigDict(extra="forbid")


class DokumentListaPage(pydantic.BaseModel):
    dokumentlista: DokumentLista

    model_config = pydantic.ConfigDict(extra="forbid")
