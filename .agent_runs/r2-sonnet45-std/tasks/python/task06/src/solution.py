import json


def sum_jsonl(path, key):
    """
    Sum numeric values for 'key' over JSON Lines file.
    Non-numeric or missing rows are ignored.
    Raises ValueError if no valid numeric values are found.
    
    Args:
        path: Path to the JSONL file
        key: Key to sum values for
        
    Returns:
        Sum of all numeric values for the given key
        
    Raises:
        ValueError: If no valid numeric values are found
    """
    total = 0
    found_any = False
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            try:
                obj = json.loads(line)
                if key in obj:
                    value = obj[key]
                    # Check if value is numeric (int or float, but not bool)
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        total += value
                        found_any = True
            except (json.JSONDecodeError, TypeError):
                # Skip invalid JSON lines
                continue
    
    if not found_any:
        raise ValueError(f"No valid numeric values found for key '{key}'")
    
    return total
