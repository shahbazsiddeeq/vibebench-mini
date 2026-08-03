# src/solution.py

class TrafficLight:
    def __init__(self):
        self._states = ['green', 'yellow', 'red']
        self._current_index = 0
        self.state = self._states[self._current_index]

    def next(self, steps: int = 1) -> str:
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a non-negative integer")
        
        self._current_index = (self._current_index + steps) % len(self._states)
        self.state = self._states[self._current_index]
        return self.state
