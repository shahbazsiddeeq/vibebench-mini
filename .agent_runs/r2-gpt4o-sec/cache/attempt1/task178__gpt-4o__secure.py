import threading
from typing import Optional
import time

class PhaseBarrier:
    def __init__(self, parties: int):
        if parties < 1:
            raise ValueError("Number of parties must be at least 1.")
        
        self.parties = parties
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._current_phase_count = 0
        self._arrival_index = 0

    def wait(self, timeout: Optional[float] = None) -> int:
        with self._condition:
            arrival_index = self._arrival_index
            self._arrival_index += 1
            self._current_phase_count += 1

            if self._current_phase_count == self.parties:
                # Last thread to arrive, reset for next phase
                self._arrival_index = 0
                self._current_phase_count = 0
                self._condition.notify_all()
                return arrival_index

            # Wait for the rest of the threads
            start_time = time.monotonic()
            while self._current_phase_count < self.parties:
                remaining = None if timeout is None else timeout - (time.monotonic() - start_time)
                if remaining is not None and remaining <= 0:
                    self._arrival_index -= 1
                    self._current_phase_count -= 1
                    raise TimeoutError("Timeout while waiting for barrier.")
                self._condition.wait(timeout=remaining)

            return arrival_index

    def n_waiting(self) -> int:
        with self._lock:
            return self._current_phase_count
