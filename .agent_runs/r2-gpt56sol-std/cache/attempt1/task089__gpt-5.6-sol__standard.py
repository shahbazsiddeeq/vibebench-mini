"""Retry utilities with exponential backoff."""

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(
    func: Callable[[], T],
    max_attempts: int,
    base_delay: float,
    exceptions: tuple[type[BaseException], ...],
) -> T:
    """Call ``func``, retrying matching exceptions with exponential backoff."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions:
            if attempt == max_attempts - 1:
                raise
            time.sleep(base_delay * (2**attempt))

    raise RuntimeError("unreachable")
