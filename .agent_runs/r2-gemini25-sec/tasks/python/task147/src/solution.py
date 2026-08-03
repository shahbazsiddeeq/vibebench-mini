def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    """
    Splits one RFC4180-style CSV record into fields.

    Args:
        line: The CSV line string to parse.
        delimiter: The single-character delimiter. Must not be '"'.

    Returns:
        A list of strings, where each string is a field from the CSV line.

    Raises:
        ValueError: If the delimiter is invalid, a quoted field is malformed,
                    or there's unexpected content after a closing quote.
    """
    if not isinstance(line, str):
        raise TypeError("line must be a string")
    if not isinstance(delimiter, str):
        raise TypeError("delimiter must be a string")
    if len(delimiter) != 1:
        raise ValueError("delimiter must be a single character")
    if delimiter == '"':
        raise ValueError("delimiter cannot be '\"'")

    fields = []
    current_field = []
    in_quoted_field = False
    i = 0
    n = len(line)

    while i < n:
        char = line[i]

        if in_quoted_field:
            if char == '"':
                # Check for escaped quote or closing quote
                if i + 1 < n and line[i + 1] == '"':
                    current_field.append('"')
                    i += 2  # Skip both quotes
                else:
                    # Closing quote
                    in_quoted_field = False
                    i += 1
                    # After a closing quote, the next character must be a delimiter or end-of-line
                    if i < n and line[i] != delimiter:
                        raise ValueError(f"Unexpected character '{line[i]}' after closing quote at position {i}")
            else:
                current_field.append(char)
                i += 1
        else:
            if char == delimiter:
                fields.append("".join(current_field))
                current_field = []
                i += 1
            elif char == '"':
                # Start of a quoted field
                in_quoted_field = True
                i += 1
            else:
                current_field.append(char)
                i += 1

    if in_quoted_field:
        raise ValueError("Unterminated quoted field")

    fields.append("".join(current_field))
    return fields
