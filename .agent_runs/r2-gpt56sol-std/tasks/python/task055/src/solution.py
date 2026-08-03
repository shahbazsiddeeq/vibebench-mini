from datetime import datetime, timezone
from pathlib import Path
from typing import Union


def append_log(
    path: Union[str, bytes, Path],
    message: str,
    timestamp: bool = True,
) -> None:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if timestamp:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        line = f"{ts} {message}\n"
    else:
        line = f"{message}\n"

    with log_path.open("a", encoding="utf-8", newline="") as log_file:
        log_file.write(line)
