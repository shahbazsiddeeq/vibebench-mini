class MinStack:
    """A stack that supports push, pop, top, and get_min operations in O(1) time."""
    
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        """Push a value onto the stack."""
        self.stack.append(val)
        
        # Push the minimum value seen so far onto the min_stack
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            current_min = self.min_stack[-1]
            self.min_stack.append(min(current_min, val))
    
    def pop(self) -> int:
        """Pop and return the top value from the stack."""
        if not self.stack:
            raise IndexError("pop from empty stack")
        
        self.min_stack.pop()
        return self.stack.pop()
    
    def top(self) -> int:
        """Return the top value without removing it."""
        if not self.stack:
            raise IndexError("top from empty stack")
        
        return self.stack[-1]
    
    def get_min(self) -> int:
        """Return the minimum value in the stack."""
        if not self.min_stack:
            raise IndexError("get_min from empty stack")
        
        return self.min_stack[-1]
