class TextBuffer:
    def __init__(self):
        self._text = ""
        self._undo_stack = []
        self._redo_stack = []

    @property
    def text(self):
        return self._text

    def append(self, s):
        if not isinstance(s, str):
            raise ValueError("s must be a str")
        self._undo_stack.append(self._text)
        self._text += s
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            return False
        self._redo_stack.append(self._text)
        self._text = self._undo_stack.pop()
        return True

    def redo(self):
        if not self._redo_stack:
            return False
        self._undo_stack.append(self._text)
        self._text = self._redo_stack.pop()
        return True
