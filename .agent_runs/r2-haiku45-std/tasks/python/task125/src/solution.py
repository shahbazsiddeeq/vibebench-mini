class TrafficLight:
    def __init__(self):
        self.state = 'green'
        self._states = ['green', 'yellow', 'red']
    
    def next(self, steps: int = 1) -> str:
        # Validate steps parameter
        # Check if it's a bool (bool is a subclass of int in Python, so check it first)
        if isinstance(steps, bool):
            raise ValueError("steps must be a non-negative integer")
        
        # Check if it's an integer
        if not isinstance(steps, int):
            raise ValueError("steps must be a non-negative integer")
        
        # Check if it's negative
        if steps < 0:
            raise ValueError("steps must be a non-negative integer")
        
        # Find current state index
        current_index = self._states.index(self.state)
        
        # Calculate new index
        new_index = (current_index + steps) % len(self._states)
        
        # Update state
        self.state = self._states[new_index]
        
        return self.state
