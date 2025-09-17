import json


def sum_jsonl(path: str, key: str) -> float:
    total = 0.0
    seen = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                v = json.loads(line).get(key)
                if isinstance(v, (int, float)):
                    total += float(v)
                    seen += 1
            except json.JSONDecodeError:
                continue
    if seen == 0:
        raise ValueError("no numeric rows")
    return total
