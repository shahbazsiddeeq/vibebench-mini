import threading


class PhaseBarrier:
    """A reusable (cyclic) barrier that releases all parties for each phase."""

    def __init__(self, parties):
        if parties < 1:
            raise ValueError("parties must be at least 1")
        self.parties = parties
        self._count = 0
        self._phase = 0
        self._cond = threading.Condition()

    def wait(self, timeout=None):
        with self._cond:
            phase = self._phase
            index = self._count
            self._count += 1

            if self._count == self.parties:
                # Last arrival trips the barrier and opens the next phase.
                self._count = 0
                self._phase += 1
                self._cond.notify_all()
                return index

            if self._cond.wait_for(lambda: self._phase != phase, timeout):
                return index

            # Timed out: back out of this phase if it has not tripped yet.
            if self._phase == phase:
                self._count -= 1
            raise TimeoutError("barrier phase did not complete in time")

    def n_waiting(self):
        with self._cond:
            return self._count
