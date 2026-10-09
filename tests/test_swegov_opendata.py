from syrupy.assertion import SnapshotAssertion

from swegov_opendata.dokument.forslag import Forslag


def test_forslag_minimum_data(snapshot_json: SnapshotAssertion) -> None:
    actual = Forslag(
        behandlas_i=None,
        beteckning=None,
        kammarbeslutstyp=None,
        kammaren=None,
        lydelse="",
        lydelse2=None,
        nummer="123",
        utskottet=None,
    )

    assert actual.model_dump() == snapshot_json
