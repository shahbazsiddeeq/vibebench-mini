import os

def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1")
    if backup_count < 0:
        raise ValueError("backup_count cannot be negative")

    line = message.encode('utf-8') + b'\n'
    line_size = len(line)

    # Check if the log file exists and is non-empty
    if os.path.exists(path) and os.path.getsize(path) > 0:
        current_file_size = os.path.getsize(path)

        # Check if rotation is needed
        if current_file_size + line_size > max_bytes:
            if backup_count == 0:
                # Discard the current file
                open(path, 'wb').close()  # Truncate the file
            else:
                # Perform rotation
                if os.path.exists(path + f'.{backup_count}'):
                    os.remove(path + f'.{backup_count}')
                for i in range(backup_count - 1, 0, -1):
                    src = path + f'.{i}'
                    dst = path + f'.{i + 1}'
                    if os.path.exists(src):
                        os.rename(src, dst)
                os.rename(path, path + '.1')

    # Write the new log line
    with open(path, 'ab') as f:
        f.write(line)
