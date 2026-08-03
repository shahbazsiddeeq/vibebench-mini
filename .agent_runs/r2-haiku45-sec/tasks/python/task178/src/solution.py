import threading
from typing import Optional


class PhaseBarrier:
    """A reusable synchronization barrier for multiple threads."""
    
    def __init__(self, parties: int) -> None:
        """Initialize a PhaseBarrier for the given number of parties.
        
        Args:
            parties: The number of threads that must call wait() to release the barrier.
            
        Raises:
            ValueError: If parties < 1.
        """
        if parties < 1:
            raise ValueError("parties must be at least 1")
        
        self.parties = parties
        self._lock = threading.Lock()
        self._phase = 0
        self._count = 0
        self._arrival_index = 0
        self._release_event = threading.Event()
        self._release_event.set()  # Start in released state for first phase
    
    def wait(self, timeout: Optional[float] = None) -> int:
        """Wait until all parties have called wait() for the current phase.
        
        Args:
            timeout: Maximum seconds to wait. None means wait forever.
            
        Returns:
            The arrival index (0 to parties-1) for this thread in the current phase.
            
        Raises:
            TimeoutError: If timeout seconds elapse before all parties arrive.
        """
        with self._lock:
            # If we're starting a new phase, reset the release event
            if self._count == 0:
                self._release_event.clear()
                self._arrival_index = 0
            
            current_phase = self._phase
            arrival_index = self._arrival_index
            self._arrival_index += 1
            self._count += 1
            
            is_last = self._count == self.parties
            
            if is_last:
                # Last thread to arrive: increment phase and release everyone
                self._phase += 1
                self._count = 0
                self._arrival_index = 0
                self._release_event.set()
        
        # Wait for release outside the lock to avoid deadlock
        if not self._release_event.wait(timeout=timeout):
            # Timeout occurred
            with self._lock:
                # Remove ourselves from the count if we haven't been released yet
                if self._phase == current_phase:
                    self._count -= 1
            raise TimeoutError(f"Barrier timeout after {timeout} seconds")
        
        return arrival_index
    
    def n_waiting(self) -> int:
        """Return the number of threads currently blocked in the present phase.
        
        Returns:
            The number of threads waiting in wait().
        """
        with self._lock:
            return self._count
