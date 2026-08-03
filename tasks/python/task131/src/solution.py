import threading


class Once:
    """Runs a callable exactly once and caches its result for all callers."""

    def __init__(self):
        self._lock = threading.Lock()
        self._done = False
        self._result = None

    def do(self, fn) -> object:
        """Run fn once (first caller wins), then always return the cached result."""
        # Fast path: already initialized, no lock needed.
        if self._done:
            return self._result
        with self._lock:
            if not self._done:
                self._result = fn()
                self._done = True
            return self._result
