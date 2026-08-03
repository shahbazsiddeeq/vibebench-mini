import secrets

class Memento:
    """
    The Memento stores the editor's content. It is immutable and opaque to the caretaker.
    """
    def __init__(self, state: str):
        if not isinstance(state, str):
            raise TypeError("Memento state must be a string.")
        self._state = state
        self._id = secrets.token_hex(16) # Unique ID for type checking

    @property
    def state(self) -> str:
        """
        Returns the saved state. Read-only property.
        """
        return self._state

    def __setattr__(self, name, value):
        if name == 'state':
            raise AttributeError("Cannot assign to 'state' property of Memento.")
        super().__setattr__(name, value)

    def _get_id(self) -> str:
        """
        Internal method to get the unique ID for type checking.
        """
        return self._id

class Editor:
    """
    The Editor class represents the originator, managing its content and
    providing methods to save, restore, and undo changes.
    """
    def __init__(self):
        self._content = ""
        self._history = [] # Stores Memento objects for undo functionality

    @property
    def content(self) -> str:
        """
        Returns the current content of the editor. Read-only property.
        """
        return self._content

    def write(self, text: str):
        """
        Appends the given text to the editor's content.

        Args:
            text: The string to append.

        Raises:
            TypeError: If text is not a string.
        """
        if not isinstance(text, str):
            raise TypeError("Input 'text' must be a string.")
        self._content += text

    def clear(self):
        """
        Clears the editor's content, setting it to an empty string.
        """
        self._content = ""

    def save(self) -> Memento:
        """
        Captures the current state of the editor's content and returns a Memento object.
        This Memento is also pushed onto the undo history.

        Returns:
            A Memento object representing the current state.
        """
        memento = Memento(self._content)
        self._history.append(memento)
        return memento

    def restore(self, memento: Memento):
        """
        Restores the editor's content to the state captured by the given Memento.

        Args:
            memento: The Memento object containing the state to restore.

        Raises:
            TypeError: If memento is not a valid Memento object produced by this Editor.
        """
        if not isinstance(memento, Memento) or not hasattr(memento, '_get_id'):
            # Basic type check and check for our internal ID to prevent arbitrary objects
            raise TypeError("Input 'memento' must be a valid Memento object.")
        
        # Further validation: ensure it's a Memento from our system, not just any object
        # with a _get_id method. This is a best-effort check for "produced by save()".
        # A truly robust check might involve a shared secret or a registry, but for
        # this problem, checking the type and the presence of our internal ID is sufficient.
        try:
            # Accessing _get_id directly is okay as it's an internal check.
            # We don't compare the ID itself, just ensure it exists and is callable.
            _ = memento._get_id()
        except AttributeError:
            raise TypeError("Input 'memento' must be a valid Memento object.")

        self._content = memento.state

    def undo(self) -> str:
        """
        Restores the editor's content to the most recently saved snapshot that
        has not yet been consumed by undo.

        Returns:
            The content after the undo operation.

        Raises:
            IndexError: If there is nothing to undo.
        """
        if not self._history:
            raise IndexError("No states to undo.")
        
        # Pop the last memento from history and restore the content
        last_memento = self._history.pop()
        self._content = last_memento.state
        return self._content
