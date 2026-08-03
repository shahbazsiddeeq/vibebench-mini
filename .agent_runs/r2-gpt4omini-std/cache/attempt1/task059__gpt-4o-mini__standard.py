# src/solution.py

def tail(path, n):
    if n < 0:
        raise ValueError("n must be non-negative")
    
    try:
        with open(path, 'r') as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"No such file: '{path}'")
    
    return lines[-n:] if n <= len(lines) else lines
