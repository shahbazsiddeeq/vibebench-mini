import collections
import functools
import threading
import inspect

class _Uncomputed:
    """Sentinel value for a result that is not yet computed."""
    pass

_UNCOMPUTED = _Uncomputed()

def memoize(fn):
    """
    A decorator that caches the results of a function.

    The cache keys are formed from the function's positional and keyword arguments.
    All arguments must be hashable. The wrapped function runs exactly once per
    distinct argument set, even under concurrent calls and when fn is recursive.
    It is thread-safe and preserves functools.wraps metadata.

    Args:
        fn (callable): The function to memoize.

    Returns:
        callable: A wrapper function that caches the results of `fn`.

    Raises:
        TypeError: If any argument to the memoized function is not hashable.
        ValueError: If the function signature cannot be inspected.
    """
    if not callable(fn):
        raise TypeError("memoize can only be applied to callable objects.")

    cache = {}
    # Lock for protecting access to the cache dictionary itself (adding/checking keys).
    # This is a coarse-grained lock for cache modification.
    cache_lock = threading.Lock()
    # Dictionary to hold per-key locks for protecting computation of a specific key.
    # This allows concurrent computation for different keys.
    key_locks = collections.defaultdict(threading.Lock)

    # Inspect the function signature once to handle default arguments and bind args.
    try:
        signature = inspect.signature(fn)
    except ValueError as e:
        raise ValueError(f"Could not inspect signature of function {fn.__name__}: {e}")

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Bind arguments to parameters to create a canonical representation
        # that includes default values and handles positional/keyword mapping.
        try:
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
        except TypeError as e:
            # This can happen if arguments don't match the signature
            raise TypeError(f"Error binding arguments to {fn.__name__}: {e}")

        # Create a hashable key from the bound arguments.
        # We use a tuple of (positional_args_tuple, frozenset_of_keyword_items).
        # This ensures that argument order for positional args matters,
        # but for keyword args it does not.
        try:
            cache_key = (
                tuple(bound_args.args),
                frozenset(bound_args.kwargs.items())
            )
        except TypeError as e:
            raise TypeError(f"Unhashable argument to memoized function {fn.__name__}: {e}")

        # Acquire the global cache_lock to safely check and potentially add the key_lock.
        with cache_lock:
            # Get the specific lock for this cache_key.
            # defaultdict will create it if it doesn't exist.
            # We need to ensure that the key_lock is acquired *before* releasing cache_lock
            # if we are the first to try and compute this key.
            # However, the pattern below is safer: acquire key_lock *after* checking cache.
            # If the key is not in cache, we acquire its specific lock.
            # If it is, we just read.

            # Check if the result is already in the cache.
            # This check is done under the global cache_lock to ensure atomicity
            # of checking and potentially setting _UNCOMPUTED.
            if cache_key in cache:
                result = cache[cache_key]
                # If another thread is currently computing this key, it will be _UNCOMPUTED.
                # We need to wait for it to finish.
                if result is _UNCOMPUTED:
                    # Release cache_lock before waiting on key_lock to avoid deadlock
                    # if another thread needs cache_lock to update the cache.
                    pass # We will acquire key_lock below.
                else:
                    return result

            # If not in cache or currently being computed, mark it as uncomputed
            # and acquire the specific key_lock to compute it.
            # This ensures only one thread computes for a given key.
            # We set _UNCOMPUTED under cache_lock to prevent other threads from
            # trying to compute it simultaneously.
            cache[cache_key] = _UNCOMPUTED

        # Acquire the specific lock for this cache_key.
        # This lock ensures that only one thread computes the result for this key.
        # Other threads that find _UNCOMPUTED in the cache will block here.
        with key_locks[cache_key]:
            # Re-check the cache *after* acquiring the key_lock.
            # Another thread might have finished computing and updated the cache
            # between our initial check and acquiring this lock.
            # This is crucial for correctness in concurrent scenarios.
            if cache_key in cache and cache[cache_key] is not _UNCOMPUTED:
                return cache[cache_key]

            # If we reach here, we are the designated thread to compute the result for this key.
            try:
                result = fn(*args, **kwargs)
            except Exception as e:
                # If computation fails, remove the _UNCOMPUTED marker and re-raise.
                # This ensures subsequent calls will re-attempt computation.
                with cache_lock:
                    if cache_key in cache and cache[cache_key] is _UNCOMPUTED:
                        del cache[cache_key]
                raise
            else:
                # Store the computed result in the cache.
                # This update must be protected by cache_lock to ensure visibility
                # and atomicity for other threads checking the cache.
                with cache_lock:
                    cache[cache_key] = result
                return result
            finally:
                # Clean up the key_lock from defaultdict if it's no longer needed.
                # This prevents unbounded growth of key_locks for transient keys.
                # This cleanup should happen after the result is stored or an error is handled.
                with cache_lock:
                    if cache_key in key_locks:
                        # Only delete if the lock is not currently held by another thread
                        # (which shouldn't happen if we are the only one computing for this key).
                        # A simpler approach is to let defaultdict manage it,
                        # but for very high cardinality keys, cleanup might be desired.
                        # For this problem, simply letting defaultdict manage is acceptable.
                        pass # No explicit cleanup of key_locks needed for correctness.

    # Attach the cache and cache_lock to the wrapper for potential introspection/testing.
    wrapper.cache = cache
    wrapper.cache_lock = cache_lock
    wrapper.key_locks = key_locks # For potential debugging/inspection

    return wrapper
