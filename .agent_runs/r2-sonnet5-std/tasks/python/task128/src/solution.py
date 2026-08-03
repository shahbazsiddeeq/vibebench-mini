"""Parallel map with order-preserving results using a thread pool."""
from concurrent.futures import ThreadPoolExecutor


def parallel_map(fn, items, workers=4):
    if workers < 1:
        raise ValueError("workers must be >= 1")

    items = list(items)
    if not items:
        return []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(fn, items))

    return results
