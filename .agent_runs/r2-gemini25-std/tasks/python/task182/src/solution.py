class Memento:
    def __init__(self, state: str):
        self._state = state

    @property
    def state(self) -> str:
        return self._state


class Editor:
    def __init__(self):
        self._content = ""
        self._history = []

    @property
    def content(self) -> str:
        return self._content

    def write(self, text: str):
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")
        self._content += text

    def clear(self):
        self._content = ""

    def save(self) -> Memento:
        memento = Memento(self._content)
        self._history.append(memento)
        return memento

    def restore(self, memento: Memento):
        if not isinstance(memento, Memento):
            raise TypeError("Memento must be a Memento object.")
        self._content = memento.state

    def undo(self) -> str:
        if not self._history:
            raise IndexError("Nothing to undo.")
        
        # Pop the current state (which was saved)
        self._history.pop() 
        
        if not self._history:
            # If history is now empty, content should be cleared
            self._content = ""
        else:
            # Restore to the previous state in history
            self._content = self._history[-1].state
            
        return self._content
