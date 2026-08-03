import threading


class Once:
    """Runs a zero-arg callable only once (on first success), caching result."""

    def __init__(self):
        self._lock = threading.Lock()
        self._done = False
        self._result = None

    def do(self, fn):
        if self._done:
            return self._result
        with self._lock:
            if not self._done:
                result = fn()
                self._result = result
                self._done = True
            return self._result
