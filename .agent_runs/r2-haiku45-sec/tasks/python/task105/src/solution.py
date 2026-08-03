import queue
import threading
from typing import Any, Callable, List, TypeVar

T = TypeVar('T')
U = TypeVar('U')


def produce_consume(items: List[T], process_fn: Callable[[T], U], n_workers: int = 2) -> List[U]:
    """
    Apply process_fn to each item using n_workers threads via queue.Queue.
    Returns results in input order.
    
    Args:
        items: List of items to process
        process_fn: Function to apply to each item
        n_workers: Number of worker threads (must be >= 1)
    
    Returns:
        List of processed results in the same order as input items
    
    Raises:
        ValueError: If n_workers < 1
    """
    if n_workers < 1:
        raise ValueError("n_workers must be at least 1")
    
    if not items:
        return []
    
    # Queue to hold (index, item) tuples for processing
    work_queue: queue.Queue = queue.Queue()
    
    # Queue to hold (index, result) tuples from workers
    result_queue: queue.Queue = queue.Queue()
    
    # Populate work queue with indexed items
    for index, item in enumerate(items):
        work_queue.put((index, item))
    
    # Add sentinel values to signal workers to stop
    for _ in range(n_workers):
        work_queue.put(None)
    
    def worker() -> None:
        """Worker thread function that processes items from work_queue."""
        while True:
            work_item = work_queue.get()
            
            # Check for sentinel value (None) to stop processing
            if work_item is None:
                break
            
            index, item = work_item
            try:
                result = process_fn(item)
                result_queue.put((index, result))
            except Exception as e:
                # Put exception with index so we can handle it properly
                result_queue.put((index, e))
    
    # Create and start worker threads
    threads = []
    for _ in range(n_workers):
        thread = threading.Thread(target=worker, daemon=False)
        thread.start()
        threads.append(thread)
    
    # Wait for all workers to complete
    for thread in threads:
        thread.join()
    
    # Collect results from result_queue and sort by original index
    results_dict: dict = {}
    while not result_queue.empty():
        index, result = result_queue.get()
        results_dict[index] = result
    
    # Build output list in original order
    output = []
    for i in range(len(items)):
        result = results_dict[i]
        # If an exception occurred during processing, raise it
        if isinstance(result, Exception):
            raise result
        output.append(result)
    
    return output
