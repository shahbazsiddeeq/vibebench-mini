import threading


class AtomicCounter:
    """A thread-safe integer counter."""

    def __init__(self, initial: int = 0) -> None:
        if initial < 0:
            raise ValueError("initial value must be non-negative")
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
