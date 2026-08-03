import threading
from typing import Optional

class PhaseBarrier:
    def __init__(self, parties: int):
        if parties < 1:
            raise ValueError("Number of parties must be at least 1.")
        self.parties = parties
        self._lock = threading.Lock()
        self._phase_complete = threading.Condition(self._lock)
        self._current_phase_count = 0
        self._arrival_index = 0
        self._phase = 0

    def wait(self, timeout: Optional[float] = None) -> int:
        with self._lock:
            phase = self._phase
            arrival_index = self._arrival_index
            self._arrival_index += 1
            self._current_phase_count += 1

            if self._current_phase_count == self.parties:
                self._phase += 1
                self._arrival_index = 0
                self._current_phase_count = 0
                self._phase_complete.notify_all()
                return arrival_index

            while phase == self._phase:
                if not self._phase_complete.wait(timeout):
                    if phase == self._phase:
                        self._current_phase_count -= 1
                        self._arrival_index -= 1
                        raise TimeoutError("Timeout while waiting for barrier.")
            return arrival_index

    def n_waiting(self) -> int:
        with self._lock:
            return self._current_phase_count
