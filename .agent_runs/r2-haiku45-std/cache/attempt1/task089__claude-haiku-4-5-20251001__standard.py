import time


def retry(func, max_attempts, base_delay, exceptions):
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
            # Sleep before retrying, but not after the last attempt
            if attempt < max_attempts - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
    
    # If we've exhausted all attempts, raise the last exception
    raise last_exception
