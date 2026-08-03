"""A small file-backed JSON key-value store."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


class KVStore:
    """Persist string keys and JSON-serializable values in a JSON file."""

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self._path = Path(path)
        self._data: dict[str, Any] = self._load()

    @staticmethod
    def _validate_key(key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if "/" in key:
            raise ValueError('key must not contain "/"')

    def _load(self) -> dict[str, Any]:
        try:
            with self._path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return {}

        if not isinstance(data, dict) or not all(
            isinstance(key, str) for key in data
        ):
            raise ValueError("store file must contain a JSON object")
        return data

    def _persist(self, data: dict[str, Any]) -> None:
        parent = self._path.parent
        parent.mkdir(parents=True, exist_ok=True)

        descriptor, temporary_path = tempfile.mkstemp(
            prefix=f".{self._path.name}.",
            suffix=".tmp",
            dir=str(parent),
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, separators=(",", ":"))
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary_path, self._path)
        except BaseException:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass
            raise

    def set(self, key: str, value: Any) -> None:
        self._validate_key(key)
        updated = self._data.copy()
        updated[key] = value
        self._persist(updated)
        self._data = updated

    def get(self, key: str, default: Any = None) -> Any:
        self._validate_key(key)
        return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        self._validate_key(key)
        if key not in self._data:
            return False

        updated = self._data.copy()
        del updated[key]
        self._persist(updated)
        self._data = updated
        return True

    def keys(self) -> list[str]:
        return list(self._data.keys())
