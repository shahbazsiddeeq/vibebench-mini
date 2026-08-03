import json
import os
from typing import Any, List, Dict

class KVStore:
    def __init__(self, path: str):
        self._path = path
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if os.path.exists(self._path):
            try:
                with open(self._path, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            except json.JSONDecodeError:
                # If the file is corrupted or empty, initialize with an empty dictionary
                self._data = {}
        else:
            self._data = {}

    def _save(self):
        # Ensure the directory exists before writing
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=4)

    def set(self, key: str, value: Any):
        if "/" in key:
            raise ValueError("Key cannot contain '/'")
        self._data[key] = value
        self._save()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False

    def keys(self) -> List[str]:
        return list(self._data.keys())
