from pathlib import Path

import pytest
from lxml import etree

from swegov_opendata.core.component.preprocess.preprocess_sfs import build_sparv_source
from swegov_opendata.lxml_extension import print_tree
from tests.integration.preprocess_xml_integration_test import assert_elem_equal


@pytest.fixture(name="example")
def fixture_example(assets_path: Path) -> Path:
    return assets_path / "cks6riksg"


@pytest.fixture(name="target_dir")
def fixture_target_dir(assets_path: Path) -> Path:
    return assets_path / "gen"


def test_preprocess_sfs_json(example: Path, target_dir: Path):
    corpus_source_dir = target_dir / "example"
    print("act")

    build_sparv_source(example, corpus_source_dir)

    actual_path = corpus_source_dir / "example-1.xml"
    actual_source = actual_path.read_text(encoding="utf-8")
    actual_tree = etree.parse(actual_path)
    actual = actual_tree.getroot()
    # actual_source = preprocess_json(example[0])
    # # print(f"{actual_source}")
    # actual = etree.fromstring(actual_source)
    # print_tree(actual)
    # clean_element(actual)
    print("assert")
    print_tree(actual, verbose=True)
    expected_path = example.with_name(f"{example.stem}.expected.xml")
    expected_source = expected_path.read_text(encoding="utf-8")
    expected = etree.fromstring(expected_source)
    print("assert:expected")
    print_tree(expected, verbose=True)
    assert_elem_equal(actual, expected)
