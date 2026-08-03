# src/solution.py

def count_lines(path: str) -> int:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError("An error occurred while reading the file.") from e
