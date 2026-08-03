"""
Text Editor Memento (Snapshot / Undo) implementation.

This module implements the Memento pattern for a text editor with undo functionality.
"""

from typing import Any


class Memento:
    """
    Immutable snapshot of editor content.
    
    The Memento captures the state of the editor at a point in time.
    The state property is read-only to prevent tampering by the caretaker.
    """
    
    def __init__(self, state: str) -> None:
        """
        Initialize a Memento with the given state.
        
        Args:
            state: The content to capture in this memento.
        """
        if not isinstance(state, str):
            raise TypeError("Memento state must be a string")
        self._state = state
    
    @property
    def state(self) -> str:
        """
        Get the captured state.
        
        Returns:
            The content captured in this memento.
        """
        return self._state
    
    @state.setter
    def state(self, value: Any) -> None:
        """
        Prevent modification of the memento state.
        
        Raises:
            AttributeError: Always, as state is read-only.
        """
        raise AttributeError("can't set attribute")


class Editor:
    """
    Text editor with memento-based undo functionality.
    
    The editor maintains content and can save snapshots (mementos) for later restoration.
    It also maintains an undo history of saved snapshots.
    """
    
    def __init__(self) -> None:
        """Initialize the editor with empty content and empty undo history."""
        self._content = ""
        self._undo_history: list[Memento] = []
    
    @property
    def content(self) -> str:
        """
        Get the current content.
        
        Returns:
            The current editor content.
        """
        return self._content
    
    def write(self, text: str) -> None:
        """
        Append text to the current content.
        
        Args:
            text: The text to append.
            
        Raises:
            TypeError: If text is not a string.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        self._content += text
    
    def clear(self) -> None:
        """Clear the editor content."""
        self._content = ""
    
    def save(self) -> Memento:
        """
        Save the current content as a memento.
        
        The saved memento is also pushed onto the undo history.
        
        Returns:
            A Memento object capturing the current content.
        """
        memento = Memento(self._content)
        self._undo_history.append(memento)
        return memento
    
    def restore(self, memento: Memento) -> None:
        """
        Restore the editor content to a previously saved memento.
        
        This does not affect the undo history.
        
        Args:
            memento: The memento to restore from.
            
        Raises:
            TypeError: If memento is not a Memento object produced by save().
        """
        if not isinstance(memento, Memento):
            raise TypeError("memento must be a Memento object")
        self._content = memento.state
    
    def undo(self) -> str:
        """
        Restore to the most recently saved snapshot.
        
        Consumes the snapshot from the undo history, so repeated calls
        will restore to earlier snapshots.
        
        Returns:
            The content after undoing.
            
        Raises:
            IndexError: If there is nothing to undo.
        """
        if not self._undo_history:
            raise IndexError("nothing to undo")
        memento = self._undo_history.pop()
        self._content = memento.state
        return self._content
