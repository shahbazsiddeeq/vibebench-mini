import time


def retry(func, max_attempts, base_delay, exceptions):
    """
    Calls func(); on exceptions, waits base_delay*2^attempt seconds;
    raises last exception after max_attempts.

    Args:
        func (callable): The function to call.
        max_attempts (int): The maximum number of times to attempt calling func.
        base_delay (float): The base delay in seconds for exponential backoff.
        exceptions (tuple): A tuple of exception types to catch and retry on.

    Returns:
        Any: The result of func if it succeeds within max_attempts.

    Raises:
        ValueError: If max_attempts is less than 1.
        Exception: The last exception raised by func if all attempts fail.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    last_exception = None
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_attempts - 1:
                delay = base_delay * (2**attempt)
                time.sleep(delay)
        except Exception as e:
            # If it's not one of the specified exceptions, re-raise immediately
            raise e

    if last_exception:
        raise last_exception
    # This case should ideally not be reached if max_attempts >= 1 and func always raises
    # or returns. However, if func never raises and max_attempts is 0 (which is caught
    # by ValueError), or if func returns None and that's an expected outcome,
    # this path is technically possible. For the given problem, it implies func
    # must have returned something or raised an exception.
    # If func never raised and max_attempts was 1, it would have returned.
    # So, if we reach here, it means func was called max_attempts times,
    # and the last call raised an exception that was caught.
    # The last_exception should always be set in this loop if all attempts fail.
    # This line is mostly for type checkers or extremely unusual edge cases.
    raise RuntimeError("Unexpected state: func did not return and no exception was raised.")
