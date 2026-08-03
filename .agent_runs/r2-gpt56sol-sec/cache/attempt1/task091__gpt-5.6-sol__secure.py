"""Thread-safe atomic counter implementation."""

from __future__ import annotations

import threading


class AtomicCounter:
    """A counter whose read and update operations are thread-safe."""

    __slots__ = ("_value", "_lock")

    def __init__(self, initial: int = 0) -> None:
        if isinstance(initial, bool) or not isinstance(initial, int):
            raise TypeError("initial must be an integer")
        if initial < 0:
            raise ValueError("initial must be non-negative")

        self._value = initial
        self._lock = threading.Lock()

    def increment(self) -> int:
        """Increment the counter by one and return its new value."""
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self) -> int:
        """Decrement the counter by one and return its new value."""
        with self._lock:
            self._value -= 1
            return self._value

    def value(self) -> int:
        """Return the counter's current value."""
        with self._lock:
            return self._value
