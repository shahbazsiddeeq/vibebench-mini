import os
from pathlib import Path
from datetime import datetime, timezone


def append_log(path, message, timestamp=True):
    """
    Append a single line to a UTF-8 text file at the given path.
    
    Args:
        path: File path as string
        message: Message to append
        timestamp: If True, prepend ISO-8601 UTC timestamp
    
    Returns:
        None
    """
    # Validate inputs
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if not isinstance(timestamp, bool):
        raise TypeError("timestamp must be a boolean")
    
    # Validate path is not empty
    if not path or not path.strip():
        raise ValueError("path cannot be empty")
    
    # Convert to Path object and resolve to absolute path
    try:
        file_path = Path(path).resolve()
    except (ValueError, RuntimeError) as e:
        raise ValueError(f"Invalid path: {e}")
    
    # Create parent directories if they don't exist
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError) as e:
        raise IOError(f"Cannot create parent directories: {e}")
    
    # Prepare the line to write
    if timestamp:
        # Get current UTC time in ISO-8601 format to seconds precision
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        line = f"{ts} {message}\n"
    else:
        line = f"{message}\n"
    
    # Append to file
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(line)
    except (OSError, PermissionError, IOError) as e:
        raise IOError(f"Cannot write to file: {e}")
    
    return None
