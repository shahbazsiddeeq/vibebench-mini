import queue
import threading

def produce_consume(items, process_fn, n_workers=2):
    """
    Applies process_fn to each item using n_workers threads via queue.Queue;
    returns results in input order.

    Args:
        items (iterable): An iterable of items to be processed.
        process_fn (callable): The function to apply to each item.
        n_workers (int): The number of worker threads to use.

    Returns:
        list: A list of results in the same order as the input items.

    Raises:
        ValueError: If n_workers is less than 1.
    """
    if n_workers < 1:
        raise ValueError("n_workers must be at least 1.")

    if not items:
        return []

    # Use a list to store results in the correct order
    results = [None] * len(items)
    
    # Input queue for tasks (index, item)
    task_queue = queue.Queue()
    # Output queue for processed results (index, result)
    result_queue = queue.Queue()

    # Populate the task queue with (index, item) tuples
    for i, item in enumerate(items):
        task_queue.put((i, item))

    # Sentinel values to signal workers to exit
    for _ in range(n_workers):
        task_queue.put(None)

    def worker():
        while True:
            task = task_queue.get()
            if task is None:
                break
            index, item = task
            processed_item = process_fn(item)
            result_queue.put((index, processed_item))
            task_queue.task_done()
        task_queue.task_done() # Mark the sentinel as done

    threads = []
    for _ in range(n_workers):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Wait for all tasks to be processed
    task_queue.join()

    # Collect results from the result_queue
    # The number of results should be equal to the number of items
    for _ in range(len(items)):
        index, result = result_queue.get()
        results[index] = result
        result_queue.task_done()

    # Wait for all results to be collected (optional, but good practice)
    result_queue.join()

    # Join all worker threads
    for thread in threads:
        thread.join()

    return results
