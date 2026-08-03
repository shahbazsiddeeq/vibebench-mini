import os


def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    """
    Appends a log line to the file at `path` with size-based rotation.
    
    Args:
        path: Path to the log file
        message: Message to log (will be encoded as UTF-8)
        max_bytes: Maximum file size in bytes before rotation
        backup_count: Number of backup files to keep (0 = discard on rotation)
    
    Raises:
        ValueError: If max_bytes < 1 or backup_count < 0
    """
    # Validate inputs
    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1")
    if backup_count < 0:
        raise ValueError("backup_count must be non-negative")
    
    # Validate path is a string
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    
    # Validate message is a string
    if not isinstance(message, str):
        raise ValueError("message must be a string")
    
    # Encode the message with newline
    line_bytes = message.encode('utf-8') + b'\n'
    line_size = len(line_bytes)
    
    # Check if rotation is needed
    should_rotate = False
    if os.path.exists(path):
        try:
            current_size = os.path.getsize(path)
            # Only rotate if file is non-empty AND would exceed max_bytes
            if current_size > 0 and current_size + line_size > max_bytes:
                should_rotate = True
        except OSError:
            # If we can't get file size, don't rotate
            pass
    
    # Perform rotation if needed
    if should_rotate:
        if backup_count == 0:
            # Discard the current file (truncate to empty)
            try:
                os.remove(path)
            except OSError:
                pass
        else:
            # Delete the oldest backup if it exists
            oldest_backup = path + '.' + str(backup_count)
            if os.path.exists(oldest_backup):
                try:
                    os.remove(oldest_backup)
                except OSError:
                    pass
            
            # Rotate existing backups
            for i in range(backup_count - 1, 0, -1):
                old_backup = path + '.' + str(i)
                new_backup = path + '.' + str(i + 1)
                if os.path.exists(old_backup):
                    try:
                        os.rename(old_backup, new_backup)
                    except OSError:
                        pass
            
            # Rename current log to .1
            backup_path = path + '.1'
            try:
                os.rename(path, backup_path)
            except OSError:
                pass
    
    # Write the new line
    # Use binary mode to avoid newline translation
    with open(path, 'ab') as f:
        f.write(line_bytes)
