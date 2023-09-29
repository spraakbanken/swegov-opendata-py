import json
from pathlib import Path


def write_xml(text, xmlpath):
    """Wrap 'text' in a file tag and save as 'xmlpath'."""
    corpus_source_dir = Path(xmlpath).parent
    corpus_source_dir.mkdir(exist_ok=True, parents=True)
    text = b"<file>\n" + text + b"\n</file>"
    with open(xmlpath, "wb") as f:
        f.write(text)
    print(f"  File {xmlpath} written")


def write_json(data, filepath):
    """Write json data to filepath."""
    dirpath = Path(filepath).parent
    dirpath.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
