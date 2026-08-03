import collections
import queue
import threading
import secrets

def produce_consume(items, process_fn, n_workers=2):
    """
    Applies process_fn to each item using n_workers threads via queue.Queue;
    returns results in input order.

    Args:
        items (iterable): An iterable of items to be processed.
        process_fn (callable): A function to apply to each item.
        n_workers (int): The number of worker threads to use. Must be >= 1.

    Returns:
        list: A list of results, in the same order as the input items.

    Raises:
        ValueError: If n_workers is less than 1.
        TypeError: If process_fn is not callable.
    """
    if not isinstance(n_workers, int) or n_workers < 1:
        raise ValueError("n_workers must be an integer greater than or equal to 1.")
    if not callable(process_fn):
        raise TypeError("process_fn must be a callable function.")

    # Use a deque for efficient appending and popping from both ends if needed,
    # though here we primarily append and then convert to list.
    # This also ensures 'items' is consumed once if it's an iterator.
    items_list = list(items)
    total_items = len(items_list)

    if total_items == 0:
        return []

    # Use a thread-safe queue for tasks
    task_queue = queue.Queue()
    # Use a thread-safe dictionary to store results by their original index
    # collections.defaultdict is not strictly necessary here as we'll set keys
    # explicitly, but it's a common pattern for thread-safe result aggregation.
    # A regular dict with a lock would also work.
    results_map = {}
    results_lock = threading.Lock()

    # Sentinel object to signal workers to exit
    # Using a unique object ensures it won't conflict with actual data
    STOP_SIGNAL = object()

    def worker():
        while True:
            task = task_queue.get()
            if task is STOP_SIGNAL:
                task_queue.task_done()
                break

            index, item = task
            try:
                result = process_fn(item)
                with results_lock:
                    results_map[index] = result
            except Exception as e:
                # In a real-world scenario, you might want to log the error
                # or store it in the results_map to indicate failure for that item.
                # For this problem, we re-raise after all tasks are done,
                # or store the exception to be re-raised later.
                # For simplicity, we'll just store the exception.
                with results_lock:
                    results_map[index] = e # Store the exception itself
            finally:
                task_queue.task_done()

    # Start worker threads
    workers = []
    for _ in range(n_workers):
        worker_thread = threading.Thread(target=worker)
        worker_thread.daemon = True  # Allow program to exit even if threads are blocked
        worker_thread.start()
        workers.append(worker_thread)

    # Populate the task queue with (index, item) tuples
    for index, item in enumerate(items_list):
        task_queue.put((index, item))

    # Add stop signals for workers
    for _ in range(n_workers):
        task_queue.put(STOP_SIGNAL)

    # Wait for all tasks to be completed
    task_queue.join()

    # Collect results in the original order
    final_results = []
    for i in range(total_items):
        with results_lock:
            result_or_exception = results_map[i]
        if isinstance(result_or_exception, Exception):
            # Re-raise any exceptions encountered during processing
            raise result_or_exception
        final_results.append(result_or_exception)

    return final_results
