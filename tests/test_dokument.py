import json
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from swegov_opendata.dokument_status import DokumentStatusPage


@pytest.mark.parametrize(
    "file_name",
    [
        "assets/dokument-sfs-1981-369.json",
    ],
)
def test_dokumentstatuspage_errors(file_name: str, snapshot_json: SnapshotAssertion) -> None:
    actual_path = Path(file_name)
    with actual_path.open() as file:
        actual_dict = json.load(file)
        actual_contents = actual_dict["extra"]["contents"]
        content_path = Path("tmp") / actual_path
        content_path.parent.mkdir(parents=True, exist_ok=True)
        content_path.write_text(actual_contents)
        if isinstance(actual_contents, str):
            actual = DokumentStatusPage.deserialize_from_str(actual_contents)
        else:
            actual = DokumentStatusPage.model_validate(actual_contents)
        assert actual.model_dump(by_alias=True) == snapshot_json()
