#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic",
# ]
# ///
import datetime as dt
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
    time: dt.datetime
    target: str
    line: int
    file: str
    err: Err | None = None

    model_config = pydantic.ConfigDict(extra="allow")


def main() -> None:
    args = _parse_args()
    filename = Path(args.filename)
    output_dir = Path(args.output_dir or "assets")
    print(filename, output_dir)

    from_counter = 0
    tom_counter = 0
    lineno = 0
    unknown_errors = 0
    with filename.open(encoding="utf-8") as fp:
        for lineno, line in enumerate(fp, start=1):
            try:
                bunyan_record = BunyanRecord.model_validate_json(line)
            except pydantic.ValidationError as exc:
                print(f"Error on line {lineno}: {exc}", file=sys.stderr)
                raise
            bunyan_record_extra: dict[str, str] = bunyan_record.__pydantic_extra__["extra"]  # ty: ignore[not-subscriptable]
            rel_path = bunyan_record_extra.get("rel_path", "")
            if rel_path.startswith("dokumentlista"):
                if m := re.search(r"doktyp=(\w+)", bunyan_record_extra["rel_path"]):
                    doktyp = m.group(1).lower()
                else:
                    doktyp = "doktyp"
                if m := re.search(r"from=(\d+-\d+-\d+)", bunyan_record_extra["rel_path"]):
                    from_ = m.group(1)
                else:
                    from_counter += 1
                    from_ = f"{from_counter}"
                if m := re.search(r"tom=(\d+-\d+-\d+)", bunyan_record_extra["rel_path"]):
                    tom = m.group(1)
                else:
                    tom_counter += 1
                    tom = f"{tom_counter}"
                output_path = output_dir / f"dokumentlista-{doktyp}-from-{from_}-tom-{tom}.json"
                output_path.write_text(bunyan_record.model_dump_json())
            elif rel_path.startswith("dataset"):
                if "Extracted file is empty" in bunyan_record.msg:
                    continue
                rel_path = (
                    bunyan_record_extra["rel_path"]
                    .removesuffix(".json.zip")
                    .replace("/", "-")
                    .lower()
                )
                dok_id = bunyan_record_extra["zippath"].removesuffix(".json")
                output_path = output_dir / f"{rel_path}-{dok_id}.json"
                output_path.write_text(bunyan_record.model_dump_json())
            elif rel_path.startswith("dokument/"):
                dok_id = bunyan_record_extra["rel_path"].replace("/", "-").lower()
                output_path = output_dir / f"{dok_id}"
                output_path.write_text(bunyan_record.model_dump_json())
            else:
                url = (
                    bunyan_record_extra["url"]
                    .removeprefix("http:")
                    .removeprefix("https:")
                    .removeprefix("//")
                    .removeprefix("data.riksdagen.se/")
                    .replace("/", "-")
                )
                output_path = output_dir / url
                output_path = output_path.with_suffix(".json")

                output_path.write_text(bunyan_record.model_dump_json())
                unknown_errors += 1
    print(f"Read {lineno} examples")
    print(f"  added {lineno - unknown_errors} to '{output_dir}'")

    print(f"  found {unknown_errors} examples")


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
