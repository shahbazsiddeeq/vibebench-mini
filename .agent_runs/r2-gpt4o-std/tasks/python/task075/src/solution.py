import json
import os

class KVStore:
    def __init__(self, path: str):
        self.path = path
        self._load_store()

    def _load_store(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self.store = json.load(f)
        else:
            self.store = {}

    def _save_store(self):
        with open(self.path, 'w') as f:
            json.dump(self.store, f)

    def set(self, key: str, value):
        if '/' in key:
            raise ValueError("Key cannot contain '/'")
        self.store[key] = value
        self._save_store()

    def get(self, key: str, default=None):
        return self.store.get(key, default)

    def delete(self, key: str) -> bool:
        if key in self.store:
            del self.store[key]
            self._save_store()
            return True
        return False

    def keys(self) -> list[str]:
        return list(self.store.keys())
