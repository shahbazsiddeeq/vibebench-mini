# src/solution.py

class File:
    def __init__(self, name: str, size: int):
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Invalid file name")
        if not isinstance(size, int) or size < 0:
            raise ValueError("Invalid file size")
        
        self._name = name
        self._size = size

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    def total_size(self) -> int:
        return self.size


class Directory:
    def __init__(self, name: str):
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Invalid directory name")
        
        self._name = name
        self._children = {}

    @property
    def name(self) -> str:
        return self._name

    def add(self, child) -> 'Directory':
        if not isinstance(child, (File, Directory)):
            raise TypeError("Child must be a File or Directory")
        if child.name in self._children:
            raise ValueError("Child with the same name already exists")
        
        self._children[child.name] = child
        return self

    def total_size(self) -> int:
        return sum(child.total_size() for child in self._children.values())

    def count_files(self) -> int:
        count = 0
        for child in self._children.values():
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Directory):
                count += child.count_files()
        return count

    def list_paths(self) -> list[str]:
        paths = []
        for child in self._children.values():
            if isinstance(child, File):
                paths.append(child.name)
            elif isinstance(child, Directory):
                sub_paths = child.list_paths()
                for sub_path in sub_paths:
                    paths.append(f"{child.name}/{sub_path}")
        return sorted(paths)
