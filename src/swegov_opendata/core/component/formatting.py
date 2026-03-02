from collections.abc import Callable


class LazyStr:
    def __init__(self, func: Callable[[...], str], *args, **kwargs) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        return self.func(*self.args, **self.kwargs)
