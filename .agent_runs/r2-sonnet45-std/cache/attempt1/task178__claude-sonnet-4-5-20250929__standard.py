import threading
import time


class PhaseBarrier:
    def __init__(self, parties: int):
        if parties < 1:
            raise ValueError("parties must be at least 1")
        
        self.parties = parties
        self._lock = threading.Lock()
        self._count = 0  # Number of threads that have arrived in current phase
        self._phase = 0  # Current phase number
        self._arrival_index = 0  # Next arrival index to assign
        self._condition = threading.Condition(self._lock)
        
    def n_waiting(self) -> int:
        with self._lock:
            return self._count
    
    def wait(self, timeout: float | None = None) -> int:
        with self._lock:
            # Record which phase this thread is joining
            my_phase = self._phase
            
            # Get arrival index for this thread
            my_index = self._arrival_index
            self._arrival_index += 1
            
            # Increment count of arrived threads
            self._count += 1
            
            # If this is the last thread to arrive, release everyone
            if self._count == self.parties:
                # Reset for next phase
                self._count = 0
                self._arrival_index = 0
                self._phase += 1
                # Wake up all waiting threads
                self._condition.notify_all()
                return my_index
            
            # Not the last thread, so wait for others
            # Calculate deadline if timeout is specified
            if timeout is not None:
                deadline = time.time() + timeout
            
            # Wait until the phase changes (meaning all parties arrived)
            while self._phase == my_phase:
                if timeout is None:
                    self._condition.wait()
                else:
                    remaining = deadline - time.time()
                    if remaining <= 0:
                        # Timeout occurred - remove ourselves from the count
                        self._count -= 1
                        raise TimeoutError()
                    
                    # Wait with timeout
                    self._condition.wait(timeout=remaining)
                    
                    # Check if we timed out
                    if self._phase == my_phase and time.time() >= deadline:
                        # Timeout occurred - remove ourselves from the count
                        self._count -= 1
                        raise TimeoutError()
            
            # Phase changed, we can proceed
            return my_index
