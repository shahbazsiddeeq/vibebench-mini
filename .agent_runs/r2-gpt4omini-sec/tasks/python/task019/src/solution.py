# src/solution.py

class MinStack:
    def __init__(self):
        self._stack = []
        self._min_stack = []

    def push(self, val: int) -> None:
        if not isinstance(val, (int, float)):
            raise ValueError("Value must be an integer or float.")
        
        self._stack.append(val)
        
        if not self._min_stack or val <= self._min_stack[-1]:
            self._min_stack.append(val)

    def pop(self) -> int:
        if not self._stack:
            raise IndexError("Pop from an empty stack.")
        
        val = self._stack.pop()
        
        if val == self._min_stack[-1]:
            self._min_stack.pop()
        
        return val

    def top(self) -> int:
        if not self._stack:
            raise IndexError("Top from an empty stack.")
        
        return self._stack[-1]

    def get_min(self) -> int:
        if not self._min_stack:
            raise IndexError("Get min from an empty stack.")
        
        return self._min_stack[-1]
