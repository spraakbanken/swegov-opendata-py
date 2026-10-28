import datetime as dt

import pydantic


class SfsMetadata(pydantic.BaseModel):
    sfs_nummer: str = pydantic.Field(alias="sfs-nummer")
    publicerad: dt.date
    title: str
