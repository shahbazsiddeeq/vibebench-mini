import functools
import threading
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


def memoize(fn: F) -> F:
    """
    Decorator that caches function results based on positional and keyword arguments.
    Thread-safe and handles recursion without deadlocking.
    """
    cache = {}
    lock = threading.RLock()
    in_progress = {}
    
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Create a hashable key from args and kwargs
        key = (args, tuple(sorted(kwargs.items())))
        
        thread_id = threading.get_ident()
        
        with lock:
            # If result is already cached, return it
            if key in cache:
                return cache[key]
            
            # If this thread is already computing this key, we're in a recursive call
            # Return a sentinel that will be filled in later
            if key in in_progress:
                if in_progress[key] == thread_id:
                    # Recursive call from same thread - compute it
                    # (don't cache yet, let the outer call handle it)
                    result = fn(*args, **kwargs)
                    return result
            
            # Mark this key as being computed by this thread
            in_progress[key] = thread_id
        
        try:
            # Compute the result without holding the lock
            # This allows recursive calls to proceed
            result = fn(*args, **kwargs)
            
            with lock:
                cache[key] = result
                del in_progress[key]
            
            return result
        except Exception:
            with lock:
                if key in in_progress:
                    del in_progress[key]
            raise
    
    return wrapper
