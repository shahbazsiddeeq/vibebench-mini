"""Undo/redo text buffer implementation."""

from __future__ import annotations


class TextBuffer:
    """A text buffer supporting append, undo, and redo operations."""

    def __init__(self) -> None:
        self._text = ""
        self._undo_stack: list[str] = []
        self._redo_stack: list[str] = []

    @property
    def text(self) -> str:
        """Return the current buffer contents."""
        return self._text

    def append(self, s: str) -> None:
        """Append a string and record the operation for undo."""
        if not isinstance(s, str):
            raise ValueError("append value must be a string")

        self._text += s
        self._undo_stack.append(s)
        self._redo_stack.clear()

    def undo(self) -> bool:
        """Undo the most recent append, if one exists."""
        if not self._undo_stack:
            return False

        appended = self._undo_stack.pop()
        if appended:
            self._text = self._text[: -len(appended)]
        self._redo_stack.append(appended)
        return True

    def redo(self) -> bool:
        """Redo the most recently undone append, if one exists."""
        if not self._redo_stack:
            return False

        appended = self._redo_stack.pop()
        self._text += appended
        self._undo_stack.append(appended)
        return True
