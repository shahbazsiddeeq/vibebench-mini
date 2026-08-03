import concurrent.futures
from typing import Callable, List

def parallel_map(fn: Callable, items: List, workers: int = 4) -> List:
    if workers < 1:
        raise ValueError("Number of workers must be at least 1.")
    
    if not items:
        return []
    
    results = [None] * len(items)
    
    def task(index, item):
        results[index] = fn(item)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(task, i, item): i for i, item in enumerate(items)}
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Wait for the task to complete
    
    return results
