import json
import os


class KVStore:
    def __init__(self, path):
        self.path = path
        self.data = {}
        self._load()
    
    def _load(self):
        """Load data from the JSON file if it exists."""
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = {}
        else:
            self.data = {}
    
    def _save(self):
        """Save data to the JSON file."""
        with open(self.path, 'w') as f:
            json.dump(self.data, f)
    
    def set(self, key, value):
        """Set a key-value pair. Raises ValueError if key contains '/'."""
        if '/' in key:
            raise ValueError("Key cannot contain '/'")
        self.data[key] = value
        self._save()
    
    def get(self, key, default=None):
        """Get a value by key, returning default if not found."""
        return self.data.get(key, default)
    
    def delete(self, key):
        """Delete a key. Returns True if key existed, False otherwise."""
        if key in self.data:
            del self.data[key]
            self._save()
            return True
        return False
    
    def keys(self):
        """Return a list of all keys."""
        return list(self.data.keys())
