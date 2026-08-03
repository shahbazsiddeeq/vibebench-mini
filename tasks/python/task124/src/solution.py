"""Command pattern: a text buffer supporting undo and redo of append commands."""
from __future__ import annotations


class TextBuffer:
    """A text buffer where each append is an undoable/redoable command."""

    def __init__(self) -> None:
        self._parts: list[str] = []
        self._undone: list[str] = []

    @property
    def text(self) -> str:
        return "".join(self._parts)

    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError("s must be a string")
        self._parts.append(s)
        self._undone.clear()

    def undo(self) -> bool:
        if not self._parts:
            return False
        self._undone.append(self._parts.pop())
        return True

    def redo(self) -> bool:
        if not self._undone:
            return False
        self._parts.append(self._undone.pop())
        return True
