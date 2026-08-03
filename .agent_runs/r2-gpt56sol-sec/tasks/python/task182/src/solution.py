"""Text editor with immutable memento snapshots and undo support."""

from __future__ import annotations

import threading
import weakref
from typing import NoReturn


_MEMENTO_STATES: weakref.WeakKeyDictionary[Memento, str]
_MEMENTO_LOCK = threading.RLock()


class Memento:
    """An opaque, immutable snapshot created by :meth:`Editor.save`."""

    __slots__ = ("__weakref__",)

    def __new__(cls, *args: object, **kwargs: object) -> NoReturn:
        raise TypeError("Memento objects can only be created by Editor.save()")

    def __setattr__(self, name: str, value: object) -> NoReturn:
        raise AttributeError("Memento objects are immutable")

    def __delattr__(self, name: str) -> NoReturn:
        raise AttributeError("Memento objects are immutable")

    @property
    def state(self) -> str:
        """The captured editor content."""
        with _MEMENTO_LOCK:
            try:
                return _MEMENTO_STATES[self]
            except KeyError as exc:
                raise AttributeError("invalid memento") from exc


_MEMENTO_STATES = weakref.WeakKeyDictionary()


def _create_memento(state: str) -> Memento:
    memento = object.__new__(Memento)
    with _MEMENTO_LOCK:
        _MEMENTO_STATES[memento] = state
    return memento


def _get_memento_state(memento: object) -> str:
    if type(memento) is not Memento:
        raise TypeError("memento must be a Memento produced by Editor.save()")

    with _MEMENTO_LOCK:
        try:
            return _MEMENTO_STATES[memento]
        except KeyError as exc:
            raise TypeError(
                "memento must be a Memento produced by Editor.save()"
            ) from exc


class Editor:
    """A text editor supporting snapshots, restoration, and saved-state undo."""

    __slots__ = ("_content", "_history")

    def __init__(self) -> None:
        self._content = ""
        self._history: list[Memento] = []

    @property
    def content(self) -> str:
        """The editor's current content."""
        return self._content

    def write(self, text: str) -> None:
        """Append text to the current content."""
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        self._content += text

    def clear(self) -> None:
        """Remove all content."""
        self._content = ""

    def save(self) -> Memento:
        """Capture the current content and add it to the undo history."""
        memento = _create_memento(self._content)
        self._history.append(memento)
        return memento

    def restore(self, memento: Memento) -> None:
        """Restore a valid saved snapshot without changing undo history."""
        self._content = _get_memento_state(memento)

    def undo(self) -> str:
        """Restore and consume the most recently saved snapshot."""
        if not self._history:
            raise IndexError("nothing to undo")

        memento = self._history.pop()
        self._content = _get_memento_state(memento)
        return self._content
