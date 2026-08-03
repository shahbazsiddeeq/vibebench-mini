import threading
from typing import Optional


class PhaseBarrier:
    """A reusable synchronization barrier for multiple threads."""
    
    def __init__(self, parties: int):
        """Initialize the barrier with the given number of parties.
        
        Args:
            parties: Number of threads that must call wait() to release the barrier.
            
        Raises:
            ValueError: If parties < 1.
        """
        if parties < 1:
            raise ValueError("parties must be at least 1")
        
        self.parties = parties
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._count = 0  # Number of threads that have arrived in current phase
        self._phase = 0  # Current phase number
        self._indices = []  # Arrival indices for current phase
    
    def wait(self, timeout: Optional[float] = None) -> int:
        """Wait until all parties have arrived at the barrier.
        
        Args:
            timeout: Maximum time to wait in seconds. None means wait forever.
            
        Returns:
            The arrival index (0 to parties-1) for this thread in the current phase.
            
        Raises:
            TimeoutError: If timeout seconds elapse before all parties arrive.
        """
        with self._condition:
            # Record the phase this thread is joining
            current_phase = self._phase
            
            # Assign arrival index to this thread
            arrival_index = self._count
            self._count += 1
            self._indices.append(arrival_index)
            
            # Check if this is the last thread to arrive
            if self._count == self.parties:
                # Last thread arrives - release everyone
                self._phase += 1
                self._count = 0
                self._indices = []
                self._condition.notify_all()
                return arrival_index
            
            # Not the last thread - wait for others
            while self._phase == current_phase:
                try:
                    self._condition.wait(timeout=timeout)
                except Exception:
                    raise
                
                # Check if we were released (phase changed)
                if self._phase != current_phase:
                    # Successfully released
                    return arrival_index
                
                # If we're still in the same phase, timeout occurred
                if timeout is not None:
                    # Remove ourselves from the count
                    self._count -= 1
                    if arrival_index in self._indices:
                        self._indices.remove(arrival_index)
                    raise TimeoutError()
            
            return arrival_index
    
    def n_waiting(self) -> int:
        """Return the number of threads currently blocked in the present phase.
        
        Returns:
            Number of threads waiting in the current phase.
        """
        with self._lock:
            return self._count
