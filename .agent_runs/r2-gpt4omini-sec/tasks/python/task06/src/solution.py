import json
import os

def sum_jsonl(path: str, key: str) -> float:
    if not isinstance(path, str) or not isinstance(key, str):
        raise ValueError("Path and key must be strings.")
    
    if not os.path.isfile(path):
        raise ValueError("The provided path does not point to a valid file.")
    
    total = 0.0
    count = 0

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data = json.loads(line)
                value = data.get(key)
                if isinstance(value, (int, float)):
                    total += value
                    count += 1
            except json.JSONDecodeError:
                continue  # Ignore lines that are not valid JSON

    if count == 0:
        raise ValueError("No valid numeric values found for the specified key.")

    return total
