# src/solution.py

import os

def tail(path: str, n: int) -> list:
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No such file: '{path}'")
    
    with open(path, 'r') as file:
        lines = file.read().splitlines()
    
    return lines[-n:] if n < len(lines) else lines
