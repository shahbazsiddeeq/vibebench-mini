class TextBuffer:
    def __init__(self):
        self._text = ""
        self._undo_stack = []
        self._redo_stack = []
    
    @property
    def text(self) -> str:
        return self._text
    
    def append(self, s: str) -> None:
        if not isinstance(s, str):
            raise ValueError(f"Expected str, got {type(s).__name__}")
        
        # Record the command for undo
        self._undo_stack.append(s)
        # Clear redo stack when a new command is executed
        self._redo_stack.clear()
        # Apply the command
        self._text += s
    
    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        
        # Pop the last command from undo stack
        last_append = self._undo_stack.pop()
        # Push it to redo stack
        self._redo_stack.append(last_append)
        # Remove the appended text
        self._text = self._text[:-len(last_append)]
        return True
    
    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        
        # Pop the last undone command from redo stack
        last_undone = self._redo_stack.pop()
        # Push it back to undo stack
        self._undo_stack.append(last_undone)
        # Re-apply the command
        self._text += last_undone
        return True
