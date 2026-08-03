"""CSV Line Tokenizer (Quote-Aware) - RFC4180 compliant parser."""

def parse_csv_line(line: str, delimiter: str = ',') -> list[str]:
    """
    Parse a single RFC4180-style CSV record into fields.
    
    Args:
        line: The CSV line to parse
        delimiter: Single character delimiter (must not be '"')
        
    Returns:
        List of parsed fields
        
    Raises:
        ValueError: If delimiter is invalid or line is malformed
    """
    # Validate delimiter
    if not isinstance(delimiter, str) or len(delimiter) != 1:
        raise ValueError("delimiter must be a single character")
    if delimiter == '"':
        raise ValueError("delimiter cannot be a double quote")
    
    # Validate input type
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    
    fields = []
    i = 0
    
    while i <= len(line):
        # Parse one field
        if i == len(line):
            # End of line - we've already added all fields via delimiters
            break
            
        if line[i] == '"':
            # Quoted field
            field, i = _parse_quoted_field(line, i, delimiter)
            fields.append(field)
        else:
            # Unquoted field
            field, i = _parse_unquoted_field(line, i, delimiter)
            fields.append(field)
        
        # After a field, we expect either a delimiter or end of line
        if i < len(line):
            if line[i] == delimiter:
                i += 1
            else:
                raise ValueError(f"Expected delimiter or end of line at position {i}")
    
    return fields


def _parse_quoted_field(line: str, start: int, delimiter: str) -> tuple[str, int]:
    """
    Parse a quoted field starting at position start (which points to the opening quote).
    
    Returns:
        Tuple of (field_content, position_after_field)
        
    Raises:
        ValueError: If field is malformed
    """
    i = start + 1  # Skip opening quote
    field = []
    
    while i < len(line):
        if line[i] == '"':
            # Check if it's an escaped quote or closing quote
            if i + 1 < len(line) and line[i + 1] == '"':
                # Escaped quote - add one quote to field
                field.append('"')
                i += 2
            else:
                # Closing quote
                i += 1
                # After closing quote, must be delimiter or end of line
                if i < len(line) and line[i] != delimiter:
                    raise ValueError(f"Text after closing quote at position {i}")
                return ''.join(field), i
        else:
            # Regular character
            field.append(line[i])
            i += 1
    
    # Reached end of line without closing quote
    raise ValueError("Unterminated quoted field")


def _parse_unquoted_field(line: str, start: int, delimiter: str) -> tuple[str, int]:
    """
    Parse an unquoted field starting at position start.
    
    Returns:
        Tuple of (field_content, position_after_field)
    """
    i = start
    field = []
    
    while i < len(line) and line[i] != delimiter:
        field.append(line[i])
        i += 1
    
    return ''.join(field), i
