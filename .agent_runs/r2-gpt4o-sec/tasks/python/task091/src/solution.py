import threading

class AtomicCounter:
    def __init__(self, initial=0):
        if not isinstance(initial, int) or initial < 0:
            raise ValueError("Initial value must be a non-negative integer.")
        self._value = initial
        self._lock = threading.Lock()

    def increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self) -> int:
        with self._lock:
            if self._value == 0:
                raise ValueError("Counter cannot be decremented below zero.")
            self._value -= 1
            return self._value

    def value(self) -> int:
        with self._lock:
            return self._value
