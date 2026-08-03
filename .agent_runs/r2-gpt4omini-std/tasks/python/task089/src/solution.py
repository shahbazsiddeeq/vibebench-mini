# src/solution.py

import time

def retry(func, max_attempts, base_delay, exceptions):
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_attempts - 1:  # No sleep after the last attempt
                time.sleep(base_delay * (2 ** attempt))
    
    raise last_exception
