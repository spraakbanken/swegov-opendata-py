from swegov_opendata.sfs import SfsMetadata


def test_sfs_metadata_from_aliases() -> None:
    kwargs = {
        "sfs-nummer": "2018:2107",
        "publicerad": "2018-12-27",
        "title": "Förordning om ändring i förordningen (1998:928) om bygde- och fiskeavgifter (pdf 372 kB)",
    }

    SfsMetadata(**kwargs)
