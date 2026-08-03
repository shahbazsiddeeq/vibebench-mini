"""
Text Editor Memento (Snapshot / Undo) implementation.

This module implements the Memento pattern for a text editor with undo functionality.
"""


class Memento:
    """
    Memento class that captures and stores the state of the Editor.
    
    The state is exposed through a read-only property to prevent tampering.
    """
    
    def __init__(self, state: str):
        """
        Initialize a Memento with the given state.
        
        Args:
            state: The content state to capture
            
        Raises:
            TypeError: If state is not a string
        """
        if not isinstance(state, str):
            raise TypeError("State must be a string")
        self._state = state
    
    @property
    def state(self) -> str:
        """
        Read-only property that returns the captured state.
        
        Returns:
            The captured content state
        """
        return self._state
    
    @state.setter
    def state(self, value):
        """
        Setter that raises AttributeError to prevent modification.
        
        Raises:
            AttributeError: Always, as state is read-only
        """
        raise AttributeError("can't set attribute")


class Editor:
    """
    Text editor with memento pattern support for snapshots and undo functionality.
    
    The editor maintains content that can be modified, saved to mementos,
    and restored. It also maintains an internal undo history.
    """
    
    def __init__(self):
        """Initialize an empty editor."""
        self._content = ""
        self._undo_history = []
    
    @property
    def content(self) -> str:
        """
        Read-only property that returns the current content.
        
        Returns:
            The current content of the editor
        """
        return self._content
    
    def write(self, text: str) -> None:
        """
        Append text to the current content.
        
        Args:
            text: The text to append
            
        Raises:
            TypeError: If text is not a string
        """
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        self._content += text
    
    def clear(self) -> None:
        """Set the content to an empty string."""
        self._content = ""
    
    def save(self) -> Memento:
        """
        Capture the current content and return a Memento.
        
        This also pushes the current state onto the undo history.
        
        Returns:
            A Memento object containing the current content state
        """
        memento = Memento(self._content)
        self._undo_history.append(memento)
        return memento
    
    def restore(self, memento: Memento) -> None:
        """
        Restore the editor's content from a memento.
        
        This does not affect the undo history.
        
        Args:
            memento: The Memento to restore from
            
        Raises:
            TypeError: If memento is not a Memento instance
        """
        if not isinstance(memento, Memento):
            raise TypeError("Argument must be a Memento instance")
        self._content = memento.state
    
    def undo(self) -> str:
        """
        Restore the content to the most recently saved snapshot.
        
        This consumes the most recent snapshot from the undo history.
        
        Returns:
            The content after undoing
            
        Raises:
            IndexError: If there is nothing to undo
        """
        if not self._undo_history:
            raise IndexError("Nothing to undo")
        
        memento = self._undo_history.pop()
        self._content = memento.state
        return self._content
