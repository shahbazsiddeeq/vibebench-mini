#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)  # workspace task dir
    ap.add_argument("--ref", required=True)  # original task dir
    args = ap.parse_args()

    ref_sol = Path(args.ref) / "src" / "solution.py"
    dst_sol = Path(args.task) / "src" / "solution.py"
    dst_sol.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ref_sol, dst_sol)


if __name__ == "__main__":
    main()
