import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List


def run_bounded(fns: List[Callable[[], Any]], max_concurrent: int) -> List[Any]:
    """
    Run zero-arg callables with bounded concurrency.
    
    Args:
        fns: List of zero-argument callables to execute
        max_concurrent: Maximum number of concurrent executions (must be >= 1)
    
    Returns:
        List of results in the same order as fns
    
    Raises:
        ValueError: If max_concurrent < 1
    """
    # Validate max_concurrent
    if not isinstance(max_concurrent, int) or max_concurrent < 1:
        raise ValueError("max_concurrent must be an integer >= 1")
    
    # Handle empty input
    if not fns:
        return []
    
    # Validate fns is a list/sequence and all items are callable
    if not isinstance(fns, (list, tuple)):
        raise TypeError("fns must be a list or tuple")
    
    for fn in fns:
        if not callable(fn):
            raise TypeError("All items in fns must be callable")
    
    # Use ThreadPoolExecutor to manage bounded concurrency
    results = [None] * len(fns)
    
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        # Submit all tasks and keep track of futures with their indices
        futures = {executor.submit(fn): i for i, fn in enumerate(fns)}
        
        # Collect results as they complete, but store in original order
        for future in futures:
            index = futures[future]
            try:
                results[index] = future.result()
            except Exception as e:
                # Re-raise the exception from the callable
                raise e
    
    return results
