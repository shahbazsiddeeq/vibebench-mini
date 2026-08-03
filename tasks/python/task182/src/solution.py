from __future__ import annotations


class Memento:
    """Opaque snapshot of an Editor's content."""

    __slots__ = ("_state",)

    def __init__(self, state: str) -> None:
        object.__setattr__(self, "_state", state)

    @property
    def state(self) -> str:
        return self._state

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("Memento is immutable")


class Editor:
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
        self._history.append(memento)
        return memento

    def restore(self, memento: Memento) -> None:
        if not isinstance(memento, Memento):
            raise TypeError("restore requires a Memento")
        self._content = memento.state

    def undo(self) -> str:
        if not self._history:
            raise IndexError("nothing to undo")
        memento = self._history.pop()
        self._content = memento.state
        return self._content
