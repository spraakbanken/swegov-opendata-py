import datetime
import enum
import typing as t
from pathlib import Path

import pydantic

from swegov_opendata.dokument.aktivitet import DokAktivitet
from swegov_opendata.dokument.bilaga import DokBilaga
from swegov_opendata.dokument.debatt import Debatt
from swegov_opendata.dokument.forslag import (
    DokForslag,
    DokMotForslag,
    DokUtskottsForslag,
)
from swegov_opendata.dokument.intressent import DokIntressent
from swegov_opendata.dokument.media import WebbMedia
from swegov_opendata.dokument.referens import DokReferens
from swegov_opendata.dokument.uppgift import DokUppgift

_DOKUMENT_TYP_MAP: dict[str, str] = {
    "bet": "betänkande",
    "dir": "kommittéedirektiv",
    "ds": "departementsserien",
    "eundok": "utskottsdokument",
    "f-lista": "föredragningslista",
    "fr": "skriftlig fråga",
    "frs": "svar på skriftlig fråga",
    "frsrdg": "framställningar",
    "ip": "interpellation",
    "kf-lista": "kallelser och föredragningslistor",
    "KOM": "EU-förslag",
    "komm": "kommittéeberättelser",
    "prop": "proposition",
    "prot": "protokoll",
    "rfr": "rapporter från riksdagen",
    "rir": "riksrevisionens granskningsrapporter",
    "rskr": "riksdagsskrivelse",
    "sou": "statens offentliga utredningar",
    "t-lista": "talarlista",
    "urf": "utredningar från Riksdagsförvaltningen",
    "utskottsdokument": "utskottsdokument",
    "yttr": "yttrande",
}


class DokumentTyp(str, enum.Enum):
    Bet = "bet"
    Diarie = "diarie"
    Dir = "dir"
    Ds = "ds"
    EuDokument = "eu-dokument"
    Eunbil = "eunbil"
    Eundok = "eundok"
    FLista = "f-lista"
    Fpm = "fpm"
    Fr = "fr"
    Frs = "frs"
    Frsrdg = "frsrdg"
    Ip = "ip"
    Kalakt = "kalakt"
    Kammakt = "kammakt"
    KfLista = "kf-lista"
    Kom = "KOM"
    Komm = "komm"
    Mot = "mot"
    Prop = "prop"
    Prot = "prot"
    Rfr = "rfr"
    Rir = "rir"
    Rskr = "rskr"
    Samtr = "samtr"
    Sfs = "sfs"
    Skrsam = "skrsam"
    Sou = "sou"
    TLista = "t-lista"
    Urf = "urf"
    Utskottsdokument = "utskottsdokument"
    Uttag = "uttag"
    Yttr = "yttr"

    @classmethod
    def _missing_(cls, value) -> t.Self:
        for member in cls:
            if member.value == value.lower():
                return member
        raise ValueError(f"Unknown value '{value}'.")

    def short_name(self) -> str:
        return self.value

    def long_name(self) -> str:
        return _DOKUMENT_TYP_MAP.get(self.value) or self.value


def split_space_take_first(value: t.Any) -> t.Any:
    if isinstance(value, str):
        return "" if not value else value.split()[0]
    return value


def ensure_none_if_empty(value: t.Any) -> t.Any:
    if isinstance(value, str):
        return None if value == "" else value
    return value


def ensure_string(value: t.Any) -> t.Any:
    def _ensure_str(v: t.Any) -> str:
        return v if isinstance(v, str) else str(v)

    if isinstance(value, list):
        if len(value) == 0:
            return ""
        return _ensure_str(value[0])
    return _ensure_str(value)


class Dokument(pydantic.BaseModel):
    beteckning: str | None
    datum: t.Annotated[
        datetime.date | None,
        pydantic.BeforeValidator(split_space_take_first),
        pydantic.BeforeValidator(ensure_none_if_empty),
    ]
    debattnamn: str | None = None
    dok_id: str
    doktyp: t.Annotated[str, pydantic.BeforeValidator(ensure_string)]
    dokument_url_html: pydantic.HttpUrl
    dokument_url_text: pydantic.HttpUrl
    dokumentnamn: str | None = None
    dokumentstatus_url_xml: pydantic.HttpUrl
    hangar_id: str
    html: str | None = None
    htmlformat: str | None
    images: str | None = None
    metadata: str | None = None
    mottagare: str | None
    nummer: str | None
    organ: str | None
    pretext: str | None = None
    publicerad: t.Annotated[
        datetime.datetime | None, pydantic.BeforeValidator(ensure_none_if_empty)
    ]
    relaterat_id: str | None
    rm: str | None
    rubriker: str | None = None
    slutnummer: str | None
    source: str | None
    sourceid: str | None
    status: str | None
    subtitel: str | None
    subtyp: str | None
    # systemdatum: datetime.datetime
    systemdatum: t.Annotated[
        datetime.datetime | None,
        pydantic.BeforeValidator(split_space_take_first),
        pydantic.BeforeValidator(ensure_none_if_empty),
    ]
    tempbeteckning: str | None
    text: str | None = None
    titel: str | None
    typ: t.Annotated[DokumentTyp | None, pydantic.BeforeValidator(ensure_none_if_empty)]
    typrubrik: str | None = None
    utskottsforslag_url_xml: str | None = None

    model_config = pydantic.ConfigDict(extra="forbid")

    def get_rm(self) -> str:
        return self.rm or "missing"

    def get_typ_short_name(self) -> str:
        return self.typ.short_name() if self.typ else "missing"

    def get_typ_long_name(self) -> str:
        return self.typ.long_name() if self.typ else "missing"


class DokumentStatus(pydantic.BaseModel):
    debatt: Debatt | None = None
    dokaktivitet: DokAktivitet | None = None
    dokbilaga: DokBilaga | None = None
    dokforslag: DokForslag | None = None
    dokintressent: DokIntressent | None = None
    dokmotforslag: DokMotForslag | None = None
    dokreferens: DokReferens | None = None
    dokument: Dokument
    dokuppgift: DokUppgift | None = None
    dokutskottsforslag: DokUtskottsForslag | None = None
    webbmedia: WebbMedia | None = None

    model_config = pydantic.ConfigDict(extra="forbid")


class DokumentStatusPage(pydantic.BaseModel):
    dokumentstatus: DokumentStatus | None

    @classmethod
    def deserialize_from_str(cls, src: str | bytes | bytearray) -> "DokumentStatusPage":
        try:
            return DokumentStatusPage.model_validate_json(src)
        except pydantic.ValidationError as exc:
            print(f"error type: '{exc.errors()[0]['type']}'")
            exc_msg = exc.errors()[0]["msg"]
            print(f"error msg: '{exc_msg}'")
            print(f"{exc=}")
            if exc.errors()[0]["type"] != "json_invalid":
                raise
                column = int(exc_msg.split()[-1])
                print(f"{src[column - 50:column + 50]=}")
            new_src: str = src if isinstance(src, str) else src.decode("utf-8")
            new_src = (
                new_src.replace("{/* RESERVATIONSTEXT */}", r'""')
                .replace("/* RESERVATIONSTEXT */", "")
                .replace('\\"', "TEMPSLASH")
                .replace(r"\"", '"')
                .replace("TEMPSLASH", r"\"")
                .replace(r"\\r\\n", r"\r\n")
                .replace('"p":}', '"p":""}')
            )
            try:
                return DokumentStatusPage.model_validate_json(new_src)
            except pydantic.ValidationError as exc:
                dt = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%dT%H%M%S")
                Path(f"new_src-{dt}.json").write_text(new_src)
                print(f"error type: '{exc.errors()[0]['type']}'")
                exc_msg = exc.errors()[0]["msg"]
                print(f"error msg: '{exc_msg}'")
                print(f"{exc=}")
                if exc.errors()[0]["type"] != "json_invalid":
                    raise
                column = int(exc_msg.split()[-1])
                print(f"{new_src[column - 50:column + 50]=}")
                # new_src = src.replace("{/* RESERVATIONSTEXT */}", "")
                raise
