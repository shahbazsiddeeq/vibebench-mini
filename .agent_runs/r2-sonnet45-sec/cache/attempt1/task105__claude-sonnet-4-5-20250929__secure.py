import queue
import threading
from typing import Any, Callable, List, TypeVar

T = TypeVar('T')
R = TypeVar('R')


def produce_consume(
    items: List[T],
    process_fn: Callable[[T], R],
    n_workers: int = 2
) -> List[R]:
    """
    Apply process_fn to each item using n_workers threads via queue.Queue.
    Returns results in input order.
    
    Args:
        items: List of items to process
        process_fn: Function to apply to each item
        n_workers: Number of worker threads (must be >= 1)
    
    Returns:
        List of results in the same order as input items
    
    Raises:
        ValueError: If n_workers < 1
    """
    # Validate n_workers
    if n_workers < 1:
        raise ValueError("n_workers must be at least 1")
    
    # Handle empty input
    if not items:
        return []
    
    # Queue for work items (index, item)
    work_queue: queue.Queue = queue.Queue()
    
    # Queue for results (index, result)
    result_queue: queue.Queue = queue.Queue()
    
    # Exception queue to capture worker errors
    exception_queue: queue.Queue = queue.Queue()
    
    # Worker function
    def worker():
        try:
            while True:
                try:
                    # Get work item with timeout to allow checking for completion
                    index, item = work_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                
                if item is None:  # Sentinel value to stop worker
                    work_queue.task_done()
                    break
                
                try:
                    # Process the item
                    result = process_fn(item)
                    result_queue.put((index, result))
                except Exception as e:
                    # Capture any exception during processing
                    exception_queue.put(e)
                finally:
                    work_queue.task_done()
        except Exception as e:
            # Capture any unexpected exception in worker
            exception_queue.put(e)
    
    # Start worker threads
    workers = []
    for _ in range(n_workers):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        workers.append(t)
    
    # Enqueue all work items with their indices
    for index, item in enumerate(items):
        work_queue.put((index, item))
    
    # Add sentinel values to stop workers
    for _ in range(n_workers):
        work_queue.put((None, None))
    
    # Wait for all work to complete
    work_queue.join()
    
    # Wait for all workers to finish
    for t in workers:
        t.join(timeout=1.0)
    
    # Check if any exceptions occurred
    if not exception_queue.empty():
        raise exception_queue.get()
    
    # Collect results and sort by index to preserve order
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    # Sort by index and extract values
    results.sort(key=lambda x: x[0])
    return [result for _, result in results]
