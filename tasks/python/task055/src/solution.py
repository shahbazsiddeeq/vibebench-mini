from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def append_log(path: str, message: str, timestamp: bool = True) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if timestamp:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        line = f"{ts} {message}\n"
    else:
        line = f"{message}\n"
    with p.open("a", encoding="utf-8") as f:
        f.write(line)
