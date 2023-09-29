from pathlib import Path
from typing import Tuple

import pytest
from lxml import etree

from swegov_opendata.preprocess.preprocess_xml import clean_text, preprocess_xml
from tests.etree_asserts import assert_elem_equal


@pytest.fixture(name="example1")
def fixture_example1(assets_path: Path) -> Tuple[str, Path]:
    example1_path = assets_path / "example1.xml"
    return (example1_path.read_text(encoding="utf-8"), example1_path)


def test_preprocess_xml(example1: Tuple[str, Path]):
    output = preprocess_xml(example1[0], example1[1])
    actual = etree.fromstring(output)

    expected_path = example1[1].with_stem(f"{example1[1].stem}.expected")
    expected_source = expected_path.read_text(encoding="utf-8")
    expected = etree.fromstring(expected_source)

    assert_elem_equal(actual, expected)
