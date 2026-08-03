import os

def tail(path, n):
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No such file: '{path}'")
    
    lines = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception as e:
        raise IOError("An error occurred while reading the file") from e
    
    # Strip newlines and return the last n lines
    return [line.rstrip('\n') for line in lines[-n:]]
