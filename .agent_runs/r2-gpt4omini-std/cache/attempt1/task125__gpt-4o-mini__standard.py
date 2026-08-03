# src/solution.py

class TrafficLight:
    def __init__(self):
        self.state = 'green'
        self.states = ['green', 'yellow', 'red']
        self.current_index = 0

    def next(self, steps: int = 1) -> str:
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a non-negative integer")
        
        self.current_index = (self.current_index + steps) % len(self.states)
        self.state = self.states[self.current_index]
        return self.state
