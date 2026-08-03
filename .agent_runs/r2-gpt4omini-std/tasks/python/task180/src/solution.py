# src/solution.py

class File:
    def __init__(self, name: str, size: int):
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Invalid file name.")
        if not isinstance(size, int) or size < 0:
            raise ValueError("Invalid file size.")
        
        self.name = name
        self.size = size

    def total_size(self) -> int:
        return self.size


class Directory:
    def __init__(self, name: str):
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Invalid directory name.")
        
        self.name = name
        self.children = {}

    def add(self, child) -> 'Directory':
        if not isinstance(child, (File, Directory)):
            raise TypeError("Child must be a File or Directory.")
        if child.name in self.children:
            raise ValueError("Child with the same name already exists.")
        
        self.children[child.name] = child
        return self

    def total_size(self) -> int:
        return sum(child.total_size() for child in self.children.values())

    def count_files(self) -> int:
        return sum(child.count_files() if isinstance(child, Directory) else 1
                   for child in self.children.values())

    def list_paths(self) -> list[str]:
        paths = []
        for child in self.children.values():
            if isinstance(child, File):
                paths.append(child.name)
            else:
                sub_paths = child.list_paths()
                for path in sub_paths:
                    paths.append(f"{child.name}/{path}")
        return sorted(paths)
