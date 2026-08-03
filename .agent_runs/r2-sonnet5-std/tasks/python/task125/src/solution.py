class TrafficLight:
    _CYCLE = ('green', 'yellow', 'red')

    def __init__(self):
        self._index = 0

    @property
    def state(self) -> str:
        return self._CYCLE[self._index]

    def next(self, steps: int = 1) -> str:
        if isinstance(steps, bool) or not isinstance(steps, int):
            raise ValueError("steps must be a non-negative integer")
        if steps < 0:
            raise ValueError("steps must be a non-negative integer")
        self._index = (self._index + steps) % len(self._CYCLE)
        return self.state
