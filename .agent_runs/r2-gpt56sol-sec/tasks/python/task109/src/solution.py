from collections.abc import Callable
from typing import Any


def pipeline(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose unary callables, applying them from left to right."""
    if not all(callable(fn) for fn in fns):
        raise TypeError("pipeline arguments must be callable")

    def composed(value: Any) -> Any:
        for fn in fns:
            value = fn(value)
        return value

    return composed
