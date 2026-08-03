# src/solution.py

class TextBuffer:
    def __init__(self):
        self.text = ""
        self.undo_stack = []
        self.redo_stack = []

    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError("Input must be a string.")
        
        self.undo_stack.append(self.text)
        self.redo_stack.clear()
        self.text += s

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        
        self.redo_stack.append(self.text)
        self.text = self.undo_stack.pop()
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        
        self.undo_stack.append(self.text)
        self.text = self.redo_stack.pop()
        return True
