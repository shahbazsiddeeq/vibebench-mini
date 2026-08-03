from __future__ import annotations

from weakref import WeakSet


class Memento:
    """An immutable snapshot of editor content."""

    __slots__ = ("__state", "__weakref__")

    def __init__(self, state: str) -> None:
        if not isinstance(state, str):
            raise TypeError("state must be a str")
        object.__setattr__(self, "_Memento__state", state)

    @property
    def state(self) -> str:
        return self.__state

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("Memento objects are immutable")


_saved_mementos: WeakSet[Memento] = WeakSet()


class Editor:
    """A text editor supporting snapshots, restoration, and undo."""

    __slots__ = ("_content", "_history")

    def __init__(self) -> None:
        self._content = ""
        self._history: list[Memento] = []

    @property
    def content(self) -> str:
        return self._content

    def write(self, text: str) -> None:
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        self._content += text

    def clear(self) -> None:
        self._content = ""

    def save(self) -> Memento:
        memento = Memento(self._content)
        _saved_mementos.add(memento)
        self._history.append(memento)
        return memento

    def restore(self, memento: Memento) -> None:
        if type(memento) is not Memento or memento not in _saved_mementos:
            raise TypeError("memento must have been produced by Editor.save()")
        self._content = memento.state

    def undo(self) -> str:
        if not self._history:
            raise IndexError("nothing to undo")
        self._content = self._history.pop().state
        return self._content
