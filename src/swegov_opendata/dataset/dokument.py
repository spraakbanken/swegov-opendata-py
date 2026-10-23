import typing as t

import pydantic

from swegov_opendata import validators
from swegov_opendata._core.dokument_base import DokumentBase


class Dokument(DokumentBase):
    doktyp: t.Annotated[str, pydantic.BeforeValidator(validators.ensure_string)]
    dokument_url_html: pydantic.HttpUrl
    dokument_url_text: pydantic.HttpUrl
    dokumentstatus_url_xml: pydantic.HttpUrl
    htmlformat: str | None
    mottagare: str | None
    relaterat_id: str | None
    source: str | None
    sourceid: str | None

    model_config = pydantic.ConfigDict(extra="forbid")

    def get_rm(self) -> str:
        return self.rm or "missing"

    def get_typ_short_name(self) -> str:
        return self.typ.short_name() if self.typ else "missing"

    def get_typ_long_name(self) -> str:
        return self.typ.long_name() if self.typ else "missing"
