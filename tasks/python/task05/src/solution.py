from pathlib import Path
def safe_join(base: str, user_path: str) -> str:
    base_p = Path(base).resolve()
    target = (base_p / user_path).resolve()
    if base_p in target.parents or base_p == target:
        return str(target)
    raise ValueError("path traversal detected")