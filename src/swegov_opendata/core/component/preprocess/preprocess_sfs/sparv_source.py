import gzip
import logging
from pathlib import Path

from swegov_opendata.core.component.preprocess.preprocess_sfs import sfs_json
from swegov_opendata.core.component.sparv.xml_source_writer import XmlSourceWriter

logger = logging.getLogger(__name__)


def build_sparv_source(path: Path, corpus_source_dir: Path):
    corpus_source_dir.mkdir(parents=True, exist_ok=True)
    source_writer = XmlSourceWriter(target_dir=corpus_source_dir)
    for file_path in path.iterdir():
        logger.debug("reading a file", extra={"file_path": file_path})
        filecontents = read_text(file_path)
        xmlstring = sfs_json.preprocess_json(filecontents)
        source_writer.write(xmlstring)
    source_writer.flush()


def read_text(path: Path) -> str:
    if path.suffix == ".gz":
        with gzip.open(path, mode="rt", encoding="utf-8") as file:
            return file.read()
    return path.read_text(encoding="utf-8")
