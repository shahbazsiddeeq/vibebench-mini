import json
import os

class KVStore:
    def __init__(self, path: str):
        self.path = path
        self.store = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as file:
                self.store = json.load(file)

    def save(self):
        with open(self.path, 'w') as file:
            json.dump(self.store, file)

    def set(self, key: str, value: any):
        if '/' in key:
            raise ValueError("Key cannot contain '/'")
        self.store[key] = value
        self.save()

    def get(self, key: str, default=None) -> any:
        return self.store.get(key, default)

    def delete(self, key: str) -> bool:
        if key in self.store:
            del self.store[key]
            self.save()
            return True
        return False

    def keys(self) -> list[str]:
        return list(self.store.keys())
