import json
import os
import tempfile
import threading
from typing import Any, Optional, Union


class KVStore:
    """A simple JSON file-backed key-value store."""

    def __init__(self, path: Union[str, os.PathLike[str]]) -> None:
        try:
            file_path = os.fspath(path)
        except TypeError as exc:
            raise TypeError("path must be a string or path-like object") from exc

        if not isinstance(file_path, str):
            raise TypeError("path must resolve to a string")
        if not file_path or "\x00" in file_path:
            raise ValueError("path must be a valid non-empty path")

        self._path = file_path
        self._lock = threading.RLock()
        self._data: dict[str, Any] = self._load()

    @staticmethod
    def _validate_key(key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if "/" in key:
            raise ValueError('key must not contain "/"')

    def _load(self) -> dict[str, Any]:
        try:
            with open(self._path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return {}
        except (json.JSONDecodeError, UnicodeError) as exc:
            raise ValueError("store file contains invalid JSON") from exc

        if not isinstance(data, dict):
            raise ValueError("store file must contain a JSON object")

        for key in data:
            if not isinstance(key, str) or "/" in key:
                raise ValueError("store file contains an invalid key")

        return data

    @staticmethod
    def _serialize(data: dict[str, Any]) -> str:
        try:
            return json.dumps(
                data,
                ensure_ascii=True,
                allow_nan=False,
                separators=(",", ":"),
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("value is not JSON serializable") from exc

    def _persist(self, data: dict[str, Any]) -> None:
        serialized = self._serialize(data)
        directory = os.path.dirname(os.path.abspath(self._path))
        prefix = f".{os.path.basename(self._path)}."
        descriptor: Optional[int] = None
        temporary_path: Optional[str] = None

        try:
            descriptor, temporary_path = tempfile.mkstemp(
                dir=directory,
                prefix=prefix,
                suffix=".tmp",
                text=True,
            )
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as file:
                descriptor = None
                file.write(serialized)
                file.flush()
                os.fsync(file.fileno())

            os.replace(temporary_path, self._path)
            temporary_path = None
        finally:
            if descriptor is not None:
                os.close(descriptor)
            if temporary_path is not None:
                try:
                    os.unlink(temporary_path)
                except FileNotFoundError:
                    pass

    def set(self, key: str, value: Any) -> None:
        self._validate_key(key)
        with self._lock:
            updated = self._data.copy()
            updated[key] = value
            self._persist(updated)
            self._data = updated

    def get(self, key: str, default: Any = None) -> Any:
        self._validate_key(key)
        with self._lock:
            return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        self._validate_key(key)
        with self._lock:
            if key not in self._data:
                return False

            updated = self._data.copy()
            del updated[key]
            self._persist(updated)
            self._data = updated
            return True

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._data.keys())
