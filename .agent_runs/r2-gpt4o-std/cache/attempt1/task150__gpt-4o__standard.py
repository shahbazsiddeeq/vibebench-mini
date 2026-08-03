import os

def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1")
    if backup_count < 0:
        raise ValueError("backup_count cannot be negative")

    line = message.encode('utf-8') + b'\n'
    line_size = len(line)

    if os.path.exists(path):
        current_file_size = os.path.getsize(path)
    else:
        current_file_size = 0

    if current_file_size > 0 and current_file_size + line_size > max_bytes:
        # Perform rotation
        if backup_count == 0:
            # Discard the current file
            os.remove(path)
        else:
            # Delete the oldest backup if it exists
            oldest_backup = f"{path}.{backup_count}"
            if os.path.exists(oldest_backup):
                os.remove(oldest_backup)

            # Shift backups
            for i in range(backup_count - 1, 0, -1):
                src = f"{path}.{i}"
                dst = f"{path}.{i + 1}"
                if os.path.exists(src):
                    os.rename(src, dst)

            # Rename current file to .1
            os.rename(path, f"{path}.1")

    # Write the new log line
    with open(path, 'ab') as f:
        f.write(line)
