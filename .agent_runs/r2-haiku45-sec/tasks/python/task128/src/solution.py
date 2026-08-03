import threading
from queue import Queue
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
    
    # Queue to hold (index, item) tuples for workers to process
    task_queue: Queue = Queue()
    
    # Dictionary to store results: index -> result
    results: dict = {}
    results_lock = threading.Lock()
    
    # Exception storage for error handling
    exception_holder: dict = {"exc": None}
    exception_lock = threading.Lock()
    
    def worker() -> None:
        """Worker thread function that processes items from the queue."""
        while True:
            try:
                # Get task from queue (blocks until available or queue is empty)
                item = task_queue.get()
                
                # Sentinel value to signal worker shutdown
                if item is None:
                    task_queue.task_done()
                    break
                
                index, value = item
                
                try:
                    # Apply function to the item
                    result = fn(value)
                    
                    # Store result with its original index
                    with results_lock:
                        results[index] = result
                
                except Exception as e:
                    # Capture exception to re-raise in main thread
                    with exception_lock:
                        if exception_holder["exc"] is None:
                            exception_holder["exc"] = e
                
                finally:
                    task_queue.task_done()
            
            except Exception:
                # Catch any unexpected exceptions in worker loop
                task_queue.task_done()
                break
    
    # Create and start worker threads
    threads = []
    actual_workers = min(workers, len(items))
    
    for _ in range(actual_workers):
        thread = threading.Thread(target=worker, daemon=False)
        thread.start()
        threads.append(thread)
    
    # Enqueue all tasks with their indices
    for index, item in enumerate(items):
        task_queue.put((index, item))
    
    # Wait for all tasks to complete
    task_queue.join()
    
    # Send sentinel values to stop workers
    for _ in range(actual_workers):
        task_queue.put(None)
    
    # Wait for all worker threads to finish
    for thread in threads:
        thread.join()
    
    # Check if any exception occurred during processing
    if exception_holder["exc"] is not None:
        raise exception_holder["exc"]
    
    # Build result list in original order
    result_list = [results[i] for i in range(len(items))]
    
    return result_list
