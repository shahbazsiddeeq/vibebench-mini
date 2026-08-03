class TextBuffer:
    def __init__(self):
        self._text = ""
        self._undo_stack = []  # Stack of commands that have been executed
        self._redo_stack = []  # Stack of commands that have been undone
    
    @property
    def text(self):
        return self._text
    
    def append(self, s):
        if not isinstance(s, str):
            raise ValueError("Argument must be a string")
        
        # Clear redo stack when a new command is executed
        self._redo_stack.clear()
        
        # Record the command (the string to append)
        self._undo_stack.append(s)
        
        # Execute the command
        self._text += s
    
    def undo(self):
        if not self._undo_stack:
            return False
        
        # Pop the last command from undo stack
        last_command = self._undo_stack.pop()
        
        # Move it to redo stack
        self._redo_stack.append(last_command)
        
        # Revert the text by removing the last appended string
        self._text = self._text[:-len(last_command)]
        
        return True
    
    def redo(self):
        if not self._redo_stack:
            return False
        
        # Pop the last undone command from redo stack
        command = self._redo_stack.pop()
        
        # Move it back to undo stack
        self._undo_stack.append(command)
        
        # Re-apply the command
        self._text += command
        
        return True
