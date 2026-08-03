# src/solution.py

import os

def count_lines(path: str) -> int:
    # Validate the input path
    if not isinstance(path, str):
        raise ValueError("The path must be a string.")
    
    # Check if the file exists
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except Exception as e:
        raise RuntimeError("An error occurred while reading the file.") from e
