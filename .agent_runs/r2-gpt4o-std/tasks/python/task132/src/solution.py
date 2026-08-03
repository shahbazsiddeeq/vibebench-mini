# src/solution.py

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_bounded(fns, max_concurrent):
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be at least 1")
    
    if not fns:
        return []

    results = [None] * len(fns)
    index_lock = threading.Lock()
    current_index = 0

    def worker(fn_index):
        nonlocal current_index
        result = fns[fn_index]()
        with index_lock:
            results[fn_index] = result

    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = {executor.submit(worker, i): i for i in range(len(fns))}
        for future in as_completed(futures):
            future.result()  # Ensure any exceptions are raised

    return results
