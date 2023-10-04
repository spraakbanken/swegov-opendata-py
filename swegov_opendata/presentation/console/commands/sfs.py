from pathlib import Path

import typer
from typing_extensions import Annotated

from swegov_opendata.core.component.preprocess.preprocess_corpura import (
    PreprocessCorpuraOption,
    preprocess_corpura,
)

app = typer.Typer()


@app.command()
def preprocess(
    input_: Annotated[
        Path, typer.Argument(metavar="INPUT", exists=True, dir_okay=True)
    ],
    output: Annotated[Path, typer.Argument(dir_okay=True, file_okay=False)],
):
    print("sfs preprocess")
    preprocess_corpura("sfs", PreprocessCorpuraOption(input=input_, output=output))
