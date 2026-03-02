import json
from pathlib import Path
from typing import Annotated

import typer

from swegov_opendata.core.component.preprocess.preprocess_corpura import (
    PreprocessCorpuraOption,
    preprocess_corpura,
)
from swegov_opendata.corpusinfo import ALL_CORPORA

app = typer.Typer()
PROCESSED_JSON: Path = Path("process_rd.json")


@app.command()
def preprocess(
    input_: Annotated[Path, typer.Argument(metavar="INPUT", exists=True, dir_okay=True)],
    output: Annotated[Path, typer.Argument(dir_okay=True, file_okay=False)],
):
    processed_rd_json = {}
    if PROCESSED_JSON.is_file():
        with PROCESSED_JSON.open() as f:
            processed_rd_json = json.load(f)
    try:
        preprocess_corpura(
            ALL_CORPORA,
            PreprocessCorpuraOption(
                input=input_, output=output, processed_files=processed_rd_json
            ),
        )
    finally:
        with PROCESSED_JSON.open("w") as f:
            json.dump(processed_rd_json, f)
