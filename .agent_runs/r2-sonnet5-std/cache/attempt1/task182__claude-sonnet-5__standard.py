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
            raise TypeError("text must be a str")
        self._content += text

    def clear(self) -> None:
        self._content = ""

    def save(self) -> Memento:
        m = Memento(self._content)
        self._history.append(m)
        return m

    def restore(self, memento: Memento) -> None:
        if not isinstance(memento, Memento):
            raise TypeError("memento must be a Memento")
        self._content = memento.state

    def undo(self) -> str:
        if not self._history:
            raise IndexError("nothing to undo")
        m = self._history.pop()
        self._content = m.state
        return self._content
