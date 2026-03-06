from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from swegov_opendata.core.component.preprocess.preprocess_rd.rd_json import (
    preprocess_json,
)
from swegov_opendata.core.component.preprocess.preprocess_rd.sparv_source import (
    load_metadata_from_path,
)


@pytest.mark.parametrize(
    "filename",
    [
        "assets/Övrigt-2014-2017-h2b51.json",
        "assets/frsrdg-2018-2021-h604er1.json",
        "assets/frsrdg-1990-1997-gk04jo1.json",
        "assets/ip-2002-2005-gq101.json",
    ],
)
def test_preprocess_json(filename: str, snapshot_single: SnapshotAssertion) -> None:
    path = Path(filename)
    filecontents = path.read_bytes()
    metadata_path = path.with_stem("-".join(path.stem.split("-")[:-1])).with_suffix(
        ".metadata.json"
    )
    metadata = load_metadata_from_path(metadata_path)

    if actual_bytes := preprocess_json(filecontents, metadata=metadata):
        actual = actual_bytes.decode("utf-8")
    else:
        actual = None
    assert actual == snapshot_single
