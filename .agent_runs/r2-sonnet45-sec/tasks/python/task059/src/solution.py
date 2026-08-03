import os
from pathlib import Path
from typing import List


def tail(path: str, n: int) -> List[str]:
    """
    Returns the last n lines of a file as a list (without newlines).
    
    Args:
        path: Path to the file to read
        n: Number of lines to return from the end of the file
        
    Returns:
        List of the last n lines (without newlines)
        
    Raises:
        ValueError: If n < 0
        FileNotFoundError: If the file does not exist
    """
    # Validate n parameter
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Handle n == 0 case early
    if n == 0:
        return []
    
    # Validate and sanitize path
    # Convert to Path object for safer path handling
    file_path = Path(path)
    
    # Check if file exists - this will raise FileNotFoundError if it doesn't
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    # Check if it's actually a file (not a directory)
    if not file_path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    
    # Read the file and get lines
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            # Read all lines and strip newlines
            lines = [line.rstrip('\n\r') for line in f]
    except PermissionError:
        raise
    except Exception as e:
        # Re-raise as appropriate exception without exposing internals
        raise OSError(f"Error reading file") from None
    
    # Return the last n lines (or all lines if n > len(lines))
    return lines[-n:] if lines else []
