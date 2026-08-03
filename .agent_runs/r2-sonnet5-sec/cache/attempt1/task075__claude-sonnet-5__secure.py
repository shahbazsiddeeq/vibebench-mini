"""
A simple, security-conscious file-backed key-value store.

The KVStore persists a dictionary of string keys to JSON-serializable
values in a JSON file on disk. Writes are performed atomically (write
to a temp file then rename) to reduce the risk of data corruption.
"""

import json
import os
import tempfile
from typing import Any, List


class KVStore:
    """A JSON file-backed key-value store.

    Keys must be non-empty strings and must not contain the "/"
    character. Values must be JSON-serializable.
    """

    def __init__(self, path: str) -> None:
        if not isinstance(path, str) or not path:
            raise ValueError("path must be a non-empty string")
        self._path = path
        self._data = {}
        self._load()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str):
            raise ValueError("key must be a string")
        if not key:
            raise ValueError("key must not be empty")
        if "/" in key:
            raise ValueError('key must not contain "/"')

    def _load(self) -> None:
        if not os.path.exists(self._path):
            self._data = {}
            return
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError:
            # Cannot read the store file; treat as empty rather than
            # exposing internal filesystem errors.
            self._data = {}
            return

        if not content.strip():
            self._data = {}
            return

        try:
            loaded = json.loads(content)
        except json.JSONDecodeError:
            # Corrupt store file; fail safe with an empty store rather
            # than raising an exception that leaks details.
            self._data = {}
            return

        if isinstance(loaded, dict):
            # Only keep string keys; ignore anything malformed.
            self._data = {
                str(k): v for k, v in loaded.items() if isinstance(k, str)
            }
        else:
            self._data = {}

    def _save(self) -> None:
        directory = os.path.dirname(os.path.abspath(self._path)) or "."
        try:
            fd, tmp_path = tempfile.mkstemp(
                prefix=".kvstore_", suffix=".tmp", dir=directory
            )
        except OSError as exc:
            raise RuntimeError("Failed to persist key-value store") from exc

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, self._path)
        except OSError as exc:
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise RuntimeError("Failed to persist key-value store") from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def set(self, key: str, value: Any) -> None:
        self._validate_key(key)
        try:
            json.dumps(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("value must be JSON-serializable") from exc

        self._data[key] = value
        self._save()

    def get(self, key: str, default: Any = None) -> Any:
        self._validate_key(key)
        return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        self._validate_key(key)
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False

    def keys(self) -> List[str]:
        return list(self._data.keys())
