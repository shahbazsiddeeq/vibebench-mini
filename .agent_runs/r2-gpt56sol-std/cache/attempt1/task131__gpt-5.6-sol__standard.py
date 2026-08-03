"""Thread-safe run-once initializer."""

from __future__ import annotations

import threading
from typing import Callable, Generic, TypeVar, cast

T = TypeVar("T")


class Once(Generic[T]):
    """Run a callable until its first successful completion, then cache its value."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._completed = False
        self._value: T | None = None

    def do(self, fn: Callable[[], T]) -> T:
        """Return the cached result, running ``fn`` if no call has succeeded yet."""
        if self._completed:
            return cast(T, self._value)

        with self._lock:
            if not self._completed:
                value = fn()
                self._value = value
                self._completed = True

            return cast(T, self._value)
