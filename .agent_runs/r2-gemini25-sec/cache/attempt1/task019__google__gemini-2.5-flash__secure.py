class MinStack:
    """
    A stack that supports push, pop, top, and retrieving the minimum element in O(1) time.
    """

    def __init__(self):
        """
        Initializes an empty MinStack.
        The stack stores tuples of (value, current_minimum).
        """
        self._stack = []

    def push(self, val: int) -> None:
        """
        Pushes an element onto the stack.

        Args:
            val: The integer value to push onto the stack.
        """
        # Input validation: Ensure val is an integer.
        if not isinstance(val, int):
            raise TypeError("Value must be an integer.")

        if not self._stack:
            self._stack.append((val, val))
        else:
            current_min = self._stack[-1][1]
            self._stack.append((val, min(val, current_min)))

    def pop(self) -> int:
        """
        Removes the element on top of the stack and returns it.

        Returns:
            The integer value that was popped from the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()[0]

    def top(self) -> int:
        """
        Get the top element without removing it.

        Returns:
            The integer value at the top of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self._stack:
            raise IndexError("top from empty stack")
        return self._stack[-1][0]

    def get_min(self) -> int:
        """
        Retrieves the minimum element in the stack.

        Returns:
            The minimum integer value currently in the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self._stack:
            raise IndexError("get_min from empty stack")
        return self._stack[-1][1]
