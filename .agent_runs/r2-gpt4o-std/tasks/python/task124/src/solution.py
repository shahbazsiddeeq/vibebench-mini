# src/solution.py

class TextBuffer:
    def __init__(self):
        self._text = ""
        self._undo_stack = []
        self._redo_stack = []

    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError("Input must be a string")
        
        self._undo_stack.append(s)
        self._text += s
        self._redo_stack.clear()

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        
        last_append = self._undo_stack.pop()
        self._redo_stack.append(last_append)
        self._text = self._text[:-len(last_append)]
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        
        last_undo = self._redo_stack.pop()
        self._undo_stack.append(last_undo)
        self._text += last_undo
        return True

    @property
    def text(self) -> str:
        return self._text
