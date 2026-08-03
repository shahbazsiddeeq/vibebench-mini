import json
import os


class KVStore:
    def __init__(self, path):
        self.path = path
        self._data = {}
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                self._data = {}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self._data, f)

    def set(self, key, value):
        if "/" in key:
            raise ValueError("Key must not contain '/'")
        self._data[key] = value
        self._save()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def delete(self, key):
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False

    def keys(self):
        return list(self._data.keys())
