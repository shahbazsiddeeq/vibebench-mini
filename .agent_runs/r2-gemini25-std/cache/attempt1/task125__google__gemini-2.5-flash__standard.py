class TrafficLight:
    _states = ["green", "yellow", "red"]

    def __init__(self):
        self._state_index = 0
        self.state = self._states[self._state_index]

    def next(self, steps: int = 1) -> str:
        if not isinstance(steps, int) or isinstance(steps, bool):
            raise ValueError("steps must be an integer.")
        if steps < 0:
            raise ValueError("steps must be a non-negative integer.")

        if steps == 0:
            return self.state

        self._state_index = (self._state_index + steps) % len(self._states)
        self.state = self._states[self._state_index]
        return self.state
