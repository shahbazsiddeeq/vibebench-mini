class MinStack:
    """A stack that supports push, pop, top, and get_min operations in O(1) time."""
    
    def __init__(self):
        """Initialize an empty stack."""
        self._stack = []
    
    def push(self, val):
        """
        Push a value onto the stack.
        
        Args:
            val: The value to push (must be comparable)
        """
        if not self._stack:
            # First element - it's also the minimum
            self._stack.append((val, val))
        else:
            # Store the value along with the current minimum
            current_min = self._stack[-1][1]
            new_min = val if val < current_min else current_min
            self._stack.append((val, new_min))
    
    def pop(self):
        """
        Remove and return the top element from the stack.
        
        Returns:
            The value that was at the top of the stack
            
        Raises:
            IndexError: If the stack is empty
        """
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()[0]
    
    def top(self):
        """
        Return the top element without removing it.
        
        Returns:
            The value at the top of the stack
            
        Raises:
            IndexError: If the stack is empty
        """
        if not self._stack:
            raise IndexError("top from empty stack")
        return self._stack[-1][0]
    
    def get_min(self):
        """
        Return the minimum element in the stack.
        
        Returns:
            The minimum value currently in the stack
            
        Raises:
            IndexError: If the stack is empty
        """
        if not self._stack:
            raise IndexError("get_min from empty stack")
        return self._stack[-1][1]
