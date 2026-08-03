"""
Text Editor Memento (Snapshot / Undo) pattern implementation.

This module provides a secure, self-contained implementation of the Memento
design pattern for a simple text editor. It avoids eval/exec, uses only the
standard library, and validates all external inputs to prevent misuse or
tampering.
"""

from __future__ import annotations


class Memento:
    """
    Opaque snapshot object capturing an editor's content at a point in time.

    The captured state is read-only: attempts to assign to `state` raise
    AttributeError, preventing external tampering by a caretaker.
    """

    __slots__ = ("_state",)

    def __init__(self, state: str) -> None:
        if not isinstance(state, str):
            raise TypeError("Memento state must be a str")
        # Use object.__setattr__ to bypass our own __setattr__ guard.
        object.__setattr__(self, "_state", state)

    @property
    def state(self) -> str:
        """Read-only access to the captured content."""
        return self._state

    def __setattr__(self, name: str, value: object) -> None:
        # Prevent any attribute assignment after construction, including
        # attempts to set 'state' directly.
        raise AttributeError("Memento is immutable; cannot set attributes")

    def __delattr__(self, name: str) -> None:
        raise AttributeError("Memento is immutable; cannot delete attributes")

    def __repr__(self) -> str:  # pragma: no cover - convenience only
        return f"Memento(state={self._state!r})"


class Editor:
    """
    A simple text editor supporting the Memento pattern for save/restore
    and an internal undo history.
    """

    __slots__ = ("_content", "_history")

    def __init__(self) -> None:
        self._content: str = ""
        self._history: list[str] = []

    @property
    def content(self) -> str:
        """Read-only access to the current editor content."""
        return self._content

    def write(self, text: str) -> None:
        """
        Append text to the current content.

        Raises:
            TypeError: if `text` is not a str.
        """
        if not isinstance(text, str):
            raise TypeError("write() requires a str argument")
        self._content += text

    def clear(self) -> None:
        """Reset the content to an empty string."""
        self._content = ""

    def save(self) -> Memento:
        """
        Capture the current content into a Memento and push it onto the
        internal undo history.

        Returns:
            Memento: an opaque snapshot of the current content.
        """
        snapshot = self._content
        self._history.append(snapshot)
        return Memento(snapshot)

    def restore(self, memento: Memento) -> None:
        """
        Restore the editor's content from a previously saved Memento.

        Args:
            memento: a Memento instance produced by save().

        Raises:
            TypeError: if `memento` is not a Memento instance.
        """
        if not isinstance(memento, Memento):
            raise TypeError("restore() requires a Memento instance")
        # Reading .state does not mutate the memento; content is copied.
        self._content = memento.state

    def undo(self) -> str:
        """
        Restore content to the most recently saved snapshot not yet
        consumed by undo, and return the new content.

        Raises:
            IndexError: if there is no history to undo.
        """
        if not self._history:
            raise IndexError("No saved history to undo")
        previous = self._history.pop()
        self._content = previous
        return self._content
