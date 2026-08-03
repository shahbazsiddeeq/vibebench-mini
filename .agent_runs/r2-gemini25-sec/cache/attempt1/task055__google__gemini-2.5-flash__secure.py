import os
from datetime import datetime, timezone

def append_log(path: str, message: str, timestamp: bool = True) -> None:
    """
    Appends a single line to the UTF-8 text file at `path`.
    Any missing parent directories are created as well as the file itself.
    Each call appends exactly one line terminated by "\n".
    When timestamp is True the line is "<ts> <message>\n", where <ts> is the current time in
    UTC formatted as ISO-8601 to seconds precision (e.g. "2026-07-24T12:34:56+00:00"), followed
    by a single space and then the message.
    When timestamp is False the line is just "<message>\n".
    The function returns None.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string.")
    if not path:
        raise ValueError("path cannot be empty.")
    if not isinstance(message, str):
        raise TypeError("message must be a string.")
    if not isinstance(timestamp, bool):
        raise TypeError("timestamp must be a boolean.")

    # Sanitize path to prevent directory traversal, though os.makedirs is generally safe
    # for creating directories based on a path. The primary concern here is ensuring
    # the path is a valid file path and not something malicious.
    # For this specific task, we're assuming 'path' is intended to be a file path.
    # We'll rely on os.path.abspath and os.path.normpath to handle path normalization.
    # However, direct validation of path components is complex and often overkill
    # for simple file operations unless dealing with untrusted user input directly
    # as part of a web request or similar. For a local file system operation,
    # os.makedirs and file open will raise appropriate OS errors for invalid paths.

    # Ensure parent directories exist
    dir_name = os.path.dirname(path)
    if dir_name: # Only create if there's a directory component
        try:
            os.makedirs(dir_name, exist_ok=True)
        except OSError as e:
            # Catch OS-level errors like permission denied, invalid path components, etc.
            raise IOError(f"Failed to create directory '{dir_name}': {e}") from e

    line_to_write: str
    if timestamp:
        now_utc = datetime.now(timezone.utc)
        # Format to ISO-8601 with seconds precision and UTC offset
        # Example: "2026-07-24T12:34:56+00:00"
        ts_str = now_utc.isoformat(timespec='seconds')
        line_to_write = f"{ts_str} {message}\n"
    else:
        line_to_write = f"{message}\n"

    try:
        # Use 'a' mode for appending, 'utf-8' encoding for consistency
        with open(path, 'a', encoding='utf-8') as f:
            f.write(line_to_write)
    except OSError as e:
        # Catch file-related OS errors (e.g., permission denied, disk full)
        raise IOError(f"Failed to write to log file '{path}': {e}") from e
    except Exception as e:
        # Catch any other unexpected errors during file writing
        raise RuntimeError(f"An unexpected error occurred while writing to '{path}': {e}") from e
