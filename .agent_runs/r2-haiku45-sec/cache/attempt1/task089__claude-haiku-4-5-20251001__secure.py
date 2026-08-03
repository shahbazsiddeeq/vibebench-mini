import time
from typing import Callable, Tuple, Type, Any


def retry(
    func: Callable[[], Any],
    max_attempts: int,
    base_delay: float,
    exceptions: Tuple[Type[Exception], ...],
) -> Any:
    """
    Retry a function with exponential backoff.
    
    Args:
        func: The function to call
        max_attempts: Maximum number of attempts (must be >= 1)
        base_delay: Base delay in seconds for exponential backoff
        exceptions: Tuple of exception types to catch and retry on
        
    Returns:
        The return value of func if successful
        
    Raises:
        ValueError: If max_attempts < 1
        The last caught exception if all attempts fail
        Any other exception not in the exceptions tuple
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            # Only sleep if this is not the last attempt
            if attempt < max_attempts - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
    
    # All attempts failed, raise the last exception
    if last_exception is not None:
        raise last_exception
