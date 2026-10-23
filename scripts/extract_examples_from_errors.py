#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic",
# ]
# ///
import datetime
import re
import sys
from argparse import ArgumentParser
from pathlib import Path

import pydantic


class StackRecord(pydantic.BaseModel):
    file: str
    line: int
    function: str
    text: str

    model_config = pydantic.ConfigDict(extra="forbid")


class Err(pydantic.BaseModel):
    message: str
    name: str
    stack: list[StackRecord]

    model_config = pydantic.ConfigDict(extra="forbid")


class BunyanRecord(pydantic.BaseModel):
    v: int
    name: str
    msg: str
    level: int
    levelname: str
    hostname: str
    pid: int
    time: datetime.datetime
    target: str
    line: int
    file: str
    extra: dict[str, str]
    err: Err | None = None

    model_config = pydantic.ConfigDict(extra="forbid")


def main() -> None:
    args = _parse_args()
    filename = Path(args.filename)
    output_dir = Path(args.output_dir or "assets")
    print(filename, output_dir)

    from_counter = 0
    tom_counter = 0
    with filename.open(encoding="utf-8") as fp:
        for lineno, line in enumerate(fp):
            try:
                bunyan_record = BunyanRecord.model_validate_json(line)
            except pydantic.ValidationError as exc:
                print(f"Error on line {lineno}: {exc}", file=sys.stderr)
                raise
            rel_path = bunyan_record.extra.get("rel_path", "")
            if rel_path.startswith("dokumentlista"):
                if m := re.search(r"doktyp=(\w+)", bunyan_record.extra["rel_path"]):
                    doktyp = m.group(1).lower()
                else:
                    doktyp = "doktyp"
                if m := re.search(r"from=(\d+-\d+-\d+)", bunyan_record.extra["rel_path"]):
                    from_ = m.group(1)
                else:
                    from_counter += 1
                    from_ = f"{from_counter}"
                if m := re.search(r"tom=(\d+-\d+-\d+)", bunyan_record.extra["rel_path"]):
                    tom = m.group(1)
                else:
                    tom_counter += 1
                    tom = f"{tom_counter}"
                output_path = output_dir / f"dokumentlista-{doktyp}-from-{from_}-tom-{tom}.json"
                output_path.write_text(bunyan_record.model_dump_json())
            elif rel_path.startswith("dataset"):
                rel_path = (
                    bunyan_record.extra["rel_path"]
                    .removesuffix(".json.zip")
                    .replace("/", "-")
                    .lower()
                )
                dok_id = bunyan_record.extra["zippath"].removesuffix(".json")
                output_path = output_dir / f"{rel_path}-{dok_id}.json"
                output_path.write_text(bunyan_record.model_dump_json())
            elif rel_path.startswith("dokument/"):
                dok_id = bunyan_record.extra["rel_path"].replace("/", "-").lower()
                output_path = output_dir / f"{dok_id}"
                output_path.write_text(bunyan_record.model_dump_json())
            else:
                print(bunyan_record.model_dump())


def _parse_args():
    cli = _create_cli()
    return cli.parse_args()


def _create_cli():
    parser = ArgumentParser(prog=_prog_name(__file__))
    parser.add_argument("filename")
    parser.add_argument("-o", "--output_dir", default="assets")
    return parser


def _prog_name(file_name: str) -> str:
    return file_name.split("/")[-1]


if __name__ == "__main__":
    main()
