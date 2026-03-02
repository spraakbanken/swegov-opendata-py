import re
import sys
from dataclasses import dataclass
from pathlib import Path

import structlog
from tqdm import tqdm

from swegov_opendata.core.component.preprocess import preprocess_rd, preprocess_sfs
from swegov_opendata.core.component.sparv.config import make_corpus_config
from swegov_opendata.corpusinfo import corpusinfo

logger = structlog.get_logger(name=__name__)


@dataclass()
class PreprocessCorpuraOption:
    input: Path
    output: Path
    processed_files: dict


def preprocess_corpura(corpora: str | list[str], options: PreprocessCorpuraOption) -> None:
    logger.debug("preprocess corpora")

    if isinstance(corpora, list):
        preprocess_rd_corpora(corpora, options)
    if isinstance(corpora, str) and corpora == "sfs":
        preprocess_sfs_corpus(options)


def preprocess_sfs_corpus(options: PreprocessCorpuraOption) -> None:
    logger.debug("preprocess SFS corpus from %s", options.input)

    for year in options.input.iterdir():
        logger.debug("found path: %s", year)
        preprocess_sfs.build_sparv_source(
            year,
            options.output / "sfs" / "source" / year.stem,
        )


def preprocess_rd_corpora(corpora: list[str], options: PreprocessCorpuraOption) -> None:
    log = logger.bind(output=str(options.output), input=str(options.input))
    options.output /= options.input.stem
    log.debug("preprocess RD corpora from %s, outputting to %s", options.input, options.output)
    dataset_dir = find_dataset_dir(options.input) or options.input

    log = log.bind(dir=str(dataset_dir))
    if dataset_dir is options.input:
        log.warning("did not find 'output', using input as is")
    preprocess_dataset_dir(
        options.input,
        corpora=corpora,
        output=options.output,
        processed_files=options.processed_files,
    )


def find_dataset_dir(dir_path: Path) -> Path | None:

    for path in dir_path.iterdir():
        if path.name == "dataset":
            return path
    for path in dir_path.iterdir():
        if path.is_dir() and (path := find_dataset_dir(path)):
            return path
    return None


def preprocess_dataset_dir(
    dataset_dir: Path, *, corpora: list[str], output: Path, processed_files: dict
) -> None:
    # print(f"{dataset_dir=}")
    log = logger.bind(dir=str(dataset_dir))
    for path in tqdm(
        list(dataset_dir.iterdir()), desc=f"Reading dir '{dataset_dir}", file=sys.stdout
    ):
        # print(f"{path=}")
        log = log.bind(path=str(path))
        if path.is_dir():
            preprocess_dataset_dir(
                path, corpora=corpora, output=output, processed_files=processed_files
            )
        elif path.is_file() and path.suffix == ".zip":
            if prefix := _find_prefix(path.stem):
                prefix = prefix.strip()
                prefix = prefix.replace(" ", "+")
                # print(f"{prefix=}, {path=}")
                if corpus := corpusinfo(prefix):
                    if corpora and corpus["id"] not in corpora:
                        print(f"skipping corpus '{corpus['id']}' ...", file=sys.stderr)
                        continue
                    # print(f"  processing {path} ...", file=sys.stderr)
                    corpus_source_base = Path(path.stem).stem
                    corpus_source_dir = output / corpus["id"] / "source" / corpus_source_base
                    make_corpus_config(
                        corpus["id"],
                        corpus["names"],
                        corpus["descriptions"],
                        output / corpus["id"],
                    )
                    if str(path) not in processed_files:
                        processed_files[str(path)] = {}
                    # processed_files_path = processed_files[str(path)]
                    preprocess_rd.build_sparv_source(
                        path,
                        corpus_source_dir=corpus_source_dir,
                        processed_files=processed_files,
                    )
                    # raise RuntimeError("stop")
                else:
                    log.warning("Found no corpus with prefix '%s', skipping ...", prefix)
                    continue
                # raise RuntimeError(f"Found no corpus with prefix '{prefix}'")
            # print(f"{path=}")
            # return


PREFIX = re.compile(r"([a-zA-ZåäöÅÄÖ -]+)-\d{4}")


def _find_prefix(s: str) -> str | None:
    if prefix := PREFIX.match(s):
        return prefix[1]
    return None
