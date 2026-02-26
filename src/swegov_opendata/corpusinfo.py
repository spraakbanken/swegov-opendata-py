import typing as t


class CorpusInfo(t.TypedDict):
    id: str
    names: list[tuple[str, str]]
    descriptions: list[tuple[str, str]]


def corpusinfo(prefix: str) -> CorpusInfo | None:
    for corpus_prefix, corpus_info in _CORPUSINFO.items():
        if corpus_prefix == prefix:
            return corpus_info
    return None


_CORPUSINFO: dict[str, CorpusInfo] = {
    "bet": {
        "id": "rd-bet",
        "names": [("swe", "Riksdagens öppna data: Betänkande")],
        "descriptions": [
            (
                "swe",
                "Utskottens betänkanden och utlåtanden, inklusive rksdagens beslut, en sammanfattning av voteringsresultaten och Beslut i korthet",
            )
        ],
    },
    "ds": {
        "id": "rd-ds",
        "names": [("swe", "Riksdagens öppna data: Departementsserien")],
        "descriptions": [("swe", "Utredningar från regeringens departement")],
    },
    "EUN": {
        "id": "rd-eun",
        "names": [("swe", "Riksdagens öppna data: EUN")],
        "descriptions": [
            (
                "swe",
                "Dokument från EU-nämnden, bland annat möteskallelser, föredragningslistor, protokoll och skriftliga samråd med regeringen",
            ),
            ("eng", "Documents from the Committee on EU Affairs"),
        ],
    },
    "f-lista": {
        "id": "rd-flista",
        "names": [("swe", "Riksdagens öppna data: Föredragningslista")],
        "descriptions": [("swe", "Föredragningslistor för kammarens sammanträden")],
    },
    "fpm": {
        "id": "rd-fpm",
        "names": [("swe", "Riksdagens öppna data: Faktapromemoria")],
        "descriptions": [("swe", "Regeringens faktapromemorior om EU-kommissionens förslag")],
    },
    "frsrdg": {
        "id": "rd-frsrdg",
        "names": [("swe", "Riksdagens öppna data: Framställning/redogörelse")],
        "descriptions": [
            ("swe", "Framställningar och redogörelser från organ som utsetts av riksdagen")
        ],
    },
    "ip": {
        "id": "rd-ip",
        "names": [("swe", "Riksdagens öppna data: Interpellation")],
        "descriptions": [("swe", "Interpellationer från ledamöterna till regeringen")],
    },
    "kammakt": {
        "id": "rd-kammakt",
        "names": [("swe", "Riksdagens öppna data: Kammaraktiviteter")],
        "descriptions": [("swe", "")],
    },
    "kom": {
        "id": "rd-kom",
        "names": [("swe", "Riksdagens öppna data: KOM")],
        "descriptions": [
            ("swe", "EU-kommissionens förslag och redogörelser, så kallade KOM-dokument")
        ],
    },
    "mot": {
        "id": "rd-mot",
        "names": [("swe", "Riksdagens öppna data: Motion")],
        "descriptions": [("swe", "Motioner från riksdagens ledamöter")],
    },
    "prop": {
        "id": "rd-prop",
        "names": [("swe", "Riksdagens öppna data: Proposition")],
        "descriptions": [("swe", "Propositioner och skrivelser från regeringen")],
    },
    "prot": {
        "id": "rd-prot",
        "names": [("swe", "Riksdagens öppna data: Protokoll")],
        "descriptions": [("swe", "Protokoll från kammarens sammanträden")],
    },
    "rskr": {
        "id": "rd-rskr",
        "names": [("swe", "Riksdagens öppna data: Riksdagsskrivelse")],
        "descriptions": [("swe", "Skrivelser från riksdagen till regeringen")],
    },
    "samtr": {
        "id": "rd-samtr",
        "names": [("swe", "Riksdagens öppna data: Sammanträden")],
        "descriptions": [("swe", "")],
    },
    "Skriftliga+frågor": {
        "id": "rd-skfr",
        "names": [("swe", "Riksdagens öppna data: Skriftliga frågor")],
        "descriptions": [
            ("swe", "Skriftliga frågor från ledamöterna till regeringen och svaren på dessa")
        ],
    },
    "sou": {
        "id": "rd-sou",
        "names": [("swe", "Riksdagens öppna data: Statens offentliga utredningar")],
        "descriptions": [("swe", "Olika utredningars förslag till regeringen")],
    },
    "t-lista": {
        "id": "rd-tlista",
        "names": [("swe", "Riksdagens öppna data: Talarlista")],
        "descriptions": [("swe", "Talarlistor för kammarens sammanträden")],
    },
    "Utredningar": {
        "id": "rd-utr",
        "names": [("swe", "Riksdagens öppna data: Utredningar")],
        "descriptions": [
            (
                "swe",
                "Kommittédirektiv och kommittéberättelser för utredningar som regeringen tillsätter",
            )
        ],
    },
    "utskottsdokument": {
        "id": "rd-utsk",
        "names": [("swe", "Riksdagens öppna data: Utskottsdokument")],
        "descriptions": [
            (
                "swe",
                "Dokument från utskotten, bland annat KU-anmälningar, protokoll, verksamhetsberättelser och den gamla dokumentserien Utredningar från riksdagen",
            )
        ],
    },
    "yttr": {
        "id": "rd-yttr",
        "names": [("swe", "Riksdagens öppna data: Yttrande")],
        "descriptions": [("swe", "Utskottens yttranden")],
    },
    "Övrigt": {
        "id": "rd-ovr",
        "names": [("swe", "Riksdagens öppna data: Övrigt")],
        "descriptions": [
            (
                "swe",
                "Dokumentserierna Riksrevisionens granskningsrapporter, Utredningar från Riksdagsförvaltningen och Rapporter från riksdagen samt planeringsdokument, bilagor till dokument och uttag ur riksdagens databaser och de gamla dokumentserierna Utredningar från riksdag",
            )
        ],
    },
}

ALL_CORPORA = [
    "rd-bet",
    "rd-ds",
    "rd-eun",
    "rd-flista",
    "rd-fpm",
    "rd-frsrdg",
    "rd-ip",
    "rd-kammakt",
    "rd-kom",
    "rd-mot",
    "rd-ovr",
    "rd-prop",
    "rd-prot",
    "rd-rskr",
    "rd-samtr",
    "rd-skfr",
    "rd-sou",
    "rd-tlista",
    "rd-utr",
    "rd-utsk",
    "rd-yttr",
]
