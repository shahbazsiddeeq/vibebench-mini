import threading
from queue import Queue

def run_bounded(fns, max_concurrent):
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be at least 1")
    
    results = [None] * len(fns)
    queue = Queue()
    threads = []
    
    def worker(index):
        result = fns[index]()
        results[index] = result
        queue.task_done()
    
    for i in range(len(fns)):
        queue.put(i)
        while threading.active_count() > max_concurrent:
            queue.join()
        thread = threading.Thread(target=worker, args=(i,))
        thread.start()
        threads.append(thread)
    
    queue.join()  # Wait for all tasks to be done
    for thread in threads:
        thread.join()  # Ensure all threads have finished
    
    return results
