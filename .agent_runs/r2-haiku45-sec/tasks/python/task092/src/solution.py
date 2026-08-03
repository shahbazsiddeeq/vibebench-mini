import functools
import threading
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])

# Sentinel value to distinguish "not computed yet" from "computed to None"
_SENTINEL = object()


def memoize(fn: F) -> F:
    """
    Decorator that caches function results based on positional and keyword arguments.
    
    Thread-safe and handles recursive calls without deadlocking.
    Preserves function metadata via functools.wraps.
    
    Args:
        fn: The function to memoize
        
    Returns:
        A wrapped function that caches results
    """
    cache: dict[tuple[Any, ...], Any] = {}
    cache_lock = threading.RLock()
    
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Create a hashable key from args and kwargs
        # Sort kwargs to ensure consistent key generation
        key = (args, tuple(sorted(kwargs.items())))
        
        # Check cache first without holding lock for the entire operation
        with cache_lock:
            if key in cache:
                result = cache[key]
                if result is not _SENTINEL:
                    return result
                # If sentinel, we're currently computing - fall through to compute
            else:
                # Mark as being computed to handle recursion
                cache[key] = _SENTINEL
        
        # Compute the result outside the lock to avoid deadlock on recursive calls
        try:
            result = fn(*args, **kwargs)
        except Exception:
            # Remove sentinel on exception so retry is possible
            with cache_lock:
                if key in cache and cache[key] is _SENTINEL:
                    del cache[key]
            raise
        
        # Store the actual result
        with cache_lock:
            cache[key] = result
        
        return result
    
    return wrapper
