import json
import os
import fcntl
import secrets

class KVStore:
    """
    A file-backed key-value store that persists data to a JSON file.

    Keys must be strings and cannot contain the '/' character.
    Values can be any JSON-serializable type.

    The store uses file locking to ensure data integrity during concurrent access.
    """

    _LOCK_SUFFIX = ".lock"
    _TEMP_SUFFIX = ".tmp"

    def __init__(self, path: str):
        """
        Initializes the KVStore.

        Args:
            path: The path to the JSON file where data will be stored.
                  The directory for the path must exist.
        Raises:
            ValueError: If the path is invalid (e.g., not a string).
            IOError: If there's an issue accessing the file or its directory.
        """
        if not isinstance(path, str) or not path:
            raise ValueError("Path must be a non-empty string.")

        self._path = path
        self._lock_path = path + self._LOCK_SUFFIX
        self._data = {}
        self._load_data()

    def _validate_key(self, key: str):
        """
        Validates a key to ensure it's a string and does not contain '/'.

        Args:
            key: The key to validate.

        Raises:
            ValueError: If the key is invalid.
        """
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
        if "/" in key:
            raise ValueError("Key cannot contain '/' character.")

    def _acquire_lock(self, lock_file):
        """Acquires an exclusive file lock."""
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX)
        except OSError as e:
            raise IOError(f"Failed to acquire file lock for {self._path}: {e}") from e

    def _release_lock(self, lock_file):
        """Releases an exclusive file lock."""
        try:
            fcntl.flock(lock_file, fcntl.LOCK_UN)
        except OSError as e:
            # Log or handle this, but don't re-raise as it might mask original error
            # and the lock is likely already released by OS on file close.
            pass

    def _load_data(self):
        """
        Loads data from the JSON file into memory.
        Handles file locking to ensure safe reading.
        """
        if not os.path.exists(self._path):
            self._data = {}
            return

        try:
            with open(self._lock_path, 'a') as lock_file: # Open in append mode to create if not exists
                self._acquire_lock(lock_file)
                try:
                    with open(self._path, 'r', encoding='utf-8') as f:
                        # Ensure file is not empty before loading JSON
                        file_content = f.read().strip()
                        if file_content:
                            self._data = json.loads(file_content)
                        else:
                            self._data = {}
                except json.JSONDecodeError as e:
                    # If the file is corrupted, initialize with empty data
                    # and log the error (or raise a specific error if desired).
                    # For security, we don't expose internal details of the corruption.
                    self._data = {}
                    # In a real application, you might log this:
                    # import logging
                    # logging.error(f"Corrupted JSON data in {self._path}: {e}")
                except FileNotFoundError:
                    # This case should ideally be caught by os.path.exists,
                    # but as a safeguard.
                    self._data = {}
                except OSError as e:
                    raise IOError(f"Error reading data from {self._path}: {e}") from e
                finally:
                    self._release_lock(lock_file)
        except IOError:
            # Re-raise if lock acquisition failed
            raise
        except Exception as e:
            # Catch any other unexpected errors during load
            raise IOError(f"An unexpected error occurred during data loading: {e}") from e


    def _save_data(self):
        """
        Saves the current in-memory data to the JSON file.
        Uses a temporary file and atomic rename for durability and integrity,
        along with file locking.
        """
        temp_path = f"{self._path}.{secrets.token_hex(8)}{self._TEMP_SUFFIX}"

        try:
            with open(self._lock_path, 'a') as lock_file:
                self._acquire_lock(lock_file)
                try:
                    # Write to a temporary file first
                    with open(temp_path, 'w', encoding='utf-8') as f_tmp:
                        json.dump(self._data, f_tmp, ensure_ascii=False, indent=None, separators=(',', ':'))
                    # Atomically replace the original file
                    os.replace(temp_path, self._path)
                except OSError as e:
                    raise IOError(f"Error writing data to {self._path}: {e}") from e
                except Exception as e:
                    # Catch any other unexpected errors during save
                    raise IOError(f"An unexpected error occurred during data saving: {e}") from e
                finally:
                    self._release_lock(lock_file)
        except IOError:
            raise # Re-raise if lock acquisition failed
        finally:
            # Clean up temporary file if it still exists (e.g., due to an error before rename)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    # Log this, but don't re-raise as the main operation failed already
                    pass

    def set(self, key: str, value: any):
        """
        Sets a key-value pair in the store.

        Args:
            key: The key to set. Must be a string and not contain '/'.
            value: The value to associate with the key. Must be JSON-serializable.

        Raises:
            ValueError: If the key is invalid.
            IOError: If there's an issue saving the data.
        """
        self._validate_key(key)
        self._data[key] = value
        self._save_data()

    def get(self, key: str, default: any = None) -> any:
        """
        Retrieves the value associated with a key.

        Args:
            key: The key to retrieve. Must be a string and not contain '/'.
            default: The value to return if the key is not found. Defaults to None.

        Returns:
            The value associated with the key, or the default value if not found.

        Raises:
            ValueError: If the key is invalid.
        """
        self._validate_key(key)
        return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        """
        Deletes a key-value pair from the store.

        Args:
            key: The key to delete. Must be a string and not contain '/'.

        Returns:
            True if the key was found and deleted, False otherwise.

        Raises:
            ValueError: If the key is invalid.
            IOError: If there's an issue saving the data.
        """
        self._validate_key(key)
        if key in self._data:
            del self._data[key]
            self._save_data()
            return True
        return False

    def keys(self) -> list[str]:
        """
        Returns a list of all keys currently in the store.

        Returns:
            A list of strings representing the keys.
        """
        return list(self._data.keys())
