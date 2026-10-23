import enum
import typing as t

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


class DokumentTyp(enum.StrEnum):
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
