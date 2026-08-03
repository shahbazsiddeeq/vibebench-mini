import threading


class AtomicCounter:
    def __init__(self, initial=0):
        if initial < 0:
            raise ValueError("Initial value cannot be negative")
        self._value = initial
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._value += 1
            return self._value
    
    def decrement(self):
        with self._lock:
            self._value -= 1
            return self._value
    
    def value(self):
        with self._lock:
            return self._value
