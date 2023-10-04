from swegov_opendata.preprocess import preprocess_corpora

if __name__ == "__main__":
    # corpora = ["rd-bet", "rd-ds", "rd-eun", "rd-flista", "rd-fpm", "rd-frsrdg", "rd-ip",
    #            "rd-kammakt", "rd-kom", "rd-mot", "rd-ovr", "rd-prop", "rd-prot", "rd-rskr",
    #            "rd-samtr", "rd-skfr", "rd-sou", "rd-tlista", "rd-utr", "rd-utsk", "rd-yttr"]

    preprocess_corpora(
        corpora=["rd-fpm"],
        skip_files=[],
        #  testfile="h7a2eun10p.xml"
    )

    # with open("gr091.xml") as f:
    #     xml_string = f.read()
    #     xmlstring = preprocess_xml(xml_string, "test", testfile=True)
    #     write_xml(xmlstring, "test.xml")
