import os
import datetime

def append_log(path: str, message: str, timestamp: bool = True) -> None:
    # Validate inputs
    if not isinstance(path, str) or not isinstance(message, str):
        raise ValueError("Both path and message must be strings.")
    
    # Sanitize inputs
    path = os.path.normpath(path)
    message = message.strip()

    # Create parent directories if they do not exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Prepare the log line
    if timestamp:
        current_time = datetime.datetime.utcnow().isoformat(timespec='seconds') + "+00:00"
        log_line = f"{current_time} {message}\n"
    else:
        log_line = f"{message}\n"

    # Append the log line to the file
    with open(path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_line)
