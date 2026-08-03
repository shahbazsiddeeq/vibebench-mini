# src/solution.py

import os

def parse_fixed_width(path: str, fields: list[tuple[str, int, int]]) -> list[dict[str, str]]:
    # Validate inputs
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")
    
    if not fields:
        raise ValueError("The fields list cannot be empty.")
    
    for name, start, length in fields:
        if not isinstance(name, str) or not isinstance(start, int) or not isinstance(length, int):
            raise ValueError("Field definitions must be tuples of (str, int, int).")
        if start < 0 or length < 1:
            raise ValueError("Field start must be >= 0 and length must be > 0.")
    
    records = []
    
    with open(path, 'r', encoding='utf-8', newline='') as file:
        for line in file:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            
            record = {}
            for name, start, length in fields:
                value = stripped_line[start:start + length].strip()
                record[name] = value
            
            records.append(record)
    
    return records
