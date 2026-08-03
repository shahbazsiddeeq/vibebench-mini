def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    """
    Splits one RFC4180-style CSV record into fields.

    Args:
        line: The CSV line to parse.
        delimiter: The character used to separate fields. Must be a single
                   character other than '"'.

    Returns:
        A list of strings, where each string is a field from the CSV line.

    Raises:
        ValueError: If the delimiter is invalid, an unterminated quoted field
                    is found, or invalid characters follow a closing quote.
    """
    if not isinstance(delimiter, str) or len(delimiter) != 1 or delimiter == '"':
        raise ValueError("Delimiter must be a single character other than '\"'")

    fields = []
    current_field = []
    in_quoted_field = False
    i = 0
    n = len(line)

    while i < n:
        if in_quoted_field:
            if line[i] == '"':
                if i + 1 < n and line[i + 1] == '"':
                    # Escaped double quote ""
                    current_field.append('"')
                    i += 2
                else:
                    # Closing double quote
                    in_quoted_field = False
                    i += 1
                    # After a closing quote, the next character must be a delimiter or end-of-line
                    if i < n and line[i] != delimiter:
                        raise ValueError("Characters found after closing quote and before delimiter/end-of-line")
            else:
                current_field.append(line[i])
                i += 1
        else:
            if line[i] == delimiter:
                fields.append("".join(current_field))
                current_field = []
                i += 1
            elif line[i] == '"':
                if current_field:
                    # A double quote in an unquoted field is just a literal character
                    current_field.append(line[i])
                    i += 1
                else:
                    # Start of a quoted field
                    in_quoted_field = True
                    i += 1
            else:
                current_field.append(line[i])
                i += 1

    if in_quoted_field:
        raise ValueError("Unterminated quoted field")

    fields.append("".join(current_field))
    return fields
