import os
from datetime import datetime, timezone


def append_log(path, message, timestamp=True):
    """
    Appends a single line to the UTF-8 text file at `path`.
    Any missing parent directories are created as well as the file itself.
    Each call appends exactly one line terminated by "\n".
    When timestamp is True the line is "<ts> <message>\n", where <ts> is the current time in
    UTC formatted as ISO-8601 to seconds precision (e.g. "2026-07-24T12:34:56+00:00"), followed
    by a single space and then the message.
    When timestamp is False the line is just "<message>\n".
    The function returns None.
    """
    dirname = os.path.dirname(path)
    if dirname:  # Only create directory if path includes a directory component
        os.makedirs(dirname, exist_ok=True)

    line = ""
    if timestamp:
        now_utc = datetime.now(timezone.utc)
        # Format to ISO-8601 with seconds precision and UTC offset
        # Example: "2026-07-24T12:34:56+00:00"
        ts_str = now_utc.isoformat(timespec='seconds')
        line = f"{ts_str} {message}\n"
    else:
        line = f"{message}\n"

    with open(path, 'a', encoding='utf-8') as f:
        f.write(line)
