import typing as t

import pydantic


def ensure_int_opt(value: t.Any) -> int | None:
    if value == "":
        return None
    return value


def ensure_list(value: t.Any) -> list[t.Any]:
    if not isinstance(value, list):
        return [value]
    return value


def ensure_list_opt(value: t.Any) -> list[t.Any] | None:
    if value is None:
        return None
    return ensure_list(value)


def ensure_str(value: t.Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        if len(value) == 0:
            return ""
        if len(value) == 1:
            return ensure_str(value[0])
        nonempty_values: set[str] = {v for v in value if isinstance(v, str) and len(v) > 0}
        if len(nonempty_values) == 0:
            return ""
        if len(nonempty_values) == 1:
            return next(iter(nonempty_values))
        raise ValueError(f"Too many unique values: {list(nonempty_values)}")

    return str(value)


def ensure_str_opt(value: t.Any) -> str | None:
    if value is None:
        return None

    return ensure_str(value)


class Avdelning(pydantic.BaseModel):
    text: str


class Avdelningar(pydantic.BaseModel):
    avdelning: list[str]
