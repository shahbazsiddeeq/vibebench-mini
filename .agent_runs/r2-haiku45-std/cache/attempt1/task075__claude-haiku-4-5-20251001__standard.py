import json
import os
from typing import Any


class KVStore:
    def __init__(self, path: str):
        self.path = path
        self.data = {}
        self._load()
    
    def _load(self) -> None:
        """Load data from JSON file if it exists."""
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = {}
        else:
            self.data = {}
    
    def _save(self) -> None:
        """Save data to JSON file."""
        os.makedirs(os.path.dirname(self.path) or '.', exist_ok=True)
        with open(self.path, 'w') as f:
            json.dump(self.data, f)
    
    def set(self, key: str, value: Any) -> None:
        """Set a key-value pair. Raises ValueError if key contains '/'."""
        if "/" in key:
            raise ValueError(f"Key cannot contain '/': {key}")
        self.data[key] = value
        self._save()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key, returning default if not found."""
        return self.data.get(key, default)
    
    def delete(self, key: str) -> bool:
        """Delete a key. Returns True if key existed, False otherwise."""
        if key in self.data:
            del self.data[key]
            self._save()
            return True
        return False
    
    def keys(self) -> list[str]:
        """Return a list of all keys."""
        return list(self.data.keys())
