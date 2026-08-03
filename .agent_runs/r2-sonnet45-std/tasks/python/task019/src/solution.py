class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            # Store the minimum between current val and previous minimum
            self.min_stack.append(min(val, self.min_stack[-1]))
    
    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        self.min_stack.pop()
        return self.stack.pop()
    
    def top(self):
        if not self.stack:
            raise IndexError("top from empty stack")
        return self.stack[-1]
    
    def get_min(self):
        if not self.min_stack:
            raise IndexError("get_min from empty stack")
        return self.min_stack[-1]
