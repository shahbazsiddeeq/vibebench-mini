from __future__ import annotations

import json
from pathlib import Path


class KVStore:
    def __init__(self, path: str) -> None:
        self._path = Path(path)
        self._data: dict = {}
        if self._path.exists():
            self._data = json.loads(self._path.read_text(encoding="utf-8"))

    def _save(self) -> None:
        self._path.write_text(json.dumps(self._data), encoding="utf-8")

    def set(self, key: str, value) -> None:
        if "/" in key:
            raise ValueError("key must not contain '/'")
        self._data[key] = value
        self._save()

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False

    def keys(self) -> list[str]:
        return list(self._data.keys())
