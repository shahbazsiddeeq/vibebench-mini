def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    if delimiter == '"':
        raise ValueError("Delimiter cannot be a double quote")

    fields = []
    i = 0
    n = len(line)
    
    while i < n:
        if line[i] == '"':
            # Start of a quoted field
            i += 1
            start = i
            field = []
            while i < n:
                if line[i] == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        # Escaped quote
                        field.append('"')
                        i += 2
                    else:
                        # End of quoted field
                        i += 1
                        break
                else:
                    field.append(line[i])
                    i += 1
            else:
                # Unterminated quoted field
                raise ValueError("Unterminated quoted field")
            
            fields.append(''.join(field))
            
            if i < n and line[i] != delimiter:
                raise ValueError("Expected delimiter after closing quote")
            i += 1  # Skip the delimiter
        else:
            # Start of an unquoted field
            start = i
            while i < n and line[i] != delimiter:
                i += 1
            fields.append(line[start:i])
            i += 1  # Skip the delimiter

    # If the line ends with a delimiter, add an empty field
    if line.endswith(delimiter):
        fields.append('')

    return fields
