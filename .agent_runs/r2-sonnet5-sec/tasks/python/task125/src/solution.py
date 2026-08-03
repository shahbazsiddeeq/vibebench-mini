"""
State Pattern (Traffic Light) implementation.

This module defines a TrafficLight class that cycles through the states
'green' -> 'yellow' -> 'red' -> 'green' ... using the next() method.

Security considerations:
- All external inputs (the `steps` argument) are strictly validated.
- No use of eval/exec or dynamic code execution.
- No I/O operations are performed.
- Errors are raised with clear, non-sensitive messages (no internal state
  or stack details leaked).
"""

from typing import Tuple


class TrafficLight:
    """A simple state machine representing a traffic light."""

    _STATES: Tuple[str, str, str] = ("green", "yellow", "red")

    def __init__(self) -> None:
        self._index: int = 0  # 'green' is the initial state

    @property
    def state(self) -> str:
        """Return the current state of the traffic light."""
        return self._STATES[self._index]

    def next(self, steps: int = 1) -> str:
        """
        Advance the traffic light by `steps` steps and return the new state.

        :param steps: Non-negative integer number of steps to advance.
                       Must be a strict int (bool is rejected) and >= 0.
        :raises ValueError: If steps is not a non-negative integer.
        :return: The new state after advancing.
        """
        # Reject bool explicitly since bool is a subclass of int.
        if isinstance(steps, bool) or not isinstance(steps, int):
            raise ValueError("steps must be a non-negative integer")

        if steps < 0:
            raise ValueError("steps must be a non-negative integer")

        self._index = (self._index + steps) % len(self._STATES)
        return self.state
