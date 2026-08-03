import threading
from typing import Optional

class PhaseBarrier:
    def __init__(self, parties: int):
        if parties < 1:
            raise ValueError("Number of parties must be at least 1.")
        self.parties = parties
        self.current_phase = 0
        self.count = 0
        self.lock = threading.Lock()
        self.phase_complete = threading.Condition(self.lock)
        self.arrival_indices = [None] * parties

    def wait(self, timeout: Optional[float] = None) -> int:
        with self.lock:
            phase = self.current_phase
            index = self.count
            self.arrival_indices[index] = index
            self.count += 1

            if self.count == self.parties:
                self.count = 0
                self.current_phase += 1
                self.phase_complete.notify_all()
                return self.arrival_indices[index]

            while phase == self.current_phase:
                if not self.phase_complete.wait(timeout):
                    if phase == self.current_phase:
                        self.count -= 1
                        raise TimeoutError("Timeout waiting for barrier.")
            return self.arrival_indices[index]

    def n_waiting(self) -> int:
        with self.lock:
            return self.count
