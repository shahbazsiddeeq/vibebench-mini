import threading
from typing import List, Callable, Any


def run_bounded(fns: List[Callable[[], Any]], max_concurrent: int) -> List[Any]:
    """
    Execute zero-arg callables with bounded concurrency.
    
    Args:
        fns: List of zero-argument callables to execute
        max_concurrent: Maximum number of concurrent threads (must be >= 1)
    
    Returns:
        List of results in the same order as fns
        
    Raises:
        ValueError: If max_concurrent < 1
    """
    # Validate max_concurrent
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be at least 1")
    
    # Handle empty input
    if not fns:
        return []
    
    # Store results with their original indices
    results = [None] * len(fns)
    exceptions = [None] * len(fns)
    
    # Semaphore to limit concurrency
    semaphore = threading.Semaphore(max_concurrent)
    
    def worker(index: int, fn: Callable[[], Any]) -> None:
        """Execute a single callable and store its result."""
        semaphore.acquire()
        try:
            result = fn()
            results[index] = result
        except Exception as e:
            exceptions[index] = e
        finally:
            semaphore.release()
    
    # Create and start threads
    threads = []
    for i, fn in enumerate(fns):
        thread = threading.Thread(target=worker, args=(i, fn))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check if any exceptions occurred
    for i, exc in enumerate(exceptions):
        if exc is not None:
            raise exc
    
    return results
