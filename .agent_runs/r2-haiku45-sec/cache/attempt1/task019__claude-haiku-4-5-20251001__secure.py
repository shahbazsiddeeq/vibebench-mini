"""
MinStack implementation with O(1) push, pop, top, and get_min operations.
"""


class MinStack:
    """
    A stack that supports push, pop, top, and get_min operations all in O(1) time.
    
    The stack maintains a parallel min-tracking structure to achieve O(1) get_min.
    """
    
    def __init__(self):
        """Initialize an empty MinStack."""
        self._stack = []
        self._min_stack = []
    
    def push(self, val) -> None:
        """
        Push a value onto the stack.
        
        Args:
            val: The value to push onto the stack.
        """
        self._stack.append(val)
        
        # Track the minimum value at each level
        if not self._min_stack:
            self._min_stack.append(val)
        else:
            current_min = self._min_stack[-1]
            # Use <= to handle duplicate minimums correctly
            if val <= current_min:
                self._min_stack.append(val)
            else:
                self._min_stack.append(current_min)
    
    def pop(self) -> int:
        """
        Pop and return the top value from the stack.
        
        Returns:
            The value that was at the top of the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self._stack:
            raise IndexError("pop from empty stack")
        
        self._min_stack.pop()
        return self._stack.pop()
    
    def top(self) -> int:
        """
        Return the top value of the stack without removing it.
        
        Returns:
            The value at the top of the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self._stack:
            raise IndexError("top from empty stack")
        
        return self._stack[-1]
    
    def get_min(self) -> int:
        """
        Return the minimum value in the stack.
        
        Returns:
            The minimum value currently in the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self._min_stack:
            raise IndexError("get_min from empty stack")
        
        return self._min_stack[-1]
