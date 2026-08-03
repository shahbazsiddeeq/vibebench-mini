from functools import reduce
from typing import Any, Callable


def pipeline(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose unary functions, applying them from left to right."""
    def composed(value: Any) -> Any:
        return reduce(lambda result, fn: fn(result), fns, value)

    return composed
