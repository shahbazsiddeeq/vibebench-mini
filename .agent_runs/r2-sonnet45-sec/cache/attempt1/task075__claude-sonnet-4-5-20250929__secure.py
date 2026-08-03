import json
import os
from typing import Any, Optional


class KVStore:
    """A file-backed key-value store that persists data to a JSON file."""
    
    def __init__(self, path: str):
        """Initialize the KVStore with a file path.
        
        Args:
            path: Path to the JSON file for persistence
        """
        if not isinstance(path, str):
            raise TypeError("Path must be a string")
        
        self._path = path
        self._data = {}
        self._load()
    
    def _validate_key(self, key: str) -> None:
        """Validate that a key is acceptable.
        
        Args:
            key: The key to validate
            
        Raises:
            ValueError: If key contains "/"
            TypeError: If key is not a string
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if "/" in key:
            raise ValueError("Key cannot contain '/'")
    
    def _load(self) -> None:
        """Load data from the JSON file if it exists."""
        if os.path.exists(self._path):
            try:
                with open(self._path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        loaded_data = json.loads(content)
                        if isinstance(loaded_data, dict):
                            self._data = loaded_data
                        else:
                            self._data = {}
                    else:
                        self._data = {}
            except (json.JSONDecodeError, IOError, OSError):
                # If file is corrupted or unreadable, start with empty store
                self._data = {}
        else:
            self._data = {}
    
    def _save(self) -> None:
        """Save data to the JSON file."""
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(self._path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, mode=0o755, exist_ok=True)
            
            # Write to a temporary file first, then rename for atomicity
            temp_path = self._path + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            
            # Atomic rename
            os.replace(temp_path, self._path)
        except (IOError, OSError) as e:
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except (IOError, OSError):
                    pass
            raise IOError(f"Failed to save data") from e
    
    def set(self, key: str, value: Any) -> None:
        """Set a key-value pair in the store.
        
        Args:
            key: The key to set
            value: The value to associate with the key
            
        Raises:
            ValueError: If key contains "/"
        """
        self._validate_key(key)
        self._data[key] = value
        self._save()
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a value from the store.
        
        Args:
            key: The key to retrieve
            default: The default value to return if key is not found
            
        Returns:
            The value associated with the key, or default if not found
        """
        if not isinstance(key, str):
            return default
        return self._data.get(key, default)
    
    def delete(self, key: str) -> bool:
        """Delete a key from the store.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was deleted, False if it didn't exist
        """
        if not isinstance(key, str):
            return False
        
        if key in self._data:
            del self._data[key]
            self._save()
            return True
        return False
    
    def keys(self) -> list:
        """Get all keys in the store.
        
        Returns:
            A list of all keys
        """
        return list(self._data.keys())
