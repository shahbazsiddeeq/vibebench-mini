import threading
import time
import collections
import secrets

class PhaseBarrier:
    """
    A reusable synchronization barrier that blocks threads until a specified
    number of 'parties' have all called wait(). When the last thread arrives,
    all waiting threads are released simultaneously, and the barrier resets
    for the next phase.
    """

    def __init__(self, parties: int):
        """
        Initializes a new PhaseBarrier.

        Args:
            parties: The number of threads that must call wait() before the
                     barrier is tripped.

        Raises:
            ValueError: If parties is less than 1.
        """
        if not isinstance(parties, int):
            raise TypeError("parties must be an integer")
        if parties < 1:
            raise ValueError("parties must be at least 1")

        self.parties = parties
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._waiting_count = 0
        self._current_phase = 0
        self._arrival_order = collections.deque() # Stores arrival order for current phase
        self._arrival_indices = {} # Maps thread_id to arrival index for current phase

    def wait(self, timeout: float | None = None) -> int:
        """
        Blocks the calling thread until exactly 'parties' threads have called
        wait() for the current phase. When the last thread arrives, all waiting
        threads are released together, and the barrier automatically resets
        for the next phase.

        Args:
            timeout: The maximum time in seconds to wait. If None, waits indefinitely.

        Returns:
            The arrival index for that phase (an integer 0..parties-1).

        Raises:
            TimeoutError: If the timeout expires before all parties arrive.
        """
        if timeout is not None and not isinstance(timeout, (int, float)):
            raise TypeError("timeout must be a float or None")
        if timeout is not None and timeout < 0:
            raise ValueError("timeout must be non-negative")

        thread_id = threading.get_ident()
        arrival_index = -1
        
        with self._lock:
            current_phase_at_entry = self._current_phase

            # Check if this thread has already arrived in this phase
            if thread_id in self._arrival_indices:
                # This should not happen in a correctly used barrier,
                # but if it does, it indicates a misuse (e.g., calling wait twice
                # without the barrier resetting). We'll treat it as a new arrival
                # for robustness, but it might lead to unexpected behavior if not
                # intended. For a strict barrier, one might raise an error here.
                pass

            self._waiting_count += 1
            self._arrival_order.append(thread_id)
            self._arrival_indices[thread_id] = len(self._arrival_order) - 1
            arrival_index = self._arrival_indices[thread_id]

            if self._waiting_count < self.parties:
                # Not enough parties yet, wait
                try:
                    # Wait for the barrier to trip or timeout
                    # The predicate checks if the phase has advanced (barrier tripped)
                    # or if the thread was removed due to timeout (not implemented here,
                    # but a more complex barrier might have a mechanism for this).
                    # For this barrier, a thread only leaves wait() if the phase advances.
                    if not self._condition.wait_for(lambda: self._current_phase > current_phase_at_entry, timeout):
                        # Timeout occurred
                        self._waiting_count -= 1
                        # Remove this thread from arrival order and indices
                        # This is tricky if it's not the last one.
                        # A simpler approach for timeout is to just let it raise and
                        # assume the user handles the state.
                        # For this specific barrier, if a thread times out, it must
                        # remove itself from the current phase's count.
                        # This means we need to re-evaluate arrival_order and indices.
                        # This is a critical section for timeout handling.
                        
                        # Rebuild arrival_order and indices without the timed-out thread
                        # This is inefficient for many threads, but correct.
                        new_arrival_order = collections.deque()
                        new_arrival_indices = {}
                        idx_counter = 0
                        for tid in self._arrival_order:
                            if tid != thread_id:
                                new_arrival_order.append(tid)
                                new_arrival_indices[tid] = idx_counter
                                idx_counter += 1
                        self._arrival_order = new_arrival_order
                        self._arrival_indices = new_arrival_indices

                        # If the timed-out thread was the last one to arrive,
                        # and now there are fewer than parties, the barrier won't trip.
                        # If it was not the last, the barrier might still trip with others.
                        
                        # Notify other threads if the count changed and they might be waiting
                        # for this thread. This is complex. The simplest interpretation
                        # of "removes itself from the current phase's count" is that
                        # it decrements _waiting_count and then raises.
                        # The other threads will continue waiting for the original 'parties'
                        # count, which is problematic.
                        # A robust timeout requires a more complex state management
                        # where the barrier can be "broken" or "cancelled".

                        # Given the problem description, "removes itself from the current
                        # phase's count", we decrement _waiting_count. The other threads
                        # will still be waiting for self.parties. If self.parties is
                        # no longer reachable, they will eventually timeout too.
                        # This implies a "broken" barrier state.

                        raise TimeoutError("Barrier timed out")
                except Exception:
                    # Ensure cleanup if an exception occurs during wait_for
                    # (e.g., if the thread is interrupted, though Python threads
                    # don't have direct interruption).
                    # The problem statement implies TimeoutError is the only
                    # exception from wait().
                    raise
            else:
                # This thread is the last one to arrive, trip the barrier
                self._current_phase += 1
                self._waiting_count = 0
                self._arrival_order.clear()
                self._arrival_indices.clear()
                self._condition.notify_all() # Release all waiting threads

        return arrival_index

    def n_waiting(self) -> int:
        """
        Returns the number of threads currently blocked in the present phase.
        """
        with self._lock:
            return self._waiting_count
