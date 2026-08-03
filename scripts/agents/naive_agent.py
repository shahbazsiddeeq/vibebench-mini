#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def infer_func_name(test_path: Path) -> str | None:
    txt = test_path.read_text(encoding="utf-8")
    m = re.search(r"from\s+src\.solution\s+import\s+([A-Za-z_][A-Za-z0-9_]*)", txt)
    return m.group(1) if m else None


def write_placeholder(task_dir: Path, func: str | None):
    sol = task_dir / "src" / "solution.py"
    sol.parent.mkdir(parents=True, exist_ok=True)
    if not func:
        code = "def solve(*args, **kwargs):\n    return None\n"
    else:
        code = f"def {func}(*args, **kwargs):\n    # TODO: model-filled impl\n    return None\n"
    sol.write_text(code, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--tests", required=True)
    args = ap.parse_args()
    func = infer_func_name(Path(args.tests))
    write_placeholder(Path(args.task), func)


if __name__ == "__main__":
    main()
