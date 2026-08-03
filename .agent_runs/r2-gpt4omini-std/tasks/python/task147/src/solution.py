# src/solution.py

def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    if len(delimiter) != 1 or delimiter == '"':
        raise ValueError("Delimiter must be a single character other than '\"'.")

    fields = []
    current_field = []
    in_quotes = False
    i = 0
    length = len(line)

    while i < length:
        char = line[i]

        if in_quotes:
            if char == '"':
                # Check for escaped quote
                if i + 1 < length and line[i + 1] == '"':
                    current_field.append('"')
                    i += 1  # Skip the next quote
                else:
                    in_quotes = False  # Closing quote found
            else:
                current_field.append(char)
        else:
            if char == '"':
                in_quotes = True  # Opening quote found
            elif char == delimiter:
                fields.append(''.join(current_field))
                current_field = []
            else:
                current_field.append(char)

        i += 1

    # Handle the last field
    fields.append(''.join(current_field))

    # Check if we ended while still in quotes
    if in_quotes:
        raise ValueError("Unterminated quoted field.")

    # Check for invalid characters after closing quote
    if len(fields) > 0 and line[-1] != delimiter and line[-1] != '"':
        if fields[-1] and fields[-1][-1] != delimiter:
            raise ValueError("Invalid character after closing quote.")

    return fields
