import threading
from queue import Queue
from typing import Callable, List, Any

def parallel_map(fn: Callable[[Any], Any], items: List[Any], workers: int = 4) -> List[Any]:
    if workers < 1:
        raise ValueError("Number of workers must be at least 1")
    
    if not items:
        return []

    # Queue for tasks and results
    task_queue = Queue()
    result_queue = Queue()

    # Worker function
    def worker():
        while True:
            index, item = task_queue.get()
            if index is None:
                break
            result = fn(item)
            result_queue.put((index, result))
            task_queue.task_done()

    # Start worker threads
    threads = []
    for _ in range(workers):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Enqueue tasks
    for index, item in enumerate(items):
        task_queue.put((index, item))

    # Signal workers to exit
    for _ in range(workers):
        task_queue.put((None, None))

    # Collect results
    results = [None] * len(items)
    for _ in range(len(items)):
        index, result = result_queue.get()
        results[index] = result

    # Wait for all tasks to be done
    task_queue.join()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return results
