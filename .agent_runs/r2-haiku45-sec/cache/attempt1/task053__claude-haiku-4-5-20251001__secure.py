"""
Secure module for counting lines in UTF-8 text files.
"""

import os
from pathlib import Path


def count_lines(path: str) -> int:
    """
    Count the number of lines in a UTF-8 text file.
    
    Args:
        path: String path to the file to count lines in.
        
    Returns:
        The number of lines in the file.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If path is not a valid string.
    """
    # Validate input
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    
    if not path:
        raise ValueError("Path cannot be empty")
    
    # Convert to Path object for safe handling
    file_path = Path(path)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    # Ensure it's a file, not a directory
    if not file_path.is_file():
        raise FileNotFoundError(f"Path is not a file: {path}")
    
    # Count lines by reading the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        return line_count
    except (IOError, OSError) as e:
        raise FileNotFoundError(f"Cannot read file: {path}") from e
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {path}") from e
