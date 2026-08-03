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
                    # Check if next character is a delimiter or end of line
                    if i + 1 < length and line[i + 1] != delimiter:
                        if line[i + 1] != '\n':
                            raise ValueError("Invalid CSV format: text after closing quote.")
                    # Move to the next character
            else:
                current_field.append(char)
        else:
            if char == delimiter:
                fields.append(''.join(current_field))
                current_field = []
            elif char == '"':
                in_quotes = True
            else:
                current_field.append(char)

        i += 1

    # Add the last field
    fields.append(''.join(current_field))

    return fields
