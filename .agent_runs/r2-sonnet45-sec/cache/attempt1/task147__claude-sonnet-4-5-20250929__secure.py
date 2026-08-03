def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    """
    Parse a single CSV line according to RFC4180 rules.
    
    Args:
        line: The CSV line to parse
        delimiter: Single character delimiter (default: ',')
        
    Returns:
        List of field values
        
    Raises:
        ValueError: If delimiter is invalid or line has malformed quoted fields
    """
    # Validate delimiter
    if not isinstance(delimiter, str) or len(delimiter) != 1:
        raise ValueError("Delimiter must be a single character")
    if delimiter == '"':
        raise ValueError("Delimiter cannot be a double quote")
    
    # Validate input type
    if not isinstance(line, str):
        raise ValueError("Line must be a string")
    
    fields = []
    i = 0
    n = len(line)
    
    while i <= n:
        # Start of a new field
        if i == n:
            # End of line - add empty field if we just passed a delimiter
            if i == 0 or (i > 0 and line[i-1] == delimiter):
                fields.append('')
            break
            
        # Check if this field is quoted
        if line[i] == '"':
            # Quoted field
            field_chars = []
            i += 1  # Skip opening quote
            
            while i < n:
                if line[i] == '"':
                    # Check if it's an escaped quote or closing quote
                    if i + 1 < n and line[i + 1] == '"':
                        # Escaped quote - add one quote to field
                        field_chars.append('"')
                        i += 2
                    else:
                        # Closing quote
                        i += 1
                        # After closing quote, must be delimiter or end of line
                        if i < n and line[i] != delimiter:
                            raise ValueError("Text found after closing quote")
                        fields.append(''.join(field_chars))
                        if i < n:
                            i += 1  # Skip delimiter
                        break
                else:
                    field_chars.append(line[i])
                    i += 1
            else:
                # Reached end of line without closing quote
                raise ValueError("Unterminated quoted field")
        else:
            # Unquoted field
            field_chars = []
            while i < n and line[i] != delimiter:
                field_chars.append(line[i])
                i += 1
            fields.append(''.join(field_chars))
            if i < n:
                i += 1  # Skip delimiter
    
    return fields
