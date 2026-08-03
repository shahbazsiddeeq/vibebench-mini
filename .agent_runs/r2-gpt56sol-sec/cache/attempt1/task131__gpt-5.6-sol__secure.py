"""Thread-safe run-once initializer."""

from __future__ import annotations

import threading
from typing import Callable, Generic, TypeVar, cast


T = TypeVar("T")


class Once(Generic[T]):
    """Run an initializer until it succeeds, then cache its result."""

    __slots__ = ("_lock", "_completed", "_value")

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._completed = False
        self._value: T | None = None

    def do(self, fn: Callable[[], T]) -> T:
        """Run ``fn`` once successfully and return its cached result thereafter."""
        if not callable(fn):
            raise TypeError("fn must be callable")

        with self._lock:
            if self._completed:
                return cast(T, self._value)

            value = fn()
            self._value = value
            self._completed = True
            return value
