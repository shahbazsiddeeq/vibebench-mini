import os
from datetime import datetime, timezone
from pathlib import Path


def append_log(path, message, timestamp=True):
    """
    Append a single line to the UTF-8 text file at path.
    
    Args:
        path: Path to the log file
        message: Message to append
        timestamp: If True, prepend ISO-8601 timestamp in UTC
    
    Returns:
        None
    """
    # Create parent directories if they don't exist
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Prepare the line to write
    if timestamp:
        # Get current UTC time in ISO-8601 format with seconds precision
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        line = f"{ts} {message}\n"
    else:
        line = f"{message}\n"
    
    # Append to file
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(line)
