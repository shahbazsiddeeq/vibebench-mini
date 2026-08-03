import threading
from queue import Queue

def run_bounded(fns, max_concurrent):
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be at least 1")
    
    results = [None] * len(fns)
    queue = Queue()
    threads = []
    
    def worker(index):
        fn = fns[index]
        result = fn()
        results[index] = result
        queue.task_done()

    for i in range(len(fns)):
        while threading.active_count() > max_concurrent:
            queue.join()
        
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
        queue.put(thread)

    for thread in threads:
        thread.join()

    return results
