import threading

class Once:
    def __init__(self):
        self._initialized = False
        self._value = None
        self._lock = threading.Lock()

    def do(self, fn):
        if self._initialized:
            return self._value

        with self._lock:
            # Double-checked locking to ensure fn is called only once
            if self._initialized:
                return self._value
            
            try:
                result = fn()
                self._value = result
                self._initialized = True
                return result
            except Exception:
                # If fn raises an exception, the run is NOT recorded,
                # so _initialized remains False and a later call will retry.
                raise
