import os


def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    """
    Appends a log line to the file at path with size-based rotation.
    
    Args:
        path: Path to the log file
        message: Message to write (will be encoded as UTF-8)
        max_bytes: Maximum file size before rotation
        backup_count: Number of backup files to keep
        
    Raises:
        ValueError: If max_bytes < 1 or backup_count < 0
    """
    # Validate inputs
    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1")
    if backup_count < 0:
        raise ValueError("backup_count must be non-negative")
    
    # Calculate the size of the line to write
    line_bytes = message.encode('utf-8') + b'\n'
    line_size = len(line_bytes)
    
    # Check if rotation is needed
    needs_rotation = False
    if os.path.exists(path):
        current_size = os.path.getsize(path)
        if current_size > 0 and current_size + line_size > max_bytes:
            needs_rotation = True
    
    # Perform rotation if needed
    if needs_rotation:
        if backup_count == 0:
            # Discard the current file (it will be overwritten with new content)
            os.remove(path)
        else:
            # Delete the oldest backup if it exists
            oldest_backup = path + '.' + str(backup_count)
            if os.path.exists(oldest_backup):
                os.remove(oldest_backup)
            
            # Shift existing backups
            for i in range(backup_count - 1, 0, -1):
                old_backup = path + '.' + str(i)
                new_backup = path + '.' + str(i + 1)
                if os.path.exists(old_backup):
                    os.rename(old_backup, new_backup)
            
            # Rename current file to .1
            os.rename(path, path + '.1')
    
    # Write the new line
    # After rotation, path doesn't exist, so we write a new file
    # If no rotation, we append to existing file (or create new)
    mode = 'ab' if os.path.exists(path) else 'wb'
    with open(path, mode) as f:
        f.write(line_bytes)
