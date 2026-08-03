# src/solution.py

class TextBuffer:
    def __init__(self):
        self._text = ""
        self._undo_stack = []
        self._redo_stack = []

    @property
    def text(self):
        return self._text

    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError("Input must be a string.")
        
        self._undo_stack.append(s)
        self._text += s
        self._redo_stack.clear()  # Clear redo stack on new append

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        
        last_action = self._undo_stack.pop()
        self._text = self._text[:-len(last_action)]  # Remove last appended string
        self._redo_stack.append(last_action)  # Add to redo stack
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        
        last_undone = self._redo_stack.pop()
        self._text += last_undone  # Reapply the last undone string
        self._undo_stack.append(last_undone)  # Add back to undo stack
        return True
