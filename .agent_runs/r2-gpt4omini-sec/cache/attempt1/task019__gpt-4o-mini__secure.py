# src/solution.py

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError("Value must be an integer.")
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> int:
        if not self.stack:
            raise IndexError("pop from empty stack")
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val

    def top(self) -> int:
        if not self.stack:
            raise IndexError("top from empty stack")
        return self.stack[-1]

    def get_min(self) -> int:
        if not self.min_stack:
            raise IndexError("get_min from empty stack")
        return self.min_stack[-1]
