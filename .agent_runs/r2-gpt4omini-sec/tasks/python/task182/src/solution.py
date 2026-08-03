# src/solution.py

class Memento:
    def __init__(self, state: str):
        self._state = state

    @property
    def state(self) -> str:
        return self._state


class Editor:
    def __init__(self):
        self._content = ""
        self._history = []

    @property
    def content(self) -> str:
        return self._content

    def write(self, text: str) -> None:
        if not isinstance(text, str):
            raise TypeError("Input must be a string.")
        self._content += text

    def clear(self) -> None:
        self._content = ""

    def save(self) -> Memento:
        memento = Memento(self._content)
        self._history.append(memento)
        return memento

    def restore(self, memento: Memento) -> None:
        if not isinstance(memento, Memento):
            raise TypeError("Provided object is not a Memento.")
        self._content = memento.state

    def undo(self) -> str:
        if not self._history:
            raise IndexError("No history to undo.")
        last_memento = self._history.pop()
        self._content = last_memento.state
        return self._content
