# src/solution.py

import threading
from typing import Callable, Any, Optional

class Once:
    def __init__(self):
        self._lock = threading.Lock()
        self._result: Optional[Any] = None
        self._has_run = False
        self._exception: Optional[Exception] = None

    def do(self, fn: Callable[[], Any]) -> Any:
        if not callable(fn):
            raise ValueError("The provided argument must be a callable.")

        with self._lock:
            if self._has_run:
                return self._result
            
            try:
                self._result = fn()
                self._has_run = True
                return self._result
            except Exception as e:
                self._exception = e
                raise
