class TrafficLight:
    def __init__(self):
        self._state = "green"
        self._states = ["green", "yellow", "red"]
    
    @property
    def state(self):
        return self._state
    
    def next(self, steps=1):
        # Validate steps - must be a non-negative integer
        # Check if it's a bool first (since bool is a subclass of int in Python)
        if isinstance(steps, bool):
            raise ValueError("steps must be a non-negative integer")
        
        # Check if it's an integer
        if not isinstance(steps, int):
            raise ValueError("steps must be a non-negative integer")
        
        # Check if it's non-negative
        if steps < 0:
            raise ValueError("steps must be a non-negative integer")
        
        # Find current index and advance by steps
        current_index = self._states.index(self._state)
        new_index = (current_index + steps) % len(self._states)
        self._state = self._states[new_index]
        
        return self._state
