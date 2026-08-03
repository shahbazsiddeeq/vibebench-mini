"""
src/solution.py

A reusable cyclic phase barrier built entirely from the standard library's
``threading`` primitives.

Security / robustness notes
----------------------------
* All public inputs are validated (``parties`` must be a positive integer,
  ``timeout`` must be ``None`` or a non-negative real number) and invalid
  values raise well-defined exceptions with sanitized messages -- no
  internal state or stack traces are ever exposed to the caller.
* No use of ``eval``/``exec`` or any dynamic code execution.
* No randomness is required for this synchronization primitive, so the
  ``secrets`` module is not applicable here; the implementation relies
  solely on ``threading.Condition`` for correctness and thread-safety.
* All shared mutable state is protected by a single lock (the condition's
  internal lock), preventing race conditions between concurrent callers.
"""

from __future__ import annotations

import threading
import time
from numbers import Real


class PhaseBarrier:
    """A reusable (cyclic) barrier for synchronizing a fixed number of threads.

    ``parties`` threads must call :meth:`wait` for the barrier to trip; once
    tripped, all waiting threads are released simultaneously and the barrier
    automatically resets to be used again for the next phase.
    """

    __slots__ = ("parties", "_condition", "_count", "_generation")

    def __init__(self, parties: int) -> None:
        if isinstance(parties, bool) or not isinstance(parties, int):
            raise ValueError("parties must be an integer >= 1")
        if parties < 1:
            raise ValueError("parties must be an integer >= 1")

        self.parties = parties
        self._condition = threading.Condition()
        self._count = 0
        self._generation = 0

    def wait(self, timeout: float | None = None) -> int:
        """Block until ``parties`` threads have called ``wait`` for this phase.

        Returns the zero-based arrival index for the calling thread within
        the current phase (0 for the first arrival, ``parties - 1`` for the
        thread that trips the barrier).

        Raises ``TimeoutError`` if ``timeout`` seconds elapse before the
        barrier trips, and ``ValueError`` if ``timeout`` is invalid.
        """
        if timeout is not None:
            if isinstance(timeout, bool) or not isinstance(timeout, Real):
                raise ValueError("timeout must be a real number or None")
            if timeout < 0:
                raise ValueError("timeout must be non-negative")
            timeout = float(timeout)

        with self._condition:
            generation = self._generation
            index = self._count
            self._count += 1

            if self._count == self.parties:
                # This thread trips the barrier: release everyone and
                # advance to the next generation/phase.
                self._generation += 1
                self._count = 0
                self._condition.notify_all()
                return index

            # Otherwise wait for the barrier to trip, being careful to
            # handle spurious wakeups and honoring the overall timeout.
            deadline = None if timeout is None else (time.monotonic() + timeout)

            while generation == self._generation:
                if deadline is None:
                    self._condition.wait()
                else:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        woke = False
                    else:
                        woke = self._condition.wait(timeout=remaining)

                    if not woke and generation == self._generation:
                        # Timed out without the barrier tripping: remove
                        # ourselves from the current phase's count.
                        self._count -= 1
                        raise TimeoutError(
                            "timed out waiting for other parties to arrive"
                        )

            return index

    def n_waiting(self) -> int:
        """Return how many threads are currently blocked in the present phase."""
        with self._condition:
            return self._count
