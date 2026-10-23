import logging

import pydantic

from swegov_opendata.dokument.dokument import Dokument
from swegov_opendata.value_objects.aktivitet import DokAktivitet
from swegov_opendata.value_objects.bilaga import DokBilaga
from swegov_opendata.value_objects.debatt import Debatt
from swegov_opendata.value_objects.forslag import (
    DokForslag,
    DokMotForslag,
    DokUtskottsForslag,
)
from swegov_opendata.value_objects.intressent import DokIntressent
from swegov_opendata.value_objects.media import WebbMedia
from swegov_opendata.value_objects.referens import DokReferens
from swegov_opendata.value_objects.uppgift import DokUppgift

logger = logging.getLogger(__name__)


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
    dokumentuppgift: DokUppgift | None = None
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
            exc_type = exc.errors()[0]["type"]
            exc_msg = exc.errors()[0]["msg"]
            logger.debug(
                "Validation failed. %s...",
                "Retrying after further processing"
                if exc_type == "json_invalid"
                else "Re-raising error",
                extra={
                    "error.type": exc_type,
                    "error.msg": exc_msg,
                    "error.raw": str(exc),
                },
            )
            if exc_type != "json_invalid":
                raise
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
                exc_type = exc.errors()[0]["type"]
                exc_msg = exc.errors()[0]["msg"]
                logger.error(
                    "Validation failed again. Re-raising error",
                    extra={
                        "error.type": exc_type,
                        "error.msg": exc_msg,
                        "error.raw": str(exc),
                        "orig_src": src.decode("utf-8")
                        if isinstance(src, (bytearray, bytes))
                        else src,
                        "new_src": new_src,
                    },
                )

                raise
