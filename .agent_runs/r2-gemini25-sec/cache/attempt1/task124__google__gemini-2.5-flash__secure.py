class TextBuffer:
    def __init__(self):
        self._text = ""
        self._history = []
        self._redo_stack = []

    @property
    def text(self) -> str:
        return self._text

    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError("Append argument must be a string.")

        self._history.append(s)
        self._text += s
        self._redo_stack.clear()  # Clear redo stack on new append

    def undo(self) -> bool:
        if not self._history:
            return False

        last_append = self._history.pop()
        self._text = self._text[:len(self._text) - len(last_append)]
        self._redo_stack.append(last_append)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False

        re_append = self._redo_stack.pop()
        self._history.append(re_append)
        self._text += re_append
        return True
