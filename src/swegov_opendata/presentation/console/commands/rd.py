from pathlib import Path
from typing import Annotated

import typer

from swegov_opendata.core.component.preprocess.preprocess_corpura import (
    PreprocessCorpuraOption,
    preprocess_corpura,
)
from swegov_opendata.corpusinfo import ALL_CORPORA

app = typer.Typer()


@app.command()
def preprocess(
    input_: Annotated[Path, typer.Argument(metavar="INPUT", exists=True, dir_okay=True)],
    output: Annotated[Path, typer.Argument(dir_okay=True, file_okay=False)],
):
    print("rd preprocess")
    preprocess_corpura(ALL_CORPORA, PreprocessCorpuraOption(input=input_, output=output))
