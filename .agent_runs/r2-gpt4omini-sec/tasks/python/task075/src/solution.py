import json
import os
from typing import Any, List, Optional

class KVStore:
    def __init__(self, path: str):
        self.path = path
        self.store = {}
        self.load()

    def load(self) -> None:
        """Load the key-value store from a JSON file."""
        if os.path.exists(self.path):
            with open(self.path, 'r') as file:
                try:
                    self.store = json.load(file)
                except json.JSONDecodeError:
                    self.store = {}

    def save(self) -> None:
        """Save the key-value store to a JSON file."""
        with open(self.path, 'w') as file:
            json.dump(self.store, file)

    def set(self, key: str, value: Any) -> None:
        """Set a key-value pair in the store."""
        if '/' in key:
            raise ValueError("Key cannot contain '/'")
        self.store[key] = value
        self.save()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get the value for a key, returning default if not found."""
        return self.store.get(key, default)

    def delete(self, key: str) -> bool:
        """Delete a key from the store, returning True if successful."""
        if key in self.store:
            del self.store[key]
            self.save()
            return True
        return False

    def keys(self) -> List[str]:
        """Return a list of keys in the store."""
        return list(self.store.keys())
