def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    if len(delimiter) != 1 or delimiter == '"':
        raise ValueError("Invalid delimiter")

    fields = []
    i = 0
    n = len(line)

    while True:
        field_chars = []
        if i < n and line[i] == '"':
            # Quoted field
            i += 1
            while True:
                if i >= n:
                    raise ValueError("Unterminated quoted field")
                c = line[i]
                if c == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        field_chars.append('"')
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    field_chars.append(c)
                    i += 1
            # After closing quote, must be delimiter or EOL
            if i < n and line[i] != delimiter:
                raise ValueError("Unexpected characters after closing quote")
        else:
            # Unquoted field
            while i < n and line[i] != delimiter:
                field_chars.append(line[i])
                i += 1

        fields.append(''.join(field_chars))

        if i < n and line[i] == delimiter:
            i += 1
            continue
        else:
            break

    return fields
