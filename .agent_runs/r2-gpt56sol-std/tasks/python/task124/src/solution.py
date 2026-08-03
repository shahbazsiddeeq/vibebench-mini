class TextBuffer:
    def __init__(self) -> None:
        self._text = ""
        self._undo_stack: list[str] = []
        self._redo_stack: list[str] = []

    @property
    def text(self) -> str:
        return self._text

    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError("append value must be a string")
        self._text += s
        self._undo_stack.append(s)
        self._redo_stack.clear()

    def undo(self) -> bool:
        if not self._undo_stack:
            return False

        appended_text = self._undo_stack.pop()
        self._text = self._text[: len(self._text) - len(appended_text)]
        self._redo_stack.append(appended_text)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False

        appended_text = self._redo_stack.pop()
        self._text += appended_text
        self._undo_stack.append(appended_text)
        return True
