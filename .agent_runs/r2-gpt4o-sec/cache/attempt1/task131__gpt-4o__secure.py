import threading

class Once:
    def __init__(self):
        self._lock = threading.Lock()
        self._initialized = False
        self._result = None

    def do(self, fn):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    try:
                        self._result = fn()
                        self._initialized = True
                    except Exception as e:
                        raise e
        return self._result
