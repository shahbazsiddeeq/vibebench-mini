"""State pattern: a traffic light cycling through green, yellow and red."""
from __future__ import annotations

_CYCLE = ("green", "yellow", "red")


class TrafficLight:
    """A traffic light that advances green -> yellow -> red -> green ..."""

    def __init__(self) -> None:
        self._index = 0

    @property
    def state(self) -> str:
        return _CYCLE[self._index]

    def next(self, steps: int = 1) -> str:
        if not isinstance(steps, int) or isinstance(steps, bool):
            raise ValueError("steps must be an integer")
        if steps < 0:
            raise ValueError("steps must be >= 0")
        self._index = (self._index + steps) % len(_CYCLE)
        return self.state
