import os
import stat

def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    """
    Appends one log line to the file at `path`. Rotates the log file if
    appending the new line would exceed `max_bytes`.

    Args:
        path: The path to the log file.
        message: The string message to write to the log.
        max_bytes: The maximum size in bytes the log file can reach before rotation.
        backup_count: The number of backup files to keep. If 0, the current file
                      is discarded upon rotation.

    Raises:
        ValueError: If max_bytes < 1 or backup_count < 0.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if not isinstance(max_bytes, int):
        raise TypeError("max_bytes must be an integer")
    if not isinstance(backup_count, int):
        raise TypeError("backup_count must be an integer")

    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1")
    if backup_count < 0:
        raise ValueError("backup_count cannot be negative")

    encoded_message = message.encode('utf-8')
    line_to_write = encoded_message + b'\n'
    line_size = len(line_to_write)

    current_file_size = 0
    file_exists = False

    try:
        # Check if the file exists and get its size securely
        # Using os.stat to get file size and check existence
        # This is more robust than os.path.getsize which can raise FileNotFoundError
        # and doesn't provide as much info.
        file_stat = os.stat(path)
        if stat.S_ISREG(file_stat.st_mode): # Ensure it's a regular file
            current_file_size = file_stat.st_size
            file_exists = True
        else:
            # If it exists but is not a regular file (e.g., a directory, symlink to non-file),
            # treat it as if it doesn't exist for logging purposes to avoid issues.
            # Or, raise an error if this is an unexpected scenario.
            # For this task, we'll treat it as non-existent to create a new log.
            file_exists = False
    except FileNotFoundError:
        file_exists = False
    except OSError as e:
        # Handle other OS errors during stat, e.g., permission denied
        # For security, avoid exposing internal details. Log the error if possible.
        # For this problem, we'll re-raise as a generic OSError or let it propagate.
        raise OSError(f"Error accessing file '{path}': {e}") from e

    # Rotation condition: file exists, is non-empty, and new line would exceed max_bytes
    if file_exists and current_file_size > 0 and (current_file_size + line_size > max_bytes):
        # Perform rotation
        if backup_count == 0:
            # Discard current file by truncating it
            try:
                with open(path, 'wb') as f:
                    f.truncate(0) # Truncate to empty
                # After truncation, the file exists but is empty, so we don't need to rename.
                # The new line will be written to this now-empty file.
            except OSError as e:
                raise OSError(f"Error truncating file '{path}': {e}") from e
        else:
            # Delete the oldest backup
            oldest_backup_path = f"{path}.{backup_count}"
            try:
                if os.path.exists(oldest_backup_path):
                    os.remove(oldest_backup_path)
            except OSError as e:
                # Log or handle error, but continue with rotation if possible
                # For this problem, we'll re-raise.
                raise OSError(f"Error deleting old backup '{oldest_backup_path}': {e}") from e

            # Shift existing backups
            for i in range(backup_count - 1, 0, -1):
                src = f"{path}.{i}"
                dst = f"{path}.{i+1}"
                try:
                    if os.path.exists(src):
                        os.rename(src, dst)
                except OSError as e:
                    # Log or handle error, but continue with rotation if possible
                    raise OSError(f"Error renaming backup from '{src}' to '{dst}': {e}") from e

            # Rename current log file to the first backup
            new_backup_path = f"{path}.1"
            try:
                os.rename(path, new_backup_path)
            except OSError as e:
                raise OSError(f"Error renaming '{path}' to '{new_backup_path}': {e}") from e

    # Append the new line
    # Use 'ab' mode for appending in binary mode.
    # If the file was rotated (and backup_count > 0), 'path' no longer exists,
    # so 'ab' will create it.
    # If backup_count == 0, 'path' was truncated, so 'ab' will append to the empty file.
    # If no rotation, 'ab' appends to the existing file.
    try:
        with open(path, 'ab') as f:
            f.write(line_to_write)
    except OSError as e:
        raise OSError(f"Error writing to log file '{path}': {e}") from e
