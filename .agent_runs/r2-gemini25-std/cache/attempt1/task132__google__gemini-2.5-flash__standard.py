import threading
from collections import deque

def run_bounded(fns, max_concurrent):
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be at least 1")

    if not fns:
        return []

    results = [None] * len(fns)
    
    # A semaphore to limit the number of concurrent threads
    semaphore = threading.Semaphore(max_concurrent)
    
    # A lock to protect access to the results list
    results_lock = threading.Lock()

    # A list to hold all thread objects
    threads = []

    def worker(index, fn):
        with semaphore:
            try:
                result = fn()
                with results_lock:
                    results[index] = result
            except Exception as e:
                # In a real-world scenario, you might want to handle exceptions
                # more gracefully, e.g., store the exception in results.
                # For this problem, we assume fns don't raise unhandled exceptions.
                print(f"Error in task {index}: {e}")
                with results_lock:
                    results[index] = e # Store exception for debugging if needed

    for i, fn in enumerate(fns):
        thread = threading.Thread(target=worker, args=(i, fn))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results
