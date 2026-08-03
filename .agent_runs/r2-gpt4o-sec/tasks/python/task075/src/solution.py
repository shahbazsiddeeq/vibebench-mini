import json
import os
from typing import Any, List
from threading import Lock

class KVStore:
    def __init__(self, path: str):
        self.path = path
        self.lock = Lock()
        self._load_store()

    def _load_store(self):
        """Load the store from the JSON file."""
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.store = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.store = {}
        else:
            self.store = {}

    def _save_store(self):
        """Save the store to the JSON file."""
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.store, f, ensure_ascii=False, indent=4)

    def set(self, key: str, value: Any):
        """Set the value for a key in the store."""
        if '/' in key:
            raise ValueError("Key cannot contain '/'")
        with self.lock:
            self.store[key] = value
            self._save_store()

    def get(self, key: str, default: Any = None) -> Any:
        """Get the value for a key from the store, return default if not found."""
        with self.lock:
            return self.store.get(key, default)

    def delete(self, key: str) -> bool:
        """Delete a key from the store, return True if deleted, False if not found."""
        with self.lock:
            if key in self.store:
                del self.store[key]
                self._save_store()
                return True
            return False

    def keys(self) -> List[str]:
        """Return a list of keys in the store."""
        with self.lock:
            return list(self.store.keys())
