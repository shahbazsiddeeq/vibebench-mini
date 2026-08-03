"""
MinStack: a stack that supports push, pop, top and get_min all in O(1) time.
"""


class MinStack:
    """Stack with O(1) push, pop, top and get_min operations."""

    def __init__(self):
        self._stack = []
        self._min_stack = []

    def push(self, val):
        self._stack.append(val)
        if not self._min_stack or val <= self._min_stack[-1]:
            self._min_stack.append(val)
        else:
            self._min_stack.append(self._min_stack[-1])

    def pop(self):
        if not self._stack:
            raise IndexError("pop from empty MinStack")
        self._min_stack.pop()
        return self._stack.pop()

    def top(self):
        if not self._stack:
            raise IndexError("top from empty MinStack")
        return self._stack[-1]

    def get_min(self):
        if not self._min_stack:
            raise IndexError("get_min from empty MinStack")
        return self._min_stack[-1]
