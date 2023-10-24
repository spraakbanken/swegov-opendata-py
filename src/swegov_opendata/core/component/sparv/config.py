def make_corpus_config(corpus_id, name, descr, path):
    """Write Sparv corpus config file for sub corpus."""
    config_file = path / "config.yaml"
    if config_file.is_file():
        return
    path.mkdir(parents=True, exist_ok=True)
    config_content = (
        "parent: ../config.yaml\n"
        "\n"
        "metadata:\n"
        f"  id: {corpus_id}\n"
        "  name:\n"
        f"    swe: Riksdagens öppna data: {name}\n"
        "  description:\n"
        f"    swe: {descr}\n"
    )
    with open(config_file, "w") as f:
        f.write(config_content)
    print(f"  Config {config_file} written")
