"""
Retry with Exponential Backoff.

Provides a `retry` function that invokes a callable, retrying on
specified exceptions with exponential backoff delays between attempts.
"""

import time
from typing import Callable, Tuple, Type, TypeVar

T = TypeVar("T")


def retry(
    func: Callable[[], T],
    max_attempts: int,
    base_delay: float,
    exceptions: Tuple[Type[BaseException], ...],
) -> T:
    """
    Call `func()` and retry on specified exceptions using exponential backoff.

    Args:
        func: A zero-argument callable to invoke.
        max_attempts: Maximum number of attempts (must be >= 1).
        base_delay: Base delay in seconds; the delay before retry `attempt`
            (0-indexed) is base_delay * 2**attempt.
        exceptions: A tuple of exception types that should trigger a retry.

    Returns:
        The return value of `func()` on success.

    Raises:
        ValueError: If max_attempts < 1 or exceptions is not a valid tuple
            of exception types.
        Exception: The last exception raised by `func()` if all attempts fail.
    """
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool):
        raise ValueError("max_attempts must be an integer")
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    if not callable(func):
        raise ValueError("func must be callable")

    if not isinstance(base_delay, (int, float)) or isinstance(base_delay, bool):
        raise ValueError("base_delay must be a number")
    if base_delay < 0:
        raise ValueError("base_delay must be non-negative")

    if not isinstance(exceptions, tuple) or len(exceptions) == 0:
        raise ValueError("exceptions must be a non-empty tuple of exception types")
    for exc in exceptions:
        if not (isinstance(exc, type) and issubclass(exc, BaseException)):
            raise ValueError("exceptions must contain only exception types")

    last_exception: BaseException = None

    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as exc:
            last_exception = exc
            if attempt < max_attempts - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)

    if last_exception is not None:
        raise last_exception

    # This point should not be reachable given the logic above.
    raise RuntimeError("retry failed without capturing an exception")
