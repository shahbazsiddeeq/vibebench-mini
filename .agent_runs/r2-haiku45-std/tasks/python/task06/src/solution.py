import json


def sum_jsonl(path, key):
    """
    Sum numeric values for 'key' over JSON Lines.
    Non-numeric/missing rows are ignored.
    Raises ValueError if no numeric values are found.
    """
    total = 0
    count = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            if key not in obj:
                continue
            
            value = obj[key]
            
            # Check if value is numeric (int or float)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                total += value
                count += 1
    
    if count == 0:
        raise ValueError(f"No numeric values found for key '{key}'")
    
    return total
