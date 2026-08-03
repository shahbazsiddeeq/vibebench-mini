from __future__ import annotations

import os
from pathlib import Path


__all__ = ["safe_join"]


def safe_join(base: str | os.PathLike[str], user_path: str | os.PathLike[str]) -> str:
    """Join a relative user path to base while preventing filesystem escapes."""
    base_path = Path(base)
    relative_path = Path(user_path)

    if relative_path.is_absolute() or relative_path.anchor:
        raise ValueError("user_path must be relative")

    try:
        resolved_base = base_path.resolve(strict=False)
        resolved_path = (resolved_base / relative_path).resolve(strict=False)
        resolved_path.relative_to(resolved_base)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ValueError("path escapes base or cannot be resolved safely") from exc

    return str(resolved_path)
