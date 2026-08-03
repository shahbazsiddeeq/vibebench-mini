"""Traffic light state machine implementation."""

from __future__ import annotations


class TrafficLight:
    """Cycle through green, yellow, and red traffic-light states."""

    _STATES = ("green", "yellow", "red")

    def __init__(self) -> None:
        self._state_index = 0

    @property
    def state(self) -> str:
        """Return the current traffic-light state."""
        return self._STATES[self._state_index]

    def next(self, steps: int = 1) -> str:
        """Advance by *steps* states and return the resulting state."""
        if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a non-negative integer")

        self._state_index = (self._state_index + steps) % len(self._STATES)
        return self.state
