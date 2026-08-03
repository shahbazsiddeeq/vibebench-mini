import os
from datetime import datetime, timezone

def append_log(path, message, timestamp=True):
    if not isinstance(path, str) or not path:
        raise ValueError("Invalid path provided.")
    if not isinstance(message, str):
        raise ValueError("Message must be a string.")
    if not isinstance(timestamp, bool):
        raise ValueError("Timestamp must be a boolean.")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Prepare the log line
    if timestamp:
        current_time = datetime.now(timezone.utc).isoformat(timespec='seconds')
        log_line = f"{current_time} {message}\n"
    else:
        log_line = f"{message}\n"

    # Append the log line to the file
    with open(path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_line)
