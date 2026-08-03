class File:
    """Represents a file in the file system."""
    
    def __init__(self, name: str, size: int):
        # Validate name
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if not name:
            raise ValueError("name must be non-empty")
        if '/' in name:
            raise ValueError("name must not contain '/'")
        
        # Validate size - must be int (not bool) and >= 0
        if isinstance(size, bool):
            raise ValueError("size must be an int, not a bool")
        if not isinstance(size, int):
            raise ValueError("size must be an int")
        if size < 0:
            raise ValueError("size must be >= 0")
        
        self.name = name
        self.size = size
    
    def total_size(self) -> int:
        """Return the size of this file."""
        return self.size


class Directory:
    """Represents a directory in the file system."""
    
    def __init__(self, name: str):
        # Validate name
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if not name:
            raise ValueError("name must be non-empty")
        if '/' in name:
            raise ValueError("name must not contain '/'")
        
        self.name = name
        self._children = {}
    
    def add(self, child):
        """Add a File or Directory child to this directory.
        
        Args:
            child: A File or Directory instance
            
        Returns:
            self (for method chaining)
            
        Raises:
            TypeError: If child is not a File or Directory
            ValueError: If a child with the same name already exists
        """
        if not isinstance(child, (File, Directory)):
            raise TypeError("child must be a File or Directory")
        
        if child.name in self._children:
            raise ValueError(f"child with name '{child.name}' already exists")
        
        self._children[child.name] = child
        return self
    
    def total_size(self) -> int:
        """Return the total size of all files in this directory tree."""
        total = 0
        for child in self._children.values():
            total += child.total_size()
        return total
    
    def count_files(self) -> int:
        """Return the number of File leaves in this directory tree."""
        count = 0
        for child in self._children.values():
            if isinstance(child, File):
                count += 1
            else:  # Directory
                count += child.count_files()
        return count
    
    def list_paths(self) -> list[str]:
        """Return sorted list of paths to all File leaves in this directory tree.
        
        Paths are relative to this directory (excluding this directory's name).
        """
        paths = []
        for child_name, child in self._children.items():
            if isinstance(child, File):
                paths.append(child_name)
            else:  # Directory
                # Get paths from subdirectory and prepend the subdirectory name
                sub_paths = child.list_paths()
                for sub_path in sub_paths:
                    paths.append(f"{child_name}/{sub_path}")
        
        return sorted(paths)
