# src/solution.py

class File:
    def __init__(self, name: str, size: int):
        if not isinstance(size, int) or size < 0:
            raise ValueError("Size must be a non-negative integer.")
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Name must be a non-empty string without '/' character.")
        self.name = name
        self.size = size

    def total_size(self) -> int:
        return self.size


class Directory:
    def __init__(self, name: str):
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Name must be a non-empty string without '/' character.")
        self.name = name
        self.children = {}

    def add(self, child):
        if not isinstance(child, (File, Directory)):
            raise TypeError("Child must be a File or Directory.")
        if child.name in self.children:
            raise ValueError("A child with the same name already exists.")
        self.children[child.name] = child
        return self

    def total_size(self) -> int:
        return sum(child.total_size() for child in self.children.values())

    def count_files(self) -> int:
        count = 0
        for child in self.children.values():
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Directory):
                count += child.count_files()
        return count

    def list_paths(self) -> list[str]:
        paths = []
        for child in self.children.values():
            if isinstance(child, File):
                paths.append(child.name)
            elif isinstance(child, Directory):
                sub_paths = child.list_paths()
                for sub_path in sub_paths:
                    paths.append(f"{child.name}/{sub_path}")
        return sorted(paths)
