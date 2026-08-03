import os
from pathlib import Path


def count_lines(path):
    """
    Count the number of lines in a UTF-8 text file.
    
    Args:
        path: Path to the file to count lines in
        
    Returns:
        int: Number of lines in the file
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    # Validate input
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or Path object")
    
    # Convert to Path object for safer handling
    file_path = Path(path)
    
    # Check if file exists - this will raise FileNotFoundError if it doesn't
    if not file_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    
    # Check if it's actually a file (not a directory)
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: '{path}'")
    
    # Count lines in the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        return line_count
    except PermissionError:
        raise PermissionError(f"Permission denied: '{path}'")
    except UnicodeDecodeError:
        raise ValueError(f"File is not valid UTF-8: '{path}'")
    except Exception as e:
        # Don't expose internal details, but re-raise as a generic error
        raise IOError(f"Error reading file: '{path}'")
