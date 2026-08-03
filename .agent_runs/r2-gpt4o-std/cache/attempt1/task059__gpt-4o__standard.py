# src/solution.py

def tail(path, n):
    if n < 0:
        raise ValueError("n must be non-negative")
    
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"No such file: '{path}'")
    
    return [line.rstrip('\n') for line in lines[-n:]]
