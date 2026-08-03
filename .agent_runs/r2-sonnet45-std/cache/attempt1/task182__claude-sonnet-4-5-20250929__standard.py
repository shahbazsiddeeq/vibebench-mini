class Memento:
    """Opaque memento object that captures editor state."""
    
    def __init__(self, state: str):
        self._state = state
    
    @property
    def state(self) -> str:
        """Read-only property exposing the saved state."""
        return self._state
    
    @state.setter
    def state(self, value):
        """Prevent assignment to state."""
        raise AttributeError("can't set attribute")


class Editor:
    """Text editor with memento pattern support."""
    
    def __init__(self):
        self._content = ""
        self._undo_history = []
    
    @property
    def content(self) -> str:
        """Read-only property exposing current content."""
        return self._content
    
    def write(self, text: str) -> None:
        """Append text to content. Raises TypeError if text is not a str."""
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        self._content += text
    
    def clear(self) -> None:
        """Set content to empty string."""
        self._content = ""
    
    def save(self) -> Memento:
        """Capture current content and return a Memento. Adds to undo history."""
        memento = Memento(self._content)
        self._undo_history.append(memento)
        return memento
    
    def restore(self, memento: Memento) -> None:
        """Restore content from memento. Raises TypeError if not a Memento."""
        if not isinstance(memento, Memento):
            raise TypeError("memento must be a Memento")
        self._content = memento.state
    
    def undo(self) -> str:
        """Restore to most recent saved snapshot. Raises IndexError if nothing to undo."""
        if not self._undo_history:
            raise IndexError("nothing to undo")
        memento = self._undo_history.pop()
        self._content = memento.state
        return self._content
