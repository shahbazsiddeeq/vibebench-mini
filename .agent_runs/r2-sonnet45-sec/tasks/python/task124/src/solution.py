class TextBuffer:
    """A text buffer with undo/redo functionality using the Command Pattern."""
    
    def __init__(self):
        """Initialize an empty text buffer with empty undo/redo stacks."""
        self._text = ""
        self._undo_stack = []  # Stack of commands that can be undone
        self._redo_stack = []  # Stack of commands that can be redone
    
    def append(self, s: str) -> None:
        """
        Append a string to the text buffer.
        
        Args:
            s: The string to append
            
        Raises:
            ValueError: If s is not a string
        """
        # Validate input - security check
        if not isinstance(s, str):
            raise ValueError("append() argument must be a string")
        
        # Clear redo stack when a new command is executed
        self._redo_stack.clear()
        
        # Record the command (store the string being appended)
        self._undo_stack.append(s)
        
        # Execute the command
        self._text += s
    
    def undo(self) -> bool:
        """
        Undo the last append operation.
        
        Returns:
            True if an operation was undone, False if nothing to undo
        """
        if not self._undo_stack:
            return False
        
        # Pop the last command from undo stack
        last_command = self._undo_stack.pop()
        
        # Move it to redo stack
        self._redo_stack.append(last_command)
        
        # Revert the text by removing the last appended string
        self._text = self._text[:-len(last_command)]
        
        return True
    
    def redo(self) -> bool:
        """
        Redo the last undone append operation.
        
        Returns:
            True if an operation was redone, False if nothing to redo
        """
        if not self._redo_stack:
            return False
        
        # Pop from redo stack
        command = self._redo_stack.pop()
        
        # Move back to undo stack
        self._undo_stack.append(command)
        
        # Re-apply the command
        self._text += command
        
        return True
    
    @property
    def text(self) -> str:
        """
        Get the current text in the buffer.
        
        Returns:
            The current text as a string
        """
        return self._text
