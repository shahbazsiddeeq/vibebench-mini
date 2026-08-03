# src/solution.py

def long_lines(source: str, limit: int = 79) -> list[int]:
    if not isinstance(source, str):
        raise ValueError("Source must be a string.")
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("Limit must be an integer greater than or equal to 1.")

    # Split the source into lines using str.splitlines()
    lines = source.splitlines()
    long_line_numbers = []

    for index, line in enumerate(lines):
        if len(line) > limit:
            long_line_numbers.append(index + 1)  # 1-based index

    return long_line_numbers
