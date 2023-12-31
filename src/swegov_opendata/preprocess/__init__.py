"""Script for creating original/xml files for all rd-corpora."""

import json
import re
import zipfile
from pathlib import Path

from swegov_opendata.core.component.sparv.config import make_corpus_config
from swegov_opendata.core.component.sparv.xml_source_writer import XmlSourceWriter
from swegov_opendata.corpusinfo import corpusinfo
from swegov_opendata.lxml_extension.cleaning import clean_text
from swegov_opendata.preprocess import preprocess_xml
from swegov_opendata.serialization import write_json, write_xml

__all__ = ["clean_text"]


# Parsing large XML files:
# http://making-security-measurable.1364806.n2.nabble.com/Parsing-large-9-5mb-XML-files-with-lxml-td7580657.html

RAWDIR = "rawdata"
PROCESSED_JSON = "processed.json"


def preprocess_corpora(corpora=None, skip_files=None, testfile=None):  # noqa: C901
    """Preprocess corpora.

    corpora: List that specifies which corpora (corpus-IDs) to process (default: all)
    skip_files: Zip files which should not be processed.
    testfile: Parse only 'testfile' and output result to 'test.xml'.
    """
    # Get previously processed data
    processed_json = {}
    if Path(PROCESSED_JSON).is_file():
        with open(PROCESSED_JSON) as f:
            processed_json = json.load(f)

    for zippath in Path(RAWDIR).iterdir():
        if zippath.name.startswith(".") or not str(zippath).endswith(".zip"):
            continue

        # Don't process if in 'skip_files'
        if skip_files is not None and zippath.name in skip_files:
            continue

        # Get corpus name
        m = re.match(r"(\S+)-\d{4}-.+", zippath.name)
        if not m:
            raise RuntimeError(f"Don't know how to handle the path '{zippath.name}'")
        prefix = m[1]
        if prefix not in corpusinfo:
            raise RuntimeError(f"File {prefix} seems to be a new corpus!")
        corpus_id, name, descr = corpusinfo[prefix]

        # Process only if in 'corpora'
        if corpora is not None and corpus_id not in corpora:
            continue

        print(f"\nProcessing {zippath}")
        corpus_source_dir = (
            Path("material") / corpus_id / "source" / Path(zippath.stem).stem
        )
        make_corpus_config(corpus_id, name, descr, Path("material") / corpus_id)

        processed_zip_dict = processed_json.get(str(zippath.name), {})
        source_writer = XmlSourceWriter(
            target_dir=corpus_source_dir, counter=len(processed_zip_dict) + 1
        )

        # Iterate through files in zip file
        zipf = zipfile.ZipFile(zippath)
        for zipobj in zipf.filelist:
            # print(zipobj.filename)

            if testfile and zipobj.filename != testfile:
                continue

            # Skip if already processed
            if processed_zip_dict.get(str(zipobj.filename)) and not testfile:
                print(f"  Skipping file '{zipobj.filename}' (already processed)")

            filecontents = zipf.read(zipobj)
            xmlstring = preprocess_xml(
                filecontents, zipobj.filename, testfile=testfile is not None
            )

            if testfile:
                if xmlstring:
                    write_xml(xmlstring, "test.xml")
                exit()
            source_writer.write(xmlstring)

            processed_zip_dict[str(zipobj.filename)] = source_writer.current_filename

        # Save last file
        source_writer.flush()

        if not testfile:
            processed_json[str(zippath.name)] = processed_zip_dict
            write_json(processed_json, PROCESSED_JSON)
