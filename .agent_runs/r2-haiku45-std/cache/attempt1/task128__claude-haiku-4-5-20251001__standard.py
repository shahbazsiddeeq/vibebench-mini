import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, TypeVar, Any

T = TypeVar('T')
U = TypeVar('U')


def parallel_map(fn: Callable[[T], U], items: List[T], workers: int = 4) -> List[U]:
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
    if workers < 1:
        raise ValueError("workers must be >= 1")
    
    if not items:
        return []
    
    results = [None] * len(items)
    lock = threading.Lock()
    
    def worker_fn(index: int, item: T) -> None:
        result = fn(item)
        with lock:
            results[index] = result
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(worker_fn, i, item)
            for i, item in enumerate(items)
        ]
        # Wait for all futures to complete
        for future in futures:
            future.result()
    
    return results
