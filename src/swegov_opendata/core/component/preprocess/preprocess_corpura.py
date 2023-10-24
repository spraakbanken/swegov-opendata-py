import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from swegov_opendata.core.component.preprocess import preprocess_sfs

logger = logging.getLogger(__name__)


@dataclass()
class PreprocessCorpuraOption:
    input: Path  # noqa: A003
    output: Path


def preprocess_corpura(
    corpora: Union[str, list[str]], options: PreprocessCorpuraOption
) -> None:
    logger.debug("preprocess corpora")

    if isinstance(corpora, list):
        logger.error("not impl")
        raise NotImplementedError("")
    elif isinstance(corpora, str) and corpora == "sfs":
        preprocess_sfs_corpus(options)


def preprocess_sfs_corpus(options: PreprocessCorpuraOption) -> None:
    logger.debug("preprocess SFS corpus from %s", options.input)

    for year in options.input.iterdir():
        logger.debug("found path: %s", year)
        preprocess_sfs.build_sparv_source(
            year,
            options.output / "sfs" / "source" / year.stem,
        )
