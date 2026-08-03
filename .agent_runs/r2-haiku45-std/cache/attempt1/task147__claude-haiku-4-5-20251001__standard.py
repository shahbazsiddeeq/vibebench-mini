def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    """
    Parse a single RFC4180-style CSV record into fields.
    
    Args:
        line: The CSV line to parse
        delimiter: Single character delimiter (not '"')
    
    Returns:
        List of parsed fields
    
    Raises:
        ValueError: If delimiter is invalid or line is malformed
    """
    # Validate delimiter
    if len(delimiter) != 1 or delimiter == '"':
        raise ValueError("Delimiter must be a single character other than '\"'")
    
    fields = []
    i = 0
    
    while i <= len(line):
        # Parse one field
        if i == len(line):
            # End of line - we've already added all fields via delimiters
            break
        
        if line[i] == '"':
            # Quoted field
            field = ""
            i += 1  # Skip opening quote
            
            while i < len(line):
                if line[i] == '"':
                    # Check if it's an escaped quote or closing quote
                    if i + 1 < len(line) and line[i + 1] == '"':
                        # Escaped quote - add one quote to field
                        field += '"'
                        i += 2
                    else:
                        # Closing quote
                        i += 1
                        # Next character must be delimiter or end of line
                        if i < len(line) and line[i] != delimiter:
                            raise ValueError("Text after closing quote")
                        if i < len(line):
                            # Skip the delimiter
                            i += 1
                        break
                else:
                    field += line[i]
                    i += 1
            else:
                # Reached end of line without closing quote
                raise ValueError("Unterminated quoted field")
            
            fields.append(field)
        else:
            # Unquoted field - read until delimiter or end of line
            field = ""
            while i < len(line) and line[i] != delimiter:
                field += line[i]
                i += 1
            
            fields.append(field)
            
            # Skip delimiter if present
            if i < len(line) and line[i] == delimiter:
                i += 1
    
    return fields
