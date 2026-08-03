# src/solution.py

import os
import errno

def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    # Validate inputs
    if not isinstance(path, str) or not isinstance(message, str):
        raise ValueError("Path and message must be strings.")
    if not isinstance(max_bytes, int) or not isinstance(backup_count, int):
        raise ValueError("max_bytes and backup_count must be integers.")
    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1.")
    if backup_count < 0:
        raise ValueError("backup_count cannot be negative.")

    # Prepare the log message
    log_message = message.encode('utf-8') + b'\n'
    line_size = len(log_message)

    # Check if the log file exists and is non-empty
    current_file_size = 0
    if os.path.exists(path):
        current_file_size = os.path.getsize(path)

    # Rotate if necessary
    if current_file_size > 0 and current_file_size + line_size > max_bytes:
        if backup_count == 0:
            # Discard the current file
            os.remove(path)
        else:
            # Rotate the backups
            for i in range(backup_count, 0, -1):
                src = f"{path}.{i}"
                dst = f"{path}.{i + 1}"
                if os.path.exists(src):
                    os.rename(src, dst)
            # Rename the current log file
            os.rename(path, f"{path}.1")

    # Write the log message
    with open(path, "ab") as log_file:
        log_file.write(log_message)
