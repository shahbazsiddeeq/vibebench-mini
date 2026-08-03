"""Reusable cyclic phase barrier implemented with standard-library threading."""

from __future__ import annotations

import math
import threading
import time
from typing import Optional


class _Arrival:
    """State associated with one arrival in a phase."""

    __slots__ = ("index",)

    def __init__(self) -> None:
        self.index: Optional[int] = None


class PhaseBarrier:
    """A reusable barrier that assigns indices in arrival order."""

    __slots__ = ("_parties", "_condition", "_generation", "_arrivals")

    def __init__(self, parties: int) -> None:
        if not isinstance(parties, int) or isinstance(parties, bool):
            raise TypeError("parties must be an integer")
        if parties < 1:
            raise ValueError("parties must be at least 1")

        self._parties = parties
        self._condition = threading.Condition(threading.Lock())
        self._generation = 0
        self._arrivals: list[_Arrival] = []

    @property
    def parties(self) -> int:
        """The number of parties required to complete each phase."""
        return self._parties

    @staticmethod
    def _normalize_timeout(timeout: float | None) -> float | None:
        if timeout is None:
            return None
        if not isinstance(timeout, (int, float)):
            raise TypeError("timeout must be a number or None")
        try:
            value = float(timeout)
        except (OverflowError, ValueError):
            raise ValueError("timeout must be a valid number") from None

        if math.isnan(value):
            raise ValueError("timeout must not be NaN")
        if value == math.inf:
            return None
        return max(0.0, value)

    def wait(self, timeout: float | None = None) -> int:
        """Wait for all parties and return this call's arrival index."""
        normalized_timeout = self._normalize_timeout(timeout)
        deadline = (
            None
            if normalized_timeout is None
            else time.monotonic() + normalized_timeout
        )

        with self._condition:
            generation = self._generation
            arrival = _Arrival()
            self._arrivals.append(arrival)

            if len(self._arrivals) == self._parties:
                for index, participant in enumerate(self._arrivals):
                    participant.index = index

                self._arrivals = []
                self._generation += 1
                self._condition.notify_all()
                return self._parties - 1

            try:
                while self._generation == generation:
                    if deadline is None:
                        self._condition.wait()
                        continue

                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        self._arrivals.remove(arrival)
                        raise TimeoutError("barrier wait timed out")

                    self._condition.wait(remaining)
            except BaseException:
                if self._generation == generation:
                    try:
                        self._arrivals.remove(arrival)
                    except ValueError:
                        pass
                raise

            if arrival.index is None:
                raise RuntimeError("barrier synchronization failed")
            return arrival.index

    def n_waiting(self) -> int:
        """Return the number of threads blocked in the current phase."""
        with self._condition:
            return len(self._arrivals)
