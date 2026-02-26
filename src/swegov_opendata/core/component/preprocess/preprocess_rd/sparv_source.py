import gzip
import logging
import zipfile
from pathlib import Path

import trafilatura
from json_arrays import jsonlib
from orjson import JSONDecodeError

from swegov_opendata.core.component.sparv.xml_source_writer import XmlSourceWriter

logger = logging.getLogger(__name__)


def build_sparv_source(path: Path, corpus_source_dir: Path):
    corpus_source_dir.mkdir(parents=True, exist_ok=True)
    source_writer = XmlSourceWriter(target_dir=corpus_source_dir)

    logger.debug("reading a file", extra={"file_path": path})
    zipf = zipfile.ZipFile(path)
    for i, zippath in enumerate(zipf.filelist):
        if i > 0:
            break
        filecontents = zipf.read(zippath)
        filecontents = filecontents.decode("utf-8-sig")
        try:
            dokumentstatus_page = jsonlib.loads(filecontents)
        except JSONDecodeError as exc:
            logger.error(
                "failed to decode JSON from '%s' in the zipfile '%s'",
                zippath.filename,
                path,
                extra={"filecontents": filecontents},
            )
            raise RuntimeError("failed to read JSON") from exc
        dokumentstatus = dokumentstatus_page["dokumentstatus"]
        # logger.debug("dokumentstatus=%s", dokumentstatus)
        dokument = dokumentstatus["dokument"]
        html = dokument["html"]
        logger.debug(
            "html[..]=%s", html[115000:160000], extra={"zippath": zippath.filename, "path": path}
        )
        document = trafilatura.extract_with_metadata(
            html, output_format="xml", include_formatting=True, favor_recall=True
        )
        logger.warning("document=%s", document)
        return
        # if xmlstring is None:
        #     logger.warning("failed to extract html from '%s'", zippath)
        # else:
        #     logger.debug("xmlstring=%s", xmlstring)
        #     source_writer.write(xmlstring.encode("utf-8"))
    source_writer.flush()


def read_text(path: Path) -> str:
    if path.suffix == ".gz":
        with gzip.open(path, mode="rt", encoding="utf-8") as file:
            return file.read()
    return path.read_text(encoding="utf-8")
