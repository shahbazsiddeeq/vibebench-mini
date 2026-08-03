import functools
import collections
import threading

_UNSET = object()

class _MemoizedCall:
    """
    Represents a single call to a memoized function, managing its state
    (pending, ready, exception) and providing a way for threads to wait for
    the result.
    """
    def __init__(self):
        self.event = threading.Event()
        self.result = _UNSET
        self.exception = _UNSET

    def set_result(self, value):
        self.result = value
        self.event.set()

    def set_exception(self, exc_info):
        self.exception = exc_info
        self.event.set()

    def get_result(self):
        self.event.wait()
        if self.exception is not _UNSET:
            # Re-raise the exception with its original traceback
            raise self.exception[1].with_traceback(self.exception[2])
        return self.result

def memoize(fn):
    """
    A decorator that caches the results of a function call based on its
    positional and keyword arguments.

    The cache is thread-safe. Concurrent calls for the same arguments will
    block until the first call completes, preventing redundant computations
    and deadlocks in recursive scenarios.

    Args:
        fn: The function to be memoized.

    Returns:
        A wrapper function that memoizes the results of `fn`.
    """
    cache = {}
    # Lock for managing access to the cache dictionary itself
    cache_lock = threading.Lock()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Create a hashable key from positional and keyword arguments.
        # Keyword arguments are sorted to ensure consistent key generation.
        key = (args, frozenset(kwargs.items()))

        # Check if the result is already in the cache
        with cache_lock:
            if key in cache:
                # If a call is already in progress or completed, retrieve its state
                memoized_call = cache[key]
            else:
                # First time this key is seen, create a new _MemoizedCall object
                memoized_call = _MemoizedCall()
                cache[key] = memoized_call

        # Wait for the result if another thread is already computing it
        # or retrieve it if it's already computed.
        # This call will block if memoized_call.event is not set.
        if memoized_call.event.is_set():
            return memoized_call.get_result()

        # If we are the thread that created the _MemoizedCall object,
        # we are responsible for computing the result.
        # This path is taken only once per unique key.
        try:
            result = fn(*args, **kwargs)
            memoized_call.set_result(result)
            return result
        except Exception:
            import sys
            memoized_call.set_exception(sys.exc_info())
            # Re-raise the exception immediately for the current thread
            raise

    return wrapper
