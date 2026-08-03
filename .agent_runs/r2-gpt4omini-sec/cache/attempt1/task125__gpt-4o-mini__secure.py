# src/solution.py

class TrafficLight:
    def __init__(self):
        self.state = 'green'
        self.states = ['green', 'yellow', 'red']

    def next(self, steps: int = 1) -> str:
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a non-negative integer")
        
        # Calculate the new state index
        current_index = self.states.index(self.state)
        new_index = (current_index + steps) % len(self.states)
        self.state = self.states[new_index]
        
        return self.state
