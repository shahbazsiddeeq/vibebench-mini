# src/solution.py

def count_lines(path: str) -> int:
    """Return the number of lines in a UTF-8 text file."""
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{path}' does not exist.")
