import queue
import threading


def produce_consume(items, process_fn, n_workers=2):
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
    if n_workers < 1:
        raise ValueError("n_workers must be at least 1")
    
    if not items:
        return []
    
    # Queue for input items with their indices
    input_queue = queue.Queue()
    # Queue for results with their indices
    output_queue = queue.Queue()
    
    # Worker function
    def worker():
        while True:
            try:
                item = input_queue.get(timeout=0.1)
                if item is None:  # Sentinel value to stop worker
                    input_queue.task_done()
                    break
                
                index, value = item
                result = process_fn(value)
                output_queue.put((index, result))
                input_queue.task_done()
            except queue.Empty:
                continue
    
    # Start worker threads
    threads = []
    for _ in range(n_workers):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    # Add items to input queue with their indices
    for i, item in enumerate(items):
        input_queue.put((i, item))
    
    # Add sentinel values to stop workers
    for _ in range(n_workers):
        input_queue.put(None)
    
    # Wait for all items to be processed
    input_queue.join()
    
    # Wait for all threads to finish
    for t in threads:
        t.join()
    
    # Collect results and sort by index to preserve order
    results = []
    while not output_queue.empty():
        results.append(output_queue.get())
    
    # Sort by index and extract values
    results.sort(key=lambda x: x[0])
    return [result[1] for result in results]
