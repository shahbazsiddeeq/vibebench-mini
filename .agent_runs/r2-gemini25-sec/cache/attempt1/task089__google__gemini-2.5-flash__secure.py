import time
import math
import secrets

def retry(func, max_attempts, base_delay, exceptions):
    """
    Calls func(); on exceptions, waits base_delay*2^attempt seconds;
    raises last exception after max_attempts.

    Args:
        func (callable): The function to call.
        max_attempts (int): The maximum number of attempts. Must be >= 1.
        base_delay (float or int): The base delay in seconds for exponential backoff.
                                   Must be non-negative.
        exceptions (tuple): A tuple of exception types to catch and retry on.

    Returns:
        Any: The result of the successful call to func.

    Raises:
        ValueError: If max_attempts is less than 1 or base_delay is negative.
        Exception: The last exception raised by func if all attempts fail.
    """
    if not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be an integer greater than or equal to 1.")
    if not isinstance(base_delay, (int, float)) or base_delay < 0:
        raise ValueError("base_delay must be a non-negative number.")
    if not isinstance(exceptions, tuple):
        raise ValueError("exceptions must be a tuple of exception types.")
    if not all(isinstance(e, type) and issubclass(e, BaseException) for e in exceptions):
        raise ValueError("All elements in 'exceptions' must be exception types.")

    last_exception = None
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_attempts - 1:
                # Calculate delay with full jitter
                # The nominal delay is base_delay * 2^attempt
                # We introduce jitter by picking a random value between 0 and the nominal delay
                nominal_delay = base_delay * (2 ** attempt)
                # Ensure nominal_delay is not negative, though base_delay is checked
                if nominal_delay < 0:
                    nominal_delay = 0.0 # Should not happen with valid base_delay
                
                # Use secrets for cryptographically strong randomness for jitter
                # This is a simple full jitter implementation: random_between(0, nominal_delay)
                # For very small nominal_delay, secrets.randbelow might be problematic with floats.
                # A common approach is to scale, use randbelow, then scale back.
                # Or, for floats, generate a random float in [0, 1) and multiply.
                
                # To avoid potential floating point issues with secrets.randbelow (which expects int),
                # we can generate a random float in [0, 1) and multiply by nominal_delay.
                # secrets.SystemRandom().random() generates a float in [0.0, 1.0).
                jittered_delay = secrets.SystemRandom().random() * nominal_delay
                
                time.sleep(jittered_delay)
    
    if last_exception:
        raise last_exception
    # This part should ideally not be reached if max_attempts >= 1 and func() always raises
    # or if func() succeeds. It's a safeguard.
    raise RuntimeError("An unexpected error occurred in the retry mechanism.")
