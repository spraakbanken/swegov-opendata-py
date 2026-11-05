from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from swegov_opendata.anforande import AnforandePage


@pytest.mark.parametrize(
    "file_name",
    [
        "assets/anforande-2026-27-HE091-1.json",
        "assets/anforande-2026-27-HE097-23.json",
    ],
)
def test_dokumentstatuspage_errors(file_name: str, snapshot_json: SnapshotAssertion) -> None:
    actual_path = Path(file_name)
    actual_contents = actual_path.read_text()

    actual = AnforandePage.model_validate_json(actual_contents)
    assert actual.model_dump(by_alias=True) == snapshot_json()
