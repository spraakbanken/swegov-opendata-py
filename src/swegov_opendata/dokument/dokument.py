import pydantic

from swegov_opendata._core.dokument_base import DokumentBase
from swegov_opendata.value_objects.avdelning import Avdelningar


class Dokument(DokumentBase):
    avdelningar: Avdelningar

    model_config = pydantic.ConfigDict(extra="forbid")

    def get_rm(self) -> str:
        return self.rm or "missing"

    def get_typ_short_name(self) -> str:
        return self.typ.short_name() if self.typ else "missing"

    def get_typ_long_name(self) -> str:
        return self.typ.long_name() if self.typ else "missing"
