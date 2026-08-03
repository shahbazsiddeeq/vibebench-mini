"""Thread-safe atomic counter implementation."""

import threading


class AtomicCounter:
    """A thread-safe counter supporting atomic increment/decrement/value operations."""

    def __init__(self, initial: int = 0):
        if initial < 0:
            raise ValueError("initial must be >= 0")
        self._value = initial
        self._lock = threading.Lock()

    def increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self) -> int:
        with self._lock:
            self._value -= 1
            return self._value

    def value(self) -> int:
        with self._lock:
            return self._value
