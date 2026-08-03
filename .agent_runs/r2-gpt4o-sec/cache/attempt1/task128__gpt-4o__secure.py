import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Any

def parallel_map(fn: Callable[[Any], Any], items: List[Any], workers: int = 4) -> List[Any]:
    if workers < 1:
        raise ValueError("Number of workers must be at least 1.")
    
    if not items:
        return []

    results = [None] * len(items)
    futures = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for index, item in enumerate(items):
            future = executor.submit(fn, item)
            futures.append((index, future))

        for index, future in futures:
            try:
                results[index] = future.result()
            except Exception as e:
                results[index] = e  # Handle exceptions gracefully

    return results
