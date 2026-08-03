"""
Command Pattern (Undo/Redo Buffer) implementation.

This module provides a TextBuffer class that supports appending text
with the ability to undo and redo those append operations, using the
Command pattern. Input validation is strict to avoid unexpected
behavior or security issues (e.g., type confusion).
"""

from typing import List


class _AppendCommand:
    """Represents a single append operation for undo/redo purposes."""

    __slots__ = ("text",)

    def __init__(self, text: str) -> None:
        self.text = text


class TextBuffer:
    """
    A text buffer supporting append, undo, and redo operations.

    - append(s: str) -> None: appends s to the text, records the command,
      and clears the redo stack. Raises ValueError if s is not a str.
    - undo() -> bool: reverts the last append. Returns False if there is
      nothing to undo, else True.
    - redo() -> bool: re-applies the last undone append. Returns False if
      there is nothing to redo, else True.
    - text: property returning the current text as a str.
    """

    def __init__(self) -> None:
        self._text: str = ""
        self._undo_stack: List[_AppendCommand] = []
        self._redo_stack: List[_AppendCommand] = []

    @property
    def text(self) -> str:
        return self._text

    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError("append() expects a str argument")

        command = _AppendCommand(s)
        self._text += s
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> bool:
        if not self._undo_stack:
            return False

        command = self._undo_stack.pop()
        # Remove the trailing text that was added by this command.
        if command.text:
            if self._text.endswith(command.text):
                self._text = self._text[: -len(command.text)]
            else:
                # Should not happen under normal use, but guard against
                # inconsistent state without leaking internal details.
                self._text = self._text[: max(0, len(self._text) - len(command.text))]

        self._redo_stack.append(command)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False

        command = self._redo_stack.pop()
        self._text += command.text
        self._undo_stack.append(command)
        return True
