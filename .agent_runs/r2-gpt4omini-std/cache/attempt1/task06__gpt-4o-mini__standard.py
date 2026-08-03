import json

def sum_jsonl(path, key):
    total = 0
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
                continue
    
    if count == 0:
        raise ValueError("No valid numeric values found for the specified key.")
    
    return total
