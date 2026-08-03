import threading


class Once:
    def __init__(self):
        self._lock = threading.Lock()
        self._done = False
        self._result = None
    
    def do(self, fn):
        # Fast path: if already done, return cached result without locking
        if self._done:
            return self._result
        
        # Slow path: acquire lock and check again
        with self._lock:
            # Double-checked locking pattern
            if self._done:
                return self._result
            
            # Run the function
            result = fn()
            
            # Only mark as done and cache result if fn() succeeded (no exception)
            self._result = result
            self._done = True
            
            return result
