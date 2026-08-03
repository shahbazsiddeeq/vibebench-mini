import os
from datetime import datetime, timezone


def append_log(path, message, timestamp=True):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    if timestamp:
        ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        line = f"{ts} {message}\n"
    else:
        line = f"{message}\n"

    with open(path, "a", encoding="utf-8") as f:
        f.write(line)

    return None
