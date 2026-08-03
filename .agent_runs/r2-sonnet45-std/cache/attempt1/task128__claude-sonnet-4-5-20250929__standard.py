from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, TypeVar, Any

T = TypeVar('T')
R = TypeVar('R')


def parallel_map(fn: Callable[[T], R], items: List[T], workers: int = 4) -> List[R]:
    """
    Apply fn to each item using up to workers threads and return results in input order.
    
    Args:
        fn: Function to apply to each item
        items: List of items to process
        workers: Number of worker threads (must be >= 1)
        
    Returns:
        List of results in the same order as input items
        
    Raises:
        ValueError: If workers < 1
    """
    if workers < 1:
        raise ValueError("workers must be >= 1")
    
    if not items:
        return []
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all tasks and keep track of futures with their original indices
        futures = [executor.submit(fn, item) for item in items]
        
        # Collect results in order
        results = [future.result() for future in futures]
    
    return results
