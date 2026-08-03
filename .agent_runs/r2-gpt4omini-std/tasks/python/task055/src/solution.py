import os
from datetime import datetime

def append_log(path, message, timestamp=True):
    # Create any missing parent directories
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Prepare the line to append
    if timestamp:
        ts = datetime.utcnow().isoformat(timespec='seconds') + "+00:00"
        line = f"{ts} {message}\n"
    else:
        line = f"{message}\n"
    
    # Append the line to the file
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
