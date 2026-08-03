class MinStack:
    """A stack supporting constant-time minimum retrieval."""

    def __init__(self):
        self._stack = []

    def push(self, val):
        if not self._stack:
            current_min = val
        else:
            previous_min = self._stack[-1][1]
            current_min = val if val < previous_min else previous_min
        self._stack.append((val, current_min))

    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty MinStack")
        return self._stack.pop()[0]

    def top(self) -> int:
        if not self._stack:
            raise IndexError("top from empty MinStack")
        return self._stack[-1][0]

    def get_min(self) -> int:
        if not self._stack:
            raise IndexError("get_min from empty MinStack")
        return self._stack[-1][1]
