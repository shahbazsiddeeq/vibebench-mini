import threading
from queue import Queue

def produce_consume(items, process_fn, n_workers=2):
    if n_workers < 1:
        raise ValueError("Number of workers must be at least 1")

    # Queue for items to be processed
    task_queue = Queue()
    # Queue for results to maintain order
    result_queue = Queue()

    # Worker function
    def worker():
        while True:
            index, item = task_queue.get()
            if item is None:
                break
            result = process_fn(item)
            result_queue.put((index, result))
            task_queue.task_done()

    # Start worker threads
    threads = []
    for _ in range(n_workers):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Enqueue items with their index
    for index, item in enumerate(items):
        task_queue.put((index, item))

    # Add sentinel values to stop workers
    for _ in range(n_workers):
        task_queue.put((None, None))

    # Wait for all tasks to be processed
    task_queue.join()

    # Collect results in order
    results = [None] * len(items)
    while not result_queue.empty():
        index, result = result_queue.get()
        results[index] = result

    # Ensure all threads have finished
    for thread in threads:
        thread.join()

    return results
