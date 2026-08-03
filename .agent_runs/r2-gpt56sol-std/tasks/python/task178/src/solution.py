import math
import threading
import time


class _Waiter:
    __slots__ = ("index", "deadline", "state")

    WAITING = 0
    RELEASED = 1
    TIMED_OUT = 2

    def __init__(self, index, deadline):
        self.index = index
        self.deadline = deadline
        self.state = self.WAITING


class PhaseBarrier:
    """A reusable barrier whose timed-out waiters leave the current phase."""

    def __init__(self, parties: int):
        if parties < 1:
            raise ValueError("parties must be at least 1")
        self._parties = parties
        self._condition = threading.Condition(threading.Lock())
        self._waiters = []

    @property
    def parties(self) -> int:
        return self._parties

    def _expire_waiters_locked(self, now: float) -> None:
        expired = False
        remaining = []

        for waiter in self._waiters:
            if waiter.deadline is not None and waiter.deadline <= now:
                waiter.state = _Waiter.TIMED_OUT
                expired = True
            else:
                waiter.index = len(remaining)
                remaining.append(waiter)

        if expired:
            self._waiters = remaining
            self._condition.notify_all()

    def wait(self, timeout: float | None = None) -> int:
        with self._condition:
            now = time.monotonic()
            self._expire_waiters_locked(now)

            if timeout is None:
                deadline = None
            else:
                timeout_value = float(timeout)
                if math.isnan(timeout_value):
                    timeout_value = 0.0
                deadline = (
                    None
                    if timeout_value == math.inf
                    else now + timeout_value
                )

            waiter = _Waiter(len(self._waiters), deadline)
            self._waiters.append(waiter)

            if len(self._waiters) == self._parties:
                completed = self._waiters
                self._waiters = []
                for participant in completed:
                    participant.state = _Waiter.RELEASED
                self._condition.notify_all()
                return waiter.index

            while True:
                if waiter.state == _Waiter.RELEASED:
                    return waiter.index
                if waiter.state == _Waiter.TIMED_OUT:
                    raise TimeoutError("barrier wait timed out")

                if waiter.deadline is None:
                    self._condition.wait()
                    continue

                remaining = waiter.deadline - time.monotonic()
                if remaining <= 0:
                    if waiter.state == _Waiter.WAITING:
                        self._waiters.remove(waiter)
                        waiter.state = _Waiter.TIMED_OUT
                        for index, participant in enumerate(self._waiters):
                            participant.index = index
                        self._condition.notify_all()
                    raise TimeoutError("barrier wait timed out")

                self._condition.wait(remaining)

    def n_waiting(self) -> int:
        with self._condition:
            self._expire_waiters_locked(time.monotonic())
            return len(self._waiters)
