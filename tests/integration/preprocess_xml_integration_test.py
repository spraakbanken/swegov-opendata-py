from pathlib import Path
from typing import Tuple

import pytest
from lxml import etree

from swegov_opendata.preprocess import clean_text, preprocess_xml


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


def assert_elem_equal(left, right):
    print(f"- {left.tag=}\n-{right.tag=}")
    print(f"- {left.text=}\n-{right.text=}")
    assert left.tag == right.tag
    if trimmed_text := clean_text(right.text):
        assert left.text == trimmed_text
    else:
        assert left.text.strip() == right.text.strip()
    assert left.tail == right.tail
    assert dict(left.attrib) == dict(right.attrib)
    assert len(left) == len(right)
    for c1, c2 in zip(left, right):  # noqa: B905
        assert_elem_equal(c1, c2)
