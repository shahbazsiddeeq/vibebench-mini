class TrafficLight:
    """A traffic light cycling through green, yellow, and red states."""

    _STATES = ("green", "yellow", "red")

    def __init__(self) -> None:
        self.state = "green"

    def next(self, steps: int = 1) -> str:
        """Advance by *steps* states and return the resulting state."""
        if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a non-negative integer")

        current_index = self._STATES.index(self.state)
        self.state = self._STATES[(current_index + steps) % len(self._STATES)]
        return self.state
