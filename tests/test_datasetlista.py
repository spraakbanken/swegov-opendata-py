import re
from pathlib import Path

import pydantic
import pytest
from syrupy.assertion import SnapshotAssertion

from swegov_opendata.datasetlista import Dataset, DatasetLista


@pytest.mark.parametrize(
    "source",
    [
        "<random></random>",
        "<datasetlista><random></random></datasetlista>",
    ],
)
def test_datasetlista_from_xml_raises_value_error_on_bad_xml(
    source,
    snapshot: SnapshotAssertion,
) -> None:
    with pytest.raises(ValueError) as exc_info:
        DatasetLista.from_xml(source)
    assert exc_info.value == snapshot


PYDANTIC_VERSION: re.Pattern = re.compile(r"(https://errors.pydantic.dev/\d).\d\d(/v/[a-z]+)")


@pytest.mark.parametrize(
    "source",
    [
        "<datasetlista><dataset></dataset></datasetlista>",
        "<datasetlista><dataset><format>json</format></dataset></datasetlista>",
        "<datasetlista><dataset><format>json</format><url>/dataset/perons.json.zip</url></dataset></datasetlista>",
    ],
)
def test_datasetlista_from_xml_raises_validation_error_on_bad_xml(
    source,
    snapshot_json: SnapshotAssertion,
) -> None:
    with pytest.raises(pydantic.ValidationError) as exc_info:
        DatasetLista.from_xml(source)
    actual_value = exc_info.value
    error_msgs = []
    for error in actual_value.errors():
        error["url"] = re.sub(PYDANTIC_VERSION, r"\1.xx\2", error["url"])
        print(error)
        error_msgs.append(error)
    assert error_msgs == snapshot_json


@pytest.mark.parametrize("filename", ["assets/dataset-2026-10-27.xml"])
def test_dataset_parses_ok(filename: str, snapshot_json: SnapshotAssertion) -> None:
    actual_content = Path(filename).read_text()
    actual = Dataset.from_xml(actual_content)

    actual_json = actual.model_dump()
    assert actual_json == snapshot_json


@pytest.mark.parametrize("filename", ["assets/datasetlista-2026-10-27.xml"])
def test_datasetlista_parses_ok(filename: str, snapshot_json: SnapshotAssertion) -> None:
    actual_content = Path(filename).read_text()
    actual = DatasetLista.from_xml(actual_content)

    actual_json = actual.model_dump()
    assert actual_json == snapshot_json
