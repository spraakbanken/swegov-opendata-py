import pathlib

import structlog

from swegov_opendata.core.component.formatting import LazyStr

logger = structlog.get_logger(name=__name__)


def make_corpus_config(corpus_id: str, name, descr, path):
    """Write Sparv corpus config file for sub corpus."""
    config_file = path / "config.yaml"
    log = logger.bind(corpus_id=corpus_id, corpus_config=str(config_file))
    if config_file.is_file():
        log.debug("file exists skipping")
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
    pathlib.Path(config_file).write_text(config_content)
    log.info(
        "Config for corpus '%s' written",
        corpus_id,
        extra={"config_file": LazyStr(str, config_file)},
    )
