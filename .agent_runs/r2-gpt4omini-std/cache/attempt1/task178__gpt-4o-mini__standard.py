import threading
import time

class PhaseBarrier:
    def __init__(self, parties: int):
        if parties < 1:
            raise ValueError("Number of parties must be at least 1.")
        self.parties = parties
        self.count = 0
        self.phase = 0
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def wait(self, timeout: float = None) -> int:
        with self.lock:
            current_phase = self.phase
            self.count += 1
            index = self.count - 1
            
            if self.count == self.parties:
                self.count = 0
                self.phase += 1
                self.condition.notify_all()
                return index
            
            if timeout is not None:
                deadline = time.monotonic() + timeout
                while current_phase == self.phase:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        self.count -= 1
                        raise TimeoutError("Timeout while waiting at the barrier.")
                    self.condition.wait(remaining)
            else:
                while current_phase == self.phase:
                    self.condition.wait()
                    
            return index

    def n_waiting(self) -> int:
        with self.lock:
            return self.count
