"""
Composite File System Tree implementation.

This module implements the Composite pattern for a file system with File and Directory classes.
"""

from typing import Union, List


class File:
    """Represents a leaf file in the file system."""
    
    def __init__(self, name: str, size: int) -> None:
        """
        Initialize a File.
        
        Args:
            name: Non-empty string without '/' character
            size: Non-negative integer (bool is not valid)
            
        Raises:
            ValueError: If name is empty, contains '/', or size is invalid
        """
        # Validate name
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("File name must be a non-empty string without '/' character")
        
        # Validate size - must be int but not bool
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise ValueError("File size must be a non-negative integer")
        
        self.name = name
        self.size = size
    
    def total_size(self) -> int:
        """Return the size of this file."""
        return self.size


class Directory:
    """Represents a container directory in the file system."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize a Directory.
        
        Args:
            name: Non-empty string without '/' character
            
        Raises:
            ValueError: If name is empty or contains '/'
        """
        # Validate name
        if not isinstance(name, str) or not name or '/' in name:
            raise ValueError("Directory name must be a non-empty string without '/' character")
        
        self.name = name
        self._children: List[Union[File, Directory]] = []
    
    def add(self, child: Union['File', 'Directory']) -> 'Directory':
        """
        Add a child (File or Directory) to this directory.
        
        Args:
            child: A File or Directory instance
            
        Returns:
            This Directory instance (for chaining)
            
        Raises:
            TypeError: If child is neither File nor Directory
            ValueError: If a child with the same name already exists
        """
        if not isinstance(child, (File, Directory)):
            raise TypeError("Child must be a File or Directory instance")
        
        # Check for duplicate names
        for existing_child in self._children:
            if existing_child.name == child.name:
                raise ValueError(f"A child with name '{child.name}' already exists in this directory")
        
        self._children.append(child)
        return self
    
    def total_size(self) -> int:
        """Return the sum of total_size() over all descendants recursively."""
        total = 0
        for child in self._children:
            total += child.total_size()
        return total
    
    def count_files(self) -> int:
        """Return the number of File leaves in the whole subtree."""
        count = 0
        for child in self._children:
            if isinstance(child, File):
                count += 1
            else:  # Directory
                count += child.count_files()
        return count
    
    def list_paths(self) -> List[str]:
        """
        Return the '/'-joined path of every File leaf in the subtree.
        
        Paths are relative to (and excluding) this directory's own name,
        sorted lexicographically.
        
        Returns:
            Sorted list of file paths
        """
        paths = []
        
        for child in self._children:
            if isinstance(child, File):
                paths.append(child.name)
            else:  # Directory
                # Recursively get paths from subdirectory
                sub_paths = child.list_paths()
                for sub_path in sub_paths:
                    paths.append(f"{child.name}/{sub_path}")
        
        # Sort lexicographically
        paths.sort()
        return paths
