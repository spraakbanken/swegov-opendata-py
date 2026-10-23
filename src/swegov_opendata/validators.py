import typing as t


def ensure_list(value: t.Any) -> list[t.Any]:
    if not isinstance(value, list):
        return [value]
    return value


def ensure_list_opt(value: t.Any) -> list[t.Any] | None:
    if value is None:
        return None
    return ensure_list(value)


def ensure_str_if_list_only_one_unique_value(value: t.Any) -> str:

    if isinstance(value, list):
        if len(value) == 0:
            return ""
        if len(value) == 1:
            return _ensure_str(value[0])
        nonempty_values: set[str] = {v for v in value if isinstance(v, str) and len(v) > 0}
        if len(nonempty_values) == 0:
            return ""
        if len(nonempty_values) == 1:
            return next(iter(nonempty_values))
        raise ValueError(f"Too many unique values: {sorted(nonempty_values)}")

    return _ensure_str(value)


def ensure_str_opt(value: t.Any) -> str | None:
    if value is None:
        return None

    return _ensure_str(value)


def split_space_take_first(value: t.Any) -> t.Any:
    if isinstance(value, str):
        return "" if not value else value.split()[0]
    return value


def ensure_none_if_empty(value: t.Any) -> t.Any:
    if isinstance(value, str):
        return None if value == "" else value
    return value


def ensure_str_if_list_take_first(value: t.Any) -> t.Any:

    if isinstance(value, list):
        if len(value) == 0:
            return ""
        return _ensure_str(value[0])
    return _ensure_str(value)


def _ensure_str(v: t.Any) -> str:
    if v is None:
        return ""
    return v if isinstance(v, str) else str(v)
