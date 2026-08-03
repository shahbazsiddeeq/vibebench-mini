class Memento:
    """Immutable snapshot of editor content."""
    
    def __init__(self, state: str):
        self._state = state
    
    @property
    def state(self) -> str:
        """Read-only property for the saved content."""
        return self._state
    
    @state.setter
    def state(self, value):
        """Prevent modification of state."""
        raise AttributeError("can't set attribute")


class Editor:
    """Text editor with undo functionality using the Memento pattern."""
    
    def __init__(self):
        self._content = ""
        self._undo_history = []
    
    @property
    def content(self) -> str:
        """Read-only property for current content."""
        return self._content
    
    def write(self, text: str) -> None:
        """Append text to content. Raises TypeError if text is not a str."""
        if not isinstance(text, str):
            raise TypeError(f"expected str, not {type(text).__name__}")
        self._content += text
    
    def clear(self) -> None:
        """Set content to empty string."""
        self._content = ""
    
    def save(self) -> Memento:
        """Capture current content and return a Memento object."""
        memento = Memento(self._content)
        self._undo_history.append(memento)
        return memento
    
    def restore(self, memento: Memento) -> None:
        """Restore content to memento's captured state.
        
        Raises TypeError if memento is not a Memento produced by save().
        """
        if not isinstance(memento, Memento):
            raise TypeError(f"expected Memento, not {type(memento).__name__}")
        
        # Verify that this memento was produced by this editor's save()
        if memento not in self._undo_history:
            raise TypeError("Memento was not produced by this editor's save()")
        
        self._content = memento.state
    
    def undo(self) -> str:
        """Restore content to most recently saved snapshot not yet consumed by undo.
        
        Returns the new content.
        Raises IndexError if there is nothing to undo.
        """
        if not self._undo_history:
            raise IndexError("nothing to undo")
        
        memento = self._undo_history.pop()
        self._content = memento.state
        return self._content
