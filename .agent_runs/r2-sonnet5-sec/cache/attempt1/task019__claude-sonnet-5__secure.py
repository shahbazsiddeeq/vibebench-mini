"""
A secure, self-contained implementation of a MinStack data structure.

The MinStack supports push, pop, top, and get_min operations, all in O(1)
time complexity. It raises IndexError on pop/top/get_min when the stack
is empty, mirroring the behavior of standard Python list operations on
empty sequences.

This module uses only the Python standard library and avoids any use of
eval/exec or external/untrusted data sources.
"""

from typing import Any, List, Tuple


class MinStack:
    """
    A stack that supports push, pop, top, and retrieving the minimum
    element, all in O(1) time.

    Internally, this is implemented using a single list of tuples,
    where each tuple stores (value, current_min_at_this_point). This
    avoids needing two separate stacks to stay in sync and keeps the
    implementation simple and correct.
    """

    __slots__ = ("_stack",)

    def __init__(self) -> None:
        # Each element is a tuple (value, min_so_far)
        self._stack: List[Tuple[Any, Any]] = []

    def push(self, val: Any) -> None:
        """
        Push a value onto the stack. O(1) time.
        """
        if self._stack:
            current_min = self._stack[-1][1]
            # Use '<' to minimize comparison calls (only one comparison).
            new_min = val if val < current_min else current_min
        else:
            new_min = val
        self._stack.append((val, new_min))

    def pop(self) -> Any:
        """
        Remove and return the top value of the stack. O(1) time.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self._stack:
            raise IndexError("pop from empty MinStack")
        val, _ = self._stack.pop()
        return val

    def top(self) -> Any:
        """
        Return the top value of the stack without removing it. O(1) time.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self._stack:
            raise IndexError("top from empty MinStack")
        return self._stack[-1][0]

    def get_min(self) -> Any:
        """
        Return the minimum value currently in the stack. O(1) time.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self._stack:
            raise IndexError("get_min from empty MinStack")
        return self._stack[-1][1]

    def __len__(self) -> int:
        return len(self._stack)

    def is_empty(self) -> bool:
        """Return True if the stack has no elements."""
        return not self._stack
