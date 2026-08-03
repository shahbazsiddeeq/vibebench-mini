import threading
from typing import Optional


class PhaseBarrier:
    """A reusable synchronization barrier for coordinating multiple threads across phases."""
    
    def __init__(self, parties: int):
        """Initialize a phase barrier for the given number of parties.
        
        Args:
            parties: The number of threads that must call wait() before all are released.
            
        Raises:
            ValueError: If parties < 1.
        """
        if not isinstance(parties, int) or parties < 1:
            raise ValueError("parties must be an integer >= 1")
        
        self.parties = parties
        self._lock = threading.Lock()
        self._count = 0  # Number of threads currently waiting in this phase
        self._arrival_index = 0  # Next arrival index to assign
        self._phase = 0  # Current phase number
        self._condition = threading.Condition(self._lock)
        self._indices = {}  # Maps thread id to assigned arrival index
        
    def wait(self, timeout: Optional[float] = None) -> int:
        """Block until all parties have called wait() for the current phase.
        
        Args:
            timeout: Maximum time to wait in seconds, or None to wait forever.
            
        Returns:
            The arrival index (0 to parties-1) for this thread in this phase.
            
        Raises:
            TimeoutError: If timeout expires before all parties arrive.
        """
        thread_id = threading.get_ident()
        
        with self._condition:
            # Record the phase this thread is entering
            my_phase = self._phase
            
            # Assign arrival index
            my_index = self._arrival_index
            self._arrival_index += 1
            self._count += 1
            self._indices[thread_id] = my_index
            
            # Check if this thread completes the barrier
            if self._count == self.parties:
                # All parties have arrived - release everyone
                self._reset_barrier()
                self._condition.notify_all()
                return my_index
            
            # Wait for all parties to arrive
            while self._phase == my_phase and self._count < self.parties:
                if timeout is not None:
                    if not self._condition.wait(timeout=timeout):
                        # Timeout occurred
                        # Remove this thread from the count
                        if thread_id in self._indices:
                            del self._indices[thread_id]
                        self._count -= 1
                        raise TimeoutError("Barrier wait timed out")
                else:
                    self._condition.wait()
            
            # We were released - return our index
            result = self._indices.get(thread_id, my_index)
            if thread_id in self._indices:
                del self._indices[thread_id]
            return result
    
    def _reset_barrier(self):
        """Reset the barrier for the next phase. Must be called with lock held."""
        self._count = 0
        self._arrival_index = 0
        self._phase += 1
        self._indices.clear()
    
    def n_waiting(self) -> int:
        """Return the number of threads currently blocked in wait().
        
        Returns:
            The count of threads waiting in the current phase.
        """
        with self._lock:
            # Count is the number waiting, but if count == parties, they're all released
            # (or about to be), so return 0
            if self._count == self.parties:
                return 0
            return self._count
