import time
from typing import Callable, Tuple, Type
import secrets

def retry(func: Callable, max_attempts: int, base_delay: float, exceptions: Tuple[Type[BaseException], ...]):
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_attempts - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
    
    if last_exception:
        raise last_exception
