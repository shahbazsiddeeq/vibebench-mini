def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    if len(delimiter) != 1 or delimiter == '"':
        raise ValueError("Delimiter must be a single character other than '\"'.")

    fields = []
    i = 0
    length = len(line)
    
    while i < length:
        if line[i] == '"':
            # Start of a quoted field
            i += 1
            start = i
            field = []
            while i < length:
                if line[i] == '"':
                    if i + 1 < length and line[i + 1] == '"':
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
                raise ValueError("Unterminated quoted field.")
            
            fields.append(''.join(field))
            
            if i < length and line[i] != delimiter:
                raise ValueError("Expected delimiter after closing quote.")
        
        else:
            # Start of an unquoted field
            start = i
            while i < length and line[i] != delimiter:
                i += 1
            fields.append(line[start:i])
        
        # Skip the delimiter
        if i < length and line[i] == delimiter:
            i += 1
    
    return fields
