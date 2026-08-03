import json
from pathlib import Path

def sum_jsonl(path, key):
    total = 0.0
    found = False

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    if key in data and isinstance(data[key], (int, float)):
                        total += data[key]
                        found = True
                except json.JSONDecodeError:
                    continue

        if not found:
            raise ValueError(f"No valid numeric entries found for key: {key}")

        return total

    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
