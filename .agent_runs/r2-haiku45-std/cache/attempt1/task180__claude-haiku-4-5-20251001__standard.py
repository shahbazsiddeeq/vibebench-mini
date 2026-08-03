from typing import Union


class File:
    def __init__(self, name: str, size: int):
        # Validate name
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Name must be a non-empty string without '/' character")
        
        # Validate size - must be int and not bool
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise ValueError("Size must be a non-negative integer")
        
        self.name = name
        self.size = size
    
    def total_size(self) -> int:
        return self.size


class Directory:
    def __init__(self, name: str):
        # Validate name
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Name must be a non-empty string without '/' character")
        
        self.name = name
        self._children: dict[str, Union['Directory', File]] = {}
    
    def add(self, child: Union['Directory', File]) -> 'Directory':
        # Check if child is File or Directory
        if not isinstance(child, (File, Directory)):
            raise TypeError("Child must be a File or Directory")
        
        # Check if a child with the same name already exists
        if child.name in self._children:
            raise ValueError(f"A child with name '{child.name}' already exists")
        
        self._children[child.name] = child
        return self
    
    def total_size(self) -> int:
        total = 0
        for child in self._children.values():
            total += child.total_size()
        return total
    
    def count_files(self) -> int:
        count = 0
        for child in self._children.values():
            if isinstance(child, File):
                count += 1
            else:  # Directory
                count += child.count_files()
        return count
    
    def list_paths(self) -> list[str]:
        paths = []
        for child in self._children.values():
            if isinstance(child, File):
                paths.append(child.name)
            else:  # Directory
                sub_paths = child.list_paths()
                for sub_path in sub_paths:
                    paths.append(f"{child.name}/{sub_path}")
        return sorted(paths)
