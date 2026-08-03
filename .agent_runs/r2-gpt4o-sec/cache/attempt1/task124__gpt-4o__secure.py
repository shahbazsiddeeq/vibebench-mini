# src/solution.py

from secrets import choice
from string import ascii_letters, digits

class TextBuffer:
    def __init__(self):
        self._text = []
        self._undo_stack = []
        self._redo_stack = []

    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError("Input must be a string.")
        
        self._text.append(s)
        self._undo_stack.append(s)
        self._redo_stack.clear()

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        
        last_action = self._undo_stack.pop()
        self._redo_stack.append(last_action)
        self._text.pop()
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        
        last_undone = self._redo_stack.pop()
        self._text.append(last_undone)
        self._undo_stack.append(last_undone)
        return True

    @property
    def text(self) -> str:
        return ''.join(self._text)
