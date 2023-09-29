from swegov_opendata.preprocess import clean_text


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
