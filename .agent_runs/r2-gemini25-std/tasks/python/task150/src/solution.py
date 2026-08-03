import os

def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1")
    if backup_count < 0:
        raise ValueError("backup_count must be non-negative")

    line_bytes = message.encode('utf-8') + b'\n'
    line_size = len(line_bytes)

    current_file_size = 0
    if os.path.exists(path):
        current_file_size = os.path.getsize(path)

    should_rotate = False
    if current_file_size > 0 and current_file_size + line_size > max_bytes:
        should_rotate = True

    if should_rotate:
        if backup_count == 0:
            # Discard the current file by truncating it
            with open(path, 'wb') as f:
                f.truncate(0)
        else:
            # Delete the oldest backup if it exists
            oldest_backup_path = f"{path}.{backup_count}"
            if os.path.exists(oldest_backup_path):
                os.remove(oldest_backup_path)

            # Shift existing backups
            for i in range(backup_count - 1, 0, -1):
                src_path = f"{path}.{i}"
                dest_path = f"{path}.{i+1}"
                if os.path.exists(src_path):
                    os.rename(src_path, dest_path)

            # Rename the current log file to the first backup
            os.rename(path, f"{path}.1")

    # Append the new line
    with open(path, 'ab') as f:
        f.write(line_bytes)
