import datetime as dt

import pydantic


class PathText(pydantic.BaseModel):
    path: str
    text: str


class SfsMetadata(pydantic.BaseModel):
    sfs_nummer: str = pydantic.Field(alias="sfs-nummer")
    publicerad: dt.date
    title: str
    paths: list[PathText]
