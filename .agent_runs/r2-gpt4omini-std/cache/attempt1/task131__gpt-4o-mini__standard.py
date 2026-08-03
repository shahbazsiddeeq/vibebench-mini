import threading

class Once:
    def __init__(self):
        self._lock = threading.Lock()
        self._result = None
        self._has_run = False
        self._exception = None

    def do(self, fn):
        with self._lock:
            if self._has_run:
                if self._exception is not None:
                    raise self._exception
                return self._result
            
            try:
                self._result = fn()
                self._has_run = True
                return self._result
            except Exception as e:
                self._exception = e
                raise
