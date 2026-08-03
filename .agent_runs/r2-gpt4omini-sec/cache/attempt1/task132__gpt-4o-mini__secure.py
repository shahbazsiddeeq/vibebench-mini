import threading
from typing import List, Callable, Any

def run_bounded(fns: List[Callable[[], Any]], max_concurrent: int) -> List[Any]:
    if not isinstance(max_concurrent, int) or max_concurrent < 1:
        raise ValueError("max_concurrent must be an integer greater than or equal to 1.")
    
    results = [None] * len(fns)
    lock = threading.Lock()
    condition = threading.Condition()
    active_count = 0

    def worker(index: int):
        nonlocal active_count
        result = fns[index]()
        with lock:
            results[index] = result
            active_count -= 1
            condition.notify()

    threads = []
    for i in range(len(fns)):
        with lock:
            while active_count >= max_concurrent:
                condition.wait()
            active_count += 1
        thread = threading.Thread(target=worker, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results
