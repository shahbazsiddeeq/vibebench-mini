"""src/solution.py

JSONL Sum by Key.
"""
import json


def sum_jsonl(path, key):
    total = 0
    found = False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            if not isinstance(obj, dict):
                continue
            if key not in obj:
                continue
            val = obj[key]
            if isinstance(val, bool):
                continue
            if isinstance(val, (int, float)):
                total += val
                found = True

    if not found:
        raise ValueError(f"No numeric values found for key '{key}' in {path}")

    return total
