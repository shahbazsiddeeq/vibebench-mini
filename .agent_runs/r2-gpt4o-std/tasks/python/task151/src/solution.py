# src/solution.py

def parse_fixed_width(path: str, fields: list[tuple[str, int, int]]) -> list[dict[str, str]]:
    import os

    # Check for invalid fields
    if not fields:
        raise ValueError("Fields list cannot be empty.")
    for name, start, length in fields:
        if start < 0 or length < 1:
            raise ValueError("Field start must be >= 0 and length must be >= 1.")

    # Check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at path {path} does not exist.")

    records = []

    # Read the file and parse lines
    with open(path, 'r', encoding='utf-8', newline='') as file:
        for line in file:
            line = line.rstrip('\n\r')
            if not line.strip():
                continue  # Skip empty or whitespace-only lines

            record = {}
            for name, start, length in fields:
                value = line[start:start + length].strip()
                record[name] = value

            records.append(record)

    return records
