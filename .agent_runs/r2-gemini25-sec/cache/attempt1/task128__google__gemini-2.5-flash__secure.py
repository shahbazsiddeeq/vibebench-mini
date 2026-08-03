import collections
import threading


def parallel_map(fn, items, workers=4):
    """
    Applies fn to each item using up to `workers` threads and returns results in INPUT order.

    Args:
        fn: The function to apply to each item.
        items: An iterable of items to process.
        workers: The number of worker threads to use. Must be >= 1.

    Returns:
        A list containing the results of applying fn to each item, in the original order.

    Raises:
        ValueError: If workers is less than 1.
    """
    if not isinstance(workers, int) or workers < 1:
        raise ValueError("workers must be an integer greater than or equal to 1")

    # Convert items to a list to ensure consistent indexing and iteration
    items_list = list(items)
    if not items_list:
        return []

    # Use a dictionary to store results by index to preserve order
    results_map = {}
    # Use a lock to protect access to results_map and the index counter
    results_lock = threading.Lock()
    # Use a condition variable to signal when results are ready for collection
    results_ready_condition = threading.Condition(results_lock)

    # Use a deque as a thread-safe queue for tasks
    task_queue = collections.deque()
    for i, item in enumerate(items_list):
        task_queue.append((i, item))

    # Use a counter for active workers to know when all tasks are done
    active_workers = 0
    active_workers_lock = threading.Lock()

    def worker_fn():
        nonlocal active_workers
        with active_workers_lock:
            active_workers += 1

        try:
            while True:
                index = None
                item = None
                with results_lock:
                    if not task_queue:
                        break  # No more tasks
                    index, item = task_queue.popleft()

                try:
                    result = fn(item)
                    with results_lock:
                        results_map[index] = result
                        results_ready_condition.notify_all()  # Notify main thread that a result is ready
                except Exception as e:
                    # Store the exception to be re-raised in the main thread
                    with results_lock:
                        results_map[index] = e
                        results_ready_condition.notify_all()
                    # Continue processing other tasks if possible, or re-raise immediately if desired
                    # For this problem, we'll let the main thread collect and re-raise.
        finally:
            with active_workers_lock:
                active_workers -= 1
                # If this is the last worker, notify the main thread that all work is done
                if active_workers == 0:
                    with results_lock:
                        results_ready_condition.notify_all()

    threads = []
    for _ in range(min(workers, len(items_list))):
        thread = threading.Thread(target=worker_fn)
        thread.start()
        threads.append(thread)

    final_results = [None] * len(items_list)
    collected_count = 0

    while collected_count < len(items_list):
        with results_lock:
            # Wait until a new result is available or all workers are done
            while collected_count == len(items_list) or (
                len(results_map) == collected_count and active_workers > 0
            ):
                results_ready_condition.wait()

            # Collect results in order
            while collected_count < len(items_list) and collected_count in results_map:
                result_or_exception = results_map.pop(collected_count)
                if isinstance(result_or_exception, Exception):
                    # Re-raise the exception from the worker thread
                    # Ensure all threads are joined before re-raising
                    for t in threads:
                        t.join()
                    raise result_or_exception
                final_results[collected_count] = result_or_exception
                collected_count += 1

    for thread in threads:
        thread.join()

    return final_results
