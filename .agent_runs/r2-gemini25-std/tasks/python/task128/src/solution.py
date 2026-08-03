import threading
from collections import deque

def parallel_map(fn, items, workers=4):
    if workers < 1:
        raise ValueError("workers must be greater than or equal to 1")

    if not items:
        return []

    results = [None] * len(items)
    task_queue = deque(enumerate(items))
    
    # Use a lock to protect access to shared resources (task_queue, results, next_result_index)
    queue_lock = threading.Lock()
    
    # Condition variable to signal when a result is ready for the main thread to collect
    result_ready_condition = threading.Condition(queue_lock)
    
    # Index of the next result to be collected by the main thread
    next_result_index = 0

    def worker_fn():
        nonlocal next_result_index
        while True:
            item_index = -1
            item_value = None

            with queue_lock:
                if not task_queue:
                    break  # No more tasks
                item_index, item_value = task_queue.popleft()

            # Perform the function call outside the lock to allow other workers to pick tasks
            result = fn(item_value)

            with queue_lock:
                results[item_index] = result
                # Notify the main thread if this result is the next one it's waiting for
                if item_index == next_result_index:
                    result_ready_condition.notify_all()

    threads = []
    for _ in range(min(workers, len(items))):
        thread = threading.Thread(target=worker_fn)
        threads.append(thread)
        thread.start()

    # Main thread collects results in order
    final_ordered_results = []
    for i in range(len(items)):
        with queue_lock:
            while results[i] is None:
                # Wait for the result at index 'i' to be computed
                result_ready_condition.wait()
            final_ordered_results.append(results[i])
            next_result_index += 1 # Advance the expected next result index

    for thread in threads:
        thread.join()

    return final_ordered_results
