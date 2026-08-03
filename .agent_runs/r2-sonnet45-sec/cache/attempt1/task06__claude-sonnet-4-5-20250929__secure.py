import json
from pathlib import Path
from typing import Union


def sum_jsonl(path: str, key: str) -> Union[int, float]:
    """
    Sum numeric values for 'key' over JSON Lines file.
    
    Args:
        path: Path to the JSONL file
        key: Key to sum values for
        
    Returns:
        Sum of numeric values for the given key
        
    Raises:
        ValueError: If no valid numeric values are found for the key
    """
    # Validate inputs
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Validate path to prevent path traversal
    try:
        file_path = Path(path).resolve()
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid path: {e}")
    
    # Check if file exists and is a file
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    total = 0
    found_any = False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Skip empty lines
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parse JSON line
                    data = json.loads(line)
                    
                    # Ensure it's a dictionary
                    if not isinstance(data, dict):
                        continue
                    
                    # Check if key exists
                    if key not in data:
                        continue
                    
                    value = data[key]
                    
                    # Check if value is numeric (int or float)
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        total += value
                        found_any = True
                        
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue
                except (TypeError, ValueError):
                    # Skip lines with invalid data
                    continue
    
    except (IOError, OSError) as e:
        raise ValueError(f"Error reading file: {e}")
    
    if not found_any:
        raise ValueError(f"No valid numeric values found for key '{key}'")
    
    return total
