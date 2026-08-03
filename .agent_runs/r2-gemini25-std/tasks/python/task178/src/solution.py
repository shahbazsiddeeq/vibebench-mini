import threading
import time


class PhaseBarrier:
    def __init__(self, parties: int):
        if parties < 1:
            raise ValueError("parties must be at least 1")
        self.parties = parties
        self._condition = threading.Condition()
        self._waiting = 0
        self._phase = 0
        self._arrival_index = 0
        self._broken = False

    def wait(self, timeout: float | None = None) -> int:
        with self._condition:
            if self._broken:
                raise threading.BrokenBarrierError("Barrier is in a broken state.")

            current_phase = self._phase
            arrival_index = self._arrival_index
            self._arrival_index += 1
            self._waiting += 1

            if self._waiting == self.parties:
                # Last thread to arrive, trip the barrier
                self._phase += 1
                self._arrival_index = 0
                self._waiting = 0
                self._condition.notify_all()
                return arrival_index
            else:
                # Not the last thread, wait
                try:
                    # Wait until the phase changes (barrier tripped) or timeout
                    if not self._condition.wait(timeout=timeout):
                        # Timeout occurred
                        self._waiting -= 1
                        if self._waiting == 0 and self._arrival_index == self.parties:
                            # If this was the last thread to leave due to timeout
                            # and all others have also left or timed out,
                            # reset arrival_index for the next phase.
                            self._arrival_index = 0
                        elif self._waiting == 0 and self._arrival_index > 0:
                            # If this was the last thread to leave due to timeout
                            # and some threads are still waiting for this phase,
                            # mark barrier as broken.
                            self._broken = True
                            self._condition.notify_all() # Notify others about broken state
                        raise TimeoutError("Timeout occurred while waiting for barrier.")
                    
                    # Check if the barrier was broken while waiting
                    if self._broken and self._phase == current_phase:
                        raise threading.BrokenBarrierError("Barrier is in a broken state.")

                    return arrival_index
                except TimeoutError:
                    # Re-raise TimeoutError after decrementing _waiting
                    raise
                except Exception:
                    # If any other exception occurs, decrement _waiting and re-raise
                    self._waiting -= 1
                    if self._waiting == 0 and self._arrival_index == self.parties:
                        self._arrival_index = 0
                    elif self._waiting == 0 and self._arrival_index > 0:
                        self._broken = True
                        self._condition.notify_all()
                    raise

    def n_waiting(self) -> int:
        with self._condition:
            return self._waiting
