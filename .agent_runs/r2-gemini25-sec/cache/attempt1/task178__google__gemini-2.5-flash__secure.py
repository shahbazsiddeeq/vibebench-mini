import threading
import time
import collections

class PhaseBarrier:
    """
    A cyclic barrier that blocks threads until all parties have called wait.

    When the last thread arrives, all waiting threads are released together,
    and the barrier automatically resets for the next phase.
    """

    def __init__(self, parties: int):
        """
        Initializes a new PhaseBarrier.

        Args:
            parties: The number of threads required to trip the barrier.

        Raises:
            ValueError: If parties is less than 1.
        """
        if not isinstance(parties, int) or parties < 1:
            raise ValueError("parties must be an integer greater than or equal to 1")

        self._parties = parties
        self._current_phase = 0
        self._waiting_count = 0
        self._arrival_indices = collections.deque()
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._release_cond = threading.Condition(self._lock) # Condition for threads to wait on after tripping

    @property
    def parties(self) -> int:
        """The number of threads required to trip the barrier."""
        return self._parties

    def n_waiting(self) -> int:
        """Returns the number of threads currently blocked in the present phase."""
        with self._lock:
            return self._waiting_count

    def wait(self, timeout: float | None = None) -> int:
        """
        Blocks the calling thread until all parties have arrived for the current phase.

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

        with self._lock:
            current_phase_at_entry = self._current_phase
            self._waiting_count += 1
            arrival_index = -1 # Will be set if this thread is the one that trips the barrier

            # Assign arrival index
            if len(self._arrival_indices) < self._parties:
                self._arrival_indices.append(self._waiting_count - 1)
                arrival_index = self._waiting_count - 1
            else:
                # This should ideally not happen if logic is correct, but as a safeguard
                # if a thread somehow re-enters without reset, it gets a new index.
                # This path is less likely with the phase check.
                self._arrival_indices.append(self._waiting_count - 1)
                arrival_index = self._waiting_count - 1


            if self._waiting_count == self._parties:
                # This thread is the last one to arrive, trip the barrier
                self._current_phase += 1
                self._waiting_count = 0
                # Notify all waiting threads to wake up
                self._release_cond.notify_all()
                # The arrival indices are now finalized for this phase
                # We need to ensure the order is preserved for return values
                # The deque stores them in arrival order.
                return self._arrival_indices.popleft()
            else:
                # Not the last thread, wait for the barrier to trip or timeout
                # We need to wait on a condition that is specific to this phase
                # to avoid spurious wakeups from previous phases or future phases.
                # The _release_cond is used to signal all threads to proceed.
                # The thread will wait until _current_phase changes, indicating a trip.
                # Or until timeout.
                
                # Store the index for this thread to retrieve it later
                my_assigned_index = self._arrival_indices[-1]

                # Wait for the barrier to trip
                if not self._release_cond.wait(timeout):
                    # Timeout occurred
                    self._waiting_count -= 1
                    # Remove this thread's index from the deque if it hasn't been processed yet
                    # This is tricky because other threads might have already popped.
                    # A simpler approach is to just let the deque clear on trip.
                    # If a thread times out, its index is effectively lost for this phase.
                    # The problem statement implies that a timed-out thread "removes itself
                    # from the current phase's count". This means it should not contribute
                    # to the `parties` count for this phase.
                    
                    # To correctly remove the index, we need to find and remove it.
                    # This is inefficient for a deque, but given small `parties`, it's acceptable.
                    try:
                        # Find and remove the specific index assigned to this thread
                        # This assumes arrival_indices stores the actual return values.
                        # If it stores the temporary _waiting_count, then it's different.
                        # Let's assume it stores the final return values.
                        # The problem states "arrival index for that phase, an integer 0..parties-1,
                        # where the first thread to arrive gets 0 and the thread that trips the barrier gets parties-1."
                        # So, _arrival_indices should store these 0..parties-1 values.
                        # The current implementation assigns _waiting_count - 1 as the index.
                        # This means the deque contains 0, 1, 2, ... up to _waiting_count - 1.
                        # If a thread times out, its assigned index needs to be removed.
                        
                        # This is a critical section for _arrival_indices.
                        # If a thread times out, it should not affect the indices of others.
                        # The simplest way to handle this is to only assign final indices
                        # when the barrier trips. But the problem implies indices are assigned on arrival.
                        
                        # Let's re-think: The indices are 0..parties-1.
                        # The first thread gets 0, second 1, etc.
                        # The `_arrival_indices` deque should store these in order.
                        # When a thread calls wait, it gets the next available index.
                        # If it times out, that index is "lost" for this phase.
                        # The next phase will start fresh.
                        
                        # The current `_arrival_indices.append(self._waiting_count - 1)`
                        # correctly assigns 0, 1, 2...
                        # If a thread times out, its index is in the deque.
                        # We need to remove it.
                        
                        # This is problematic if the deque is used for final return order.
                        # A better approach for indices might be to assign them only when
                        # the barrier trips, or to use a list and mark slots.
                        
                        # Let's stick to the current `_arrival_indices` as the source of truth
                        # for return values. If a thread times out, its index is still in the deque.
                        # This means the deque will have `parties` elements when tripped,
                        # but some might correspond to timed-out threads.
                        # This contradicts "removes itself from the current phase's count".
                        
                        # A more robust way:
                        # Each thread gets a unique ID for the phase.
                        # When `wait` is called, we increment `_waiting_count`.
                        # The `_arrival_indices` should be a list of `(thread_id, index)`
                        # or just `index` if we can guarantee order.
                        
                        # Let's assume `_arrival_indices` stores the actual return values.
                        # If a thread times out, its index should not be returned.
                        # The problem states "returns the arrival index for that phase, an integer 0..parties-1".
                        # This implies the set of returned indices for a successful phase is exactly {0, 1, ..., parties-1}.
                        
                        # If a thread times out, it means it didn't successfully participate in the phase.
                        # Its assigned index should not be part of the final set of indices for that phase.
                        # This means the `_arrival_indices` deque should only contain indices of threads
                        # that successfully waited.
                        
                        # This implies that if a thread times out, its index must be removed from the deque.
                        # But `deque.remove()` is O(N). For small `parties`, it's fine.
                        
                        # Let's try to remove the assigned index if timeout occurs.
                        # This is only safe if `_arrival_indices` is not being popped by other threads.
                        # The `_arrival_indices` is only popped when the barrier trips.
                        # So, during the waiting phase, it's safe to remove.
                        self._arrival_indices.remove(my_assigned_index)
                    except ValueError:
                        # Should not happen if logic is correct, but handle defensively
                        pass
                    raise TimeoutError("Barrier timeout")

                # If we reach here, the barrier was tripped.
                # The `_release_cond.wait()` returned True, meaning `notify_all` was called.
                # The `_current_phase` has been incremented by the tripping thread.
                # We need to ensure we get our correct arrival index.
                # The tripping thread already popped its index.
                # Other threads need to pop their indices in order.
                
                # This requires a careful dance. The `_arrival_indices` deque is populated
                # in arrival order. The tripping thread pops the last one (parties-1).
                # The other threads should pop their respective indices.
                # This means the deque should be popped `parties` times in total.
                # The tripping thread pops one. The other `parties-1` threads need to pop one each.
                
                # The current implementation of `_arrival_indices.popleft()` for the tripping thread
                # is incorrect if it's supposed to get `parties-1`.
                # The problem states: "the first thread to arrive gets 0 and the thread that trips the barrier gets parties-1."
                # This means the indices are assigned based on arrival order, and the last one to arrive
                # (which trips the barrier) gets `parties-1`.
                
                # Let's re-design `_arrival_indices` and index assignment.
                # We need to store the indices in the order they should be returned.
                # A simple list `_arrival_order` can store the indices 0 to parties-1.
                # When a thread arrives, it claims the next available index.
                
                # New approach for indices:
                # `_arrival_order_map`: a dictionary mapping thread_id to assigned_index.
                # Or, simpler, a list of `(thread_id, assigned_index)` tuples.
                # Or, even simpler, just assign `_waiting_count - 1` as the index.
                # The problem is that `_waiting_count` resets, but the indices need to be stable.
                
                # Let's use a list to store the assigned indices for the current phase.
                # `_phase_indices`: list of indices [0, 1, ..., parties-1] in arrival order.
                # When a thread arrives, it gets `len(_phase_indices)` as its index.
                # This list is cleared on reset.
                
                # Resetting the barrier:
                # The tripping thread increments `_current_phase`.
                # It also clears `_phase_indices` and `_waiting_count`.
                # All other threads, after waking up, will see the new `_current_phase`.
                # They need to retrieve their assigned index from somewhere.
                
                # This implies that the index must be stored per-thread or in a way
                # that each thread can retrieve its own.
                
                # Let's use a `collections.deque` to store the indices in arrival order.
                # When a thread arrives, it appends its index to the deque.
                # When the barrier trips, all threads pop their index from the deque.
                # The tripping thread gets the last one (parties-1).
                # The first thread gets 0.
                # This means the deque should be popped from the right for the last thread,
                # and from the left for the first thread. This is not a simple deque usage.
                
                # A list of `(thread_id, index)` tuples, or just `index` if we can guarantee order.
                # Let's use a list `_arrival_order_list` to store the indices in arrival order.
                # When a thread arrives, it appends its index `self._waiting_count - 1` to this list.
                # When the barrier trips, the list is complete.
                # Each thread needs to retrieve its specific index from this list.
                # This means the list needs to be stable until all threads have retrieved their index.
                
                # Let's try this:
                # `_arrival_indices_for_phase`: a list that stores the assigned index for each thread.
                # When a thread arrives, it gets `len(_arrival_indices_for_phase)` as its index.
                # This list is built up.
                # When the barrier trips, this list is complete.
                # Each thread needs to retrieve its index from this list.
                # The list is then cleared for the next phase.
                
                # Re-attempting index management:
                # `_arrival_order_list`: A list to store the arrival order of indices for the current phase.
                # When a thread calls `wait`, it gets `len(_arrival_order_list)` as its index.
                # This index is stored in `_arrival_order_list`.
                # If a thread times out, its index needs to be removed from `_arrival_order_list`.
                # When the barrier trips, `_arrival_order_list` contains `parties` elements.
                # Each thread needs to retrieve its specific index.
                # This implies that the index must be returned directly by the `wait` call.
                # So, the tripping thread returns its index.
                # The other threads, after waking up, need to know their index.
                # This means the index must be assigned and stored *before* waiting.
                
                # Let's use a `collections.deque` to store the indices that are *available* to be returned.
                # When the barrier trips, the deque is populated with `0, 1, ..., parties-1`.
                # Each thread, upon waking, pops an index from the deque.
                # This doesn't guarantee "first thread gets 0", "last thread gets parties-1".
                # It guarantees that the set of returned indices is {0, ..., parties-1}.
                
                # To guarantee "first thread gets 0, last thread gets parties-1":
                # Each thread needs to know its arrival order.
                # `_arrival_order_counter`: an integer, incremented on each arrival.
                # `my_arrival_order = self._arrival_order_counter - 1`.
                # This `my_arrival_order` is the index to be returned.
                # This needs to be stored per-thread.
                
                # Let's use a dictionary `_thread_indices` to map `threading.get_ident()` to the assigned index.
                # This dictionary is cleared on phase reset.
                
                # Final attempt at index management:
                # `_arrival_indices_map`: dict[int, int] maps thread_ident to its assigned index for the current phase.
                # `_current_arrival_idx`: int, increments from 0 to parties-1 for each phase.
                
                # Inside `wait`:
                # 1. Acquire lock.
                # 2. Check `_current_phase_id` to ensure we're in the correct phase.
                # 3. Assign `my_index = self._current_arrival_idx`.
                # 4. Store `_arrival_indices_map[threading.get_ident()] = my_index`.
                # 5. Increment `self._current_arrival_idx`.
                # 6. Increment `self._waiting_count`.
                
                # If `_waiting_count == self._parties`:
                #    a. Barrier trips.
                #    b. Increment `_current_phase_id`.
                #    c. Reset `_waiting_count = 0`.
                #    d. Reset `_current_arrival_idx = 0`.
                #    e. Notify all waiting threads.
                #    f. Return `my_index`.
                # Else (not tripping thread):
                #    a. Wait on `_release_cond`.
                #    b. If timeout:
                #       i. Decrement `_waiting_count`.
                #       ii. Remove `threading.get_ident()` from `_arrival_indices_map`.
                #       iii. Raise `TimeoutError`.
                #    c. If woke up (not timeout):
                #       i. Retrieve `my_index` from `_arrival_indices_map`.
                #       ii. Remove `threading.get_ident()` from `_arrival_indices_map` (cleanup).
                #       iii. Return `my_index`.
                
                # This seems more robust.
                
                # Let's refine the `_arrival_indices_map` and `_current_arrival_idx` logic.
                # The `_current_arrival_idx` should be the index assigned to the *next* arriving thread.
                # So, `my_index = self._current_arrival_idx`.
                # Then `self._current_arrival_idx += 1`.
                
                # The `_arrival_indices_map` needs to be cleared *after* all threads have retrieved their index.
                # This means the tripping thread cannot clear it immediately.
                # This implies a two-phase barrier or a more complex state machine.
                
                # Let's simplify. The problem states "returns the arrival index for that phase, an integer 0..parties-1".
                # This means the *set* of returned values is {0, ..., parties-1}.
                # The specific mapping "first gets 0, last gets parties-1" is a strong hint.
                
                # Let's use a `collections.deque` to store the indices in the order they are assigned.
                # `_assigned_indices_queue`: stores the indices 0, 1, ..., parties-1 in arrival order.
                # When a thread arrives, it appends `self._waiting_count - 1` to this queue.
                # When the barrier trips, this queue is full.
                # The tripping thread gets `_assigned_indices_queue.pop()`. (last one)
                # Other threads get `_assigned_indices_queue.popleft()`. (first ones)
                # This requires the deque to be accessible by all.
                
                # This is still tricky. The `pop()` and `popleft()` need to be coordinated.
                
                # Let's go back to the original `_arrival_indices` deque.
                # It stores `0, 1, ..., parties-1` in arrival order.
                # When the barrier trips, the `_arrival_indices` deque contains `[0, 1, ..., parties-1]`.
                # The tripping thread needs to return `parties-1`.
                # The first thread needs to return `0`.
                # This means the deque needs to be consumed in a specific order.
                
                # A simpler approach for indices:
                # `_arrival_order_list`: a list of `parties` elements.
                # When a thread arrives, it claims the next available slot in this list.
                # `_next_available_index_slot = 0`
                # `my_index = _next_available_index_slot`
                # `_arrival_order_list[my_index] = threading.get_ident()`
                # `_next_available_index_slot += 1`
                
                # This is getting too complex. Let's assume the simplest interpretation:
                # The `wait` method returns an index from 0 to parties-1.
                # The *set* of indices returned by `parties` threads is {0, ..., parties-1}.
                # The specific mapping (first gets 0, last gets parties-1) is a strong hint,
                # but might be an implementation detail rather than a strict requirement for *all* cases.
                # If it's a strict requirement, the implementation becomes much harder.
                
                # Let's assume the simplest: `_arrival_indices` deque stores the indices 0, 1, ...
                # in the order they are assigned.
                # When the barrier trips, the deque is full.
                # The tripping thread gets the last assigned index.
                # Other threads get their assigned index from the deque.
                
                # Let's use a `_thread_arrival_map` to store the assigned index for each thread.
                # This map is cleared when the barrier trips.
                
                # Re-attempt with `_thread_arrival_map` and `_current_arrival_idx`:
                
                # State variables for the current phase:
                # `_current_phase_id`: An integer representing the current phase. Incremented when barrier trips.
                # `_waiting_count`: Number of threads currently waiting in the current phase.
                # `_current_arrival_idx`: The next index to be assigned (0 to parties-1).
                # `_thread_arrival_map`: Maps `threading.get_ident()` to the assigned index for the current phase.
                # `_lock`: Protects all state variables.
                # `_cond`: Condition for threads to wait on until the barrier trips.
                
                # When `wait` is called:
                # 1. Acquire `_lock`.
                # 2. Record `phase_at_entry = self._current_phase_id`.
                # 3. Assign `my_index = self._current_arrival_idx`.
                # 4. Store `self._thread_arrival_map[threading.get_ident()] = my_index`.
                # 5. Increment `self._current_arrival_idx`.
                # 6. Increment `self._waiting_count`.
                
                # If `self._waiting_count == self._parties`: (Tripping thread)
                #    a. Increment `self._current_phase_id`.
                #    b. Reset `self._waiting_count = 0`.
                #    c. Reset `self._current_arrival_idx = 0`.
                #    d. `self._cond.notify_all()`.
                #    e. Return `my_index`.
                # Else (Waiting thread):
                #    a. Loop while `self._current_phase_id == phase_at_entry`:
                #       i. If `self._cond.wait(timeout)` returns `False` (timeout):
                #          1. Decrement `self._waiting_count`.
                #          2. Remove `threading.get_ident()` from `self._thread_arrival_map`.
                #          3. Raise `TimeoutError`.
                #    b. After loop (barrier tripped):
                #       i. Retrieve `my_index` from `self._thread_arrival_map`.
                #       ii. Remove `threading.get_ident()` from `self._thread_arrival_map` (cleanup).
                #       iii. Return `my_index`.
                
                # This looks like a solid plan. The `_thread_arrival_map` will be cleared implicitly
                # as threads retrieve their index and remove themselves.
                # The `_current_arrival_idx` is reset by the tripping thread.
                
                # Let's implement this.

            current_phase_at_entry = self._current_phase
            
            # Assign arrival index for this thread
            my_index = self._current_arrival_idx
            self._thread_arrival_map[threading.get_ident()] = my_index
            self._current_arrival_idx += 1
            self._waiting_count += 1

            if self._waiting_count == self._parties:
                # This thread is the last one to arrive, trip the barrier
                self._current_phase += 1
                self._waiting_count = 0
                self._current_arrival_idx = 0 # Reset for the next phase
                self._cond.notify_all() # Wake up all waiting threads
                return my_index
            else:
                # Not the last thread, wait for the barrier to trip or timeout
                # We need to wait until the phase ID changes, indicating the barrier has tripped.
                # If timeout occurs, we remove ourselves from the count.
                
                # The loop is crucial to handle spurious wakeups and ensure the phase ID has changed.
                # The `_cond.wait()` returns False on timeout.
                
                # Store the start time for timeout calculation if needed in the loop
                start_time = time.monotonic()
                remaining_timeout = timeout

                while self._current_phase == current_phase_at_entry:
                    if not self._cond.wait(remaining_timeout):
                        # Timeout occurred
                        self._waiting_count -= 1
                        # Remove this thread's index from the map
                        if threading.get_ident() in self._thread_arrival_map:
                            del self._thread_arrival_map[threading.get_ident()]
                        raise TimeoutError("Barrier timeout")
                    
                    # If woke up, recalculate remaining timeout if in a loop
                    if timeout is not None:
                        elapsed_time = time.monotonic() - start_time
                        remaining_timeout = timeout - elapsed_time
                        if remaining_timeout <= 0:
                            # If we woke up but timeout has effectively passed, treat as timeout
                            self._waiting_count -= 1
                            if threading.get_ident() in self._thread_arrival_map:
                                del self._thread_arrival_map[threading.get_ident()]
                            raise TimeoutError("Barrier timeout")

                # Barrier has tripped, retrieve our assigned index
                # It's possible another thread timed out and removed our entry,
                # but that should not happen if we successfully waited.
                # Defensive check:
                if threading.get_ident() not in self._thread_arrival_map:
                    # This indicates an error in logic or unexpected state.
                    # For robustness, we could raise an internal error or return a default.
                    # Given the problem constraints, this path should ideally not be hit.
                    # If it is, it means the map was cleared prematurely or our entry was lost.
                    # Let's raise an error to indicate an internal inconsistency.
                    raise RuntimeError("Internal error: Thread's arrival index lost after barrier trip.")
                
                ret_index = self._thread_arrival_map[threading.get_ident()]
                del self._thread_arrival_map[threading.get_ident()] # Clean up
                return ret_index

    # Redefine __init__ with the new state variables
    def __init__(self, parties: int):
        if not isinstance(parties, int) or parties < 1:
            raise ValueError("parties must be an integer greater than or equal to 1")

        self._parties = parties
        self._current_phase = 0 # Incremented when barrier trips
        self._waiting_count = 0 # Number of threads currently waiting
        self._current_arrival_idx = 0 # Next index to assign (0 to parties-1)
        self._thread_arrival_map = {} # Maps thread_ident to assigned index
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock) # Condition for threads to wait on
