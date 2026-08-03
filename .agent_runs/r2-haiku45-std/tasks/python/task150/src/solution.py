import os


def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    """
    Appends a log line to the file at `path`. Rotates the file if necessary.
    
    Args:
        path: Path to the log file
        message: Message to append
        max_bytes: Maximum size of the log file before rotation
        backup_count: Number of backup files to keep
        
    Raises:
        ValueError: If max_bytes < 1 or backup_count < 0
    """
    if max_bytes < 1:
        raise ValueError("max_bytes must be >= 1")
    if backup_count < 0:
        raise ValueError("backup_count must be >= 0")
    
    # Encode the message and add newline
    line_bytes = message.encode('utf-8') + b'\n'
    line_size = len(line_bytes)
    
    # Check if rotation is needed
    should_rotate = False
    if os.path.exists(path) and os.path.getsize(path) > 0:
        current_size = os.path.getsize(path)
        if current_size + line_size > max_bytes:
            should_rotate = True
    
    # Perform rotation if needed
    if should_rotate:
        if backup_count == 0:
            # Discard the current file
            os.remove(path)
        else:
            # Delete the oldest backup if it exists
            oldest_backup = path + '.' + str(backup_count)
            if os.path.exists(oldest_backup):
                os.remove(oldest_backup)
            
            # Rename backups: path.i -> path.(i+1) for i from backup_count-1 down to 1
            for i in range(backup_count - 1, 0, -1):
                old_name = path + '.' + str(i)
                new_name = path + '.' + str(i + 1)
                if os.path.exists(old_name):
                    os.rename(old_name, new_name)
            
            # Rename current file to path.1
            os.rename(path, path + '.1')
    
    # Write the new line (creating the file if absent)
    with open(path, 'ab') as f:
        f.write(line_bytes)
