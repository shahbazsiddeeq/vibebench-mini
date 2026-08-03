import threading
from queue import Queue
from typing import List, Callable, Any


def run_bounded(fns: List[Callable[[], Any]], max_concurrent: int) -> List[Any]:
    """
    Run zero-arg callables with at most max_concurrent running at once.
    Returns results in the order of fns.
    
    Args:
        fns: List of zero-argument callables
        max_concurrent: Maximum number of concurrent executions (must be >= 1)
        
    Returns:
        List of results in the same order as fns
        
    Raises:
        ValueError: If max_concurrent < 1
    """
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be >= 1")
    
    if not fns:
        return []
    
    # Queue to hold (index, fn) pairs
    task_queue = Queue()
    for i, fn in enumerate(fns):
        task_queue.put((i, fn))
    
    # Queue to hold (index, result) pairs
    result_queue = Queue()
    
    # Lock for synchronization
    lock = threading.Lock()
    
    def worker():
        while True:
            try:
                index, fn = task_queue.get_nowait()
            except:
                break
            
            try:
                result = fn()
                result_queue.put((index, result))
            except Exception as e:
                result_queue.put((index, e))
    
    # Create and start worker threads
    threads = []
    num_workers = min(max_concurrent, len(fns))
    
    for _ in range(num_workers):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Collect results in order
    results = [None] * len(fns)
    while not result_queue.empty():
        index, result = result_queue.get()
        if isinstance(result, Exception):
            raise result
        results[index] = result
    
    return results
