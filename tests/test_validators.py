import typing as t

import pytest
from syrupy.assertion import SnapshotAssertion

from swegov_opendata import validators


@pytest.mark.parametrize("value", [None, "", 1, [], [None], [1], ["", "one", "one"]])
def test_ensure_str_if_list_only_one_unique_value(
    value: t.Any, snapshot: SnapshotAssertion
) -> None:
    actual = validators.ensure_str_if_list_only_one_unique_value(value)
    assert actual == snapshot


@pytest.mark.parametrize("value", [["", "one", "two"]])
def test_ensure_str_if_list_only_one_unique_value_raises_value_error(
    value: t.Any, snapshot: SnapshotAssertion
) -> None:
    with pytest.raises(ValueError) as exc_info:
        validators.ensure_str_if_list_only_one_unique_value(value)
    assert exc_info.value == snapshot


@pytest.mark.parametrize("value", [None, "", 1, [], [None], [""], [1], ["one", "two"]])
def test_ensure_str_if_list_take_first(value: t.Any, snapshot: SnapshotAssertion) -> None:
    actual = validators.ensure_str_if_list_take_first(value)
    assert actual == snapshot
