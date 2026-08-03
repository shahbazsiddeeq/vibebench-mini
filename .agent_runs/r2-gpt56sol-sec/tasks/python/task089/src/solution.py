"""Utilities for retrying callables with exponential backoff."""

import math
import time
from numbers import Real
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(
    func: Callable[[], T],
    max_attempts: int,
    base_delay: Real,
    exceptions: type[BaseException] | tuple[type[BaseException], ...],
) -> T:
    """Call ``func``, retrying matching exceptions with exponential backoff."""
    if not callable(func):
        raise TypeError("func must be callable")

    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int):
        raise TypeError("max_attempts must be an integer")
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    if isinstance(base_delay, bool) or not isinstance(base_delay, Real):
        raise TypeError("base_delay must be a real number")
    if not math.isfinite(base_delay) or base_delay < 0:
        raise ValueError("base_delay must be finite and non-negative")

    exception_types = exceptions if isinstance(exceptions, tuple) else (exceptions,)
    if not all(
        isinstance(exc, type) and issubclass(exc, BaseException)
        for exc in exception_types
    ):
        raise TypeError("exceptions must contain exception classes")

    for attempt in range(max_attempts):
        try:
            return func()
        except exception_types:
            if attempt == max_attempts - 1:
                raise
            time.sleep(base_delay * (2**attempt))

    raise RuntimeError("retry reached an unreachable state")
