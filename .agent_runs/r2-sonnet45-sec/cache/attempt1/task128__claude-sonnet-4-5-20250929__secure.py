import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, TypeVar, Any

T = TypeVar('T')
R = TypeVar('R')


def parallel_map(fn: Callable[[T], R], items: List[T], workers: int = 4) -> List[R]:
    """
    Apply fn to each item using up to `workers` threads and return results in INPUT order.
    
    Args:
        fn: Function to apply to each item
        items: List of items to process
        workers: Number of worker threads (must be >= 1)
        
    Returns:
        List of results in the same order as input items
        
    Raises:
        ValueError: If workers < 1
    """
    # Validate workers parameter
    if workers < 1:
        raise ValueError("workers must be >= 1")
    
    # Handle empty list
    if not items:
        return []
    
    # Use ThreadPoolExecutor to manage thread pool
    # Store results with their original indices to preserve order
    results = [None] * len(items)
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all tasks and store futures with their indices
        futures = {}
        for index, item in enumerate(items):
            future = executor.submit(fn, item)
            futures[future] = index
        
        # Collect results as they complete
        for future in futures:
            index = futures[future]
            try:
                results[index] = future.result()
            except Exception as e:
                # Re-raise the exception from the worker function
                raise e
    
    return results
