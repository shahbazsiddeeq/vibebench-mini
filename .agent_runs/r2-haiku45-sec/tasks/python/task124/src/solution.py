"""
TextBuffer implementation with undo/redo functionality using the Command Pattern.
"""


class TextBuffer:
    """A text buffer with undo/redo capabilities."""

    def __init__(self) -> None:
        """Initialize an empty text buffer with empty undo/redo stacks."""
        self._text: str = ""
        self._undo_stack: list[str] = []
        self._redo_stack: list[str] = []

    @property
    def text(self) -> str:
        """Return the current text in the buffer."""
        return self._text

    def append(self, s: str) -> None:
        """
        Append a string to the text buffer.

        Args:
            s: The string to append.

        Raises:
            ValueError: If s is not a string.
        """
        if not isinstance(s, str):
            raise ValueError(f"Expected str, got {type(s).__name__}")

        # Record the current state before modification
        self._undo_stack.append(self._text)
        # Clear redo stack when a new command is executed
        self._redo_stack.clear()
        # Apply the command
        self._text += s

    def undo(self) -> bool:
        """
        Undo the last append operation.

        Returns:
            True if an undo was performed, False if there is nothing to undo.
        """
        if not self._undo_stack:
            return False

        # Save current state to redo stack
        self._redo_stack.append(self._text)
        # Restore previous state
        self._text = self._undo_stack.pop()
        return True

    def redo(self) -> bool:
        """
        Redo the last undone append operation.

        Returns:
            True if a redo was performed, False if there is nothing to redo.
        """
        if not self._redo_stack:
            return False

        # Save current state to undo stack
        self._undo_stack.append(self._text)
        # Restore next state
        self._text = self._redo_stack.pop()
        return True
