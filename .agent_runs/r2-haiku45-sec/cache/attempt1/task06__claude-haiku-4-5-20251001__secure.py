import json
from pathlib import Path


def sum_jsonl(path, key):
    """
    Sum numeric values for 'key' over JSON Lines.
    
    Non-numeric or missing values are ignored.
    Raises ValueError if no numeric values are found for the key.
    
    Args:
        path: Path to JSONL file
        key: Key to sum values for
        
    Returns:
        Sum of numeric values for the key
        
    Raises:
        ValueError: If no numeric values found for the key
    """
    # Validate inputs
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Convert to Path and validate it exists and is readable
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    total = 0
    count = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue
                
                if not isinstance(obj, dict):
                    # Skip non-object lines
                    continue
                
                if key not in obj:
                    # Skip lines missing the key
                    continue
                
                value = obj[key]
                
                # Try to convert to numeric type
                if isinstance(value, bool):
                    # bool is a subclass of int, but we should skip it
                    continue
                
                if isinstance(value, (int, float)):
                    total += value
                    count += 1
                else:
                    # Try to convert string to number
                    try:
                        numeric_value = float(value)
                        total += numeric_value
                        count += 1
                    except (ValueError, TypeError):
                        # Skip non-numeric values
                        continue
    
    except IOError as e:
        raise IOError(f"Error reading file: {path}") from e
    
    if count == 0:
        raise ValueError(f"No numeric values found for key '{key}'")
    
    return total
