"""Traffic Light State Pattern Implementation"""


class TrafficLight:
    """A traffic light that cycles through green -> yellow -> red -> green."""
    
    # Define the cycle of states
    _STATES = ("green", "yellow", "red")
    
    def __init__(self):
        """Initialize the traffic light in the 'green' state."""
        self._current_state_index = 0
    
    @property
    def state(self) -> str:
        """Return the current state of the traffic light."""
        return self._STATES[self._current_state_index]
    
    def next(self, steps: int = 1) -> str:
        """
        Advance the traffic light cycle by the given number of steps.
        
        Args:
            steps: Number of steps to advance (must be a non-negative integer)
        
        Returns:
            The new state after advancing
        
        Raises:
            ValueError: If steps is not a non-negative integer
        """
        # Validate that steps is an integer (but not a bool, since bool is a subclass of int)
        if isinstance(steps, bool) or not isinstance(steps, int):
            raise ValueError("steps must be a non-negative integer")
        
        # Validate that steps is non-negative
        if steps < 0:
            raise ValueError("steps must be a non-negative integer")
        
        # Advance the state by the given number of steps
        self._current_state_index = (self._current_state_index + steps) % len(self._STATES)
        
        return self.state
