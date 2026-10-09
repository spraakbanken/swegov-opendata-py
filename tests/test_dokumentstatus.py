import json
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from swegov_opendata.dokument.dokument import DokumentStatusPage


def test_utskottsdokument_2006_2009_gua19e5(snapshot_json: SnapshotAssertion) -> None:
    actual_path = Path("assets/utskottsdokument-2006-2009-gua19e5-contents.json")
    actual_data = actual_path.read_text()
    actual = DokumentStatusPage.model_validate_json(actual_data)

    assert actual.model_dump(by_alias=True) == snapshot_json


@pytest.mark.parametrize(
    "file_name",
    [
        "assets/dokument-bet-1980-1989-GD01SkU31.json",
        "assets/dokument-bet-2002-2005-gq01ku12.json",
        "assets/dokument-bet-2002-2005-GT01NU16.json",
        "assets/dokument-bet-2010-2013-gz01fiu23.json",
        "assets/dokument-bet-2018-2021-h601ku14.json",
        "assets/dokument-bet-2022-2025-ha01cu4.json",
        "assets/dokument-eun-2000-2009-gv0l27.json",
        "assets/dokument-eun-2010-2013-h1a42c21fb.json",
        "assets/dokument-eun-2014-2017-h2a431a908.json",
        "assets/dokument-eun-2014-2017-H20L1.json",
        "assets/dokument-eun-2018-2021-h60l1.json",
        "assets/dokument-f-lista-2000-2009-gv0i26.json",
        "assets/dokument-fpm-2000-2009-gr06fpm1.json",
        "assets/dokument-fpm -2010-2013-gy06fpm1.json",
        "assets/dokument-fpm-2014-2017-H206FPM1.json",
        "assets/dokument-fpm-2018-2021-h606fpm1.json",
        "assets/dokument-fpm-2022-2025-ha06fpm1.json",
        "assets/dokument-frsrdg-1998-2001-gm04er1.json",
        "assets/dokument-frsrdg-1998-2001-go04rr12.json",
        "assets/dokument-ip-1998-2001-gn10370.json",
        "assets/dokument-ip-2006-2009-gu10665.json",
        "assets/dokument-ip-2014-2017-H210999.json",
        "assets/dokument-kammakt-2010-2013-gyc101503f83-8d76-420d-9c3b-2e2c52d7a2d2.json",
        "assets/dokument-kammakt-2010-2013-gyc120101005ro.json",
        "assets/dokument-kammakt-2010-2013-h0c110188tt.json",
        "assets/dokument-kammakt-2014-2017-h2c10005cf43-fcc4-436a-a7d4-112b03d70bee.json",
        "assets/dokument-kammakt-2014-2017-h2c120150314oh.json",
        "assets/dokument-kammakt-2018-2021-h6c100481cf4-6666-4e69-b983-f82883c4d56b.json",
        "assets/dokument-kammakt-2018-2021-h6c120180918ad.json",
        "assets/dokument-kammakt-2022-2025-hac10060b75d-1ba5-4ada-95c4-6cf9d3f07bb9.json",
        "assets/dokument-kammakt-2022-2025-hac120221017zz.json",
        "assets/dokument-kom-2010-2014-h0b6109.json",
        "assets/dokument-kom-2020--h8b6111.json",
        "assets/dokument-mot-1998-2001-gm02a1.json",
        "assets/dokument-mot-2002-2005-gq02a1.json",
        "assets/dokument-mot-2006-2009-gu021781.json",
        "assets/dokument-mot-2010-2013-gy02a1.json",
        "assets/dokument-mot-2014-2017-h2021.json",
        "assets/dokument-mot-2014-2017-H2022673.json",
        "assets/dokument-mot-2018-2021-h6021.json",
        "assets/dokument-mot-2022-2025-ha021.json",
        "assets/dokument-prop-2018-2021-h6031.json",
        "assets/dokument-riksdagens diarium-2022-2025-had21.json",
        "assets/dokument-rskr-2000-2009-gs0k001.json",
        "assets/dokument-rskr-2010-2013-gy0k10.json",
        "assets/dokument-rskr-2014-2017-H20K1.json",
        "assets/dokument-rskr-2018-2021-h60k1.json",
        "assets/dokument-rskr-2022-2025-ha0k1.json",
        "assets/dokument-samtr-2010-2013-gyc220101004zz3.json",
        "assets/dokument-samtr-2010-2013-h1c220140218ou3.json",
        "assets/dokument-samtr-2018-2021-h6c220181114pk2.json",
        "assets/dokument-samtr-2014-2017-H2C220141031ko1.json",
        "assets/dokument-samtr-2022-2025-hac220230111se1.json",
        "assets/dokument-samtr-2022-2025-hdc220251028ss2.json",
        "assets/dokument-skriftliga frågor-2002-2005-gq1142.json",
        "assets/dokument-skriftliga frågor-2022-2025-hb111007.json",
        "assets/dokument-utredningar-1961--emb2ju51.json",
        "assets/dokument-utskottsdokument-2014-2017-H2A12EADB8.json",
    ],
)
def test_dokumentstatuspage_errors(file_name: str, snapshot_json: SnapshotAssertion) -> None:
    actual_path = Path(file_name)
    with actual_path.open() as file:
        actual_dict = json.load(file)
        actual_contents = actual_dict["extra"]["filecontents"]
        if isinstance(actual_contents, str):
            actual = DokumentStatusPage.deserialize_from_str(actual_contents)
        else:
            actual = DokumentStatusPage.model_validate(actual_contents)
        assert actual.model_dump(by_alias=True) == snapshot_json()
