import json

def sum_jsonl(path, key):
    total = 0
    found = False

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
        raise ValueError("No valid numeric values found for the given key.")

    return total
