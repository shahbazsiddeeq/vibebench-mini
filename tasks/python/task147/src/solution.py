def parse_csv_line(line: str, delimiter: str = ",") -> list[str]:
    """Split one CSV record into fields, honoring double-quote quoting rules."""
    if not isinstance(delimiter, str) or len(delimiter) != 1 or delimiter == '"':
        raise ValueError("delimiter must be a single character other than '\"'")

    fields = []
    i = 0
    n = len(line)
    while True:
        # Parse one field starting at index i.
        if i < n and line[i] == '"':
            # Quoted field.
            i += 1
            buf = []
            closed = False
            while i < n:
                c = line[i]
                if c == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        buf.append('"')
                        i += 2
                        continue
                    # closing quote
                    i += 1
                    closed = True
                    break
                buf.append(c)
                i += 1
            if not closed:
                raise ValueError("unterminated quoted field")
            # After a closing quote, only a delimiter or end-of-line is allowed.
            if i < n and line[i] != delimiter:
                raise ValueError("unexpected character after closing quote")
            fields.append("".join(buf))
        else:
            # Unquoted field: read until the next delimiter.
            start = i
            while i < n and line[i] != delimiter:
                i += 1
            fields.append(line[start:i])

        if i < n and line[i] == delimiter:
            i += 1
            continue
        break
    return fields
