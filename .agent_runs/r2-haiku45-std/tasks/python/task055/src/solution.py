import os
from datetime import datetime, timezone


def append_log(path, message, timestamp=True):
    """
    Appends a single line to the UTF-8 text file at `path`.
    
    Args:
        path: File path to append to
        message: Message to append
        timestamp: If True, prepend ISO-8601 timestamp to the message
    
    Returns:
        None
    """
    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    
    # Format the line to append
    if timestamp:
        # Get current UTC time in ISO-8601 format to seconds precision
        ts = datetime.now(timezone.utc).isoformat(timespec='seconds')
        line = f"{ts} {message}\n"
    else:
        line = f"{message}\n"
    
    # Append to file
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
