"""
src/solution.py

A reusable cyclic phase barrier implemented on top of threading.Condition.

PhaseBarrier(parties) blocks each calling thread in wait() until `parties`
threads have called wait() for the current phase. When the last thread
arrives, all waiting threads are released together and the barrier
transparently resets for the next phase (it can be reused indefinitely).
"""

import threading
import time


class PhaseBarrier:
    def __init__(self, parties: int):
        if parties < 1:
            raise ValueError("parties must be >= 1")
        self.parties = parties
        self._lock = threading.Condition()
        self._count = 0
        self._generation = 0

    def wait(self, timeout: float = None) -> int:
        with self._lock:
            gen = self._generation
            index = self._count
            self._count += 1

            if self._count == self.parties:
                # This thread trips the barrier: release everyone.
                self._count = 0
                self._generation += 1
                self._lock.notify_all()
                return index

            # Otherwise, wait for the barrier to trip for our generation.
            if timeout is None:
                while gen == self._generation:
                    self._lock.wait()
                return index
            else:
                deadline = time.monotonic() + timeout
                while gen == self._generation:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        # Timed out: remove ourselves from this phase's count.
                        # (Only valid if the phase hasn't already tripped.)
                        if gen == self._generation:
                            self._count -= 1
                        raise TimeoutError(
                            "Timed out waiting for PhaseBarrier"
                        )
                    self._lock.wait(remaining)
                return index

    def n_waiting(self) -> int:
        with self._lock:
            return self._count
