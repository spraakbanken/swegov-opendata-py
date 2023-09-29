from pathlib import Path
from typing import Tuple

import pytest
from lxml import etree

from swegov_opendata.preprocess.preprocess_sfs import preprocess_json
from tests.integration.preprocess_xml_integration_test import assert_elem_equal


@pytest.fixture(name="example1")
def fixture_example1(assets_path: Path) -> Tuple[str, Path]:
    example1_path = assets_path / "sfs-1976-257.json"
    return (example1_path.read_text(encoding="utf-8"), example1_path)


def test_preprocess_sfs_json(example1: Tuple[str, Path]):
    actual_source = preprocess_json(example1[0])
    # print(f"{actual_source}")
    actual = etree.fromstring(actual_source)
    # print_tree(actual)
    expected_path = example1[1].with_name(f"{example1[1].stem}.expected.xml")
    expected_source = expected_path.read_text(encoding="utf-8")
    expected = etree.fromstring(expected_source)

    assert_elem_equal(actual, expected)
