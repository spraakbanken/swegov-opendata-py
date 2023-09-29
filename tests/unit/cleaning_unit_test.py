from swegov_opendata.lxml_extension.cleaning import clean_text


def test_clean_test():
    # source = "1985:458   Denna förordning"
    source = "11 §\r\n\r\n   Föreskrifter för verkställighet"
    expected = "11 § Föreskrifter för verkställighet"

    actual = clean_text(source)

    assert actual == expected
