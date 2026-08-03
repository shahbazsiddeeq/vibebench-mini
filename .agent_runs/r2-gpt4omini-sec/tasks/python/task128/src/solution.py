# src/solution.py

import concurrent.futures
import threading
from typing import Callable, List, Any

def parallel_map(fn: Callable[[Any], Any], items: List[Any], workers: int = 4) -> List[Any]:
    if not isinstance(workers, int) or workers < 1:
        raise ValueError("workers must be an integer greater than or equal to 1")
    
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    
    results = [None] * len(items)

    def worker(index: int, item: Any):
        results[index] = fn(item)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(worker, i, item): i for i, item in enumerate(items)}
        for future in concurrent.futures.as_completed(futures):
            future.result()  # This will raise any exceptions that occurred in the worker

    return results
