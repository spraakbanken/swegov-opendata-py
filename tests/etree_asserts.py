import itertools

from swegov_opendata.lxml_extension.cleaning import clean_text_opt
from swegov_opendata.lxml_extension.printing import debug_tree


def assert_elem_equal(left, right):
    # print(f"- {left.tag=}\n-{right.tag=}")
    # print(f"- {left.text=}\n-{right.text=}")
    assert left.tag == right.tag, f"left.tag ({left.tag}) != right.tag ({right.tag})"

    if trimmed_text := clean_text_opt(right.text):
        assert (
            left.text == trimmed_text
        ), f"<{left.tag}> left.text != trimmed_text '{left.text}' != '{trimmed_text}'"
    else:
        assert (
            left.text is None or len(left.text.strip()) == 0
        ), f"<{left.tag}> {left.text} is None or {len(left.text.strip())} != 0"
    if trimmed_tail := clean_text_opt(right.tail):
        assert (
            left.tail == trimmed_tail
        ), f"<{left.tag}> left.tail != trimmed_tail '{left.tail}' != '{trimmed_tail}'"
    else:
        assert (
            left.tail is None or len(left.tail.strip()) == 0
        ), f"<{left.tag}> left.tail != right.tail '{left.tail}' != '{right.tail}'"
    assert dict(left.attrib) == dict(
        right.attrib
    ), f"'<{left.tag}> {left.attrib} != {right.attrib}"
    # assert len(left) == len(
    #     right
    # ), f"<{left.tag} len(left) != len(right) [{len(left)} != {len(right)}]"
    for c1, c2 in itertools.zip_longest(left, right):
        if c1 is None and c2 is None:
            assert False, "both is None"
        assert c1 is not None, f"right is longer c2={debug_tree(c2)}"
        assert c2 is not None, f"left is longer c1={debug_tree(c1)}"
        assert_elem_equal(c1, c2)


def assert_elem_equal_no_trim(left, right):
    # print(f"- {left.tag=}\n-{right.tag=}")
    # print(f"- {left.text=}\n-{right.text=}")
    assert left.tag == right.tag, f"left.tag ({left.tag}) != right.tag ({right.tag})"

    if trimmed_text := right.text:
        assert (
            left.text == trimmed_text
        ), f"<{left.tag}> left.text != trimmed_text '{left.text}' != '{trimmed_text}'"
    else:
        assert (
            left.text is None or len(left.text.strip()) == 0
        ), f"<{left.tag}> {left.text} is None or {len(left.text.strip())} != 0"
    if trimmed_tail := right.tail:
        assert (
            left.tail == trimmed_tail
        ), f"<{left.tag}> left.tail != trimmed_tail '{left.tail}' != '{trimmed_tail}'"
    else:
        assert (
            left.tail is None or len(left.tail.strip()) == 0
        ), f"<{left.tag}> left.tail != right.tail '{left.tail}' != '{right.tail}'"
    assert dict(left.attrib) == dict(
        right.attrib
    ), f"'<{left.tag}> {left.attrib} != {right.attrib}"
    # assert len(left) == len(
    #     right
    # ), f"<{left.tag} len(left) != len(right) [{len(left)} != {len(right)}]"
    for c1, c2 in itertools.zip_longest(left, right):
        if c1 is None and c2 is None:
            assert False, "both is None"
        assert c1 is not None, f"right is longer c2={debug_tree(c2)}"
        assert c2 is not None, f"left is longer c1={debug_tree(c1)}"
        assert_elem_equal_no_trim(c1, c2)
