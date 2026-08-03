def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    if len(delimiter) != 1 or delimiter == '"':
        raise ValueError("Delimiter must be a single character other than '\"'.")

    fields = []
    field = []
    in_quotes = False
    i = 0
    length = len(line)

    while i < length:
        char = line[i]

        if in_quotes:
            if char == '"':
                if i + 1 < length and line[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(char)
        else:
            if char == '"':
                if not field:
                    in_quotes = True
                else:
                    raise ValueError("Unexpected quote character.")
            elif char == delimiter:
                fields.append(''.join(field))
                field = []
            else:
                field.append(char)

        i += 1

    if in_quotes:
        raise ValueError("Unterminated quoted field.")

    fields.append(''.join(field))
    return fields
