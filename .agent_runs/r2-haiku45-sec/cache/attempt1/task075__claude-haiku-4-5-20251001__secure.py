import json
import os
from pathlib import Path
from typing import Any, Optional


class KVStore:
    """A simple file-backed key-value store using JSON."""
    
    def __init__(self, path: str) -> None:
        """Initialize the KVStore with a file path.
        
        Args:
            path: Path to the JSON file for persistence.
        """
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        
        self.path = path
        self._data: dict[str, Any] = {}
        self._load()
    
    def _validate_key(self, key: str) -> None:
        """Validate that a key doesn't contain forbidden characters.
        
        Args:
            key: The key to validate.
            
        Raises:
            ValueError: If the key contains a forward slash.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        
        if "/" in key:
            raise ValueError("key cannot contain '/'")
    
    def _load(self) -> None:
        """Load data from the JSON file if it exists."""
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        self._data = json.loads(content)
                    else:
                        self._data = {}
            except (json.JSONDecodeError, IOError):
                self._data = {}
        else:
            self._data = {}
    
    def _save(self) -> None:
        """Save data to the JSON file."""
        # Ensure directory exists
        directory = os.path.dirname(self.path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False)
    
    def set(self, key: str, value: Any) -> None:
        """Set a key-value pair in the store.
        
        Args:
            key: The key to set.
            value: The value to associate with the key.
            
        Raises:
            ValueError: If the key contains a forward slash.
        """
        self._validate_key(key)
        self._data[key] = value
        self._save()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the store.
        
        Args:
            key: The key to retrieve.
            default: The default value if the key is not found.
            
        Returns:
            The value associated with the key, or default if not found.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        
        return self._data.get(key, default)
    
    def delete(self, key: str) -> bool:
        """Delete a key from the store.
        
        Args:
            key: The key to delete.
            
        Returns:
            True if the key was deleted, False if it didn't exist.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False
    
    def keys(self) -> list[str]:
        """Get all keys in the store.
        
        Returns:
            A list of all keys currently in the store.
        """
        return list(self._data.keys())
