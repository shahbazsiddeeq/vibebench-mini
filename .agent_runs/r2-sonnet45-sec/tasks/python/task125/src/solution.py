class TrafficLight:
    """Traffic light that cycles through green -> yellow -> red -> green."""
    
    def __init__(self):
        """Initialize traffic light in green state."""
        self._state = 'green'
        self._states = ['green', 'yellow', 'red']
    
    @property
    def state(self):
        """Get current state of the traffic light."""
        return self._state
    
    def next(self, steps=1):
        """
        Advance the traffic light by the given number of steps.
        
        Args:
            steps: Number of steps to advance (must be non-negative integer)
            
        Returns:
            str: The new state after advancing
            
        Raises:
            ValueError: If steps is not a non-negative integer
        """
        # Validate that steps is an integer (but not a bool, which is a subclass of int)
        if isinstance(steps, bool):
            raise ValueError("steps must be a non-negative integer, not bool")
        
        if not isinstance(steps, int):
            raise ValueError("steps must be a non-negative integer")
        
        if steps < 0:
            raise ValueError("steps must be a non-negative integer")
        
        # Find current position in cycle
        current_index = self._states.index(self._state)
        
        # Calculate new position (modulo to wrap around)
        new_index = (current_index + steps) % len(self._states)
        
        # Update state
        self._state = self._states[new_index]
        
        return self._state
