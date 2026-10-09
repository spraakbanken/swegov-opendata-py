import json
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from swegov_opendata.dokument.dokumentlista import DokumentListaPage


def test_dokumentlista_1(snapshot_json: SnapshotAssertion) -> None:
    actual_path = Path("assets/dokumentlista-contents.json")
    actual_data = actual_path.read_text()
    actual = DokumentListaPage.model_validate_json(actual_data)

    assert actual.model_dump(by_alias=True) == snapshot_json


@pytest.mark.parametrize(
    "file_name",
    [
        "assets/dokumentlista-sfs-from-1880-01-01-tom-1900-12-31.json",
        "assets/dokumentlista-sfs-from-1901-01-01-tom-1920-12-31.json",
        "assets/dokumentlista-sfs-from-1921-01-01-tom-1940-12-31.json",
        "assets/dokumentlista-sfs-from-1941-01-01-tom-1960-12-31.json",
        "assets/dokumentlista-sfs-from-1961-01-01-tom-1980-12-31.json",
        "assets/dokumentlista-sfs-from-1981-01-01-tom-2000-12-31.json",
        "assets/dokumentlista-sfs-from-2001-01-01-tom-2020-12-31.json",
        "assets/dokumentlista-sfs-from-2021-01-01-tom-2026-12-31.json",
    ],
)
def test_dokumentlistapage_errors(file_name: str, snapshot_json: SnapshotAssertion) -> None:
    actual_path = Path(file_name)
    with actual_path.open() as file:
        actual_dict = json.load(file)
        actual_contents = actual_dict["extra"]["contents"]
        if isinstance(actual_contents, str):
            actual = DokumentListaPage.model_validate_json(actual_contents)
        else:
            actual = DokumentListaPage.model_validate(actual_contents)
        assert actual.model_dump(by_alias=True) == snapshot_json()
