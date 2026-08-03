class MinStack:
    """
    A stack that supports push, pop, top, and retrieving the minimum element
    in O(1) time complexity.
    """

    def __init__(self):
        """
        Initializes an empty MinStack.
        """
        self._stack = []  # Stores tuples of (value, current_min)

    def push(self, val: int) -> None:
        """
        Pushes an element onto the stack.

        Args:
            val: The integer value to push onto the stack.
        """
        # Input validation: Allow any type for val, as per test case _CInt.
        # The problem description implies integers, but the test uses a custom
        # object that behaves like an integer for comparisons.
        # We'll assume the comparison operators are correctly implemented for `val`.

        current_min = val
        if self._stack:
            # If stack is not empty, compare with the current minimum
            # which is the second element of the last tuple in _stack.
            if val > self._stack[-1][1]:
                current_min = self._stack[-1][1]
        
        self._stack.append((val, current_min))

    def pop(self) -> int:
        """
        Removes and returns the element at the top of the stack.

        Raises:
            IndexError: If the stack is empty.

        Returns:
            The value of the element that was removed.
        """
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()[0]

    def top(self) -> int:
        """
        Returns the element at the top of the stack without removing it.

        Raises:
            IndexError: If the stack is empty.

        Returns:
            The value of the element at the top.
        """
        if not self._stack:
            raise IndexError("top from empty stack")
        return self._stack[-1][0]

    def get_min(self) -> int:
        """
        Retrieves the minimum element currently in the stack.

        Raises:
            IndexError: If the stack is empty.

        Returns:
            The minimum value in the stack.
        """
        if not self._stack:
            raise IndexError("get_min from empty stack")
        return self._stack[-1][1]
