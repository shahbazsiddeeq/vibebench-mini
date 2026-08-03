import time


def retry(func, max_attempts, base_delay, exceptions):
    """
    Calls func() and retries on specified exceptions with exponential backoff.
    
    Args:
        func: Callable to execute
        max_attempts: Maximum number of attempts (must be >= 1)
        base_delay: Base delay in seconds for exponential backoff
        exceptions: Tuple of exception types to catch and retry on
    
    Returns:
        The result of func() if successful
        
    Raises:
        ValueError: If max_attempts < 1
        The last exception raised by func if all attempts fail
        Any exception not in the exceptions tuple
    """
    # Validate inputs
    if not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be an integer >= 1")
    
    if not isinstance(base_delay, (int, float)) or base_delay < 0:
        raise ValueError("base_delay must be a non-negative number")
    
    if not isinstance(exceptions, tuple):
        raise ValueError("exceptions must be a tuple")
    
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            # Don't sleep after the last attempt
            if attempt < max_attempts - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
        # Let any other exceptions propagate immediately
    
    # If we've exhausted all attempts, raise the last exception
    if last_exception is not None:
        raise last_exception
