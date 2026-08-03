# src/solution.py

import time
import math

def retry(func, max_attempts, base_delay, exceptions):
    if not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer.")
    
    if not isinstance(base_delay, (int, float)) or base_delay < 0:
        raise ValueError("base_delay must be a non-negative number.")
    
    if not isinstance(exceptions, tuple):
        raise ValueError("exceptions must be a tuple of exception types.")
    
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_attempts - 1:  # No sleep after the last attempt
                time.sleep(base_delay * (2 ** attempt))
    
    raise last_exception
