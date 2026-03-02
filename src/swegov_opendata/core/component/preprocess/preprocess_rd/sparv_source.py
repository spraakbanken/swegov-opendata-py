import gzip
import sys
import typing as t
import zipfile
from pathlib import Path

import structlog
from json_arrays import jsonlib
from tqdm import tqdm

from swegov_opendata.core.component.preprocess.preprocess_rd import rd_json
from swegov_opendata.core.component.sparv.xml_source_writer import XmlSourceWriter

logger = structlog.get_logger(name=__name__)


def load_metadata_from_path(path: Path) -> dict[str, t.Any]:
    logger.info("loading metadata from '%s'", path)
    metadata_src = path.read_bytes()
    return jsonlib.loads(metadata_src)


def build_sparv_source(path: Path, corpus_source_dir: Path, processed_files: dict):
    corpus_source_dir.mkdir(parents=True, exist_ok=True)
    processed_zip_dict = processed_files[str(path)]
    source_writer = XmlSourceWriter(
        target_dir=corpus_source_dir, counter=len(processed_zip_dict) + 1
    )

    zipf = zipfile.ZipFile(path)
    log = logger.bind(zipfile=str(path))
    log.info("building sparv source from %s", path, extra={"len_zipf": len(zipf.filelist)})
    metadata_path = path.with_stem(f"{Path(path.stem).stem}").with_suffix(".metadata.json")
    metadata = load_metadata_from_path(metadata_path)
    try:
        for zippath in tqdm(zipf.filelist, desc=f"Reading zip file '{path}'", file=sys.stdout):
            if processed_zip_dict.get(str(zippath.filename)):
                log.debug("skipping file '%s' (already processed)", zippath.filename)
                continue
            log.debug("reading %s from %s", zippath.filename, path)
            # if i > 0:
            #     break
            filecontents = zipf.read(zippath)
            try:
                xmlstring = rd_json.preprocess_json(
                    filecontents, metadata, logger=log.bind(path_in_zipfile=zippath.filename)
                )
            except Exception:
                log.error(
                    "preprocessing json failed, writing file to assets",
                    path_in_zipfile=zippath.filename,
                )
                Path(f"assets/{Path(path.stem).stem}-{zippath.filename}").write_bytes(
                    filecontents
                )
                jsonlib.dump_to_file(metadata, Path("assets") / metadata_path.name)
                raise

            if xmlstring is None:
                log.warning(
                    "failed to extract html, writing file to assets/no-extract",
                    path_in_zipfile=zippath.filename,
                )
                Path(f"assets/no-extract/{Path(path.stem).stem}-{zippath.filename}").write_bytes(
                    filecontents
                )
                jsonlib.dump_to_file(metadata, Path("assets/no-extract") / metadata_path.name)
            else:
                # logger.debug("xmlstring=%s", xmlstring)
                source_writer.write(xmlstring)
                processed_zip_dict[str(zippath.filename)] = str(source_writer.current_path)
            # break
    finally:
        source_writer.flush()


def read_text(path: Path) -> str:
    if path.suffix == ".gz":
        with gzip.open(path, mode="rt", encoding="utf-8") as file:
            return file.read()
    return path.read_text(encoding="utf-8")
