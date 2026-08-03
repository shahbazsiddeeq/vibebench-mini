import queue
import threading
from typing import Any, Callable, List


def produce_consume(items: List[Any], process_fn: Callable[[Any], Any], n_workers: int = 2) -> List[Any]:
    """
    Apply process_fn to each item using n_workers threads via queue.Queue.
    Returns results in input order.
    
    Args:
        items: List of items to process
        process_fn: Function to apply to each item
        n_workers: Number of worker threads (must be >= 1)
    
    Returns:
        List of processed items in the same order as input
    
    Raises:
        ValueError: If n_workers < 1
    """
    if n_workers < 1:
        raise ValueError("n_workers must be at least 1")
    
    if not items:
        return []
    
    # Queue to hold (index, item) tuples
    task_queue = queue.Queue()
    # Queue to hold (index, result) tuples
    result_queue = queue.Queue()
    
    def worker():
        while True:
            try:
                index, item = task_queue.get_nowait()
            except queue.Empty:
                break
            
            result = process_fn(item)
            result_queue.put((index, result))
    
    # Populate task queue with (index, item) pairs
    for index, item in enumerate(items):
        task_queue.put((index, item))
    
    # Create and start worker threads
    threads = []
    for _ in range(n_workers):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)
    
    # Wait for all workers to complete
    for thread in threads:
        thread.join()
    
    # Collect results and sort by original index
    results = []
    while not result_queue.empty():
        index, result = result_queue.get()
        results.append((index, result))
    
    # Sort by index to maintain input order
    results.sort(key=lambda x: x[0])
    
    # Extract just the results
    return [result for _, result in results]
