"""
File tail module - returns the last n lines of a file.
"""

from pathlib import Path


def tail(path: str, n: int) -> list[str]:
    """
    Returns the last n lines of a file as a list (without newlines).
    
    Args:
        path: Path to the file as a string
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
    
    # Convert path to Path object for validation and reading
    file_path = Path(path)
    
    # Check if file exists - will raise FileNotFoundError if not
    if not file_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    
    # Check if it's actually a file
    if not file_path.is_file():
        raise FileNotFoundError(f"Not a file: '{path}'")
    
    # Read the file and split into lines
    try:
        content = file_path.read_text(encoding='utf-8')
    except (OSError, IOError) as e:
        raise FileNotFoundError(f"Cannot read file: '{path}'") from e
    
    # Handle empty file
    if not content:
        return []
    
    # Split by newlines and filter out empty trailing element if file ends with newline
    lines = content.split('\n')
    
    # Remove the last empty string if the file ends with a newline
    if lines and lines[-1] == '':
        lines = lines[:-1]
    
    # Return the last n lines
    if n == 0:
        return []
    
    return lines[-n:] if n > 0 else []
