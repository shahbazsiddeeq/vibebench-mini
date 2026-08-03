from __future__ import annotations

import time
from typing import Any, Callable


def retry(
    func: Callable,
    max_attempts: int,
    base_delay: float,
    exceptions: tuple,
) -> Any:
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as exc:
            last_exc = exc
            if attempt < max_attempts - 1:
                time.sleep(base_delay * (2**attempt))
    raise last_exc
