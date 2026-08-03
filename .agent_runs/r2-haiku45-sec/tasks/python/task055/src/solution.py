import os
from datetime import datetime, timezone


def append_log(path, message, timestamp=True):
    """
    Append a single line to a UTF-8 text file at `path`.
    
    Creates any missing parent directories and the file itself.
    Each call appends exactly one line terminated by "\\n".
    
    When timestamp is True, the line is "<ts> <message>\\n" where <ts> is
    the current time in UTC formatted as ISO-8601 to seconds precision.
    When timestamp is False, the line is just "<message>\\n".
    
    Args:
        path: File path (string)
        message: Message to append (string)
        timestamp: Whether to prepend ISO-8601 timestamp (bool, default True)
    
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
    
    # Sanitize path - ensure it's not empty and doesn't contain null bytes
    if not path:
        raise ValueError("path cannot be empty")
    if '\0' in path:
        raise ValueError("path cannot contain null bytes")
    
    # Create parent directories if needed
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
